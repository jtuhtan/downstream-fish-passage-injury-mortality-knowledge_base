---
name: passage-stressor-response
description: >-
  Extract the QUANTITATIVE RELATIONSHIPS and runnable MODELS that link physical stressors and system
  characteristics to fish injury and mortality during downstream passage — thresholds (with their
  conditions), dose–response data points, fitted models / equations with PUBLISHED COEFFICIENTS, and
  digitized figures. Predictors span the stressors (pressure / barotrauma RPC·LRP·nadir, fluid shear /
  strain rate, blade-strike velocity & probability, turbulence, cavitation, gas supersaturation / TDG,
  grinding) AND system characteristics (turbine / pump type, runner geometry, operating point, head,
  discharge) AND fish traits (species, family, life stage, length, mass, acclimation). Use this skill
  WHENEVER the user wants the underlying functional relationships and response models — "extract the
  dose–response data / coefficients", "pull the thresholds and equations", "build a stressor–response /
  dose–response dataset", "relate turbine type / operating point / geometry to mortality", "what is the
  biological response model / equation for barotrauma or blade strike", "ingest the PNNL / BioPA / HBET
  models", "compile the dose–response curves across studies", "where are the coverage gaps", or before
  fitting or plotting any injury-vs-exposure model.
---

# Passage stressor–response extraction

## What this skill is for

The `passage-injury-mortality-review` skill captures **one row per study**. This skill captures the
**functional relationships and runnable models inside the studies** — the dose–response points,
thresholds with their exact conditions, and the **fitted model coefficients** (logistic b0/b1,
blade-strike, shear) that let you *compute, overlay and compare* injury/mortality vs exposure across
species. It produces three normalized tables in `data/`:

- **`stressor_response.csv`** — one row per relationship / data point (predictor → response, units,
  conditions, provenance, extraction method). `references/schema.md` §A.
- **`equations.csv`** — one row per predictive equation / model *form* (variables, parameters, domain
  of validity). §B.
- **`dose_response_models.csv`** — one row per **runnable fitted model** (e.g. logistic
  `logit(p) = b0 + b1·LRP` per species), so curves are **computed analytically and overlaid** on a
  shared axis. §D.

A controlled predictor/units vocabulary (`references/stressors_and_predictors.md`,
`data/variables_units.csv`) and a build/assessment step (`scripts/build_stressor_response.py`) sit on
top: the build **validates** the data, **standardizes units** (pressure → kPa, length → mm, mass → g,
all logged for traceability), emits the **coverage/gap** and **thresholds** tables
(`outputs/stressor_response_*.csv`), and renders the interactive explorer (`docs/stressor_response.html`).

## When to use it

Whenever the goal is the *relationship or model*, not the study summary: extracting dose–response
curves/coefficients, thresholds with conditions, equations; ingesting synthesis reports that compile
response models; building a predictor→outcome dataset; or assessing coverage and gaps. Complements
`passage-injury-mortality-review` (study-level) and `passage-literature-discovery` (corpus growth).

## Core workflow

1. **Target the high-yield sources.** Relationships and models live in **lab dose–response** studies,
   **modelling** papers (blade-strike, barotrauma, BioPA / HBET), **field** survival-vs-operating-point
   studies, and — most valuably — **synthesis / review reports that consolidate models across many
   species**: the **PNNL "Biological Response Models" report (Pflugrath et al. 2020)**, BioPA / HBET
   documentation, EPRI compilations. One synthesis report can yield dozens of fitted models at once.

2. **Prefer EXACT published coefficients/tables over tracing figures.** A dose–response curve is
   usually printed twice — as a *figure* and as a *coefficient table* with an equation number. Always
   take the **table coefficients**: they are exact, copyright-clean (facts, not the image), and need no
   digitization. Only digitize a figure when the data exists *solely* as a figure with no published
   equation (`references/figure_digitization.md` + its copyright policy).

3. **First pass (breadth).** `scripts/extract_relationships.py <pdf_or_folder>` surfaces candidate
   equations, threshold sentences and dose–response captions with page + relevance score. A finder,
   not an extractor.

4. **Extract relationships & thresholds (depth)** into `stressor_response.csv` per `schema.md`:
   predictor (from `stressors_and_predictors.md`), response, value(s) + units, the **conditions**
   (species, family, life stage, length/mass, structure type & detail, operating point), and a
   **mandatory `source_location`**.

5. **Capture equations & runnable models.** Model *forms* go in `equations.csv`; **fitted per-species
   coefficients** go in `dose_response_models.csv` (b0/b1, `x_metric`, range). These drive the curve
   overlay analytically — no point-cloud needed.

6. **Build, validate & assess.** Run `scripts/build_stressor_response.py`: it validates rows,
   standardizes units (kPa / mm / g, logged), writes the **coverage matrix** and **thresholds
   summary** to `outputs/`, and rebuilds the explorer. Read the coverage output to see what is
   quantified and **where the gaps are**.

7. **Document in the SAME change (REQUIRED).** Methodology + CHANGELOG + vocab/schema, every time.

## Practical extraction notes (learned the hard way)

- **Same name, inverse metric:** RPC = P_A/P_N (Brown/Pflugrath; ≥1) vs RPC = P_N/P_A (Boys; 0–1).
  Record which convention; never pool. **`LRP = ln(RPC_AN)`** is the standard logistic x-axis, so all
  LRP-based models overlay directly.
- **pdftotext table gotcha:** numeric columns extract reliably, but the **species / scientific-name
  column often shifts by a row** — realign by common name and verify.
- **Cross-check every coefficient:** a logistic should reproduce the paper's stated 50 % point
  (`RPC50 = exp(−b0/b1)`). If it doesn't, the extraction is wrong.
- **Watch dropped decimals** in extracted text (e.g. `7377` → `7.377`); confirm against the curve or a
  stated value before trusting a slope.
- **Different mechanisms use different x-axes:** barotrauma → LRP; blade strike → strike velocity
  (& L/t ratio); shear → strain rate. Keep `x_metric` explicit and never put them on one axis.

## Reference files

- `references/schema.md` — columns for all three tables (relationships, equations, dose-response
  models) + units & pressure/size standardization.
- `references/stressors_and_predictors.md` — controlled predictor vocabulary + canonical units.
- `references/extraction_playbook.md` — where/how to read thresholds, equations, dose–response.
- `references/figure_digitization.md` — figure protocol + **copyright & digitization policy**.
- Reuse `../passage-injury-mortality-review/references/metrics_thresholds.md` and `mechanisms.md`.

## Principles

- **Exact coefficients beat eyeballed points.** Mine tables/equations first; digitize only what exists
  solely as a figure.
- **Synthesis reports are goldmines** — they consolidate fitted models across many species/mechanisms.
- **One row = one relationship/model, fully conditioned.** No units / species / source → not a row.
- **Predictors are first-class** (stressor AND machine AND fish-trait), with **standardized units**
  (kPa, mm, g) and traceability; missing covariates stay blank and are surfaced, never guessed.
- **Provenance is mandatory:** reported ≠ digitized ≠ refit.
- **Compare only within a metric / x-axis and condition set.** RPC ≠ nadir ≠ LRP; strain rate ≠ shear
  stress; barotrauma LRP ≠ strike velocity ≠ strain rate.
- **Preserve disagreement; document continuously** (methodology + CHANGELOG + vocab).
