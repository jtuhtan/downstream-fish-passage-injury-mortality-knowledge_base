#!/usr/bin/env python3
"""Offline verification tool for the Downstream Fish Passage knowledge base.

Runs entirely on your own machine (no internet, no installs - Python 3 standard
library only). It opens each paper's PDF beside an editable form so you can
confirm / deny / change every source-of-truth field, then writes the result back
to data/extraction.csv and records who verified it and when in
data/verification_log.csv.

USAGE
  python tools/verification/verify.py
  # then open http://127.0.0.1:8000 in your browser (it opens automatically)

On first run it asks for (a) the folder where your PDFs live (the local
"Barotrauma" library, organised in study-type subfolders) and (b) your initials.
These are stored in tools/verification/config.json (git-ignored).

See tools/verification/README.md and methodology/08_verification_protocol.md
for the rules: what each confidence level means and how to confirm a row.
"""
import csv, json, os, datetime, html, webbrowser, threading, urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, "data")
EXTRACTION = os.path.join(DATA, "extraction.csv")
CORPUS = os.path.join(DATA, "corpus.csv")
LOG = os.path.join(DATA, "verification_log.csv")
CONFIG = os.path.join(HERE, "config.json")
PORT = 8000

# Fields the verifier confirms/edits (identity columns are read-only references).
EDIT_FIELDS = ["Title", "Mechanism(s)", "Species", "Life stage", "Fish size",
               "Thresholds/metrics", "Mortality/survival", "Sample size (n=)",
               "Turbine/structure", "Methodology", "Hypotheses/assumptions",
               "Outcome summary", "Notes", "Source depth"]
REF_FIELDS = ["citation_key", "Year", "First author", "Category"]


def load_cfg():
    if os.path.exists(CONFIG):
        return json.load(open(CONFIG, encoding="utf-8"))
    return {}


def save_cfg(cfg):
    json.dump(cfg, open(CONFIG, "w", encoding="utf-8"), indent=2)


def read_csv(p):
    with open(p, encoding="utf-8") as f:
        r = list(csv.DictReader(f))
    return r, (list(r[0].keys()) if r else [])


def write_extraction(rows, fields):
    with open(EXTRACTION, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)


def corpus_index():
    rows, _ = read_csv(CORPUS)
    return {r["citation_key"]: r for r in rows}


def log_event(key, verifier, action, changed):
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["citation_key", "verifier", "date", "action", "fields_changed"])
        w.writerow([key, verifier, datetime.date.today().isoformat(), action, "; ".join(changed)])


def pdf_path(cfg, corp_row):
    base = cfg.get("pdf_base", "")
    return os.path.join(base, corp_row.get("study_type", ""), corp_row.get("local_filename", ""))


CSS = """
*{box-sizing:border-box} body{margin:0;font-family:-apple-system,Segoe UI,Roboto,sans-serif;color:#16313f}
.bar{background:#0e2a3b;color:#fff;padding:10px 16px;display:flex;gap:16px;align-items:center}
.bar b{font-size:15px} .bar .prog{margin-left:auto;font-size:13px;color:#bcd4dd}
.split{display:flex;height:calc(100vh - 48px)}
.pdf{flex:1;border:0} .form{width:46%;max-width:680px;overflow:auto;padding:16px 20px;background:#f7fafb}
.ref{font-size:12px;color:#5b7383;margin-bottom:8px}
label{display:block;font-size:11px;font-weight:700;text-transform:uppercase;color:#5b7383;margin:10px 0 3px}
textarea,input[type=text]{width:100%;padding:7px 9px;border:1px solid #cdd9df;border-radius:6px;font:inherit;font-size:13px}
textarea{min-height:42px;resize:vertical}
.btns{position:sticky;bottom:0;background:#f7fafb;padding:12px 0;border-top:1px solid #dde5e9;margin-top:14px}
button{padding:9px 14px;border:0;border-radius:7px;font-weight:700;cursor:pointer;font-size:13px;margin-right:8px}
.v{background:#2e8b57;color:#fff} .f{background:#d39a2d;color:#fff} .s{background:#e3e9ec;color:#16313f}
a{color:#1f7a8c} .doi{font-size:12px}
.note{background:#fff;border:1px solid #dde5e9;border-radius:6px;padding:8px;font-size:12px;color:#5b7383}
"""


def esc(v):
    return html.escape(v or "", quote=True)


def setup_page(msg=""):
    return f"""<!doctype html><meta charset=utf-8><title>Setup</title><style>{CSS}
    body{{padding:30px;max-width:680px;margin:0 auto}}</style>
    <h2>Verification tool - one-time setup</h2>
    <p class=note>{esc(msg)}</p>
    <form method=post action=/setup>
      <label>Folder where your PDFs live (the local library with study-type subfolders)</label>
      <input type=text name=pdf_base placeholder="e.g. C:\\Users\\You\\...\\Literature\\Barotrauma" style="width:100%">
      <label>Your initials (recorded as the verifier)</label>
      <input type=text name=verifier placeholder="e.g. JAT">
      <div class=btns><button class=v type=submit>Save and start</button></div>
    </form>"""


