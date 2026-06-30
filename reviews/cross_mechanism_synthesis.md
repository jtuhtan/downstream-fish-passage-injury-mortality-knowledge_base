# Cross-mechanism synthesis (barotrauma x collision x shear)

A first synthesis across the three mechanism modules and the three-axis framework
(mechanism x exposure pathway x outcome timing), covering the 120-study union
within a 255-paper corpus now coded on all three axes. Companion file:
`outputs/Cross_mechanism_gap_matrix.xlsx`.

## 1. Reproducibility vs. scope - an inverse relationship

| Mechanism | Papers | Live-fish studies scored | Mean reporting completeness |
|---|---|---|---|
| Barotrauma | 66 | 39 (32 lab + 7 field) | 74% |
| Collision (blade strike & impact) | 53 | 25 (9 simulated + 16 field) | 83% |
| Shear (fluid shear / strain rate) | 39 | 12 (lab only) | 94% |

The headline pattern: **the better-reported a mechanism is, the narrower its
evidence base.** Shear has near-complete reporting but rests on ~12 lab studies
from essentially one apparatus lineage; barotrauma has the broadest, most diverse
evidence but the weakest reporting (undefined pressure-change metrics, missing
acclimation duration). High internal reproducibility (shear) and broad external
coverage (barotrauma) are, so far, mutually exclusive in this literature.

## 2. Taxonomic coverage - concentrated on salmonids and eels

Studies per mechanism by family group (from `Cross_mechanism_gap_matrix.xlsx`):

| Family group | Barotrauma | Collision | Shear |
|---|---|---|---|
| Salmonids | 41 | 29 | 19 |
| Eels | 20 | 19 | 13 |
| Perches & relatives | 10 | 1 | 4 |
| Cyprinids (s.l.) | 8 | 7 | 4 |
| Lampreys | 5 | 2 | 2 |
| Sturgeons | 4 | 6 | 0 |
| Clupeids (shads & herrings) | 3 | 4 | 7 |
| Catfishes | 3 | 0 | 0 |
| **Gobies** | **0** | **0** | **0** |
| **Sculpins** | **0** | **0** | **0** |
| **Livebearers** | **0** | **0** | **0** |

- **Two taxa carry the field.** Salmonids and eels account for the large majority
  of all live-fish evidence across every mechanism.
- **Whole families have no data.** Gobies, sculpins and livebearers are absent
  across all three mechanisms - i.e. small-bodied and benthic/bottom-associated
  fishes are systematically untested, despite encountering the same structures.
- **Per-mechanism holes:** shear has been tested on no sturgeon, catfish, goby,
  sculpin or livebearer; collision has essentially no catfish or perch data;
  barotrauma is the broadest but still thin for clupeids and catfishes.

## 3. Outcome timing - the iceberg below immediate survival

Studies reporting each outcome-timing class (multi-valued):

| Timing | Barotrauma | Collision | Shear |
|---|---|---|---|
| Immediate | 50 | 38 | 26 |
| Delayed | 51 | 28 | 20 |
| Sublethal | 46 | 34 | 24 |
| Latent / long-term | 7 | 1 | 3 |
| Indirect (e.g. predation) | 17* | 6* | 14* |

Immediate, delayed and sublethal endpoints are well represented, but
**latent/long-term mortality is barely measured** (2-9 studies per mechanism) and
indirect (post-passage predation) mortality is mostly *discussed* rather than
*quantified* (*the Indirect counts flag studies that address it, not that they
measured it - treat as an upper bound). The true population-level cost of passage
- delayed death, fitness loss, and predation on disoriented/injured fish - is the
least-quantified part of the whole field.

## 4. Exposure pathway - lab-bound and rarely localised

- **Study environment.** Shear is almost entirely laboratory; barotrauma is
  mostly lab chamber with some field; collision is the most balanced (simulated
  rigs + field passage). Field live-fish shear injury is effectively absent.
- **Location during passage.** Real-structure live-fish studies overwhelmingly
  report **"whole-route (not localised)"** - balloon-tag/recapture survival can
  rarely attribute injury to a component. Only CFD studies localise to the
  runner, draft tube, wicket gates, etc. So the place where injury actually
  happens inside a machine is known mostly from models, not from fish.

## 5. What the gaps tell us to do next

1. **Add the missing direct-contact and gas mechanisms** - grinding/abrasion
   (completes the contact picture with collision) and gas supersaturation/GBT
   (de-conflates from barotrauma). These were the prior priority and the matrix
   confirms they are not covered by the existing three.
2. **Break the salmonid/eel monoculture.** Prioritise benthic and small-bodied
   fishes (gobies, sculpins, catfishes) and non-temperate species, and report
   `family`/`family_group` so coverage can be tracked.
3. **Measure the iceberg.** Build latent/long-term, sublethal and quantified
   indirect (predation) endpoints into study designs - the biggest blind spot.
4. **Localise injury in the field.** Couple lab dose-response and CFD component
   exposure to field passage so real injuries can be attributed to a location,
   not just to "the turbine".
5. **Trade reproducibility for breadth deliberately.** Apply shear's reporting
   discipline (its minimum-reporting rigour) to the broader, messier barotrauma
   and collision evidence.

## Provenance & caveats
Mechanism membership and metrics come from the per-mechanism registers; family
groups are mapped from `data/vocab/species.csv`; exposure/timing from
`data/axes_exposure_timing.csv` (all 255 rows (currently Mined, pending verification); the 97 field/numerical
rows were reviewed per-paper, 66 corrected - see `methodology/07`). Indirect-timing counts are upper bounds
(coverage, not quantification). Counts exceed unique-paper totals because studies
span several taxa, environments and timing classes.
