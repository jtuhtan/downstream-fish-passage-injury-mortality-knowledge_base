# Extraction schema (one row per study)

Keep list-valued cells semicolon-separated (`A; B; C`) so spreadsheet filters
work. Leave blank if not reported (do not guess). Prefer the values the study
*itself* tested/reported over what it cites.

| Column | Content | Allowed / convention |
|---|---|---|
| Year | Publication year | YYYY; use 20XX / 200X if unknown |
| First author | Surname | single token; particles joined (vanEsch) |
| Category | Study type bucket | Review / Lab / Field / Numerical / Guidelines |
| Title | Paper title | as published |
| Mechanism(s) | Injury mechanism(s) studied | from `mechanisms.md` controlled list |
| Species | Taxa tested | common (scientific); from controlled list |
| Life stage | egg / larva / fry-fingerling / juvenile / smolt / yearling / adult |
| Fish size | Length/mass range tested | e.g. "80–165 mm"; keep units |
| Thresholds/metrics | Key quantitative thresholds | metric + value + unit (RPC, kPa, s⁻¹, %TDG) |
| Mortality/survival | Headline injury/mortality outcome | % with what it refers to |
| Sample size (n=) | Fish/trials | numbers as reported |
| Turbine/structure | Passage structure studied | Kaplan/Francis/bulb/propeller/pump/screw/weir/spillway/VLH/MHK/tidal/… |
| Methodology | How the study was done | from `study_templates.md` (chamber/flume/strike-rig/Sensor Fish/CFD/telemetry/…) |
| Hypotheses/assumptions | Main hypothesis or baked-in assumption | Boyle's law / dynamic model / surrogacy / neutral buoyancy / dose–response / threshold |
| Outcome summary | 1-sentence headline finding | free text (add during curation) |
| Confidence | Data provenance | "Mined" (auto) / "Verified" (read & checked) |
| Notes | Anything else useful | free text |

## Conventions
- **Mechanism** = what the study *measures*, not what it merely mentions.
- **Thresholds**: always carry units and the species/stage they apply to.
- **Numbers** (mortality %, n, sizes, kPa, s⁻¹) come from full text; everything
  categorical should reflect the abstract/methods, not the reference list.
- Add **Outcome summary** and set **Confidence = Verified** only after reading
  the paper; the mining script fills the rest as "Mined".
