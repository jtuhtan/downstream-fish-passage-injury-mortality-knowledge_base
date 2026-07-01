#!/usr/bin/env python3
"""First-pass finder for the `passage-stressor-response` skill.

Surfaces candidate **equations**, **threshold sentences** and **dose-response
captions/coefficient tables** in a passage paper, each with its **page, relevance
score and snippet** -- so a human (or a careful pass) knows where to read. It does
NOT write schema rows: all structured extraction stays manual, `confidence = Mined`
until verified (see references/extraction_playbook.md).

Usage:
    python scripts/extract_relationships.py <pdf_or_folder> [options]

Options:
    --top N          max candidates shown per file (default 25; 0 = all)
    --min-score S    hide candidates scoring below S (default 6)
    --types T,...    restrict to categories: equation,threshold,dose (default all)
    --context        also print the line above/below each hit
    --csv PATH       write all candidates (file,page,score,category,snippet) to CSV
    --quiet          per-file summary only, no candidate lines

Requires the `pdftotext` binary (poppler / Git-for-Windows). No Python deps.
"""
from __future__ import annotations

import argparse
import csv
import re
import shutil
import subprocess
import sys
from pathlib import Path

# --------------------------------------------------------------------------- #
# Detection rules.  Each: (compiled regex, category, base weight).
# Categories: "dose" (dose-response caption / coefficient table) > "equation" >
# "threshold".  A line may match several rules; it takes the highest base weight
# and earns bonuses for the others plus quantitative signals.
# --------------------------------------------------------------------------- #
I = re.IGNORECASE
RULES = [
    # ---- dose-response captions & coefficient tables (highest value) ----
    (re.compile(r"dose[\s–-]?response", I), "dose", 8),
    (re.compile(r"biological response model", I), "dose", 8),
    (re.compile(r"probability of (injury|mortality|death|major injury|survival|being struck)", I), "dose", 7),
    (re.compile(r"\btable\s*\d+\b.{0,70}(coefficient|logistic|regression|probabilit|E\s?D?50|mortalit)", I), "dose", 9),
    (re.compile(r"\bfigure\s*\d+\b.{0,90}(probabilit|mortalit|surviv|dose|versus|\bvs\b|strain rate|strike velocit)", I), "dose", 6),
    (re.compile(r"(response|survival|mortality)\s+curve|susceptibilit", I), "dose", 5),
    # ---- equations / model forms ----
    (re.compile(r"\bequation\s*\(?\s*\d+\s*\)?", I), "equation", 7),
    (re.compile(r"\b(log[-\s]?logistic|logistic regression|multiple linear regression|logit)\b", I), "equation", 7),
    (re.compile(r"P\s*\(\s*[MSXms]\s*\)\s*=|f\s*\(\s*x", I), "equation", 7),
    (re.compile(r"1\s*/\s*\(\s*1\s*\+|1\s*\+\s*e\s*\^|\bexp\s*\(", I), "equation", 6),
    (re.compile(r"\b(β0|β1|b0|b1|Vcrit|inclination point|intercept|slope|E\s?D?50|LD50|RPC50|S50)\b"), "equation", 6),
    (re.compile(r"=\s*[-−]?\d+\.\d+\s*[+\-−]\s*\d+\.\d+"), "equation", 6),  # a + b*x
    (re.compile(r"\bLn?\s*\(\s*x|\bln\s*\("), "equation", 4),
    # ---- threshold sentences (number + outcome / landmark dose) ----
    (re.compile(r"\b\d{1,3}(\.\d+)?\s*%\s*(mortalit|surviv|injur|descal)", I), "threshold", 6),
    (re.compile(r"(mortalit|surviv|injur\w*)\D{0,25}\b\d{1,3}(\.\d+)?\s*%", I), "threshold", 5),
    (re.compile(r"\b(E\s?D?50|LD50|S50|RPC50|EM50)\b"), "threshold", 7),
    (re.compile(r"\b(threshold|onset|began to occur|no (injur|mortalit|fish (surv|die))|all fish (die|surv)|100\s*%)", I), "threshold", 5),
    (re.compile(r"\b\d+(\.\d+)?\s*(m\s*s[−-]?1|m/s)\b", I), "threshold", 3),   # strike velocity
    (re.compile(r"\b\d{2,4}\s*s[−-]?1\b", I), "threshold", 3),                  # strain rate
    (re.compile(r"\b\d+(\.\d+)?\s*kPa\b", I), "threshold", 3),                       # pressure
    (re.compile(r"\b(RPC|L/t)\b\D{0,12}\d", I), "threshold", 3),
]

