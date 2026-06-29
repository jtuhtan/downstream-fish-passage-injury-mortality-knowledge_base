# Changelog

All notable changes to this knowledge base are recorded here. Dates are ISO 8601.
The knowledge base follows a simple MAJOR.MINOR.PATCH scheme (data + methodology).

## [0.5.2] - 2026-06-29
Documentation sync to current status.

### Changed
- Renamed `data/reproducibility_scorecard.csv` →
  `data/barotrauma_reproducibility_scorecard.csv` so all three mechanism
  scorecards share the `<mechanism>_reproducibility_scorecard.csv` convention;
  updated references in `methodology/` and `README.md`/`CONTRIBUTING.md`.

### Documentation
- Updated `README.md` (status v0.1.0 → v0.5.1; coverage; "how to use" now covers
  all three mechanisms, the three axes, family roll-ups and the cross-mechanism
  synthesis), `CONTRIBUTING.md` (documentation-as-you-go rule; per-mechanism
  registers; an explicit axes-coding step), `reviews/README.md` (fixed ordering;
  cross-mechanism synthesis listed) and `methodology/README.md` (documentation
  principle). No data changed.

## [0.5.1] - 2026-06-29
Verification pass on the cross-cutting axes.

### Changed
- All 97 Field/Numerical rows in `data/axes_exposure_timing.csv` reviewed
  per-paper and flipped from `Mined` to `Verified` (66 corrected). The axes
  table is now 229/229 Verified. Corrections fixed mis-tagged structures,
  removed spurious Indirect/Latent timing tags, and set Sensor-Fish exposure
  studies to outcome timing "Not reported". Documented in
  `methodology/07_axes_exposure_and_timing.md`.
- Regenerated `outputs/Cross_mechanism_gap_matrix.xlsx` and updated the timing
  table in `reviews/cross_mechanism_synthesis.md` to the verified counts.

## [0.5.0] - 2026-06-29
Consolidation + first cross-mechanism synthesis.

### Added
- `reviews/cross_mechanism_synthesis.md` (+ `outputs/Cross_mechanism_synthesis.docx`)
  comparing the three mechanisms across reproducibility, taxonomy, outcome timing
  and exposure pathway.
- `outputs/Cross_mechanism_gap_matrix.xlsx` - coverage matrices (mechanism x
  family group / environment / outcome timing) with data-gap highlighting.

### Changed
- `data/axes_exposure_timing.csv` extended from the 120-study union to ALL 229
  analysed papers; added a `confidence` verification rule (132 Verified =
  lab/model/review/guideline; 97 Mined = field/numerical). Documented in
  `methodology/07_axes_exposure_and_timing.md`.

### Key findings
- Reproducibility and scope are inversely related (shear 94% but ~12 lab studies;
  barotrauma 74% but the broadest base).
- Evidence is concentrated on salmonids and eels; gobies, sculpins and livebearers
  have ZERO studies across all three mechanisms.
- Latent/long-term and quantified indirect (predation) mortality are the least-
  measured outcomes field-wide.

## [0.4.0] - 2026-06-29
Added the two cross-cutting framework axes (exposure pathway, outcome timing).

### Changed
- `data/vocab/species.csv` now carries `family` (precise taxonomic family) and
  `family_group` (coarser grouping, e.g. "Cyprinids (s.l.)") so findings can be
  aggregated by taxon, not just species. Decision: recently-split cyprinid
  families (Cyprinidae, Leuciscidae, Gobionidae) keep their precise `family` but
  share the `family_group` "Cyprinids (s.l.)"; Alosa kept under Clupeidae.
  Documented in `methodology/04_extraction_schema_and_vocab.md`.
- `skill/SKILL.md`: documentation updating is now an explicit, REQUIRED workflow
  step and principle — every data-processing rule/decision must be recorded in
  methodology + CHANGELOG + vocab in the same change.

### Added
- `data/axes_exposure_timing.csv` - one row per study coding **exposure
  pathway** (`study_environment` + `location_during_passage`) and **outcome
  timing**
  (multi-valued + `delayed_window_h`), keyed by `citation_key`. Coded for the
  120-study union of the barotrauma, collision and shear registers.
- Controlled vocabularies `data/vocab/study_environment.csv`,
  `data/vocab/location_during_passage.csv` and `data/vocab/outcome_timing.csv`.
- `methodology/07_axes_exposure_and_timing.md` documenting the three-axis
  framework (mechanism x exposure pathway x outcome timing) and the coding rules.

### Notes
- Axes are coded once per study (single join table) to avoid duplication/drift.
- Automated first pass (`confidence = Mined`), reviewed; categorical fields read
  from title+abstract and guarded against intro/reference noise; Indirect/Latent
  timing tags are outcome-context-gated. Corpus-wide coding deferred pending
  review of the framework.

## [0.3.0] - 2026-06-29
Added the fluid-shear (strain-rate) module.

### Added
- Shear deep-dive defining shear as fluid-shear / strain-rate injury (submerged
  jets, shear layers, draft-tube and spillway-plunge turbulence), distinct from
  collision and barotrauma.
- `data/shear_register.csv` (36 shear papers),
  `data/shear_reproducibility_scorecard.csv` (12 live-fish lab jet/flume
  studies), `data/shear_metrics_catalogue.csv`.
- `reviews/shear_overview.md` and generated artefacts in `outputs/`
  (`Shear_metrics_reproducibility.xlsx`, `Shear_state_of_the_art_overview.docx`).

### Notes
- Live-fish shear reporting completeness was the highest of the three mechanisms
  (mean 94% among 11 machine-readable studies; 11 High). But the base is small
  and LAB-ONLY: there is effectively no field live-fish shear set, and external
  reproducibility is untested. One foundational study (Neitzel 2004) is a scanned
  PDF that could not be machine-assessed and is flagged for manual scoring.

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
  (`data/barotrauma_register.csv`), reproducib