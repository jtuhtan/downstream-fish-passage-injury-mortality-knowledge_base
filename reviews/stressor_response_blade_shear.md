# Stressor–response: blade strike & fluid shear (dose–response models)

Companion to the barotrauma [synthesis](stressor_response_synthesis.md). This extends the runnable
dose–response layer from one mechanism to **three**, each on its **own dose axis**, all built from
**exact published coefficients** in the PNNL *Biological Response Models* report (Pflugrath et al.
2020) — no figure tracing. The explorer's "Dose–response curves (modelled)" section now renders one
panel per mechanism (barotrauma · blade strike · fluid shear).

## Why three axes (not one)

Each mechanism injures fish through a different physical dose, so the curves are **not**
comparable on a shared x-axis — pooling them would be a category error:

| Mechanism | Dose (x-axis) | Model form | PNNL source |
|---|---|---|---|
| Barotrauma | `ln(RPC)` = LRP (pressure ratio) | logistic (Eq 12) | Tables 11–13 |
| **Blade strike** | **strike velocity (m s⁻¹)** | curvilinear (Eq 10) · logistic in V ± L/t (Eq 9) · MLR (Eq 8) | Tables 3–5 |
| **Fluid shear** | **strain rate (s⁻¹)** | logistic (Eq 14) | Tables 14–16 |

`build_stressor_response.py` therefore groups models by `x_metric` and draws a **separate panel** for
each, with its own axis, range and tick scale; a `probAt()` dispatcher evaluates each `form`
(`logistic`, `loglogistic`, `linear_survival`) analytically.

## What was added

- **34 fluid-shear models** (Eq 14, `P = 1/(1+e^-(b0+b1·S))`): 11 injury, 9 major injury, 14 mortality,
  spanning ~17 species (Neitzel salmonids, Pflugrath shad, Baumgartner/Colotelo/Engbrecht ornamentals
  & centrarchids, Turnpenny herring/eel/salmon).
- **11 blade-strike models**: 7 whole-fish **curvilinear** (Eq 10, log-logistic component plotted;
  American eel, Alosa spp., bluegill, brook trout, gizzard shad, hybrid striped bass, rainbow trout),
  2 **logistic in velocity** (Eq 9, bluegill functional & combined mortality), 2 **MLR** (Eq 8,
  rainbow trout at L/t = 2 and 4, showing the length-to-blade-thickness effect).
- **21 landmark relationship rows** for the comparator / coverage / thresholds tables: 7 blade-strike
  **E50** (strike velocity at ½ of asymptotic whole-fish mortality) and 14 shear **S50** (strain rate
  at 50 % mortality).
- **5 equations** (Eq 8, 9, 10, 14, 15 incl. the strain-rate definition) and **5 variables**
  (V, L/t, S, E50, S50, each with a passage-injury definition).

Total runnable models: **91** (46 barotrauma + 34 shear + 11 blade strike).

## QA — coefficient cross-check (all pass)

A Python port of `probAt()` re-derived the landmark doses and checked every curve is monotonic and
bounded in [0, 1]:

- **Blade Eq 10:** `P(e) = f/2` confirmed for all 7 (validates the b=b0 / e=b1 / f=b2 mapping);
  rainbow-trout **ED50 = 7.06 m s⁻¹ matches the report's stated ~7.08** ✓. Whole-fish maxima
  f = 0.38–0.55 (American eel most tolerant, brook trout most sensitive).
- **Blade Eq 9 / Eq 8:** bluegill V50 ≈ 5.3 (functional) / 6.1 (combined) m s⁻¹; rainbow-trout V50 =
  13.3 (L/t 2) → 9.4 (L/t 4) m s⁻¹ — thinner blade relative to fish ⇒ lower V50 (more injurious), the
  expected direction.
- **Shear Eq 14:** S50 = −b0/b1 spans 130–1946 s⁻¹. Bala shark is the most shear-sensitive
  (S50 ≈ 130, injury); salmonids are tolerant (rainbow-trout/steelhead injury S50 ≈ 1070/796). **Two
  mortality models (blue gourami 1946, brown trout 1696)** have S50 beyond the ~1600 s⁻¹ test range —
  flagged as extrapolations, not errors.

## Primary blade-strike sources (beyond the synthesis)

The first blade-strike pass took every model from the PNNL synthesis report (`Pflugrath2020c`). A
second pass read the **underlying primary studies** directly, so blade strike now stands on six
primary citations, not one:

| Study | Contribution | Extracted |
|---|---|---|
| **Saylor 2019** | bluegill (small/medium × observed/combined mortality) | 4 log-logistic models + 2 E50 |
| **Saylor 2020** | large & small rainbow trout, brook trout, gizzard shad, Alosa spp. | 5 log-logistic models + 5 ED50 (Table 1) |
| **Bevelhimer 2019** | blade-thickness effect, 3 species, 950 fish | thickness→mortality relationship |
| **Amaral 2020** | blade slant & within-body strike location (rainbow trout) | 98% vs 26.8% survival at L/t=2; 68% vs 7.9% by location |
| **Amaral 2011** | L/t ratio design threshold | L/t ≤ 1 → sharply higher injury |
| **Meng 2022** | fish-friendly turbine, crucian carp | gross immediate mortality 10.9%, injury 80.5% |