# small controlled-vocabulary bonus (aligns with stressors_and_predictors.md)
VOCAB = re.compile(
    r"\b(strain[ _]?rate|shear|blade|strike|barotrauma|nadir|acclimat|decompress|"
    r"RPC|LRP|turbine|pump|Kaplan|Francis|mutilation|von raben|velocit|strand)\b", I)
UNIT = re.compile(r"\b(m\s*s[−-]?1|m/s|s[−-]?1|kPa|m\s*s[−-]?2|%)\b", I)
NUM = re.compile(r"[-−]?\d+\.?\d*")
COEFF = re.compile(r"\b(E\s?D?50|LD50|S50|RPC50|coefficient|estimate|β[01]|b[01])\b", I)
CAT_RANK = {"dose": 0, "equation": 1, "threshold": 2}


def find_pdftotext() -> str:
    exe = shutil.which("pdftotext")
    if exe:
        return exe
    for c in [
        r"C:\Users\User\AppData\Local\Programs\Git\mingw64\bin\pdftotext.exe",
        r"C:\Program Files\Git\mingw64\bin\pdftotext.exe",
        "/usr/bin/pdftotext", "/usr/local/bin/pdftotext",
    ]:
        if Path(c).exists():
            return c
    sys.exit("ERROR: `pdftotext` not found. Install poppler-utils (or use Git for Windows).")


def pdf_pages(pdf: Path, pt: str) -> list[str]:
    """Return page texts (layout mode; page breaks on form-feed)."""
    r = subprocess.run([pt, "-layout", str(pdf), "-"], capture_output=True)
    if r.returncode != 0:
        return []
    text = r.stdout.decode("utf-8", "replace")
    pages = text.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages


def collapse(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("�", " ")).strip()


def score_line(line: str):
    """Return (category, score, hit_types) or None."""
    hits = {}
    for rx, cat, w in RULES:
        if rx.search(line):
            hits[cat] = max(hits.get(cat, 0), w)
    if not hits:
        return None
    cat = min(hits, key=lambda c: CAT_RANK[c])  # best (dose>equation>threshold)
    base = hits[cat]
    bonus = sum(v for c, v in hits.items() if c != cat) * 0.5      # multi-signal
    bonus += min(len(set(m.group(0).lower() for m in VOCAB.finditer(line))), 5)
    bonus += min(len(NUM.findall(line)), 4) * 0.5                  # quantitative
    if UNIT.search(line):
        bonus += 2
    if COEFF.search(line):
        bonus += 5                                                # landmark/coeff
    return cat, round(base + bonus), sorted(hits)


def scan_pdf(pdf: Path, pt: str, types: set[str], min_score: int):
    pages = pdf_pages(pdf, pt)
    chars = sum(len(p) for p in pages)
    cands = []
    for pno, page in enumerate(pages, 1):
        for raw in page.splitlines():
            line = collapse(raw)
            if len(line) < 6:
                continue
            res = score_line(line)
            if not res:
                continue
            cat, sc, _ = res
            if cat not in types or sc < min_score:
                continue
            cands.append({"page": pno, "score": sc, "category": cat, "snippet": line[:200]})
    cands.sort(key=lambda c: (-c["score"], c["page"]))
    return cands, len(pages), chars


