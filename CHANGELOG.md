# Changelog

All notable changes to this knowledge base are recorded here. Dates are ISO 8601.
The knowledge base follows a simple MAJOR.MINOR.PATCH scheme (data + methodology).

## [0.22.0] - 2026-06-30
Updated the stressor–response skill to current state and re-ran the barotrauma analysis under it.

### Changed
- **Updated the `passage-stressor-response` skill** (SKILL.md + schema.md): three output tables incl.
  `dose_response_models.csv`; a synthesis-report-first, coefficients-over-figure-digitization workflow;
  unit standardization (kPa/mm/g); the coverage/assessment layer; and documented PDF table-extraction
  gotchas (species-column shift, dropped decimals, RPC50 cross-check).
- **Re-ran the full barotrauma analysis under the updated skill:**
  - **Coefficient cross-check** (`RPC50 = exp(−b0/b1)`) on all 46 dose–response models — all pass and
    validate the extractions (grayling RPC50 10.3 ≈ stated 10–12; nase 2.67 ≈ 2.7).
  - **Reconciled 3 relationship rows** (Brown 2012; Pflugrath 2018 ×2) from `digitized_figure /
    pending digitization` → `reported` — curves are now held as exact coefficients.
  - Re-ran the assessment: coverage 35 cells (24 quantified/modelled), 13 threshold groups.
- Added **`reviews/stressor_response_skill_update.md`** documenting the old-vs-updated-skill changes.

### Notes
- Two immediate-mortality models (Murray cod, silver perch) have RPC50 beyond the realistic range —
  consistent with low immediate mortality, not extraction errors.
- Figure-only datasets still pending digitization: Stephenson Fig 3, Boys piecewise, Doyle life-stage.

## [0.21.0] - 2026-06-30
Ingested the PNNL "Biological Response Models" report — dose–response curves now span ~15 species.

### Added
- Located and ingested the **PNNL Biological Response Models report** (Pflugrath et al., Nov 2020;
  `2020_Pflugrath_Numerical_Biol_Response_Models.pdf`, register `2020_Pflugrathc`) — a synthesis of
  dose–response models across barotrauma, blade strike and fluid shear.
- Extracted its **barotrauma logistic coefficients** (Tables 11–13, Equation 12) into
  `data/dose_response_models.csv`: ~15 species × **injury / mortal injury / immediate mortality**
  (American shad, bluegill, Chinook, kokanee, largemouth bass, Macquarie perch, Murray cod, rainbow
  trout, silver perch, tiger muskie, walleye, white sturgeon, golden gray mullet, Australian species).
  The dose–response overlay now shows **46 models** (was 17), with a new **immediate mortality** response option.
- New species added to the family vocabulary (bluegill, largemouth bass, kokanee, Macquarie perch,
  tiger muskie, walleye, golden gray mullet).

### Notes
- Coefficients are from the report's published tables (exact); the scientific-name column was
  realigned where the PDF text-extraction shifted it. All models share the ln(RPC) = LRP axis.
- Still to ingest from the same report: the **blade-strike** (vs strike velocity & L/t ratio) and
  **fluid-shear** (vs strain rate) model families — these need a multi-x-axis overlay.

## [0.20.0] - 2026-06-30
Added the Zitek 2026 dose–response curves (per-species/stage logistic models).

### Added
- 8 **Zitek 2026** logistic models in `data/dose_response_models.csv` (b0/b1 from the paper's
  Table 3, for nase, roach, European perch and European grayling × life stage), so their curves now
  appear in the dose–response overlay. Previously only Zitek's RPC-at-50% thresholds were captured
  (points, not curves). Coefficients were cross-checked against the paper's stated RPC-50 values
  (e.g. grayling b0=−5.182, b1=2.222 → RPC50 ≈ 10, matching the reported 10–12).
- The dose–response panel now overlays 17 models on the shared ln(RPC) = LRP axis.

### Notes
- The curves confirm Zitek's finding: physostomous Cypriniformes (nase, roach) and developed-
  swim-bladder stages are the most susceptible, while early larvae without a developed swim bladder
  (perch/grayling L1/L2) are the most tolerant.

## [0.19.0] - 2026-06-30
Explorer: family / life-stage / length / mass filters, a data-completeness indicator, and a dose–response legend fix.

### Added
- **Family** filter (species → family_group via `data/vocab/species.csv`); the Species dropdown is now
  sorted by family. Added Australian bass, carp gudgeon, European grayling and European perch to the vocab.
