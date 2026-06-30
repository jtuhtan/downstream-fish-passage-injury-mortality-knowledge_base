---
name: passage-stressor-response
description: >-
  Extract the QUANTITATIVE RELATIONSHIPS that link physical stressors and system
  characteristics to fish injury and mortality during downstream passage —
  thresholds (with their conditions), dose–response data points, equations/models,
  and digitized figure/table data. Predictors include the stressors (pressure /
  barotrauma RPC·LRP·nadir, fluid shear / strain rate, blade strike velocity &
  probability, turbulence, cavitation, gas supersaturation / TDG, grinding) AND
  the system characteristics (turbine type, pump type, runner geometry — blade
  count, diameter, rpm, tip speed, gap clearance; operating mode — % of best
  efficiency, head, discharge, gate setting; passage route) AND fish traits
  (species, life stage, length/mass, acclimation depth). Use this skill WHENEVER
  the user wants to go beyond one-row-per-study summaries to the underlying
  functional relationships: "extract the dose–response data", "pull the thresholds
  and equations", "digitize that figure", "build a stressor–response dataset",
  "relate turbine type / operating point / geometry to mortality", "what is the
  equation for blade strike (or barotrauma)", "compile the barotrauma dose–response
  across studies", "make a predictor → injury table", or before fitting any model
  that predicts injury/mortality from physical exposure or design/operating
  parameters.
---

# Passage stressor–response extraction

## What this skill is for

The `passage-injury-mortality-review` skill captures **one row per study** — what a
paper is and its headline number. That is not enough to *relate* stressors and
machine characteristics to outcomes: for that you need the **functional
relationships inside the studies** — the dose–response points, the threshold values
with the exact conditions they hold under, the predictive equations, and the data
behind the figures.

This skill extracts those into two normalized, machine-readable tables:

- **`data/stressor_response.csv`** — one row per quantitative relationship or data
  point: a `predictor` (stressor or system/fish characteristic) related to a
  `response` (injury or mortality metric), with units, conditions, provenance, and
  how the value was obtained (reported / digitized / refit).
- **`data/equations.csv`** — one row per equation or model that predicts an
  injury/mortality outcome from physical or design/operating variables, with its
  variables, parameters, and domain of validity.

Together they turn the corpus into a dataset you can actually model with: fit a
barotrauma dose–response across species, compare turbine types at matched operating
points, or check whether a published blade-strike equation reproduces a field
survival number.

## When to use it

Whenever the goal is the *relationship*, not the summary: extracting dose–response
curves, thresholds with their conditions, equations/models, or figure/table data;
building a predictor→outcome dataset; or preparing inputs for a model that maps
physical exposure, geometry, turbine/pump type or operating mode to injury and
mortality. It complements, and hands off to/from, `passage-injury-mortality-review`
(study-level) and `passage-literature-discovery` (corpus growth).

## Core workflow

1. **Pick the high-yield papers.** Relationships live mostly in **lab dose–response**
   studies (pressure chambers, shear/jet flumes, blade-strike rigs), **modelling**
   papers (blade-strike, barotrauma, BioPA / bio-hill), and **field studies that
   report survival vs an operating/design variable**. Use `data/extraction.csv`
   (Category = Lab / Numerical, and mechanism) to target them. Cloud-only PDFs must
   be downloaded locally before their text can be read.

2. **First pass (breadth).** Run
   `scripts/extract_relationships.py <pdf_or_folder> -o relationship_candidates.csv`.
   It surfaces **candidate equations, threshold sentences, and dose–response
   figure/table captions** with their page and a snippet. It is precision-leaning
   and *does not* fill the structured schema — it tells you where to read. Treat it
   strictly as a finder.

3. **Extract relationships (depth).** For each real relationship, write a row to
   `data/stressor_response.csv` per `references/schema.md`. Identify the
   **predictor** (use the controlled list in `references/stressors_and_predictors.md`)
   and the **response**, record value(s) + units + the **conditions** that bound them
   (species, stage, size, acclimation, turbine/pump type & model, geometry, operating
   point), and **always record `source_location`** (figure/table/equation/page). Mark
   how the value was obtained (`reported` / `digitized_figure` / `read_from_table` /
   `fitted_by_us`). See `references/extraction_playbook.md`.

4. **Capture equations/models.** Put each predictive equation in
   `data/equations.csv` per `references/schema.md` (§ Equations): the equation, every
   variable + unit, parameter values, what it predicts, its **domain of validity**,
   and the source. Note the original source if the paper is reusing someone else's
   model (e.g. von Raben / Montén strike, Boyle's-law vs dynamic barotrauma).

5. **Digitize figures rigorously (when the data only exists as a curve).** Follow
   `references/figure_digitization.md`: calibrate both axes from labelled ticks,
   record the tool and axis transform (log!), store the extracted points in
   `data/figures/<citation_key>_<figN>.csv`, and link them from the relationship row.
   Never hand-fabricate points; digitized data carries its own provenance and error.

6. **Link to the framework.** Every row carries `citation_key` (→ `data/corpus.csv`)
   and `mechanism` (→ `data/vocab/mechanisms.csv`), and where inferable the
   exposure-pathway / outcome-timing axes, so relationships slot into the same
   three-axis framework as the rest of the base.

7. **Document in the SAME change (REQUIRED).** As with the other skills, a change is
   not done until its rationale is written down — in the **methodology** file for
   relationship extraction (`methodology/` — add one if absent), the **CHANGELOG**,
   and any **vocab/schema** touched. Coding the data and documenting how it was coded
   are one task.

## Reference files (read as needed)

- `references/schema.md` — exact columns for `stressor_response.csv` (relationships)
  and `equations.csv` (models), allowed values and conventions.
- `references/stressors_and_predictors.md` — the controlled vocabulary of
  **predictors**: stressors, machine/geometry/operating characteristics, and fish
  traits, each with its canonical metric and unit. This is the predictor side of the
  relationship.
- `references/extraction_playbook.md` — where thresholds, equations and dose–response
  data live in a paper, how to read off conditions, unit handling, and the traps.
- `references/figure_digitization.md` — a rigorous, reproducible protocol for getting
  data out of figures, with provenance and error.
- Reuse, don't duplicate: the response-side metrics and their landmarks are defined in
  `../passage-injury-mortality-review/references/metrics_thresholds.md`; the mechanism
  taxonomy in `../passage-injury-mortality-review/references/mechanisms.md`.

## Principles

- **One row = one relationship, fully conditioned.** A value with no units, no
  species/stage, no operating point and no source is not a relationship — it is a
  rumour. Capture the conditions or do not capture the row.
- **Predictors are first-class.** The point of this skill is the *predictor* side —
  not just "mortality was 12%" but "mortality vs nadir pressure, for 100 mm Chinook
  acclimated to 7.6 m, in a Kaplan at 90% of best efficiency". Geometry, turbine/pump
  type and operating mode are predictors, not footnotes.
- **Provenance is mandatory.** Every value is tagged reported / digitized / refit and
  pinned to a figure, table, equation or page. Digitized ≠ reported; refit ≠ either.
- **Thresholds compare only within a metric and a condition set.** RPC ≠ nadir ≠ LRP;
  strain rate (s⁻¹) ≠ shear stress (Pa). Never silently convert or pool across them.
- **An equation is data too.** Capture the model, its parameters, and *where it is
  valid* — an extrapolated equation is a common source of wrong survival estimates.
- **Preserve disagreement.** Competing models (Boyle's-law vs dynamic barotrauma;
  strike-probability formulations) are recorded side by side, never averaged.
- **Document continuously.** Methodology + CHANGELOG + vocab, in the same change.