def print_report(pdf: Path, cands, npages, chars, args, page_lines):
    print("\n" + "=" * 96)
    print(f"{pdf.name}   ({npages} pages)")
    if npages == 0 or chars < 400:
        print("  !! no extractable text (scanned image PDF?) -- OCR needed before this finder is useful")
        return
    by_cat = {}
    by_page = {}
    for c in cands:
        by_cat[c["category"]] = by_cat.get(c["category"], 0) + 1
        by_page[c["page"]] = by_page.get(c["page"], 0) + 1
    summ = ", ".join(f"{by_cat.get(k, 0)} {k}" for k in ("dose", "equation", "threshold"))
    hot = ", ".join(f"p{p}({n})" for p, n in sorted(by_page.items(), key=lambda x: -x[1])[:6])
    print(f"  candidates: {summ}   |   hottest pages: {hot or '-'}")
    if args.quiet:
        return
    shown = cands if args.top == 0 else cands[: args.top]
    print("-" * 96)
    print(f"  {'score':>5}  {'page':>4}  {'type':<9}  snippet")
    for c in shown:
        print(f"  {c['score']:>5}  p{c['page']:<3}  {c['category']:<9}  {c['snippet'][:112]}")
        if args.context:
            lines = page_lines.get(c["page"], [])
            # best-effort context: find the snippet's source line index
            for i, ln in enumerate(lines):
                if c["snippet"][:40] in collapse(ln):
                    if i > 0:
                        print(f"            prev: {collapse(lines[i-1])[:100]}")
                    if i + 1 < len(lines):
                        print(f"            next: {collapse(lines[i+1])[:100]}")
                    break


def main(argv=None) -> int:
    try:  # keep snippets printable on any console (Windows cp125x etc.)
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(
        description="First-pass finder: candidate equations / thresholds / dose-response, with page + score.")
    ap.add_argument("path", help="a PDF file or a folder of PDFs")
    ap.add_argument("--top", type=int, default=25, help="max candidates per file (0 = all)")
    ap.add_argument("--min-score", type=int, default=6, dest="min_score")
    ap.add_argument("--types", default="equation,threshold,dose",
                    help="comma list of categories to keep")
    ap.add_argument("--context", action="store_true", help="print the line above/below each hit")
    ap.add_argument("--csv", help="also write all candidates to this CSV")
    ap.add_argument("--quiet", action="store_true", help="summaries only")
    args = ap.parse_args(argv)

    types = {t.strip() for t in args.types.split(",") if t.strip()}
    pt = find_pdftotext()
    root = Path(args.path)
    if root.is_dir():
        pdfs = sorted(root.rglob("*.pdf"))
    elif root.suffix.lower() == ".pdf":
        pdfs = [root]
    else:
        sys.exit(f"ERROR: {root} is not a PDF or folder.")
    if not pdfs:
        sys.exit(f"No PDFs found under {root}.")

    all_rows = []
    print(f"Scanning {len(pdfs)} PDF(s) with {Path(pt).name}  |  types={sorted(types)}  min-score={args.min_score}")
    for pdf in pdfs:
        cands, npages, chars = scan_pdf(pdf, pt, types, args.min_score)
        page_lines = {}
        if args.context:
            for pno, page in enumerate(pdf_pages(pdf, pt), 1):
                page_lines[pno] = page.splitlines()
        print_report(pdf, cands, npages, chars, args, page_lines)
        for c in cands:
            all_rows.append({"file": pdf.name, **c})

    if args.csv:
        with open(args.csv, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["file", "page", "score", "category", "snippet"])
            w.writeheader()
            w.writerows(all_rows)
        print(f"\nWrote {len(all_rows)} candidates -> {args.csv}")

    print(f"\nDone. {len(all_rows)} candidate location(s) across {len(pdfs)} file(s). "
          "Read the hottest pages; write schema rows by hand (confidence = Mined).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
