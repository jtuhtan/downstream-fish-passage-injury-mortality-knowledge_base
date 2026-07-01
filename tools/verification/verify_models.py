#!/usr/bin/env python3
"""Offline verifier for the dose-response MODELS (coefficients).

Confirms each fitted model in data/dose_response_models.csv against its source PDF.
Built for speed on a lot of material:
  * jumps the PDF straight to the page holding the coefficients (searches the text
    for the coefficient values + the `source_location` table);
  * shows the extracted coefficients, the derived landmark (E50/S50/V50/A50/RPC50)
    and a live curve beside the source snippet, so verifying = "do these match?";
  * groups models by source paper (batch through one PDF at a time);
  * keyboard: V = verify, F = flag, N = next/skip.

Runs locally, stdlib only (shells out to `pdftotext`). Reuses config.json
(pdf_base / verifier / library_root). Writes `confidence = Verified` back to the CSV
and logs to data/model_verification_log.csv.

    python tools/verification/verify_models.py     # opens http://127.0.0.1:8010
"""
import csv, json, os, re, math, html, datetime, tempfile, threading, webbrowser, urllib.parse, subprocess, shutil
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, "data")
DRM = os.path.join(DATA, "dose_response_models.csv")
CORPUS = os.path.join(DATA, "corpus.csv")
SMAP = os.path.join(DATA, "vocab", "source_pdf_map.csv")
LOG = os.path.join(DATA, "model_verification_log.csv")
CONFIG = os.path.join(HERE, "config.json")
PORT = 8010
EDIT = ["b0", "b1", "b2", "b3", "b4", "source_location", "notes"]

_PAGES = {}          # pdf path -> [page text]
_PDFIDX = {}         # filename -> full path
_PT = None           # pdftotext path
_PP = None           # pdftoppm path
_IMG = {}            # (path, page, dpi) -> png bytes
_BOX = {}            # (path, page, model_id) -> [(left%,top%,w%,h%)] coeff highlights


# ------------------------------------------------------------------ data/io
def load_cfg():
    return json.load(open(CONFIG, encoding="utf-8")) if os.path.exists(CONFIG) else {}


def save_cfg(cfg):
    json.dump(cfg, open(CONFIG, "w", encoding="utf-8"), indent=2)


def read_csv(p):
    with open(p, encoding="utf-8") as f:
        r = list(csv.DictReader(f))
    return r, (list(r[0].keys()) if r else [])


def write_drm(rows, fields):
    with open(DRM, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)


def corpus_index():
    rows, _ = read_csv(CORPUS)
    return {r["citation_key"]: r for r in rows}


def smap_index():
    if not os.path.exists(SMAP):
        return {}
    rows, _ = read_csv(SMAP)
    return {r["sr_citation_key"]: r["corpus_citation_key"] for r in rows}


def log_event(mid, verifier, action, changed):
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["model_id", "verifier", "date", "action", "fields_changed"])
        w.writerow([mid, verifier, datetime.date.today().isoformat(), action, "; ".join(changed)])


# ------------------------------------------------------------------ pdf
def find_pdftotext():
    exe = shutil.which("pdftotext")
    if exe:
        return exe
    for c in [r"C:\Users\User\AppData\Local\Programs\Git\mingw64\bin\pdftotext.exe",
              r"C:\Program Files\Git\mingw64\bin\pdftotext.exe", "/usr/bin/pdftotext"]:
        if os.path.exists(c):
            return c
    return None


def find_pdftoppm():
    exe = shutil.which("pdftoppm")
    if exe:
        return exe
    for c in ["/usr/bin/pdftoppm", r"C:\Program Files\Git\mingw64\bin\pdftoppm.exe"]:
        if os.path.exists(c):
            return c
    return None


def build_pdf_index(root):
    idx = {}
    if root and os.path.isdir(root):
        for dp, _, files in os.walk(root):
            for f in files:
                if f.lower().endswith(".pdf"):
                    idx.setdefault(f, os.path.join(dp, f))
    return idx


def model_pdf(cfg, corp, smap, m):
    ck = smap.get(m["citation_key"], m["citation_key"])
    fn = corp.get(ck, {}).get("local_filename", "")
    return _PDFIDX.get(fn), ck, fn


def pdf_pages(path):
    if path in _PAGES:
        return _PAGES[path]
    pages = []
    if _PT and path and os.path.exists(path):
        r = subprocess.run([_PT, "-layout", path, "-"], capture_output=True)
        if r.returncode == 0:
            pages = r.stdout.decode("utf-8", "replace").split("\f")
    _PAGES[path] = pages
    return pages


