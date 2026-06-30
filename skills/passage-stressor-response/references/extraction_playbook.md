# Extraction playbook — finding & reading relationships

How to get thresholds, equations and dose–response data out of a passage paper,
quickly and without error.

## Where relationships live
- **Abstract / highlights** — the headline relationship and often the threshold.
- **Methods** — the *conditions* (species, stage, size, acclimation, turbine/pump
  type & geometry, operating point, exposure metric & how it was computed). Capture
  these even when the relationship itself is in Results.
- **Results figures** — dose–response curves are usually figures, not text. These
  are the highest-value, lowest-availability data → digitize (see
  `figure_digitization.md`).
- **Results tables** — point estimates with n and CIs; read directly (`read_from_table`).
- **Model / theory sections** — equations, their parameters, and (sometimes) the
  validity range. Modelling papers (blade-strike, barotrauma, BioPA) are equation-rich.
- **Captions & footnotes** — units, acclimation assumptions, what "survival" counts.

## Per-relationship checklist
For each relationship, before writing the row, make sure you have:
1. **Predictor** (focal varied quantity) — code from `stressors_and_predictors.md`.
2. **Response** — exactly what it is (immediate vs latent mortality; injury *type*;
   survival including/excluding handling controls).
3. **Value(s) + units** — for the predictor and the response.
4. **Conditions** — species, stage, size, acclimation, structure type & detail,
   geometry, operating point. A relationship without conditions is not usable.
5. **Form** — threshold / point / curve / equation / categorical.
6. **Provenance** — `source_location` (Fig/Table/Eq/page) and `extraction_method`.
7. **n and uncertainty** — where given.

## Reading off thresholds
- State the *kind*: onset (first injury), 50 % (LD50/EM50), or mortal/severe.
- Keep the **metric** explicit (RPC vs nadir vs LRP; strain rate vs shear stress).
- Tie it to **species + stage + acclimation** — the same metric value means
  different things for a physostome eel vs a physoclist salmonid smolt.
- If the paper reports a depth, convert to pressure only with the hydrostatic
  relation and record both (original + converted) — note the conversion.

## Reading off equations
- Copy the equation **verbatim** first; normalize later in `notes`.
- List **every symbol** with meaning + unit; you cannot reuse a model otherwise.
- Record **parameter values** and **what they were calibrated on** (species,
  turbine, dataset).
- Record the **domain of validity** (predictor ranges, head, species). Flag in
  `notes` if the paper applies it outside that range.
- If it reuses a classic model (von Raben / Montén strike; Boyle's-law barotrauma),
  set `origin_citation_key`.

## Unit & metric hygiene (the common errors)
- **RPC, nadir pressure, LRP** are related but not interchangeable — never silently
  convert between dose metrics; record which one the figure's x-axis actually is.
- **Strain rate (s⁻¹) ≠ shear stress (Pa).**
- **Log axes:** barotrauma and strike figures often use log x-axes — digitize in log
  space (see `figure_digitization.md`) or every point is wrong.
- **% of what:** "90 % survival" — of the passage route? whole facility? control-
  corrected? Pin it down in `response`/`notes`.
- **Operating point matters:** a turbine survival number is meaningless without the
  operating point (%BEP / head / discharge); record it as a condition.

## Lab vs field vs CFD (what the relationship actually means)
- **Lab dose–response** isolates one stressor at controlled doses → clean
  predictor→response, but surrogacy and acclimation assumptions apply.
- **Field** integrates all mechanisms plus handling/tagging → a survival-vs-operating
  -point relationship, not a clean single-stressor dose.
- **CFD / BioPA** predicts *exposure* distributions; the biology comes from a coupled
  dose–response. Record the model and the dose–response it was coupled to separately.

## First-pass script
`scripts/extract_relationships.py` flags candidate equations, threshold sentences
and dose–response captions with page + snippet. It only points you to where to read;
all structured rows are written by a human (or a careful pass) into the schema, with
`confidence = Mined` until verified against the paper.