- **Life stage**, **Body length** and **Body mass** filters, with **standard conversions**
  (length → mm, mass → g; cm ×10, kg ×1000) and a "(not provided)" option.
- **Data-completeness indicator** under the filters: how many shown rows are missing life stage / length /
  mass / family — so it is clear when a row names the species but omits the more specific data.

### Fixed
- Dose–response legend coloured every curve the same and ignored the Species filter. Colours now key off a
  normalised species name (curves and the comparator share one palette), and the panel respects the
  Species/Family filter — selecting a species with no fitted model (e.g. European grayling) now says so
  explicitly instead of showing the other species.

## [0.18.0] - 2026-06-30
Dose–response curve overlay from published coefficients, plus a codified copyright-&-digitization policy.

### Added
- `data/dose_response_models.csv` — runnable per-species logistic models with **exact published
  coefficients**: Pflugrath 2018 Table 4 (injury & mortal injury × {Australian bass, carp gudgeon,
  Murray cod, silver perch}) and Carlson 2012 (Chinook). x = ln(RPC) = LRP, so all curves share one axis.
- **Dose–response curve overlay** in the explorer: the models plotted as overlaid logistic curves
  (solid = mortal injury, dashed = injury), computed **analytically from the coefficients — not digitized**.
- Zitek 2026 RPC-at-50%-mortal-injury thresholds (nase/roach ≈ 2.7; grayling/perch ≈ 10–12), capturing
  that two-chambered **Cypriniformes are highly susceptible** (swim-bladder morphology, not just
  physostome/physoclist). Relationships: 41 → 44.

### Added — policy
- **Copyright & digitization** statement in `skills/passage-stressor-response/references/figure_digitization.md`:
  data (facts) vs image (expression); the **EU DSM Art. 3 TDM research exception**; proportionality;
  attribution; prefer-primary-data; and a clearly-flagged "provisional visual extraction" interim tier.

### Notes
- Model coefficients were taken from published tables/equations (exact) — the preferred, copyright-clean
  route over tracing figures. Figure-point digitization remains the next step for figure-only data
  (e.g. Stephenson Fig 3).

## [0.17.0] - 2026-06-30
Stressor–response assessment & gap-analysis layer: derived coverage/threshold tables and an interactive coverage-gap matrix.

### Added
- **Derived analysis tables** (regenerated by `scripts/build_stressor_response.py`):
  `outputs/stressor_response_coverage.csv` (one row per mechanism × predictor × response cell with a
  coverage level — modelled / quantitative / qualitative — plus studies) and
  `outputs/stressor_response_thresholds.csv` (per mechanism × predictor × unit × response × species:
  n + min/median/max of the numeric values). The machine-readable assessment layer.
- **Coverage & gaps matrix** in the explorer: an interactive predictor × {response | species |
  structure | mechanism} heatmap, colour-coded (modelled / quantitative / qualitative-only / gap),
  respecting all filters — so what is quantified and where the gaps are is visible at a glance.

### Notes
- Current barotrauma coverage: 34 populated cells (2 modelled, 21 quantitative, 11 qualitative-only);
  9 numeric threshold groups. Biggest gaps: non-salmonid species, pump/screw/VLH structure types,
  shear, and qualitative-only cells (buoyancy, TDG, geometry) awaiting figure digitization.
- `reviews/stressor_response_synthesis.md` §6 documents the coverage findings and gaps.

## [0.16.0] - 2026-06-30
Stressor–response explorer: rename, Study filter, a variables/units table, and a documented kPa pressure standard.

### Added
- `data/variables_units.csv` — canonical variables and their physical units, rendered in the
  explorer under *Variables & physical units*.
- **kPa pressure standard**, enforced and logged at build time
  (`scripts/build_stressor_response.py` → `standardize_pressures()`): any non-kPa pressure is
  converted (factors: psi ×6.894757, bar ×100, atm ×101.325, mmHg ×0.1333224, Pa ×0.001;
  depth→kPa = 101.325 + 9.80665×m), the original is preserved in the row's `notes`, and each
  conversion is logged in the build output and the explorer for traceability. Documented in
  `skills/passage-stressor-response/references/schema.md` §C. (Current data: 9 pressures, all
  already kPa → 0 conversions.)

### Changed
- Renamed the tool to **"Stress-Response Explorer for Downstream Fish Passage — Injury and Mortality"**.
- Added a **Study** filter (by `citation_key`) to the explorer; coverage also tallies by study.
- Added a **Variables & physical units** table below the equations registry.