def row_page(cfg, rows, fields, corp, key=None):
    total = len(rows)
    done = sum(1 for r in rows if r["Confidence"] == "Verified")
    # pick row
    idx = next((i for i, r in enumerate(rows) if r["citation_key"] == key), None) if key else None
    if idx is None:
        idx = next((i for i, r in enumerate(rows) if r["Confidence"] != "Verified"), None)
    if idx is None:
        return f"<!doctype html><meta charset=utf-8><style>{CSS}</style><div class=bar><b>All done</b><span class=prog>{done}/{total} verified</span></div><p style='padding:30px'>Every row is Verified. You can close this tab.</p>"
    r = rows[idx]; key = r["citation_key"]
    crow = corp.get(key, {})
    doi = crow.get("doi", "")
    pp = pdf_path(cfg, crow)
    has_pdf = os.path.exists(pp)
    ref = " &nbsp;|&nbsp; ".join(f"<b>{esc(k)}:</b> {esc(r.get(k,''))}" for k in REF_FIELDS)
    doihtml = (f'<a class=doi href="https://doi.org/{esc(doi)}" target=_blank>{esc(doi)}</a>'
               if doi else '<span class=doi style="color:#aab">no DOI on file</span>')
    pdfpane = (f'<iframe class=pdf src="/pdf?key={urllib.parse.quote(key)}"></iframe>'
               if has_pdf else
               f'<div class=pdf style="padding:30px;background:#fff"><b>PDF not found</b><br><span class=note>Expected at:<br>{esc(pp)}<br><br>Check the PDF folder in config.json or that the file exists.</span></div>')
    inputs = []
    for fld in EDIT_FIELDS:
        val = esc(r.get(fld, ""))
        if fld in ("Title",):
            inputs.append(f'<label>{esc(fld)}</label><input type=text name="{esc(fld)}" value="{val}">')
        else:
            inputs.append(f'<label>{esc(fld)}</label><textarea name="{esc(fld)}">{val}</textarea>')
    form = "\n".join(inputs)
    return f"""<!doctype html><meta charset=utf-8><title>Verify {esc(key)}</title><style>{CSS}</style>
    <div class=bar><b>Verifying: {esc(key)}</b> {doihtml}
      <span class=prog>{done}/{total} verified &middot; verifier {esc(cfg.get('verifier',''))}</span></div>
    <div class=split>
      {pdfpane}
      <form class=form method=post action="/save">
        <input type=hidden name=key value="{esc(key)}">
        <div class=ref>{ref}</div>
        <div class=note>Read the PDF on the left. Confirm each field, edit anything that is wrong,
        then <b>Confirm &amp; mark Verified</b>. If you cannot verify it from the paper, use
        <b>Flag uncertain</b> (stays Mined) and add a note.</div>
        {form}
        <label>Verifier note (optional; saved to the log)</label>
        <input type=text name=_note value="">
        <div class=btns>
          <button class=v name=_action value=verify type=submit>Confirm &amp; mark Verified</button>
          <button class=f name=_action value=flag type=submit>Flag uncertain (stay Mined)</button>
          <a href="/?skip={urllib.parse.quote(key)}"><button class=s type=button>Skip &rarr;</button></a>
        </div>
      </form>
    </div>"""


class H(BaseHTTPRequestHandler):
    def _send(self, body, ctype="text/html; charset=utf-8", code=200):
        b = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

    def log_message(self, *a):
        pass

    def do_GET(self):
        u = urllib.parse.urlparse(self.path); q = urllib.parse.parse_qs(u.query)
        cfg = load_cfg()
        if u.path == "/pdf":
            rows, _ = read_csv(EXTRACTION); corp = corpus_index()
            key = q.get("key", [""])[0]; crow = corp.get(key, {})
            pp = pdf_path(cfg, crow)
            if os.path.exists(pp):
                self._send(open(pp, "rb").read(), "application/pdf"); return
            self._send("PDF not found", code=404); return
        if not cfg.get("pdf_base"):
            self._send(setup_page("Tell the tool where your PDFs are and who you are.")); return
        rows, fields = read_csv(EXTRACTION); corp = corpus_index()
        if u.path == "/" and "skip" in q:
            # advance past the skipped key by jumping to the next non-verified after it
            sk = q["skip"][0]
            order = [r["citation_key"] for r in rows]
            after = order[order.index(sk)+1:] if sk in order else []
            nxt = next((k for k in after if next(r for r in rows if r["citation_key"]==k)["Confidence"]!="Verified"), None)
            self._send(row_page(cfg, rows, fields, corp, key=nxt)); return
        key = q.get("key", [None])[0]
        self._send(row_page(cfg, rows, fields, corp, key=key))

    def do_POST(self):
        ln = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(ln).decode("utf-8")
        form = {k: v[0] for k, v in urllib.parse.parse_qs(body, keep_blank_values=True).items()}
        if self.path == "/setup":
            cfg = load_cfg(); cfg["pdf_base"] = form.get("pdf_base", "").strip()
            cfg["verifier"] = form.get("verifier", "").strip(); save_cfg(cfg)
            self.send_response(303); self.send_header("Location", "/"); self.end_headers(); return
        if self.path == "/save":
            cfg = load_cfg(); rows, fields = read_csv(EXTRACTION)
            key = form.get("key"); action = form.get("_action", "verify")
            note = form.get("_note", "").strip()
            r = next((x for x in rows if x["citation_key"] == key), None)
            if r:
                changed = []
                for fld in EDIT_FIELDS:
                    if fld in form and form[fld] != (r.get(fld) or ""):
                        r[fld] = form[fld]; changed.append(fld)
                if action == "verify":
                    r["Confidence"] = "Verified"
                if note:
                    changed.append(f"note:{note}")
                write_extraction(rows, fields)
                log_event(key, cfg.get("verifier", "?"),
                          "verified" if action == "verify" else "flagged", changed)
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
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    url = f"http://127.0.0.1:{PORT}"
    bar = "=" * 60
    print(f"\n{bar}\n  Verification tool running — open in your browser:\n    {url}\n"
          f"  (Ctrl+C to stop. If no browser opens, paste the URL yourself.)\n{bar}")
    threading.Timer(0.8, lambda: open_browser(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
