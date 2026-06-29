# Metrics, units & reported threshold landmarks

Thresholds are only comparable **within a metric and a species/stage**. Keep
units explicit. Below: the metric, its unit, and indicative landmarks reported
in the passage literature (verify against the actual paper; values vary by
species, life stage, and acclimation).

## Barotrauma / pressure
- **Ratio of Pressure Change (RPC)** = acclimation (or exposure-onset) pressure
  ÷ nadir pressure. Dimensionless. Higher RPC = more severe decompression.
  Often the most transferable barotrauma metric.
- **Log Ratio of Pressure (LRP)** = log10 of the pressure ratio. Used in some
  dose–response and "biological response" models.
- **Nadir pressure** — lowest absolute pressure experienced (kPa). Barotrauma
  risk rises sharply as nadir falls below acclimation pressure.
- **Acclimation / neutral-buoyancy depth** — the depth the fish equilibrated to;
  sets the baseline for RPC. A critical, often-contested assumption (fish in the
  wild may not be neutrally buoyant at the intake).
- **Landmarks (indicative, species-dependent):** mortal/severe barotrauma in
  juvenile salmonids often reported around RPC ≈ 0.5–0.7 nadir relative to
  ~surface acclimation and increasing steeply with acclimation depth; physostome
  species (e.g. eel, some cyprinids) are markedly more tolerant than
  physoclists. Always cite the specific value + species + acclimation.

## Fluid shear
- **Strain rate** (s⁻¹) — primary exposure metric from jet/flume studies.
  Reported injury onset for juvenile salmonids commonly in the high hundreds to
  ~1000 s⁻¹ range; minor-to-major injury increases with strain rate. Eye and
  operculum injuries appear first.
- Distinguish from **shear stress** (Pa) — a different quantity; do not conflate.

## Blade strike
- **Strike probability** — modeled likelihood of blade contact (function of fish
  length, blade count/speed, axial velocity).
- **Strike velocity** (m s⁻¹) — impact speed; mortality rises with velocity and
  fish length; blunt/​slanted leading edges reduce injury at a given velocity.
- **Mutilation/strike-mortality curves** vs. velocity and fish length.

## Gas supersaturation
- **Total Dissolved Gas (TDG)** — % saturation. GBT risk rises above ~110–120%
  depending on depth/compensation; depth of fish strongly modulates effect.

## Combined / survival metrics
- **Passage survival / mortality (%)** — route-, turbine-, and life-stage-
  specific; often via mark–recapture (HI-Z/balloon tags), telemetry, or modeled
  (blade-strike + barotrauma) estimates.
- **Biological Performance Assessment (BioPA)** and **bio-hill charts** — CFD-
  derived distributions of exposure (pressure, shear, strike) mapped to dose–
  response to predict survival across operating points.

## Comparison traps
- RPC vs nadir-pressure vs LRP are related but not interchangeable.
- Strain rate (s⁻¹) ≠ shear stress (Pa).
- Lab "simulated passage" exposes one mechanism at controlled doses; field
  survival integrates all mechanisms + handling/tagging effects; CFD predicts
  exposure, not biology, unless coupled to a dose–response model.
- Tag/handling burden can inflate apparent mortality (control for it).
