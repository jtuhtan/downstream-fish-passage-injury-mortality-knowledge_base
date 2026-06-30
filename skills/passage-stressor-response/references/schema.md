# Schema — relationships & equations

Two normalized tables. Keep list-valued cells semicolon-separated (`A; B; C`).
Leave blank if not reported (never guess). Prefer what the study *itself*
measured/derived over what it cites. Every numeric value carries a unit and a
`source_location`.

---

## A. `data/stressor_response.csv` — one row per relationship / data point

A "relationship" is a predictor related to a response under stated conditions. A
single dose–response curve becomes **several rows** (one per reported/digitized
point) OR **one row** describing the fitted curve (`relationship_type = curve` with
the fit in `model_or_value`) — do both when the paper gives points *and* a fit.

| Column | Content | Allowed / convention |
|---|---|---|
| `relationship_id` | Stable unique id | `<citation_key>_r###` |
| `citation_key` | Source study | matches `data/corpus.csv` |
| `mechanism` | Injury mechanism | from `data/vocab/mechanisms.csv` |
| `predictor` | The stressor/characteristic varied | code from `stressors_and_predictors.md` |
| `predictor_value` | Value or point | number; blank if `predictor_range` used |
| `predictor_range` | Range tested/covered | `lo–hi` |
| `predictor_unit` | Unit of predictor | SI / canonical (kPa, s⁻¹, m·s⁻¹, %BEP, rpm, mm, m) |
| `response` | The outcome predicted | e.g. mortality; injury_major; injury_swimbladder; survival; strike_probability; malady_index |
| `response_value` | Value | number |
| `response_unit` | Unit of response | usually `%`; or probability, index |
| `response_uncertainty` | CI / SE / SD as given | e.g. `±3.1`; `95% CI 8–17` |
| `relationship_type` | Form of the relationship | `threshold` / `point` / `curve` / `equation` / `categorical` / `qualitative` |
| `effect_direction` | Sign of the effect | `increases` / `decreases` / `nonmonotonic` / `none` |
| `model_or_value` | The threshold value, fitted form, or `equation_id` | e.g. `LD50 = 0.62 RPC`; `logit(p)=…`; `EQ → equations.csv:<id>` |
| `species` | Taxa | common (scientific); from `data/vocab/species.csv` |
| `life_stage` | Stage | egg/larva/fry-fingerling/juvenile/smolt/yearling/adult |
| `fish_size` | Length/mass tested | keep units, e.g. `95–165 mm` |
| `acclimation` | Acclimation depth / pressure / buoyancy state | e.g. `7.6 m`; `neutral @ surface` |
| `structure_type` | Turbine/pump/route | Kaplan/Francis/bulb/propeller/PIT/VLH/screw/pump(type)/weir/spillway/bypass/screen |
| `structure_detail` | Model / make / size | free text (e.g. `Hidrostal pump`, `runner Ø 7.5 m`) |
| `operating_point` | Operating mode | e.g. `90 %BEP`; `head 12 m`; `Q=…`; `gate 60 %` |
| `geometry` | Relevant geometry params | blade count; tip speed; gap clearance; leading-edge form |
| `n` | Sample size for the point | as reported |
| `exposure_pathway` | (optional axis) | from `data/vocab/` if inferable |
| `outcome_timing` | (optional axis) | immediate/latent/indirect from `data/vocab/` |
| `source_location` | **REQUIRED** provenance | `Fig 4`; `Table 2`; `Eq 3`; `p. 1147` |
| `extraction_method` | How the value was obtained | `reported` / `read_from_table` / `digitized_figure` / `fitted_by_us` |
| `digitized_points_file` | If digitized | path under `data/figures/` |
| `confidence` | Provenance grade | `Mined` (auto first pass) / `Verified` (read & checked) |
| `notes` | Caveats, assumptions, conversions applied | free text |

### Rules
- **Threshold rows** must state *what* the threshold is of (onset / 50 % / mortal)
  in `response`/`notes`, the value+unit in `model_or_value`, and the species/stage.
- **Curve rows**: put the functional form (or `equation_id`) in `model_or_value`;
  store the underlying points as additional `point` rows or a digitized file.
- **Categorical comparisons** (e.g. Kaplan vs Francis survival) use
  `relationship_type = categorical`, `predictor = structure_type` (or `pump_type`),
  with each level's response as its own row.
- Any unit conversion you apply (e.g. depth→pressure, nadir→RPC) goes in `notes`,
  with the original value preserved.

---

## B. `data/equations.csv` — one row per predictive equation / model

| Column | Content | Convention |
|---|---|---|
| `equation_id` | Stable id | `<citation_key>_eq#` |
| `citation_key` | Paper it appears in | → `data/corpus.csv` |
| `origin_citation_key` | Original source if reused | blank if first published here |
| `name` | Common name | e.g. `Deng blade-strike`; `von Raben strike`; `Boyle's-law barotrauma`; `BioPA dose–response` |
| `mechanism` | Mechanism predicted | from `data/vocab/mechanisms.csv` |
| `predicts` | Response variable | strike_probability / mortality / injury / survival |
| `form` | Model class | `deterministic` / `probabilistic` / `empirical-fit` / `mechanistic` / `statistical(GLM…)` |
| `equation` | The equation | plain text / pseudo-LaTeX, e.g. `P = 1 − exp(−n·L/(60·v)·…)` |
| `variables` | Each symbol | `sym: meaning [unit]; …` |
| `parameters` | Fitted/assumed constants | `name=value [unit]; calibrated for …` |
| `domain_of_validity` | Where it holds | predictor ranges; species; turbine types; head range |
| `response_metric` | What the output means precisely | e.g. "immediate strike mortality, balloon-tag" |
| `source_location` | **REQUIRED** | `Eq 3`, `p. …` |
| `validation` | How (if) it was validated | dataset / R² / against field survival |
| `confidence` | `Mined` / `Verified` | |
| `notes` | Assumptions, surrogacy, extrapolation warnings | |