The **9 primary models** are the **mid-body lateral 90° single-strike** form
`P(M) = 1/(1+(V/e)^b)` with the upper bound fixed at **1** — so `e` is a *true* LD50 (P(e)=0.5) and
these are the worst-case, per-strike-location curves. They are deliberately kept **alongside** the
7 PNNL **whole-fish** curvilinear models (which integrate all 36 strike area/angle combinations and
therefore peak at `f` ≈ 0.4–0.55): the pair lets you compare the severity of a single square hit
against the fleet-averaged outcome for the same species. Cross-check confirmed every primary ED50
against its source table (rainbow trout 6.59 / 7.08, brook trout 5.99, gizzard shad 5.66, Alosa 7.87,
bluegill 5.68 / 6.43 m s⁻¹).

Turnpenny (2000) was reviewed but **not** ingested here: its blade-strike model is a geometry-based
*strike-probability* model (runner geometry × fish length × rpm) combined with a mutilation ratio, a
different paradigm from velocity dose–response — flagged as a distinct model class to add later.

## Primary fluid-shear sources (confirmation + re-attribution)

The shear pass read the primary studies behind the synthesis Tables 14–16. Unlike blade strike (where
the primaries yielded *new* single-strike curves), the shear coefficients are **identical** to the
synthesis — so this pass **validated** the earlier extraction and **re-attributed** the models to
their sources:

| Study | Species | Result |
|---|---|---|
| **Pflugrath 2020b** (Water) | American shad | Table 4 strain-rate coefficients **match the synthesis exactly** (−8.418/0.023 etc.); re-keyed to primary |
| **Colotelo 2018** | blue gourami, iridescent shark | Table 3 (sign-flipped: synthesis β = −Colotelo b) **matches exactly** (gourami injury 0.007, shark injury 0.016 …); re-keyed to primary |
| **Neitzel 2004** | Chinook, rainbow trout, steelhead | scanned PDF (no text layer) — kept synthesis attribution, flagged for OCR |

Pflugrath 2020b additionally gives **3 American-shad models on an ACCELERATION axis** (m s⁻², the
quantity Sensor Fish actually measure) — new data absent from the synthesis, added as a fifth dose
panel (A50 = 341 / 516 / 682 m s⁻² for injury / major injury / mortality).

## Turnpenny (2000) — a new blade-strike model class

Turnpenny's STRIKER model is a **geometry-based collision** model, a different paradigm from velocity
dose–response, now ingested as its own class:

- **Von Raben strike probability** — `P_strike = L_f / L_w`, water-length `L_w = V_a /(cos α · Z·N/60)`,
  axial velocity `V_a = Q / A_swept` (Z blades, N rpm, Q discharge). Strike rate rises with **fish
  length**; field-validated (5.9% predicted vs 4.4% observed strike at full load).
- **Mutilation ratio** (damage | strike) — `MR = 0.1533·ln(L) + 0.0125` (L in cm), refining Von Raben's
  fixed 0.43. Added as a **runnable model on a fish-length dose axis** — the framework's first
  length-based curve (MR rises 0.01 → 0.64 over 1–60 cm).
- **Compound mortality** — `P = 1 − (1−P_pressure)(1−P_shear)(1−P_strike)` (cross-mechanism combiner),
  plus Turnpenny's classic **barotrauma** regressions (physoclist vs physostome mortality vs Pₑ/Pₐ),
  captured in `equations.csv`.

## Caveats

- **Blade Eq 10** is a piecewise **log-logistic + linear** model; the explorer plots the dominant
  **log-logistic component** (peak = whole-fish max `f`). The small high-velocity linear tail
  (slope m ≈ 0.009 m⁻¹s) is stored in the CSV (b3, b4) but omitted from the curve.
- **Whole-fish** blade curves integrate all 36 strike area/angle combinations, so their maxima are
  well below 1 — a mid-body 90° strike alone is far more lethal than the whole-fish average.
- Shear strain rate uses the **dy = 1.8 cm** (fish-width) convention (Neitzel 2000); magnitudes are
  only comparable because every PNNL model shares it.
- Blade Eq 9 for **hybrid striped bass** carries an L/t term (b2 = 2.88); it is recorded in
  `equations.csv` but not plotted (the velocity-only Eq 10 curve is used for that species instead).

## Files

- Models: [`../data/dose_response_models.csv`](../data/dose_response_models.csv) (now with `b2,b3,b4`)
- Equations: [`../data/equations.csv`](../data/equations.csv) · Variables:
  [`../data/variables_units.csv`](../data/variables_units.csv)
- Explorer: [`../docs/stressor_response.html`](../docs/stressor_response.html) →
  *Dose–response curves (modelled)*
