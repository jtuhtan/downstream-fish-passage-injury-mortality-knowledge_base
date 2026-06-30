# Stressor–response synthesis — barotrauma (demonstrator)

> **Scope & status.** A demonstrator built from the `passage-stressor-response` skill
> on **8 barotrauma lab papers**. All rows are `confidence = Mined` (extracted, not yet
> PDF-verified via `tools/verification/`). It exists to show the value chain
> *curated relationships → analysis/comparison/exploration/reporting*; it is **not** a
> complete barotrauma synthesis. Sources: [`data/stressor_response.csv`](../data/stressor_response.csv),
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

`equations.csv` registers 6: Boyle's-law volume change (static) and its dynamic critique
[Brown2012]; the two RPC definitions and LRP; the **per-species logistic** `logit(p) = b0 +
b1·ln(RPC)` [Pflugrath2018]; and McKinstry's **AIC-selected mortal-injury metric** (the
8-injury endpoint reused across the PNNL/WA studies) [McKinstry2007]. Each carries its
**domain of validity** — the guard against extrapolating a salmonid model onto an eel.

## 5. Biggest gap (what to do next)

The **dose–response curves themselves are in figures** (Brown Fig 3 mortal-injury vs LRP;
Pflugrath Figs 2–3 injury vs ln(RPC); Stephenson Fig 3 vs nadir). Until they are
**digitized** (`references/figure_digitization.md`) the explorer plots only the scalar
thresholds. Digitizing those four figures + extracting the per-species logistic
coefficients would turn this into a real, overlay-able barotrauma dose–response dataset.
