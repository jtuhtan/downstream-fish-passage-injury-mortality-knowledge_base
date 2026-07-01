# Stressor–response synthesis — barotrauma (demonstrator)

> **Scope & status.** Built with the `passage-stressor-response` skill across the
> **full barotrauma corpus** — the finder ran over all **72 available barotrauma PDFs**
> (2,385 candidate findings), from which **41 relationships + 11 equations** are curated
> so far across ~25 papers. All rows are `confidence = Mined` (extracted, not yet
> PDF-verified via `tools/verification/`). It shows the value chain
> *curated relationships → analysis/comparison/exploration/reporting*; curation of the
> remaining candidates and figure digitization are ongoing. Sources: [`data/stressor_response.csv`](../data/stressor_response.csv),
> [`data/equations.csv`](../data/equations.csv); explore interactively at
> [`docs/stressor_response.html`](../docs/stressor_response.html); regenerate with
> `python scripts/build_stressor_response.py`.

## 1. The dose metric — and a comparability trap

Barotrauma severity is governed by the **pressure ratio**, not absolute depth. Two
incompatible conventions for "RPC" appear in the corpus and **must not be pooled**:

| Convention | Definition | Range | Used by | code |
|---|---|---|---|---|
| Acclimation/nadir | RPC = P_A / P_N | ≥ 1 (higher = worse) | Brown, Pflugrath | `rpc_AN` |
| Exposure/acclimation | RPC = P_N / P_A | 0–1 (lower = worse) | Boys 2016 | `rpc_EA` |

`LRP = ln(P_A/P_N)` linearises the dose for logistic models. The structured schema
keeps each metric in its own lane (see the explorer) precisely so a "RPC of 0.4"
[@Boys2016] is never mis-read against a "RPC of 2" [@Pflugrath2018].

## 2. Threshold landmarks (Mined — verify before citing)

- **Juvenile Chinook (physoclist):** mortality reported at **RPC(A/N) ≈ 2 (≈50 % pressure
  reduction)**; injury/mortality rise with nadir 8–19 kPa; caudal-vein-rupture
  haemorrhage in **88–93 %** at severe decompression [Brown2009, Pflugrath2018].
- **Australian larvae (physoclist):** haemorrhaging increases sharply once **RPC(E/A) falls
  below ~0.4** (pressure < 40 % of acclimation) [Boys2016]; but **egg hatching success is
  unaffected by RPC** (a documented *null* dose–response) and short-term larval mortality
  is weakly linked to decompression.
- **Buoyancy state matters:** at a given nadir, **negatively buoyant** fish are injured more
  than neutrally buoyant ones; nadir explained ~15–23 % of injury deviance, buoyancy ~6 %
  [Stephenson2010]. A **maximum neutral-buoyancy depth** caps how deep fish acclimate
  [Pflugrath2012] — setting the worst-case acclimation pressure.

## 3. Species susceptibility (comparison)

- **Physostomes ≫ tolerant.** Brook and Pacific lamprey ammocoetes showed **minimal
  barotrauma** after rapid decompression [Colotelo2012] — consistent with the general
  physostome (lamprey/eel/some cyprinids) vs physoclist (salmonids/perch) split.
- **Within physoclists:** **silver perch** has a *lower* swim-bladder-rupture threshold than
  **Murray cod** [Pflugrath2018] — species-specific logistic curves, not one threshold.

## 4. Models available to predict outcomes

`equations.csv` registers 11: Boyle's-law volume change (static) and its dynamic critique
[Brown2012]; the two RPC definitions and LRP; the **per-species logistic** `logit(p) = b0 +
b1·ln(RPC)` [Pflugrath2018, Zitek2026]; McKinstry's **AIC-selected mortal-injury metric**
(the 8-injury endpoint reused across the PNNL/WA studies) [McKinstry2007]; **Carlson's
fitted model** `logit(p) = −5.997 + 4.201·LRP + 0.603·TB` adding **tag burden** as a
predictor (so e.g. RPC = 2.18 → ~14–24 % mortal injury depending on tag load) [Carlson2012];
the BioPA-style **CFD-coupled** model that integrates a dose–response over a modelled
nadir-pressure distribution [Martinez2025, Hou2018]; and a **shear** threshold (LS10)
[Boys2014]. Each carries its **domain of validity** — the guard against extrapolating a
salmonid model onto an eel. New since the 8-paper demo: **tag burden, operating point /
runner geometry (CFD), and many more species** (American shad, American eel, gambusia,
redfin, crucian carp, pictus catfish, Neotropical and European potamodromous fishes).

