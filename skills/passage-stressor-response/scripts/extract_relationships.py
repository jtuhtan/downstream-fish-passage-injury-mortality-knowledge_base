#!/usr/bin/env python3
"""First-pass finder for stressor->response relationships in passage PDFs.

It does NOT fill the structured schema. It surfaces *candidates* — equations,
statistical results, threshold/dose sentences, and dose-response figure/table
captions — each with its page, a relevance `score`, and a snippet, so a human (or a
careful pass) knows exactly where to read and can then write rows into
data/stressor_response.csv and data/equations.csv per
skills/passage-stressor-response/references/schema.md.

Precision-leaning. A hit needs a relevant UNIT or NAMED METRIC to co-occur with an
injury/mortality cue (thresholds), statistical-test markers with a dose/injury cue
(stat results), recognised math structure (equations), or a relational phrase in a
figure/table caption. Table-of-contents leader lines are dropped. Output is sorted
by `score` (dose metric + %-outcome rank highest).

Dependencies: Python stdlib + `pdftotext` (poppler) on PATH. No PDFs enter the repo;
only extracted candidate text.

Usage:
    python extract_relationships.py <pdf_or_folder> -o relationship_candidates.csv
"""
from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

# --- lexicons --------------------------------------------------------------
UNIT = re.compile(
    r"(kPa|MPa|psi|\bm\s?[·/]?\s?s\s?[-−^]?1?\b|\bm/s\b|\bs\s?[-−^]?1\b|\b1/s\b|"
    r"%\s?(?:TDG|saturation|BEP)?|\bRPC\b|\bLRP\b|\bTDG\b|\brpm\b|\bs⁻¹\b)",
    re.IGNORECASE,
)
INJURY = re.compile(
    r"(mortalit|surviv|injur|malad|ruptur|h[ae]morrhag|exophthalm|emboli|barotrauma|"
    r"decompress|strain rate|strike (?:velocit|probabilit)|nadir|LD\s?50|"
    r"E[MC]\s?50|LC\s?50|threshold|dose[- ]?response|GBT|gas[- ]bubble)",
    re.IGNORECASE,
)
DOSE_METRIC = re.compile(
    r"(\bRPC\b|\bLRP\b|\bnadir\b|ratio of pressure|log ratio of pressure|strain rate|"
    r"strike velocit|acclimat)", re.IGNORECASE,
)
# Statistical-result markers (so stats stop being mis-read as equations).
STAT = re.compile(
    r"(\bP\s*[=<>]\s*0?\.\d|\bd\.?\s?f\.?\s*=|\bp\s*[<=>]\s*0?\.\d|\bχ\s*2|"
    r"chi-?square|\bR²|\br2\s*=|95\s*%\s*CI|odds[- ]?ratio|Fisher)", re.IGNORECASE,
)
NUMBER = re.compile(r"\d")
EQ_MATH = re.compile(r"=")
EQ_TOKENS = re.compile(r"(exp|log|ln|√|Σ|∑|≈|≤|≥|×|·|\^|/|\bP\s*=|[α-ωΑ-Ω])")
EQ_CUE = re.compile(r"\b(equation|eq\.?)\s*\(?\d", re.IGNORECASE)
CAPTION = re.compile(r"^\s*(fig(?:ure)?\.?|table)\s*\.?\s*\d", re.IGNORECASE)
RELATIONAL = re.compile(
    r"(as a function of|versus|\bvs\.?\b|relationship|probabilit|"
    r"mortalit|surviv|dose|response|against|with increasing)",
    re.IGNORECASE,
)
TOC_LEADER = re.compile(r"\.\s?\.\s?\.\s?\.")  # dotted leader => table-of-contents

COLUMNS = ["citation_key", "source_pdf", "page", "kind", "score", "matched_terms", "snippet"]


def citation_key(pdf: Path) -> str:
    """Provisional key from the `YYYY_FirstAuthor_...` naming convention."""
    parts = pdf.stem.split("_")
    if len(parts) >= 2 and re.fullmatch(r"\d{3,4}", parts[0]):
        return f"{re.sub(r'[^A-Za-z]', '', parts[1])}{parts[0]}"
    return pdf.stem


