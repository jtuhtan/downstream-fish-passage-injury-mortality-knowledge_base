# Changelog

All notable changes to this knowledge base are recorded here. Dates are ISO 8601.
The knowledge base follows a simple MAJOR.MINOR.PATCH scheme (data + methodology).

## [0.11.0] - 2026-06-30
Offline verification tool + reset all rows to Mined.

### Added
- `tools/verification/verify.py` — an **offline, dependency-free** (Python stdlib)
  local web app for confirming the source-of-truth data against the original PDFs.
  Shows each PDF beside an editable form of every field; writes confirmed data back
  to `data/extraction.csv` (sets `Confidence = Verified`) and appends provenance
  (`verifier, date, fields_changed`) to `data/verification_log.csv`. Runs locally
  because it needs the (uncommitted) PDF library. Includes `README.md` and
  `config.example.json`; `config.json` is git-ignored.
- `methodology/08_verification_protocol.md` — the protocol and per-field rules for
  what counts as "Verified"; added stage 8 to the methodology pipeline.

### Changed
- **Reset all `extraction.csv` rows to `Mined`** (37 were Verified). Earlier ad-hoc
  verification predates this formal PDF-in-hand process, so the slate is cleared;
  rows become Verified only via `verify.py`. Dashboard "Verified" KPI now 0.

### Rationale
- Makes verification a documented, repeatable, auditable process others can run and
  extend — not a one-off. Provenance is recorded per row.

## [0.10.0] - 2026-06-30
Regenerated outputs; DOI column and full titles in the dashboard.

### Added
- `scripts/build_outputs.py` — reproducibly regenerates everything in `outputs/`
  from the source data + reviews (Word reports via pandoc; workbooks via openpyxl;
  recomputed cross-mechanism gap matrix). Replaces hand-built artefacts.

### Changed
- Regenerated all 10 `outputs/` artefacts so they reflect the current corpus
  (post-dedup, corrected titles).
- Synced `extraction.csv` titles to the authoritative `corpus.csv` titles (101
  rows) so the dashboard and extraction workbook show full, corrected titles.
- Dashboard (`docs/index.html`): added a **DOI column** after Author (linked to
  doi.org; 140/228 rows have a DOI), the evidence table now shows the **full
  title**, and search covers DOI. Removed hard-coded counts from the template.

## [0.9.2] - 2026-06-29
Duplicate consolidation and a full title QA pass.

### Removed
- Confirmed `200x_Dixon` and `2011_Amaralb` are the **same** document (identical
  author, creation timestamp, page count; first-3-page text overlap = 1.00 — both
  the Amaral & Hecker 2011 conference presentation). Removed the `200x_Dixon`
  rows from `corpus.csv`, `extraction.csv`, `collision_register.csv`,
  `collision_reproducibility_scorecard.csv` and `axes_exposure_timing.csv`, and
  moved its PDF to `_Duplicates_review/`. New counts: **245** catalogued, **228**
  analysed; collision 47 papers / 24 live-fish (9 simulated-strike + 15 field).

### Changed
- Full QA re-scan of all remaining titles (`Barotrauma/title_qa.csv`). 219 were
  correct; 25 "fuller" flags were journal-name prefixes (current titles already
  correct); **2 genuinely truncated titles fixed** (Schneider 2025, Zillig 2025)
  and those 2 PDFs re-renamed. One supplementary-material file (Zítek 2026) left
  as "Supplementary".
- Updated counts in `README.md` (status, coverage, study-type pie) and rebuilt
  `docs/index.html`.

## [0.9.1] - 2026-06-29
Manual review of the low-confidence (`review`-tier) titles.