## [0.15.0] - 2026-06-30
Added the stressor–response module: quantitative relationships (thresholds, dose–response, equations) linking physical stressors and system characteristics to injury and mortality.

### Added
- **Skill** `skills/passage-stressor-response/` — extracts one row per quantitative
  relationship (thresholds with conditions, dose–response points, equations, digitized
  figures), with a controlled predictor vocabulary, schema, extraction playbook,
  figure-digitization protocol, and a dependency-free first-pass finder
  (`scripts/extract_relationships.py`).
- **Data** `data/stressor_response.csv` (41 relationships) and `data/equations.csv`
  (11 models) — barotrauma demonstrator curated from a finder run over all 72 available
  barotrauma PDFs (2,385 candidates). Predictors include RPC (both conventions), LRP,
  nadir pressure, strain rate, acclimation depth, buoyancy state, tag burden, operating
  point and runner geometry; species span salmonids, eel, lamprey, shad, perch, gambusia,
  catfish, Cypriniformes and Neotropical/European fishes. All rows `Mined` (source-located).
- **Build/explorer** `scripts/build_stressor_response.py` → self-contained
  `docs/stressor_response.html` (within-metric comparator, relationships table, equations
  registry, coverage), published via GitHub Pages and linked from the README.
- **Synthesis** `reviews/stressor_response_synthesis.md`.

### Notes
- Captures the metric-comparability trap explicitly: RPC = PA/PN (Brown/Pflugrath) vs
  RPC = PN/PA (Boys) are inverse conventions and are never pooled.
- Curation of the remaining candidates and figure digitization are ongoing.

## [0.14.0] - 2026-06-30
Screened the 13 second-ingest papers into the mechanism deep-dives, so they
are now treated identically to the rest of the corpus.

### Added / changed
- **Mechanism registers** now include the 13 new papers where relevant:
  barotrauma register 61 → **66** (Foye 1965, Davies 1988, Cada 1997, Perry 2001,
  Koukouvinis 2023); collision register 47 → **53** (Davies, Cada, Bickford 2000,
  Skalski 2002, Jansen 2007, Koukouvinis); shear register 36 → **39** (Davies, Cada,
  Koukouvinis).
- **Reproducibility scorecards** scored the new live-fish studies against the
  10-criterion checklists: barotrauma 38 → **39** (Foye 1965, lab pressure-survival,
  70% Medium); collision 24 → **25** (Jansen 2007, field HI-Z passage, 90% High;
  field split now 9 simulated + **16** field). Shear unchanged (no new live-fish
  shear study). Per-criterion completeness tables in the three `reviews/*_overview.md`
  recomputed accordingly.
- **Three axes** recoded for the 12 newly-screened papers (Koukouvinis was already
  coded): real `study_environment` / `location_during_passage` / `outcome_timing`
  replace the placeholder "Not reported" values; gas-supersaturation (Ebel 1969,
  Bouck 1980) and behavioural (Long 1968, Haro 1998) papers are tagged outside the
  three mechanism modules with explanatory notes.
- **Docs synced:** `reviews/cross_mechanism_synthesis.md` mechanism table, the three
  overviews, `reviews/state_of_the_art.md` study-type table (corrected from the stale
  229-total to 255: Lab 77 / Field 68 / Numerical 48 / Review 49 / Guidelines 13) and
  its mechanism-coverage tallies, and the README deep-dive bullets.
- Regenerated `docs/index.html` and `outputs/`.

### Known issue
- `data/extraction.csv` contains two rows for `2012_Normandeau` (one Field with a
  mechanism, one Numerical with a blank mechanism); the second looks like a
  defective duplicate. Left as-is pending a decision on whether to drop it
  (would move the analysed count 255 → 254).

## [0.13.0] - 2026-06-30
Second literature ingest: 13 reviewed PDFs added.

### Added
- Ingested 13 reviewed PDFs into the collection (downloaded via the
  `_candidates_to_check` workflow with institutional/OA access): Foye 1965,
  Long 1968, Ebel 1969, Bouck 1980, Davies 1988, Brookshier 1995, Cada 1997
  ("Shaken, not stirred" — corrected paper), Haro 1998, Bickford 2000, Perry 2001,
  Skalski 2002, Jansen 2007, and the Koukouvinis & Anagnostopoulos 2023 review
  (Energies, 10.3390/en16062661). Filed into study-type folders, added to
  `corpus.csv` (now **272**) with Mined rows in `extraction.csv` and
  `axes_exposure_timing.csv` (now **255**). Study-type split: Lab 77 / Field 68 /
  Numerical 48 / Review 49 / Guidelines 13.
