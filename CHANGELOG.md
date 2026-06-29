# Changelog

All notable changes to this knowledge base are recorded here. Dates are ISO 8601.
The knowledge base follows a simple MAJOR.MINOR.PATCH scheme (data + methodology).

## [0.2.0] - 2026-06-29
Added the collision (blade strike & impact) module.

### Added
- Collision deep-dive defining collision as any mechanical impact/contact event
  (turbine blade strike, impeller/pump, Archimedean-screw/structure contact,
  wall/draft-tube/plunge-pool impact, pinch/grinding), covering simulated and
  field-observed events.
- `data/collision_register.csv` (48 collision papers),
  `data/collision_reproducibility_scorecard.csv` (25 live-fish studies: 10
  simulated-strike + 15 field-observed), `data/collision_metrics_catalogue.csv`.
- `reviews/collision_overview.md` and generated artefacts in `outputs/`
  (`Collision_metrics_reproducibility.xlsx`,
  `Collision_state_of_the_art_overview.docx`).

### Notes
- Mean reporting completeness for live-fish collision studies was 81% (20 High /
  4 Medium / 1 Low). Largest gaps: explicit collision metric (60%), injury-
  scoring protocol (64%), statistics/dose-response (64%).

## [0.1.0] - 2026-06-29
Initial public release.

### Added
- Bibliographic corpus of 246 publications (1928–2026) with DOIs where found
  (`data/corpus.csv`).
- Structured extraction table for 229 analysed papers across Review / Lab /
  Field / Numerical / Guidelines (`data/extraction.csv`).
- Barotrauma deep-dive: register of 61 barotrauma papers
  (`data/barotrauma_register.csv`), reproducibility scorecard for 38 live-fish
  studies (`data/reproducibility_scorecard.csv`), and a metrics catalogue
  (`data/barotrauma_metrics_catalogue.csv`).
- Controlled vocabularies for mechanisms, metrics and species (`data/vocab/`).
- Documented methodology (`methodology/`) and the `passage-injury-mortality-review`
  skill (`skill/`) plus extraction script (`scripts/`).
- Human-readable reviews (`reviews/`) and generated Excel/Word artefacts
  (`outputs/`).

### Notes
- Categorical/structured fields are a reviewed first pass; 37 quantitative
  claims and 38 reproducibility scores have been checked against sources.
- Source PDFs are intentionally excluded for copyright reasons.