### Changed
- Corrected 6 titles after a manual walk-through: Linnansaari 2015
  ("Fish passage in large rivers: a literature review"), Dixon 200x
  ("Designing leading edges of turbine blades to increase fish survival from
  blade strike"), Sættem 1990 ("Skadefrekvens hos laksefisk etter nedvandring i
  foss"), STOWA 2012 ("Gemalen of vermalen worden?"), Benigni 2020 ("Downstream
  fish migration in a Kaplan turbine – Part 2: …"), MacMillan 2016 ("Evaluation
  of the response of American eels to rapid decompression"). 3 PDFs re-renamed;
  the other 3 already had an equivalent ISO-4 stem. The remaining 10 `review`
  rows were confirmed correct as-is.
- Flagged **Dixon 200x** and **Amaral 2011b** as likely duplicates (same title)
  in `title_scan_manifest.csv` for verification against the PDFs.

## [0.9.0] - 2026-06-29
Re-read titles from the PDFs and corrected the corpus.

### Changed
- Scanned all 246 PDFs and extracted authoritative titles from embedded `pdfinfo`
  metadata + a largest-font first-page heuristic (`pdftohtml -xml`), with masthead
  stripping, all-caps normalisation and noisy-tail trimming. Each was confidence-
  flagged and reviewed via `Barotrauma/title_scan_manifest.csv`.
- Applied **112** corrected titles to `data/corpus.csv` (tiers improved + likely +
  review): fuller titles with recovered subtitles, typo fixes (e.g. "hydraulc" →
  "Hydraulic"), de-cruft (e.g. "…-amaral"), and several non-English originals.
  103 already matched; 31 had no clean extraction and were kept.
- Re-derived ISO-4 filenames from the corrected titles and **renamed 110 PDFs in
  place** (two-phase rename; `local_filename` re-synced; reorganization manifest
  refreshed). Rebuilt `docs/index.html`.
- Documented the title source in `methodology/01_corpus_acquisition_and_naming.md`.

### Notes
- The `review`-tier titles (16) are low-confidence; a few are known to be wrong
  (e.g. Linnansaari 2015 picked up an affiliation, "MAES Canadian Rivers
  Institute"). The manifest is the audit trail for correcting them.

## [0.8.1] - 2026-06-29
Resolved the Medium-priority candidates' ISO-4 short titles.

### Changed
- `data/candidate_additions.csv`: the 15 **Medium**-priority candidates resolved to
  canonical titles; `short_title_iso4` recomputed via `iso4_abbreviate.py` (no
  longer "(pending canonical resolution)"). DOIs verified for 8 (Muir 2001, Mathur
  2000, Paish 2002, Bracken 2013, McNabb 2003, Larinier 2002, Cada 1990, Weitkamp
  1980); Ferguson 2006 title verified, DOI unconfirmed; the rest are conference/
  trade/report/grey literature without DOIs. Two data-quality flags recorded in
  `notes`: Bracken 2013 is about **lampreys** (not "fish" as loosely parsed), and
  the Mathur 2000 reference parse was garbled/merged with a Normandeau report —
  the key→work mapping should be confirmed. All High + Medium (26 of 72) now have
  ISO-4 short titles; the 46 Low-priority remain pending.
- Rebuilt `docs/index.html` so the dashboard's candidate table shows the resolved
  short titles.

## [0.8.0] - 2026-06-29
Added an interactive dashboard (GitHub Pages) and native README diagrams.

### Added
- `docs/index.html` — a self-contained interactive dashboard built from the CSVs:
  KPI cards, publications-by-decade, papers-by-mechanism, live-fish
  reproducibility tiers, outcome-timing coverage, study-type and study-environment
  charts, plus a filterable/sortable evidence table (229 studies) and the top
  candidate-additions table. Data embedded as JSON; Chart.js via CDN; no PDFs.
- `scripts/build_dashboard.py` + `scripts/dashboard_template.html` — reproducible
  generator (`python scripts/build_dashboard.py` rebuilds `docs/index.html`).
- README "Visual overview": natively-rendered **Mermaid** pipeline + study-type
  diagrams, a link to the dashboard, and a **GitHub Pages** publishing guide
  (Deploy from a branch → `/docs`).

### Changed
- `CITATION.cff` `repository-code` corrected to the actual repo URL
  (`…-injury-mortality-knowledge_base`).

## [0.7.0] - 2026-06-29
Adopted the ISO 4 / LTWA short title as the local PDF filename convention.

### Changed
- Local PDF naming convention is now
  `YYYY_FirstAuthor_StudyType_ShortTitle.pdf`, where `ShortTitle` is the
  **ISO 4 / LTWA** short title (via `iso4_abbreviate.py`) rendered filename-safe
  (ASCII transliteration; periods/colons removed; spaces and hyphens → `_`).
  This aligns filenames with the `short_title_iso4` field used for candidates, so
  titles are abbreviated by one standard everywhere. Documented in
  `methodology/01_corpus_acquisition_and_naming.md`.
- Renamed all 246 catalogued PDFs in place across the six study-type folders and
  updated `data/corpus.csv` `local_filename` accordingly (data↔file link intact).

### Added / refreshed
- `Barotrauma/title_abbreviation_rename_manifest.csv` — the reviewed old→new map
  (status `renamed`); `Barotrauma/_reorganization_manifest.csv` "New location"
  basenames updated to current names.

### Verification
- Post-rename: 246/246 PDFs present; per-folder counts unchanged; every corpus
  row resolves on disk; zero residual spaced (old-style) names; zero duplicates;
  exact corpus↔disk set match per folder.

## [0.6.2] - 2026-06-29
Resolved the High-priority candidates and filled their ISO-4 short titles.

### Changed
- `data/candidate_additions.csv`: the 11 **High**-priority candidates resolved to
  canonical titles; `short_title_iso4` recomputed via `scripts/iso4_abbreviate.py`
  (no longer "(pending canonical resolution)"). DOIs verified for 3 (Rummer 2005
  `10.1577/T04-235.1`; Mathur 1996 `10.1139/f95-206` — journal is CJFAS, not
  Hydrobiologia; Larinier 2008 `10.1007/s10750-008-9398-9`). The other 8 are
  pre-DOI / grey literature (Turnpenny 1998 book chapter; Harvey 1963 dissertation;
  Carlson 2008 PNNL report — likely duplicate of 2008_Deng; von Raben 1957; etc.),
  each annotated in `notes` with canonical title + DOI status. Medium/Low rows
  unchanged.

### Notes
- The Crossref/OpenAlex REST resolution pass was attempted but those JSON APIs are
  unreachable from this build's sandbox (Crossref timed out; OpenAlex empty), so
  resolution used `WebSearch` to confirm titles/DOIs, then the abbreviator.
  Provenance recorded in `skills/passage-literature-discovery/references/candidate_schema.md`.

## [0.6.1] - 2026-06-29
Standardised title abbreviation on ISO 4 / LTWA.

### Added
- `skills/passage-literature-discovery/references/title_abbreviation.md` — adopts
  **ISO 4:1997** and the **LTWA** (ISSN International Centre; the journal-
  abbreviation standard) as the fixed schema for short titles, with rules,
  citations, the canonical-resolution-first workflow, and worked examples.
- `skills/passage-literature-discovery/scripts/iso4_abbreviate.py` (ISO 4
  abbreviator) and `assets/ltwa_subset.csv` (verifiable LTWA subset; upgrade path
  to the full official LTWA / AbbrevIso / abbrevr).

### Changed
- `data/candidate_additions.csv`: replaced ad-hoc `title_snippet_approx` with
  `title_as_cited` (verbatim parse) + `short_title_iso4` (ISO-4/LTWA short title,
  provisional until DOI-resolved). Updated the discovery script, candidate schema,
  SKILL.md and reviews note accordingly.

### Rationale
- Short titles now follow an established, citeable standard rather than home-grown
  truncation — reusing the same vocabulary as journal abbreviations for rigour and
  reproducibility. ISO 4's native scope is serial titles; applying its LTWA word
  list to article titles is a documented extension (see the reference file).

## [0.6.0] - 2026-06-29
Added a literature-discovery skill and a ranked candidate-additions list.

### Added
- New skill `skills/passage-literature-discovery/` — gap-driven discovery of works
  MISSING from the collection, via citation snowballing (works cited by many
  included papers but not in the corpus), ranked by in-collection citation
  frequency and tagged to mechanism themes. Includes `SKILL.md`, a ranking rubric,
  a candidate schema, and `scripts/discover_candidates.py`.
- `data/candidate_additions.csv` — 72 candidate works (>=5 citing collection
  papers; 11 High / 15 Medium / 46 Low priority) with theme tags and approximate
  titles, plus `reviews/candidate_additions.md` summarising the top items and
  caveats.

### Changed
- Reorganised skills under a `skills/` directory: the existing skill moved to
  `skills/passage-injury-mortality-review/` (was `skill/`). Updated references in
  `README.md` and `methodology/README.md`.

### Notes
- Candidate titles are approximate (parsed from reference text); author+year are
  reliable. Resolve full citations + DOIs before adding. Several High items are
  field classics (e.g. Turnpenny 1992/1998, Cada 1990/1997, Cramer 1964, von
  Raben 1957, MontEn 1985 — already in the library as a .zip but uncatalogued).

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
  collision an