- Removed the 12 corresponding rows from `data/candidate_additions.csv`
  (50 → **38**; 8 High remain).

### Notes
- During folder cleanup, two duplicate downloads (a second Skalski 2002 and a
  second Haro 1998) were moved to `_candidates_rejected/`; an unidentified scan was
  resolved to Brookshier 1995. New rows are **Mined** (image-only scans, e.g. Cada
  and Brookshier, have sparse fields) pending the verification pass.
- Recovered `candidate_additions.csv` from a OneDrive NUL-corrupted state before
  editing. Integrity verified: no duplicate keys, no orphan PDFs, all rows resolve.
- Regenerated `outputs/` and `docs/index.html`.

### Documentation
- Synced all corpus-level counts to current status across `README.md`, the five
  `reviews/*.md` (state-of-the-art, barotrauma/collision/shear overviews,
  cross-mechanism synthesis), `reviews/candidate_additions.md`, and
  `methodology/07_axes_exposure_and_timing.md`: 255 analysed papers, 272 catalogued,
  38 candidates (8 High / 8 Medium / 22 Low). Mechanism deep-dive counts
  (barotrauma 61/38, collision 47/24, shear 36/12) are unchanged — the 13 new
  papers are not yet screened into the registers/scorecards (pending verification).

## [0.12.5] - 2026-06-30
Removed 4 invalid candidates flagged in review.

### Removed
- Deleted 4 candidates from `data/candidate_additions.csv` (54 → 50), logged with
  reasons in new `data/candidate_removals_log.csv`:
  - **#52 Associates 2005** — not a real publication; a garbled reference to
    Deng et al. 2005 (CJFAS 10.1139/F05-091), already in the corpus as `2005_Deng`.
  - **#62 McEwen 1992**, **#63 Bell 1991**, **#68 Johnson 1972** — reviewer marked
    "Not valid" (engineering/USACE report fragments; not valid/locatable works).

### Note
- `docs/index.html` candidate count (and the candidates tab) will refresh to 50 on
  the next `scripts/build_dashboard.py` run — the rebuild was deferred this pass
  because the working copy was mid-sync. Data, removal log, and README are current.

## [0.12.4] - 2026-06-30
Web-searched every remaining candidate for a free PDF.

### Added
- New `pdf_url` column in `data/candidate_additions.csv`: searched all 54 remaining
  candidates (regardless of DOI) and recorded the best free/OA or institutional
  landing link found. **20 of 54** have a usable link (OSTI, USGS, UMass
  ScholarWorks, UBC cIRcle, SINTEF Brage, MDPI/PMC, J. Exp. Biol. archive, SLU,
  Oxford); the other **34 have no free source** (offline USACE/NMFS/ETSU/Normandeau
  reports, theses, books, and non-OA legacy journals) — annotated in `notes`.
- Staged **Cada 1997 "Shaken, not stirred"** (the correct paper this time, OSTI
  510550; image-only scan) in `_candidates_to_check/` for review — fixing candidate
  #3, whose earlier download was the wrong Cada paper.

### Notes
- Per-item interactive download was not pursued for these (grey-lit yield is low and
  most are landing pages, not direct PDFs); the recorded links support manual
  retrieval. Candidate count unchanged at 54 (Cada pending your review/ingest).

## [0.12.3] - 2026-06-30
Catalogued Montén 1985 (already on disk); concluded the OA download hunt.

### Added
- **Montén 1985, "Fish and turbines: fish injuries during passage through power
  station turbines"** — a foundational turbine fish-injury monograph that was
  already in the library as a chapter-by-chapter zip
  (`Misc/1985_Monten…zip`). Merged the 18 chapter PDFs (in order) into one file,
  filed it in `Review/`, and catalogued it: `corpus.csv` (now 260), Mined rows in
  `extraction.csv` (243) + `axes_exposure_timing.csv` (243). Removed the duplicate
  candidate rows #37/#66.

