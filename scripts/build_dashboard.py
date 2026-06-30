#!/usr/bin/env python3
"""Build the interactive GitHub Pages dashboard (docs/index.html).

Reads the repository CSVs in data/, pre-aggregates them, and writes a single
self-contained HTML file with embedded JSON (no external data fetches; Chart.js
via CDN). Re-run after any data change:

    python scripts/build_dashboard.py

The output (docs/index.html) is served by GitHub Pages from the /docs folder.
No PDFs or copyrighted text are included — only derived counts and metadata.
"""
import csv, json, os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "docs", "index.html")


def rd(f):
    with open(os.path.join(D, f), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def build_data():
    ex = rd("extraction.csv"); ax = rd("axes_exposure_timing.csv")
    corp = rd("corpus.csv"); cand = rd("candidate_additions.csv")

    catOrder = ["Lab", "Field", "Numerical", "Review", "Guidelines"]
    byCat = Counter(r["Category"] for r in ex)

    mech = Counter()
    for r in ex:
        for m in [x.strip() for x in r["Mechanism(s)"].split(";") if x.strip()]:
            mech[m] += 1

    dec = Counter()
    for r in corp:
        try:
            dec[f"{(int(r['year'])//10)*10}s"] += 1
        except ValueError:
            pass
    decLabels = sorted(dec, key=lambda s: int(s[:-1]))

    repro = {}
    for m in ["barotrauma", "collision", "shear"]:
        sc = rd(f"{m}_reproducibility_scorecard.csv")
        tk = "Tier" if "Tier" in sc[0] else "tier"
        c = Counter(r[tk] for r in sc)
        repro[m] = {t: c.get(t, 0) for t in ["High", "Medium", "Low"]}

    tim = Counter()
    for r in ax:
        for t in [x.strip() for x in r["outcome_timing"].split(";") if x.strip()]:
            tim[t] += 1
    env = Counter(r["study_environment"].strip() for r in ax if r["study_environment"].strip())

    def srt(counter):
        z = sorted(counter.items(), key=lambda x: -x[1])
        return {"labels": [a for a, _ in z], "data": [b for _, b in z]}

    doi = {r["citation_key"]: r["doi"] for r in corp}
    table = [{"key": r["citation_key"], "year": r["Year"], "author": r["First author"],
              "doi": doi.get(r["citation_key"], ""),
              "cat": r["Category"], "title": r["Title"], "mech": r["Mechanism(s)"],
              "species": r.get("Species", ""), "outcome": r.get("Mortality/survival", ""),
              "conf": r["Confidence"]} for r in ex]

    cands = sorted(
        [{"rank": int(r["rank"]), "priority": r["priority"], "author": r["first_author"],
          "year": r["year"], "cited": int(r["times_cited"]), "themes": r["themes"],
          "short": r["short_title_iso4"]} for r in cand if r["priority"] in ("High", "Medium")],
        key=lambda x: x["rank"])

    return {
        "kpis": {"catalogued": len(corp), "analysed": len(ex), "modules": 3,
                 "candidates": len(cand),
                 "verified": sum(1 for r in ex if r["Confidence"] == "Verified")},
        "byCat": {"labels": catOrder, "data": [byCat[c] for c in catOrder]},
        "byMech": srt(mech), "byDecade": {"labels": decLabels, "data": [dec[l] for l in decLabels]},
        "repro": repro, "byTiming": srt(tim), "byEnv": srt(env),
        "table": table, "cands": cands,
    }


# HTML template lives next to this script to keep them in sync.
TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard_template.html")


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    data = json.dumps(build_data(), ensure_ascii=False)
    with open(TEMPLATE, encoding="utf-8") as fh:
        html = fh.read()
    html = html.replace("__DATA__", data)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"Wrote {OUT} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