def page_png(path, page, dpi=130):
    key = (path, page, dpi)
    if key in _IMG:
        return _IMG[key]
    png = b""
    if _PP and path and os.path.exists(path):
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "pg")
            r = subprocess.run([_PP, "-png", "-f", str(page), "-l", str(page),
                                "-singlefile", "-r", str(dpi), path, out], capture_output=True)
            fn = out + ".png"
            if r.returncode == 0 and os.path.exists(fn):
                with open(fn, "rb") as fh:
                    png = fh.read()
    _IMG[key] = png
    return png


def coeff_variants(v):
    out = set()
    try:
        f = float(v)
    except (TypeError, ValueError):
        return out
    a = abs(f)
    s = ("%f" % a).rstrip("0").rstrip(".")          # 12.60 -> 12.6
    out.add(s)
    out.add("%.2f" % a)                              # 12.60
    out.add("%.3f" % a)
    return {x for x in out if x and x not in ("0", "0.0")}


def find_page(path, m):
    """Return (page_1based, [snippet lines]) for the coefficient table."""
    pages = pdf_pages(path)
    if not pages:
        return 1, []
    want0 = coeff_variants(m.get("b0")); want1 = coeff_variants(m.get("b1"))
    tbl = re.search(r"table\s*(\d+)", m.get("source_location", ""), re.I)
    tbl_pat = re.compile(r"table\s*%s\b" % tbl.group(1), re.I) if tbl else None
    best, best_score, best_lines = 0, 0, []
    for i, page in enumerate(pages):
        low = page
        s = 0
        if want0 and any(w in low for w in want0):
            s += 3
        if want1 and any(w in low for w in want1):
            s += 3
        if tbl_pat and tbl_pat.search(low):
            s += 2
        if s > best_score:
            lines = []
            for ln in page.splitlines():
                t = re.sub(r"\s+", " ", ln.replace("�", " ")).strip()
                if not t:
                    continue
                if (any(w in t for w in want0) or any(w in t for w in want1)
                        or (tbl_pat and tbl_pat.search(t))):
                    lines.append(t[:180])
            best, best_score, best_lines = i + 1, s, lines[:4]
    if best:
        return best, best_lines
    return 1, []