## 5. Dose–response curves — overlaid from published coefficients

The per-species logistic **coefficients** are extracted *exactly* from the source tables/equations
into [`../data/dose_response_models.csv`](../data/dose_response_models.csv) — Pflugrath 2018 Table 4
(injury & mortal injury × Australian bass, carp gudgeon, Murray cod, silver perch) and Carlson 2012
(Chinook). Because `LRP = ln(RPC)`, all nine models share one x-axis, so the explorer **overlays the
curves analytically** (solid = mortal injury, dashed = injury) — the preferred route over tracing
figures (and copyright-clean: published coefficients, no image). This is where you read off, e.g.,
that silver perch's injury curve is the steepest and Murray cod's mortal-injury curve is shifted
rightmost (most tolerant). Remaining **figure-point digitization** (e.g. Stephenson Fig 3, % vs
nadir, which exists only as a figure) follows the protocol and the **copyright & digitization
policy** in `skills/passage-stressor-response/references/figure_digitization.md`.

> **Now multi-mechanism.** The overlay is no longer barotrauma-only: the explorer renders **one panel
> per mechanism on its own dose axis** — barotrauma (`ln(RPC)`), **blade strike** (strike velocity,
> m s⁻¹) and **fluid shear** (strain rate, s⁻¹) — **91 runnable models** in total. See the companion
> [blade-strike & fluid-shear review](stressor_response_blade_shear.md) for the model forms
> (curvilinear Eq 10, logistic Eq 9/14, MLR Eq 8), the coefficient cross-check, and caveats.

## 6. Coverage & gaps — the assessment framework

`build_stressor_response.py` emits two machine-readable tables that operationalise the base for
assessment and gap analysis, and the explorer renders them as an interactive **coverage & gaps
matrix** (predictor × {response | species | structure | mechanism}, colour-coded so quantified,
qualitative-only, and blank/unstudied cells are obvious):

- `outputs/stressor_response_coverage.csv` — one row per (mechanism × predictor × response) cell
  with a **coverage level** (modelled / quantitative / qualitative) and the contributing studies.
- `outputs/stressor_response_thresholds.csv` — per (mechanism × predictor × unit × response ×
  species): **n** and **min/median/max** of the numeric values.

**Current barotrauma coverage (41 relationships → 34 populated cells):** **2 modelled, 21
quantitative, 11 qualitative-only**; **9 numeric threshold groups**.

- **Best quantified / modelled:** pressure-ratio dose (**LRP / RPC**) → (mortal) injury, with
  logistic models [Pflugrath2018, Carlson2012, Zitek2026] — the densest, most model-ready cell.
- **Qualitative-only cells (the curation gaps — exist but not yet numeric):** buoyancy / swim-bladder
  state → injury/mortality (3 studies, categorical), **TDG** → injury/mortality, turbine/pump
  **structure_type** comparisons, runner **geometry** → nadir. Their numbers live in figures/tables
  not yet digitized.
- **Sparse thresholds:** only 9 numeric groups (e.g. RPC_AN ≈ 2 → 50 % mortality, Chinook;
  RPC_EA ≈ 0.4 injury onset, Australian larvae; strain rate 1000 s⁻¹ → −16 % survival, gambusia).

**Major gaps (blank / thin cells):** non-salmonid species (eel, shad, lamprey, cyprinids,
Neotropical/European) mostly have single qualitative cells; **pump / screw / VLH** structure types
are barely represented vs Kaplan; **shear** is almost absent from the barotrauma corpus; and the
operating-point/geometry → outcome link is qualitative (CFD nadir distributions exist, but the
nadir → survival step is not yet numeric here). The highest-value action to convert qualitative
cells to quantitative remains **digitizing the dose–response figures** and extracting the
per-species logistic coefficients.