### Rules
- Record the equation **as written**, then (optionally) a normalized form in `notes`.
- Capture the **domain of validity** explicitly — most wrong survival estimates come
  from running a model outside the range/species/turbine it was fit for.
- If a relationship row in table A *is* this equation, set its `model_or_value` to
  `EQ → equations.csv:<equation_id>`.

---

## C. Units & pressure standardization

The canonical variables and their physical units are listed in
[`../../../data/variables_units.csv`](../../../data/variables_units.csv) (rendered in the
explorer under *Variables & physical units*).

**Pressure is standardized to kPa.** Two complementary places enforce this, for full
traceability of *where and when* a conversion happens:

1. **At curation (source CSV).** Enter pressures in **kPa**. When a source reports another
   unit, convert it and record the original in `notes`, e.g. `acclimation 4.6 m (146.2 kPa)`.
2. **At build time (enforced + logged).** `scripts/build_stressor_response.py`
   (`standardize_pressures()`) converts any pressure field whose unit is not kPa, using the
   factors below, **appends the original value to that row's `notes`** as
   `[conv: <value> <unit> ×<factor> -> kPa]`, and writes a conversion entry to the build log
   and the explorer's *Variables & units* panel. If everything is already kPa it reports
   `0 conversions` (the current state of the dataset).

**Conversion factors (× value → kPa):** `Pa ×0.001`, `hPa ×0.1`, `kPa ×1`, `MPa ×1000`,
`psi ×6.894757`, `bar ×100`, `atm ×101.325`, `mmHg ×0.1333224`.
**Depth → pressure (freshwater):** absolute kPa = `101.325 + 9.80665 × depth_m`.

Note: **shear stress (Pa)** is a distinct quantity and is *not* folded into the pressure
standard; strain rate (s⁻¹) ≠ shear stress (Pa) ≠ pressure (kPa).

**Length & mass are standardized too:** length → **mm**, mass → **g** (parsed from the free-text
`fish_size` field by the build; `cm ×10`, `m ×1000`, `kg ×1000`, `mg ×0.001`). The build adds derived
`length_mm` / `mass_g` (used by the explorer's body-length / body-mass filters and the
data-completeness indicator). A field that is absent stays blank and shows as *(not provided)* — never
imputed.

---

## D. `data/dose_response_models.csv` — one row per runnable fitted model

Holds the **fitted coefficients** so a dose–response curve can be **computed** (and overlaid on a
shared axis) without digitizing points. This is where published model tables land (e.g. PNNL
Biological Response Models Tables 11–13; Pflugrath 2018 Table 4; Zitek 2026 Table 3).

| Column | Content | Convention |
|---|---|---|
| `model_id` | Stable id | `DRM_<src>_<resp>_<species>` |
| `citation_key` | Source | → `data/corpus.csv` (e.g. `Pflugrath2020c` = the PNNL report) |
| `mechanism` | Mechanism | `barotrauma` / `strike` / `shear` |
| `species` | Taxon (+ stage if needed) | `Common name (Scientific name)`; matches relationship rows for shared colour/filter |
| `response` | What the curve predicts | `injury` / `mortal injury` / `immediate mortality` / `survival` |
| `x_metric` | **The x-axis** | `ln(RPC)` (=LRP, barotrauma) / `strike velocity` / `strain rate` — models compare only within one x_metric |
| `x_min`, `x_max` | Domain to draw over | numeric, in x_metric units |
| `form` | Functional form | `logistic` (`P = 1/(1+exp(-(b0+b1·x)))`), `curvilinear`, … |
| `b0`, `b1` | Coefficients | as published |
| `source_location` | **REQUIRED** | `Table 12`, `Eqn 12`, `p. …` |
| `confidence` | `Mined` / `Verified` | |
| `notes` | Original study, caveats, inferred values | |

**Rules**
- **`x_metric` is mandatory and segregates the plot** — barotrauma (LRP), blade strike (velocity),
  and shear (strain rate) each get their own axis; never overlay across metrics.
- Verify each model against a stated landmark (e.g. `RPC50 = exp(−b0/b1)`) before use.
- A model taken from a synthesis report cites the report in `citation_key`, with the original study in `notes`.

---

## E. Derived (generated) tables — the assessment layer

`scripts/build_stressor_response.py` regenerates these into `outputs/` on every build; they are the
machine-readable assessment / gap-analysis layer (do **not** hand-edit):

- `outputs/stressor_response_coverage.csv` — one row per (mechanism × predictor × response) cell with a
  **coverage level** (`modelled` / `quantitative` / `qualitative`) + the contributing studies.
- `outputs/stressor_response_thresholds.csv` — per (mechanism × predictor × unit × response × species):
  `n` and `min/median/max` of the numeric values.