### Notes
- OA download hunt concluded: of the original 72 candidates, 15 are now in the
  collection and 3 were rejected; **54 remain**, overwhelmingly grey literature
  (old USACE/NMFS/ETSU reports, theses, conference proceedings) not freely online,
  plus a few at non-subscribed publishers. Five still carry DOIs (Rummer 2005,
  Mathur 1996, Cada 1990, Fjeldstad 2018, Bouck 1980) and keep their
  `candidate_link`/`doi_or_url` for manual retrieval.
- Regenerated `outputs/` and `docs/index.html`.

## [0.12.2] - 2026-06-30
Ingested 3 more candidates; fixed a study-type tagging bug.

### Added
- Ingested 3 reviewed candidates into the collection (all Field, via Oxford
  institutional access): **Muir 2001** (bypass/turbine/spillway survival, Snake
  River), **McNabb 2003** (Archimedes lifts & Hidrostal pump, Red Bluff),
  **Backman 2002** (gas-bubble-trauma incidence, Columbia River). Filed in
  `Field/`, added to `corpus.csv` (now 259), with Mined rows in `extraction.csv`
  (now 242) and `axes_exposure_timing.csv`. Removed from the candidate list (now 56).

### Fixed
- The extraction script tagged `Category` from the (temp) folder name, so the 14
  candidates ingested in 0.12.0/0.12.2 were mis-tagged ("ingest"/"ing2") and
  dropped out of the study-type chart. Corrected all 14 `Category` values from the
  corpus `study_type`; study-type counts are now Lab 75 / Field 63 / Numerical 48 /
  Review 43 / Guidelines 13 = 242. Noted the post-extraction Category-sync step in
  `methodology/09_adding_literature.md`.

- Regenerated `outputs/` and `docs/index.html`.

## [0.12.1] - 2026-06-30
Replaced the erroneous `2008_Deng` record with the Carlson paper.

### Changed
- `2008_Deng` ("Data overview of sensor data", Misc) was a wrong/mislabelled
  record; replaced it with **`2008_Carlson`** — "Data overview for Sensor Fish
  samples acquired at Ice Harbor, John Day, and Bonneville II dams in 2005, 2006,
  and 2007" (PNNL-17398). Swapped the PDF (the wrong file moved to
  `_candidates_rejected/`), updated `data/corpus.csv`, and removed Carlson from
  `data/candidate_additions.csv` (now 59; 9 High). Catalogued total unchanged (256);
  it remains a `Misc` data-overview (not in the analysed set) pending screening.
- `.gitignore`: exclude stale working leftovers (`data/*.csv.tmp`,
  `candidate_additions_enriched.csv`) — locked locally; delete when convenient.

## [0.12.0] - 2026-06-30
First literature ingest from the candidate list (11 works added).

### Added
- Ingested **11** reviewed candidate PDFs into the collection: Weitkamp 1980,
  Coutant 1997, Mathur 2000, Turnpenny 2000 (Risk Assessment report), Killgore
  2001, Humphries 2002, Larinier 2008, Calles 2010, Baumgartner 2012, Bracken
  2013, Calles 2013. Each was renamed to the repo convention, filed in its
  study-type folder, and added to `data/corpus.csv` (now 256) with a `Mined`
  row in `data/extraction.csv` (now 239) and a `Mined` placeholder in
  `data/axes_exposure_timing.csv`. PDFs are not committed (copyright).
- Downloaded via the `_candidates_to_check` → review → `_candidates_accepted`
  workflow (Chrome + institutional access for Wiley/Springer/Oxford; OA for
  reports/KMAE/EPA/OSTI). Reviewed with `_candidates_to_check/REVIEW_CHECKLIST.csv`.

### Changed / removed
- `data/candidate_additions.csv`: removed the 11 ingested rows and 2 out-of-scope
  rows (Larinier 2002 — upstream passage; Paish 2002 — no downstream-passage
  content) → 60 candidates remain. Annotated #3 Cada (the OA link resolved to a
  different, already-held paper = 1999_Cada "Exploring shear stress…"; rejected)
  and put #1 Carlson **on hold** as a probable duplicate of existing `2008_Deng`
  "Data overview of sensor data" (pending confirmation).
- Regenerated `outputs/` and `docs/index.html`.

### Pending (next pass)
- Mechanism **registers / reproducibility scorecards** were not scored for the 11
  new papers, and their extraction + axes rows are `Mined` — these are completed
  via the verification protocol (`tools/verification/verify.py`,
  `methodology/08`). Resolve the Carlson-vs-Deng duplicate; obtain the true
  "Shaken, not stirred" (Cada #3).

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