def pages(pdf: Path) -> list[str]:
    out = subprocess.run(
        ["pdftotext", str(pdf), "-"], capture_output=True, text=True, errors="ignore"
    )
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip() or "pdftotext failed")
    return out.stdout.split("\f")


def _score(kind: str, snippet: str) -> int:
    base = {"equation": 3, "equation_ref": 2, "stat_result": 2,
            "figure_or_table": 2, "threshold_or_dose": 1}.get(kind, 1)
    s = base
    if DOSE_METRIC.search(snippet):
        s += 2
    if "%" in snippet and INJURY.search(snippet):
        s += 2
    if UNIT.search(snippet):
        s += 1
    return s


def _row(key: str, pdf: Path, page: int, kind: str, snippet: str) -> dict:
    terms = sorted({m.group(0).strip().lower() for m in UNIT.finditer(snippet)} |
                   {m.group(0).lower() for m in INJURY.finditer(snippet)} |
                   {m.group(0).lower() for m in DOSE_METRIC.finditer(snippet)})
    return {
        "citation_key": key, "source_pdf": pdf.name, "page": page, "kind": kind,
        "score": _score(kind, snippet),
        "matched_terms": "; ".join(t for t in terms if t),
        "snippet": snippet.strip(),
    }


def scan(pdf: Path) -> list[dict]:
    key = citation_key(pdf)
    rows: list[dict] = []
    for pno, text in enumerate(pages(pdf), start=1):
        lines = [ln.strip() for ln in text.splitlines()]
        for i, ln in enumerate(lines):
            ctx = ln + " " + (lines[i + 1] if i + 1 < len(lines) else "")
            if CAPTION.match(ln) and RELATIONAL.search(ctx) and not TOC_LEADER.search(ctx):
                rows.append(_row(key, pdf, pno, "figure_or_table", ln[:300]))
        blob = re.sub(r"\s+", " ", text)
        for sent in re.split(r"(?<=[.;])\s+", blob):
            s = sent.strip()
            if not s or len(s) > 400 or TOC_LEADER.search(s):
                continue
            if EQ_CUE.search(s):
                kind = "equation_ref"
            elif STAT.search(s) and (DOSE_METRIC.search(s) or INJURY.search(s)):
                kind = "stat_result"
            elif (EQ_MATH.search(s) and EQ_TOKENS.search(s) and not STAT.search(s)
                  and len(s) < 200 and not s.endswith(".")):
                kind = "equation"
            elif NUMBER.search(s) and UNIT.search(s) and INJURY.search(s):
                kind = "threshold_or_dose"
            else:
                continue
            rows.append(_row(key, pdf, pno, kind, s[:300]))
    return _dedupe(rows)


def _dedupe(rows: list[dict]) -> list[dict]:
    seen, out = set(), []
    for r in rows:
        k = (r["kind"], r["snippet"][:120])
        if k not in seen:
            seen.add(k)
            out.append(r)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", help="A PDF file or a folder of PDFs.")
    ap.add_argument("-o", "--out", default="relationship_candidates.csv")
    args = ap.parse_args(argv)

    src = Path(args.input)
    pdfs = sorted(src.glob("**/*.pdf")) if src.is_dir() else [src]
    if not pdfs:
        print(f"No PDFs found at {src}", file=sys.stderr)
        return 1

    all_rows: list[dict] = []
    for pdf in pdfs:
        try:
            hits = scan(pdf)
            all_rows.extend(hits)
            print(f"[{pdf.name}] {len(hits)} candidates")
        except FileNotFoundError:
            print("ERROR: `pdftotext` not found — install poppler-utils.", file=sys.stderr)
            return 2
        except Exception as e:
            print(f"[{pdf.name}] skipped: {e}", file=sys.stderr)

    all_rows.sort(key=lambda r: (-r["score"], r["citation_key"], r["page"]))
    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(all_rows)
    print(f"\nWrote {len(all_rows)} candidate rows (sorted by score) from "
          f"{len(pdfs)} PDF(s) -> {args.out}")
    print("Next: read each candidate's page and write structured rows per "
          "references/schema.md (confidence=Mined until verified).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
