# 4. Extraction schema & controlled vocabularies

One row per study in `data/extraction.csv`. Keep list-valued cells
semicolon-separated (`A; B; C`) so they filter cleanly. Leave blank if not
reported — do not guess. Prefer what the study itself tested over what it cites.

## Columns

| Column | Content |
|---|---|
| `citation_key` | Links to `data/corpus.csv` (`YYYY_FirstAuthor`) |
| `Year`, `First author`, `Category`, `Title` | Bibliographic basics |
| `Mechanism(s)` | From `data/vocab/mechanisms.csv` |
| `Species` | Common (scientific); from `data/vocab/species.csv` |
| `Life stage` | egg / larva / fry-fingerling / juvenile / smolt / yearling / adult |
| `Fish size` | Length/mass ranges with units |
| `Thresholds/metrics` | Metric + value + unit (RPC, kPa, s⁻¹, %TDG, strike velocity) |
| `Mortality/survival` | Headline injury/mortality outcome (% and what it refers to) |
| `Sample size (n=)` | Fish/trials as reported |
| `Turbine/structure` | Kaplan/Francis/bulb/pump/screw/weir/spillway/VLH/MHK/tidal/… |
| `Methodology` | chamber / flume / strike-rig / Sensor Fish / CFD / telemetry / review |
| `Hypotheses/assumptions` | Boyle's law / dynamic model / surrogacy / neutral buoyancy / dose-response |
| `Outcome summary` | One-sentence headline finding (added on verification) |
| `Confidence` | `Mined` (automated) or `Verified` (read & checked) |

## Controlled vocabularies
- `data/vocab/mechanisms.csv` — injury mechanisms + definitions.
- `data/vocab/metrics.csv` — metrics, formulas and units.
- `data/vocab/species.csv` — taxa with swim-bladder type (physostome / physoclist /
  absent), which matters for barotrauma susceptibility.

## Extraction procedure
1. **Breadth (automated).** `scripts/extract_passage_data.py` runs `pdftotext`
   and applies the vocabularies: categorical fields from title + early text;
   numeric fields (pressures, strain rate, mortality %, n, sizes) from full text.
   Output is `Confidence = Mined`.
2. **Depth (human).** Read the key papers; correct the primary mechanism, exact
   thresholds (with units + species + acclimation), sample sizes, and the
   headline outcome; set `Confidence = Verified`.

## Comparability rules
- Thresholds are only comparable within a metric and a species/life stage.
- Keep units explicit; never silently compare RPC vs nadir vs strain rate.
- Note immediate vs delayed mortality and any tag/handling controls.
