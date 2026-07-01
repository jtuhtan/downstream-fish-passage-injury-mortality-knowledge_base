#!/usr/bin/env python3
"""Add a searchable text layer to scanned source PDFs with OCRmyPDF (Tesseract).

Scanned, image-only papers (e.g. Neitzel 2004) have no text layer, so the coefficient
verifier can't find or highlight values in them. Run this first to OCR them; then point
`stage_source_pdfs.py` / the verifier's `library_root` at the OCR'd copies and they work
like any other source.

    python scripts/ocr_pdf.py <pdf_or_folder> --out <dir>
    # e.g.  python scripts/ocr_pdf.py /mnt/c/Users/You/fishkb_pdfs --out ~/fishkb_ocr

PDFs that already have a text layer are copied through unchanged (use --force to OCR anyway).

Requires ocrmypdf:   sudo apt install ocrmypdf   (pulls tesseract-ocr + ghostscript)
"""
import argparse
import os
import shutil
import subprocess
import sys


def has_text(path, pt):
    """True if the first pages already carry a real text layer."""
    if not pt:
        return False
    r = subprocess.run([pt, "-l", "3", path, "-"], capture_output=True)
    return r.returncode == 0 and len(r.stdout.strip()) > 120


def main():
    ap = argparse.ArgumentParser(description="OCR scanned PDFs so they become searchable/verifiable.")
    ap.add_argument("path", help="a PDF file or a folder of PDFs")
    ap.add_argument("--out", default=None, help="output folder (default: alongside input, with _ocr suffix)")
    ap.add_argument("--force", action="store_true", help="OCR even PDFs that already have a text layer")
    ap.add_argument("--lang", default="eng", help="Tesseract language(s), e.g. 'eng' or 'eng+deu'")
    a = ap.parse_args()

    ocr = shutil.which("ocrmypdf")
    if not ocr:
        sys.exit("ERROR: ocrmypdf not found.  Install:  sudo apt install ocrmypdf")
    pt = shutil.which("pdftotext")

    if os.path.isdir(a.path):
        pdfs = [os.path.join(dp, f) for dp, _, fs in os.walk(a.path)
                for f in fs if f.lower().endswith(".pdf")]
    elif a.path.lower().endswith(".pdf"):
        pdfs = [a.path]
    else:
        sys.exit(f"{a.path} is not a PDF or a folder")
    if not pdfs:
        sys.exit(f"No PDFs found under {a.path}")
    if a.out:
        os.makedirs(a.out, exist_ok=True)

    n_ocr = n_copy = n_fail = 0
    for p in sorted(pdfs):
        name = os.path.basename(p)
        dest = os.path.join(a.out, name) if a.out else os.path.splitext(p)[0] + "_ocr.pdf"
        if not a.force and has_text(p, pt):
            if a.out:
                shutil.copy2(p, dest); n_copy += 1
                print(f"  text OK, copied     {name}")
            else:
                print(f"  text OK, skipped    {name}")
            continue
        print(f"  OCR (scanned) ...   {name}")
        mode = "--force-ocr" if a.force else "--skip-text"
        r = subprocess.run([ocr, mode, "-l", a.lang, "--output-type", "pdf", p, dest],
                           capture_output=True)
        if r.returncode == 0:
            n_ocr += 1
            print(f"       -> {dest}")
        else:
            n_fail += 1
            print(f"  OCR FAILED ({r.returncode}) {name}\n    {r.stderr.decode('utf-8','replace')[:300]}")

    print(f"\nOCR'd {n_ocr}, copied {n_copy}, failed {n_fail}.")
    if a.out:
        print(f"Point the verifier's library_root (or stage --dest) at:  {os.path.abspath(a.out)}")
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
