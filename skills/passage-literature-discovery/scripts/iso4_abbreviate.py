#!/usr/bin/env python3
"""Abbreviate a title's words following ISO 4:1997 using the LTWA.

ISO 4 ("Information and documentation - Rules for the abbreviation of title words
and titles of publications") is the international standard for abbreviating serial
titles; the abbreviations come from the List of Title Word Abbreviations (LTWA),
maintained by the ISSN International Centre (the ISO 4 registration authority).

This module applies the SAME LTWA word substitutions and ISO 4 rules to produce a
deterministic, citeable short form of a title. Native ISO 4 scope is serial
(journal) titles; applying it to article titles here is a documented extension
that reuses the LTWA vocabulary rather than inventing abbreviations (see
references/title_abbreviation.md).

Rules implemented:
  - omit articles, conjunctions and prepositions (ISO 4 drops these);
  - a title of a single (significant) word is NOT abbreviated;
  - substitute each remaining word via the LTWA (case-insensitive, with simple
    plural handling); words ABSENT from the loaded LTWA are kept in full (this is
    ISO 4-conformant - only listed words are abbreviated);
  - hyphenated compounds: abbreviate each component;
  - full stops mark abbreviations (already present in the LTWA values).

By default it loads the shipped LTWA SUBSET (assets/ltwa_subset.csv). For full
fidelity, pass --ltwa <path> pointing at the complete official LTWA exported as
two columns (word,abbreviation). Get it from https://www.issn.org/services/online-services/access-to-the-ltwa/

Usage:
    python iso4_abbreviate.py "Effects of hydraulic shearing actions on juvenile salmon"
    from iso4_abbreviate import Abbreviator; Abbreviator().abbreviate(title)
"""
import os, re, csv, sys, argparse

# Articles / conjunctions / prepositions omitted by ISO 4 (minimal multilingual set)
STOP = set("""a an the and or but of in on at to for from by with without into onto
within through across over under between among as is are be that this these those
during after before toward towards via per near about against upon throughout
del de la le les des du et un une y o e a au aux dans pour sur avec
der die das den dem des und oder von zu im am beim mit fuer für über auf
""".split())

class Abbreviator:
    def __init__(self, ltwa_path=None):
        if ltwa_path is None:
            ltwa_path = os.path.join(os.path.dirname(__file__), "..", "assets", "ltwa_subset.csv")
        self.ltwa = {}
        with open(ltwa_path, encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                self.ltwa[r["word"].strip().lower()] = r["abbreviation"].strip()

    def _lookup(self, w):
        lw = w.lower()
        for cand in (lw, re.sub(r"ies$", "y", lw), re.sub(r"es$", "", lw), re.sub(r"s$", "", lw)):
            if cand in self.ltwa:
                return self.ltwa[cand]
        return None

    def _abbr_word(self, w):
        if "-" in w:
            return "-".join(self._abbr_word(p) for p in w.split("-"))
        ab = self._lookup(w)
        if ab:
            return ab
        return w[:1].upper() + w[1:] if w else w  # keep full, title-cased

    def abbreviate(self, title):
        title = re.sub(r"\s+", " ", (title or "").strip())
        if not title:
            return ""
        raw = title.split(" ")
        # significant words (strip surrounding punctuation, drop stopwords/empties)
        sig = []
        for tok in raw:
            colon = tok.endswith(":")
            core = re.sub(r"^[^\wÀ-ſ]+|[^\wÀ-ſ-]+$", "", tok)
            if not core or not re.search(r"[A-Za-zÀ-ſ]", core):
                continue
            if core.lower() in STOP:
                continue
            sig.append((core, colon))
        if len(sig) <= 1:                      # single-word titles not abbreviated
            return title
        out = []
        for core, colon in sig:
            out.append(self._abbr_word(core) + (":" if colon else ""))
        return " ".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("title", nargs="+")
    ap.add_argument("--ltwa", default=None, help="path to full LTWA csv (word,abbreviation)")
    a = ap.parse_args()
    print(Abbreviator(a.ltwa).abbreviate(" ".join(a.title)))

if __name__ == "__main__":
    main()
