# Downstream Fish Passage Injury and Mortality Knowledge Base

A community knowledge base on **how fish are injured and killed during downstream
passage** through hydropower turbines, pumps, Archimedean screws, weirs,
spillways and bypasses — and on **how reliably we actually know it**.

It has two jobs:

1. **Keep an up-to-date, structured literature review** of the field — organised
   by injury mechanism, with thresholds, species, life stages, fish sizes and
   study parameters — plus a focused deep-dive on **barotrauma metrics and the
   reproducibility of live-fish studies**.
2. **Document a rigorous, repeatable methodology** for how the base is built,
   maintained and updated, so anyone can reproduce or extend it.

> **Status:** v0.5.2. Three mechanism modules (barotrauma, collision, shear)
> with reproducibility scorecards; a three-axis framework (mechanism × exposure
> pathway × outcome timing) coded and **fully verified across all 229 analysed
> papers**; plus a first cross-mechanism synthesis and gap matrix. See
> [CHANGELOG.md](CHANGELOG.md). Not yet pushed to GitHub.

## What's inside

| Path | Contents |
|---|---|
| [`data/`](data/) | **Machine-readable source of truth (CSV).** Bibliography, extraction table, barotrauma, collision & shear registers & reproducibility scorecards, metrics catalogues, the cross-cutting exposure/timing axes table, controlled vocabularies. No PDFs. |
| [`reviews/`](reviews/) | Human-readable synthesis: state-of-the-art review; focused barotrauma / collision / shear overviews; and the cross-mechanism synthesis. |
| [`methodology/`](methodology/) | The documented, repeatable pipeline (corpus → screening → extraction → reproducibility → axes → updates). |
| [`skill/`](skill/) | The `passage-injury-mortality-review` skill that operationalises the extraction method. |
| [`scripts/`](scripts/) | Extraction and build scripts. |
| [`outputs/`](outputs/) | Generated artefacts (Excel/Word) built from `data/` + `reviews/`. |

## Important: no source PDFs

This repository **does not contain the research publications themselves** — they
remain under their publishers' copyright. It holds bibliographic metadata
(including DOIs in [`data/corpus.csv`](data/corpus.csv)), derived data and
original summaries. To read a paper, use its DOI; to cite a finding, cite the
original publication.

## How to use it

- **Browse the evidence:** open `data/extraction.csv` (one row per study) and
  filter by mechanism, species, life stage or study type.
- **Query the three axes:** join `data/axes_exposure_timing.csv` (mechanism ×
  exposure pathway × outcome timing) on `citation_key`; roll taxa up via
  `family` / `family_group` in `data/vocab/species.csv`.
- **Assess reproducibility:** see the per-mechanism scorecards
  (`data/barotrauma_reproducibility_scorecard.csv`,
  `data/collision_reproducibility_scorecard.csv`,
  `data/shear_reproducibility_scorecard.csv`) and the matching `reviews/` overviews.
- **See the big picture & gaps:** `reviews/cross_mechanism_synthesis.md` and
  `outputs/Cross_mechanism_gap_matrix.xlsx`.
- **Reproduce / extend:** follow [`methodology/`](methodology/) and run
  `scripts/extract_passage_data.py` on a folder of PDFs.

## Scope & definitions

"Downstream passage" covers fish moving downstream through or over hydraulic
structures. Injury mechanisms follow the controlled vocabulary in
[`data/vocab/mechanisms.csv`](data/vocab/mechanisms.csv): blade strike,
barotrauma, shear, cavitation, turbulence, grinding/abrasion, gas
supersaturation, and entrainment/impingement.

## Coverage at a glance (v0.5.1)

- 246 catalogued publications (1928–2026); 229 analysed across Review / Lab /
  Field / Numerical / Guidelines.
- Barotrauma deep-dive: 61 barotrauma papers; 38 live-fish studies scored for
  reproducibility of reporting.
- Collision (blade strike & impact) deep-dive: 48 collision papers; 25 live-fish
  studies (10 simulated-strike + 15 field-observed) scored.
- Shear (fluid shear / strain rate) deep-dive: 36 shear papers; 12 live-fish
  studies (lab jet/flume) scored. Field live-fish shear evidence is effectively
  absent (shear is studied almost entirely in the laboratory).
- Three-axis framework: every study is described by **mechanism** x **exposure
  pathway** (study environment + location during passage) x **outcome timing**. The two cross-cutting axes are
  coded once per study in `data/axes_exposure_timing.csv` (all 229 papers, fully
  Verified; see `methodology/07_axes_exposure_and_timing.md`).
- Cross-mechanism synthesis & gap matrix: `reviews/cross_mechanism_synthesis.md`
  and `outputs/Cross_mechanism_gap_matrix.xlsx` (coverage by mechanism x family
  group x environment x outcome timing, with explicit data gaps).

## How to cite

See [CITATION.cff](CITATION.cff). Please also cite the **original publications**
for any specific finding (DOIs in `data/corpus.csv`).

## Contributing

Additions and corrections are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).
The golden rule: **never commit PDFs**; add a bibliographic row + extracted data.

## Licensing

- **Code** (`scripts/`, `skill/`): [MIT](LICENSE-CODE)
- **Data & documentation** (`data/`, `methodology/`, `reviews/`, docs):
  [CC BY 4.0](LICENSE-DATA)

## Maintainer

Jeffrey A. Tuhtan (Tallinn University of Technology) · https://github.com/jtuhtan