def highlight_boxes(path, page, m):
    """Boxes (as % of page w/h) around words matching this model's coefficients."""
    if not (_PT and path and os.path.exists(path)):
        return []
    key = (path, page, m["model_id"])
    if key in _BOX:
        return _BOX[key]
    r = subprocess.run([_PT, "-bbox", "-f", str(page), "-l", str(page), path, "-"], capture_output=True)
    boxes = []
    if r.returncode == 0:
        xml = r.stdout.decode("utf-8", "replace")
        pm = re.search(r'<page width="([\d.]+)" height="([\d.]+)"', xml)
        wants = set()
        for f in ("b0", "b1", "b2", "b3", "b4"):
            try:
                a = abs(float(m.get(f)))
            except (TypeError, ValueError):
                continue
            s = ("%f" % a).rstrip("0").rstrip(".")   # exact value only (e.g. 0.0125, 12.6)
            if s and s not in ("0", "0.0"):
                wants.add(s)
        if pm and wants:
            pw, ph = float(pm.group(1)), float(pm.group(2))
            for wm in re.finditer(
                    r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', xml):
                x0, y0, x1, y1, txt = wm.groups()
                mnum = re.search(r'-?\d+(?:\.\d+)?', html.unescape(txt))
                if not mnum:
                    continue
                try:
                    cs = ("%f" % abs(float(mnum.group(0)))).rstrip("0").rstrip(".")
                except ValueError:
                    continue
                if cs in wants:   # exact numeric value (ignores sign & trailing zeros)
                    boxes.append((float(x0) / pw * 100, float(y0) / ph * 100,
                                  (float(x1) - float(x0)) / pw * 100, (float(y1) - float(y0)) / ph * 100))
    _BOX[key] = boxes[:60]
    return _BOX[key]


# ------------------------------------------------------------------ math
def prob_at(m, x):
    b0 = float(m["b0"] or 0); b1 = float(m["b1"] or 0)
    f = m["form"]
    if f == "loglogistic":
        e = float(m["b1"]); ff = float(m["b2"] or 1); b = float(m["b0"])
        return 0.0 if x <= 0 else ff / (1 + (x / e) ** b)
    if f == "linear_survival":
        ps = min(1.0, max(0.0, 1 + b1 * (x - b0)))
        return 1 - ps
    if f == "loglinear":
        return max(0.0, min(1.0, b0)) if x <= 0 else max(0.0, min(1.0, b0 + b1 * math.log(x)))
    return 1 / (1 + math.exp(-(b0 + b1 * x)))


def landmark(m):
    b0 = float(m["b0"] or 0); b1 = float(m["b1"] or 0); xm = m["x_metric"]
    f = m["form"]
    try:
        if f == "logistic":
            x50 = -b0 / b1
            if xm.startswith("ln(RPC)"):
                return f"LRP50 = {x50:.2f}  →  RPC50 = {math.exp(x50):.2f}"
            if xm.startswith("strain"):
                return f"S50 = {x50:.0f} s⁻¹"
            if xm.startswith("accel"):
                return f"A50 = {x50:.0f} m s⁻²"
            if xm.startswith("strike"):
                return f"V50 = {x50:.2f} m/s"
            return f"x(P=0.5) = {x50:.3f}"
        if f == "loglogistic":
            return f"ED50 = {float(m['b1']):.2f} {xm.split('(')[0].strip()}  |  max P = {float(m['b2'] or 1):.2f}"
        if f == "linear_survival":
            v = b0 - 0.5 / b1 if b1 else float('nan')
            return f"V(P=0.5) = {v:.2f} m/s   (Vcrit={b0}, m={b1})"
        if f == "loglinear":
            return f"MR(15cm) = {prob_at(m,15):.2f}   [MR = {b0} + {b1}·ln(L)]"
    except Exception:
        return "(landmark n/a)"
    return ""


def curve_svg(m):
    W, H, pl, pb, pt, pr = 380, 150, 40, 26, 10, 10
    x0 = float(m["x_min"] or 0); x1 = float(m["x_max"] or 1)
    if x1 <= x0:
        x1 = x0 + 1
    def X(x): return pl + (W - pl - pr) * (x - x0) / (x1 - x0)
    def Y(p): return pt + (H - pt - pb) * (1 - p)
    s = f'<svg width="{W}" height="{H}" style="background:#fff;border:1px solid #dde5e9;border-radius:6px">'
    for p in (0, .5, 1):
        s += f'<line x1="{pl}" y1="{Y(p):.0f}" x2="{W-pr}" y2="{Y(p):.0f}" stroke="{"#f0b429" if p==.5 else "#eef2f7"}"/>'
        s += f'<text x="{pl-5}" y="{Y(p)+3:.0f}" text-anchor="end" font-size="9" fill="#8a99a6">{p}</text>'
    pts = []
    for i in range(61):
        x = x0 + (x1 - x0) * i / 60
        p = prob_at(m, x)
        pts.append(f"{X(x):.1f},{Y(max(0,min(1,p))):.1f}")
    s += f'<polyline points="{" ".join(pts)}" fill="none" stroke="#2e8b57" stroke-width="2"/>'
    s += f'<text x="{(pl+W-pr)/2:.0f}" y="{H-4}" text-anchor="middle" font-size="9" fill="#5b7383">{esc(m["x_metric"])} ({x0:g}–{x1:g})</text>'
    return s + "</svg>"


# ------------------------------------------------------------------ html
CSS = """*{box-sizing:border-box}body{margin:0;font-family:-apple-system,Segoe UI,Roboto,sans-serif;color:#16313f}
.bar{background:#0e2a3b;color:#fff;padding:9px 16px;display:flex;gap:14px;align-items:center;font-size:14px}
.bar .prog{margin-left:auto;font-size:12px;color:#bcd4dd}
.split{display:flex;height:calc(100vh - 44px)}.pdf{flex:1;border:0}
.form{width:44%;max-width:640px;overflow:auto;padding:14px 18px;background:#f7fafb}
h3{margin:2px 0 2px}.sub{color:#5b7383;font-size:12px;margin-bottom:8px}
.grid{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin:8px 0}
label{display:block;font-size:10px;font-weight:700;text-transform:uppercase;color:#5b7383;margin:8px 0 2px}
input[type=text]{width:100%;padding:6px 7px;border:1px solid #cdd9df;border-radius:6px;font:inherit;font-size:13px}
.mono{font-family:ui-monospace,Consolas,monospace}
.lm{background:#eaf6ef;border:1px solid #bfe0cd;border-radius:6px;padding:7px 9px;font-size:13px;margin:8px 0;font-weight:600}
.src{background:#fff;border:1px solid #dde5e9;border-radius:6px;padding:8px;font-size:12px;color:#31485a;margin:8px 0}
.src b{color:#0e2a3b}.snip{font-family:ui-monospace,Consolas,monospace;font-size:11px;color:#334;display:block;margin-top:3px;white-space:pre-wrap}
.btns{position:sticky;bottom:0;background:#f7fafb;padding:10px 0;border-top:1px solid #dde5e9;margin-top:10px}
button{padding:9px 14px;border:0;border-radius:7px;font-weight:700;cursor:pointer;font-size:13px;margin-right:8px}
.v{background:#2e8b57;color:#fff}.f{background:#d39a2d;color:#fff}.s{background:#e3e9ec;color:#16313f}
.kbd{font-size:11px;color:#8a99a6;margin-left:6px}a{color:#1f7a8c}.warn{background:#fdecea;border:1px solid #f5b7b1;padding:8px;border-radius:6px;font-size:12px}"""


def esc(v):
    return html.escape(str(v or ""), quote=True)


def setup_page(msg=""):
    return f"""<!doctype html><meta charset=utf-8><style>{CSS} body{{padding:30px;max-width:640px;margin:0 auto}}</style>
    <h2>Model verifier - setup</h2><p class=warn>{esc(msg)}</p>
    <form method=post action=/setup>
    <label>Library root (folder that contains all your PDFs, searched recursively)</label>
    <input type=text name=library_root value="{esc(load_cfg().get('library_root',''))}" style="width:100%">
    <label>Your initials</label><input type=text name=verifier value="{esc(load_cfg().get('verifier',''))}">
    <div class=btns><button class=v type=submit>Save &amp; start</button></div></form>"""


def ordered(rows, smap):
    return sorted(rows, key=lambda r: (smap.get(r["citation_key"], r["citation_key"]), r["model_id"]))


def page(cfg, rows, fields, corp, smap, mid=None, skip=None, imgpg=None):
    order = ordered(rows, smap)
    total = len(order); done = sum(1 for r in order if r.get("confidence") == "Verified")
    seq = [r["model_id"] for r in order]
    if skip and skip in seq:
        after = seq[seq.index(skip) + 1:]
        mid = next((k for k in after if next(r for r in order if r["model_id"] == k).get("confidence") != "Verified"), None)
        if mid is None:
            mid = seq[(seq.index(skip) + 1) % total]
    m = next((r for r in order if r["model_id"] == mid), None) if mid else None
    if m is None:
        m = next((r for r in order if r.get("confidence") != "Verified"), None)
    if m is None:
        return f"<!doctype html><meta charset=utf-8><style>{CSS}</style><div class=bar><b>All models verified</b><span class=prog>{done}/{total}</span></div><p style='padding:30px'>Nothing left. Close the tab.</p>"
    mid = m["model_id"]
    path, ck, fn = model_pdf(cfg, corp, smap, m)
    # batch position within this paper
    same = [r for r in order if smap.get(r["citation_key"], r["citation_key"]) == ck]
    pos = same.index(m) + 1
    if path:
        dpg, snips = find_page(path, m)
        try:
            pg = int(imgpg) if imgpg else dpg
        except (TypeError, ValueError):
            pg = dpg
        npages = len(pdf_pages(path)) or pg
        pg = max(1, min(pg, npages))
        q = urllib.parse.quote(mid)
        boxes = highlight_boxes(path, pg, m)
        ov = "".join(
            '<div style="position:absolute;left:%.2f%%;top:%.2f%%;width:%.2f%%;height:%.2f%%;'
            'background:rgba(255,232,0,.5);mix-blend-mode:multiply;border-radius:2px;'
            'box-shadow:0 0 0 1px rgba(230,180,0,.6)"></div>' % (max(0, L - 0.3), max(0, T - 0.3), W + 0.6, H + 0.6)
            for (L, T, W, H) in boxes)
        hi = f' &nbsp;|&nbsp; <b style="background:rgba(255,232,0,.6);padding:0 3px">{len(boxes)}</b> coefficient hit(s) highlighted' if boxes else ''
        nav = (f'<a href="/?id={q}&amp;pg={pg-1}">&lsaquo; prev</a> &nbsp;'
               f'<b>page {pg}</b> / {npages} &nbsp;'
               f'<a href="/?id={q}&amp;pg={pg+1}">next &rsaquo;</a>'
               f' &nbsp;|&nbsp; <a href="/pdf?id={q}" target=_blank>open raw PDF &nearr;</a>{hi}')
        pdfpane = ('<div class=pdf style="display:flex;flex-direction:column">'
                   f'<div style="background:#eef2f5;padding:6px 10px;font-size:12px;border-bottom:1px solid #dde5e9">{nav}</div>'
                   '<div style="flex:1;overflow:auto;background:#525659;text-align:center;padding:6px">'
                   '<div style="position:relative;display:inline-block;width:100%;max-width:920px">'
                   f'<img src="/pageimg?id={q}&amp;pg={pg}" style="width:100%;display:block;background:#fff" alt="page {pg}">'
                   f'{ov}</div></div></div>')
        srcbox = (f'<div class=src><b>source_location:</b> {esc(m["source_location"])} '
                  f'&nbsp;|&nbsp; auto-jumped to <b>p{dpg}</b> of {esc(fn)}'
                  + ("".join(f'<span class=snip>{esc(s)}</span>' for s in snips) if snips
                     else '<span class=snip>(values not auto-located — use prev/next to find the table)</span>')
                  + '</div>')
    else:
        pdfpane = f'<div class=pdf style="padding:24px;background:#fff"><div class=warn><b>PDF not found</b> for {esc(m["citation_key"])} → {esc(ck)} ({esc(fn) or "no filename"}). Check data/vocab/source_pdf_map.csv.</div></div>'
        srcbox = f'<div class=src><b>source_location:</b> {esc(m["source_location"])}</div>'
    ins = []
    for fld in EDIT:
        ins.append(f'<div><label>{esc(fld)}</label><input class=mono type=text name="{fld}" value="{esc(m.get(fld,""))}"></div>')
    grid = "".join(ins[:5]); rest = "".join(ins[5:])
    st = m.get("confidence", "Mined")
    return f"""<!doctype html><meta charset=utf-8><title>Verify {esc(mid)}</title><style>{CSS}</style>
    <div class=bar><b>{esc(m["citation_key"])}</b> · model {pos}/{len(same)} in this paper
      <span class=prog>{done}/{total} verified · status: {esc(st)} · {esc(cfg.get('verifier',''))}</span></div>
    <div class=split>{pdfpane}
      <form class=form id=frm method=post action=/save>
      <input type=hidden name=id value="{esc(mid)}">
      <h3>{esc(m["species"])}</h3>
      <div class=sub>{esc(m["mechanism"])} · <b>{esc(m["response"])}</b> · form <b>{esc(m["form"])}</b> · x = {esc(m["x_metric"])}</div>
      {curve_svg(m)}
      <div class=lm>{esc(landmark(m))}</div>
      <div class=grid>{grid}</div>
      {rest}
      <label>Verifier note (optional; to the log)</label><input type=text name=_note>
      <div class=btns>
        <button class=v id=fverify name=_action value=verify type=submit>Confirm &amp; Verify <span class=kbd>V</span></button>
        <button class=f id=fflag name=_action value=flag type=submit>Flag <span class=kbd>F</span></button>
        <a href="/?skip={urllib.parse.quote(mid)}"><button class=s type=button>Skip &rarr; <span class=kbd>N</span></button></a>
      </div></form></div>
    <script>var KEY={json.dumps(mid)};document.addEventListener('keydown',function(e){{
      if(e.target.tagName=='INPUT'||e.target.tagName=='TEXTAREA')return;
      if(e.key=='v'||e.key=='V')document.getElementById('fverify').click();
      else if(e.key=='f'||e.key=='F')document.getElementById('fflag').click();
      else if(e.key=='n'||e.key=='N')location.href='/?skip='+encodeURIComponent(KEY);}});</script>"""


# ------------------------------------------------------------------ server
class H(BaseHTTPRequestHandler):
    def _send(self, body, ctype="text/html; charset=utf-8", code=200):
        b = body.encode("utf-8") if isinstance(body, str) else body
        try:
            self.send_response(code); self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def log_message(self, *a):
        pass

    def _serve_pdf(self, path):
        """Serve a PDF with HTTP Range support (Chrome/Edge PDF viewers require it)."""
        size = os.path.getsize(path)
        rng = self.headers.get("Range", "")
        start, end, partial = 0, size - 1, False
        if rng.startswith("bytes="):
            partial = True
            a, _, b = rng[6:].partition("-")
            try:
                start = int(a) if a else 0
                end = int(b) if b else size - 1
            except ValueError:
                start, end = 0, size - 1
            end = min(end, size - 1)
            if start > end or start < 0:
                start, end, partial = 0, size - 1, False
        with open(path, "rb") as fh:
            fh.seek(start)
            body = fh.read(end - start + 1)
        self.send_response(206 if partial else 200)
        self.send_header("Content-Type", "application/pdf")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Disposition", "inline")
        if partial:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_GET(self):
        u = urllib.parse.urlparse(self.path); q = urllib.parse.parse_qs(u.query)
        cfg = load_cfg()
        if u.path == "/favicon.ico":
            self.send_response(204); self.end_headers(); return
        if u.path in ("/pdf", "/pageimg"):
            rows, _ = read_csv(DRM); corp = corpus_index(); smap = smap_index()
            m = next((r for r in rows if r["model_id"] == q.get("id", [""])[0]), None)
            path = model_pdf(cfg, corp, smap, m)[0] if m else None
            if not (path and os.path.exists(path)):
                self._send("PDF not found", code=404); return
            if u.path == "/pdf":
                self._serve_pdf(path); return
            try:
                pg = max(1, int(q.get("pg", ["1"])[0]))
            except ValueError:
                pg = 1
            png = page_png(path, pg)
            if png:
                self._send(png, "image/png"); return
            self._send("render failed (pdftoppm)", code=500); return
        if not cfg.get("library_root"):
            self._send(setup_page("Point the tool at your PDF library root.")); return
        rows, fields = read_csv(DRM); corp = corpus_index(); smap = smap_index()
        self._send(page(cfg, rows, fields, corp, smap,
                        mid=q.get("id", [None])[0], skip=q.get("skip", [None])[0],
                        imgpg=q.get("pg", [None])[0]))

    def do_POST(self):
        ln = int(self.headers.get("Content-Length", 0))
        form = {k: v[0] for k, v in urllib.parse.parse_qs(self.rfile.read(ln).decode("utf-8"), keep_blank_values=True).items()}
        if self.path == "/setup":
            cfg = load_cfg(); cfg["library_root"] = form.get("library_root", "").strip()
            cfg["verifier"] = form.get("verifier", "").strip(); save_cfg(cfg)
            global _PDFIDX; _PDFIDX = build_pdf_index(cfg["library_root"])
            self.send_response(303); self.send_header("Location", "/"); self.end_headers(); return
        if self.path == "/save":
            cfg = load_cfg(); rows, fields = read_csv(DRM)
            mid = form.get("id"); action = form.get("_action", "verify"); note = form.get("_note", "").strip()
            r = next((x for x in rows if x["model_id"] == mid), None)
            if r:
                changed = [f for f in EDIT if f in form and form[f] != (r.get(f) or "")]
                for f in changed:
                    r[f] = form[f]
                if action == "verify":
                    r["confidence"] = "Verified"
                if note:
                    changed.append(f"note:{note}")
                write_drm(rows, fields)
                log_event(mid, cfg.get("verifier", "?"), action, changed)
            self.send_response(303); self.send_header("Location", "/"); self.end_headers(); return
        self._send("not found", code=404)


def open_browser(url):
    """Best-effort browser open; silences backend chatter (e.g. Linux `gio`)."""
    try:
        dn = os.open(os.devnull, os.O_WRONLY); old = os.dup(2); os.dup2(dn, 2)
        try:
            webbrowser.open(url)
        finally:
            os.dup2(old, 2); os.close(old); os.close(dn)
    except Exception:
        pass


def main():
    global _PT, _PP, _PDFIDX
    _PT = find_pdftotext()
    _PP = find_pdftoppm()
    if not _PT or not _PP:
        print("WARNING: poppler tools missing (pdftotext=%s, pdftoppm=%s).\n"
              "  The PDF page image needs pdftoppm; install:  sudo apt install poppler-utils"
              % (bool(_PT), bool(_PP)))
    cfg = load_cfg()
    if cfg.get("library_root"):
        print("Indexing PDFs under", cfg["library_root"], "...")
        _PDFIDX = build_pdf_index(cfg["library_root"])
        print(f"  {len(_PDFIDX)} PDFs indexed.")
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    url = f"http://127.0.0.1:{PORT}"
    bar = "=" * 60
    print(f"\n{bar}\n  Model verifier running — open in your browser:\n    {url}\n"
          f"  (Ctrl+C to stop. If no browser opens, paste the URL yourself.)\n{bar}")
    threading.Timer(0.8, lambda: open_browser(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
