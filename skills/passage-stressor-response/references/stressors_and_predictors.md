# Predictors — stressors, machine characteristics & fish traits

The `predictor` column in `stressor_response.csv` is drawn from this controlled
list. A predictor is anything a study relates an injury/mortality outcome to. Three
families: **(1) physical stressors** (the proximate cause of damage), **(2) system
characteristics** (design + operation that *generate* the stressors), and **(3) fish
traits** (susceptibility). Keep the canonical unit; record conversions in `notes`.

Response-side metrics (mortality, injury types, survival, malady index) and their
reported landmarks live in
`../passage-injury-mortality-review/references/metrics_thresholds.md` — do not
duplicate them here.

## 1. Physical stressors (proximate causes)

| Code | Predictor | Canonical unit | Mechanism | Notes |
|---|---|---|---|---|
| `rpc` | Ratio of pressure change (acclim ÷ nadir) | — (dimensionless) | barotrauma | Most transferable barotrauma dose; higher = worse |
| `lrp` | Log10 ratio of pressure | — | barotrauma | Used in some response models |
| `nadir_p` | Nadir (lowest) pressure | kPa | barotrauma | Pair with acclimation pressure to be meaningful |
| `accl_p` | Acclimation pressure | kPa | barotrauma | Or as depth (`accl_depth`, m) |
| `dpdt` | Rate of pressure change | kPa·s⁻¹ | barotrauma | Dynamic-model predictor |
| `strain_rate` | Fluid strain rate | s⁻¹ | shear | Primary jet/flume exposure metric |
| `shear_stress` | Shear stress | Pa | shear | **Distinct** from strain rate — never conflate |
| `strike_v` | Blade strike velocity | m·s⁻¹ | strike | Impact speed at contact |
| `strike_p` | Strike probability | — (0–1) | strike | Modeled likelihood of contact |
| `turb_tke` | Turbulent kinetic energy | m²·s⁻² | turbulence | |
| `turb_intensity` | Turbulence intensity | % | turbulence | |
| `cav_sigma` | Cavitation index σ | — | cavitation | |
| `tdg` | Total dissolved gas | % saturation | gas supersaturation | GBT risk rises >~110–120 %, depth-modulated |
| `grind_gap` | Grinding/pinch gap exposure | mm | grinding/abrasion | Runner–hub or screen gaps |
| `exposure_time` | Duration of exposure | s | (cross) | Dose = intensity × time |

## 2. System characteristics — design & operation (generate the stressors)

### Turbine / pump type (categorical predictor `structure_type`)
Kaplan · bulb · propeller · Francis · Pelton · cross-flow · very-low-head (VLH) ·
Archimedes screw · Pentair/Alden minimum-gap-runner · pump-as-turbine (PAT) ·
Hidrostal screw-centrifugal pump · axial/propeller pump · mixed-flow pump ·
internal-helical (screw) pump · MHK/tidal rotor.

### Geometry (`geometry`)
| Code | Predictor | Unit |
|---|---|---|
| `runner_d` | Runner / impeller diameter | m |
| `blade_n` | Number of blades / buckets / vanes | count |
| `rpm` | Rotational speed | rpm |
| `tip_speed` | Blade tip speed | m·s⁻¹ |
| `gap_clear` | Runner–hub / blade–shroud gap clearance | mm |
| `le_form` | Leading-edge form | blunt / slanted / sharp (categorical) |
| `runner_angle` | Blade/runner angle | ° |
| `n_stages` | Pump stages | count |

### Operating mode (`operating_point`)
| Code | Predictor | Unit |
|---|---|---|
| `pct_bep` | Fraction of best efficiency point | %BEP |
| `head` | Hydraulic head | m |
| `discharge` | Flow rate Q | m³·s⁻¹ |
| `gate` | Wicket-gate / guide-vane opening | % |
| `unit_load` | Generator load | % or MW |
| `submergence` | Draft-tube / tailwater submergence | m |
| `passage_route` | Route taken | turbine / spill / bypass / sluice / screen |

## 3. Fish traits (susceptibility predictors)

| Code | Predictor | Unit |
|---|---|---|
| `length` | Total/fork length | mm |
| `mass` | Body mass | g |
| `species` | Taxon | (controlled, `data/vocab/species.csv`) |
| `life_stage` | Stage | egg…adult |
| `accl_depth` | Acclimation / neutral-buoyancy depth | m |
| `swimbladder` | Physostome vs physoclist | categorical (modulates barotrauma) |
| `condition` | Condition factor / lipid | — |

## Using predictors well
- A relationship usually has **one focal predictor** (in `predictor`) with the rest
  pinned as **conditions** (the dedicated columns). Put the varied quantity in
  `predictor`; hold everything else fixed in `structure_type`, `operating_point`,
  `geometry`, `species`, etc.
- **Stressor vs cause:** prefer recording both when available — e.g. mortality vs
  `nadir_p` (stressor) for a given `structure_type=Kaplan` at `pct_bep=90` (cause).
  The stressor transfers across machines; the machine/operating predictor is what an
  engineer can change.
- Add a new code only when a paper genuinely needs one; record the addition in the
  CHANGELOG and (if it recurs) here.
