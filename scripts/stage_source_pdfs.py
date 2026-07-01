#!/usr/bin/env python3
"""Stage the source PDFs needed to VERIFY the dose-response models into one flat folder.

Copies only the papers referenced by data/dose_response_models.csv (resolved via
data/vocab/source_pdf_map.csv -> data/corpus.csv `local_filename`), found by a recursive
search under --library, into --dest.

Why: the verifier (tools/verification/verify_models.py) needs to open each model's source
PDF locally. When the full library lives somewhere the verifier can't read directly -- e.g.
a OneDrive library seen from WSL, where placeholder (reparse-point) files don't enumerate on
/mnt/c -- stage just the handful of source files into a plain folder and point the verifier
there.

Run it where the library reads normally (e.g. native Windows for a OneDrive library), then
point the verifier's `library_root` at --dest:

    python scripts/stage_source_pdfs.py --library "C:/…/Literature/Barotrauma" --dest C:/Users/You/fishkb_pdfs
    # then in the verifier setup / config.json:  library_root = that dest (WSL: /mnt/c/Users/You/fishkb_pdfs)
"""
import argparse
import collections
import csv
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")


def read(p):
    with open(p, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser(description="Stage dose-response model source PDFs into one flat folder.")
    ap.add_argument("--library", required=True, help="root of your full PDF library (searched recursively)")
    ap.add_argument("--dest", default=os.path.join(ROOT, "verify_pdfs"), help="flat folder to copy the sources into")
    a = ap.parse_args()

    smap = {r["sr_citation_key"]: r["corpus_citation_key"] for r in read(os.path.join(DATA, "vocab", "source_pdf_map.csv"))}
    ck = {r["citation_key"]: r for r in read(os.path.join(DATA, "corpus.csv"))}
    mods = read(os.path.join(DATA, "dose_response_models.csv"))
    need = collections.Counter(smap.get(m["citation_key"], m["citation_key"]) for m in mods)

    print(f"Indexing PDFs under {a.library} ...")
    idx = {}
    for dp, _, fs in os.walk(a.library):
        for f in fs:
            if f.lower().endswith(".pdf"):
                idx.setdefault(f, os.path.join(dp, f))
    print(f"  {len(idx)} PDFs found.\n")

    os.makedirs(a.dest, exist_ok=True)
    ok = miss = 0
    for c, n in sorted(need.items(), key=lambda x: -x[1]):
        fn = ck.get(c, {}).get("local_filename", "")
        src = idx.get(fn)
        if src:
            shutil.copy2(src, os.path.join(a.dest, fn)); ok += 1
            print(f"  OK    {c:<16} ({n:>2} models)  {fn[:52]}")
        else:
            miss += n
            print(f"  MISS  {c:<16} ({n:>2} models)  {fn or '(no filename in corpus)'}")

    print(f"\nStaged {ok} source PDF(s) -> {a.dest}   ({len(mods) - miss}/{len(mods)} models covered)")
    if miss:
        print("  Some sources were not found under --library; check the filename in data/corpus.csv "
              "and data/vocab/source_pdf_map.csv.")
    print(f"Point the verifier's library_root at:  {os.path.abspath(a.dest)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
