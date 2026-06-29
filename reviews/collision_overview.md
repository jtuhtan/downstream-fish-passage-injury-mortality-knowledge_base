**Collision (Blade Strike & Impact) in Downstream Fish Passage  
Metrics, Protocols & the Reproducibility of Live-Fish Studies**

*A state-of-the-art assessment of 48 collision papers (25 live-fish
studies scored)  
Companion to the workbook 'Collision\_metrics\_reproducibility.xlsx'*

# 1\. Purpose & scope

Collision — the direct mechanical impact of a moving blade or a fixed
structure on a fish — is, alongside barotrauma, one of the two dominant
causes of injury and mortality during downstream passage. This document
and its companion workbook catalogue every collision metric in use and
how each is calculated, describe the protocols used to generate
collision data on live fish, and assess how reproducible that live-fish
evidence base is. We then identify the major problems and gaps and
propose concrete next steps.

Definition. We treat 'collision' broadly as ANY mechanical
impact/contact event during passage: turbine blade strike (the
most-studied case), impeller/pump strike, Archimedean-screw and
structure contact, wall / draft-tube / plunge-pool impact, and
pinch/grinding contact. We cover both SIMULATED collisions (controlled
strike rigs) and FIELD-OBSERVED collisions (injuries on fish passed
through real structures).

Scope. All 229 analysed papers were screened for collision relevance
(full-text density of blade-strike / strike / collision / impact /
leading-edge terms plus title screening); 48 collision-relevant papers
were retained. Of these, 25 are live-fish studies — 10 controlled
simulated-strike experiments and 15 field-observed passage studies — and
these form the reproducibility assessment. The remaining 23
(strike-probability / CFD / DEM models, one biomimetic-sensor method,
reviews and a guideline) are catalogued for metric coverage but not
scored.

# 2\. The collision evidence base

| **Role**                                          | **Papers** | **What it provides**                                                                    |
| ------------------------------------------------- | ---------- | --------------------------------------------------------------------------------------- |
| Live-fish SIMULATED (strike rig)                  | 10         | Controlled dose-response between strike velocity/geometry/location and injury/mortality |
| Live-fish FIELD (real-structure passage)          | 15         | Collision/strike injuries & survival of fish passed through turbines/screws/structures  |
| Modeling (strike-probability, CFD, DEM, particle) | \~17       | Predicted contact likelihood and exposure (no live fish)                                |
| Reviews / method / guideline                      | \~6        | Synthesis of strike mechanisms, leading-edge design, and a VLH guideline                |

Two centres of gravity dominate the live-fish base: the Oak Ridge
National Laboratory strike-rig programme (Bevelhimer, Saylor, Pracheil)
for controlled simulated strikes, and the Alden Research Laboratory /
Natel and European field programmes (Amaral; Mueller/Geist; Normandeau;
Pauwels; Knott) for field-observed passage. Strike-probability modelling
has a long lineage (Deng, Ploskey, Ferguson) now extended by CFD/DEM
particle methods (Richmond; Romero-Gomez).

# 3\. Collision metrics and how they are calculated

The workbook's 'Metrics catalogue' gives the full list; the essentials:

| **Metric**                    | **Calculation**                                                                       | **Notes**                                                               |
| ----------------------------- | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Strike probability            | Geometric/kinematic model: f(fish length, blade number, runner speed, axial velocity) | Assumes arrival timing & orientation; ignores active avoidance          |
| Strike velocity               | Rig velocity (lab) or blade velocity at strike radius (field/CFD)                     | Lab single velocity vs a real runner's velocity distribution            |
| Blade/leading-edge geometry   | Blade thickness t; length-to-thickness ratio L/t; slant angle                         | 'Blunt/slanted is safer' holds within tested ranges; location-dependent |
| Strike location & orientation | Controlled placement (lab); observed injury region (field)                            | head/mid/tail; lateral/dorsal/ventral                                   |
| Mutilation / strike mortality | injured-or-dead / exposed, per condition                                              | Immediate vs delayed; live-vs-euthanized effects                        |
| Modeled collision probability | Lagrangian particle / discrete-element contact count through CFD field                | Particles lack behaviour/size/orientation; little field validation      |
| Strike dose-response          | Logistic P(mortal) \~ strike velocity x length (+ thickness)                          | Model form & 'mortal' definition vary; weak cross-species transfer      |

Verified quantitative landmarks (sources read directly): blade strike
often the primary turbine-kill mechanism, with roughly 3-30% of passing
fish killed depending on fish length and turbine design (Amaral & Hecker
2011); slanted, blunt leading edges raise survival dramatically — 98% vs
26.8% survival at a 30 deg vs 90 deg slant for rainbow trout struck at
10 m/s (Amaral 2020); mortality is highest for midbody strikes and
lateral orientation, and increases with strike velocity and thinner
blades (Bevelhimer 2019); body shape governs vulnerability —
anguilliform American eel resist strike whereas laterally-compressed
bluegill do not (Saylor 2019); salmonid surrogacy for untested species
is unreliable (Saylor 2020); at a Very Low Head turbine only 1.16% of
entrained fish were killed by strike (Tuononen 2020); and a novel thick,
slanted runner improved white-sturgeon blade-strike survival over a
conventional runner (Zillig 2025).

# 4\. Protocols used

## 4.1 Simulated strike (laboratory)

Live fish are subjected to a single controlled blade strike on a
mechanical rig (pneumatic/servo-driven blade analogue) at a set
velocity, blade thickness/leading-edge geometry, and strike
location/orientation, then held and assessed for injury and delayed
mortality. The Oak Ridge programme standardised this design and added a
gelatin biomimetic 'fish' with an embedded accelerometer to link impact
force to live-fish dose-response (Saylor 2021). Leading-edge design
studies (Amaral 2011, 2020; Wood 2021) vary blade thickness and slant to
quantify survival gains.

## 4.2 Field-observed collision (real-structure passage)

Live fish are passed through a turbine, pump, or Archimedean screw and
recovered (balloon-tag/HI-Z, netting, telemetry), with collision/strike
injuries identified among other injuries by external exam, necropsy, or
X-ray, against handling/tag (and sometimes live-vs-euthanized) controls.
Examples span Kaplan/Francis turbines (Normandeau; Dauble), Archimedean
screws (Brackley; Pauwels), compact and novel fish-friendly turbines
(Watson; Zillig), VLH turbines (Tuononen), and shaft hydropower (Knott).

# 5\. Reproducibility assessment

Method. Each of the 25 live-fish studies was scored against a 10-element
collision reporting checklist (C1-C10; see workbook 'Legend'). Score =
reported / 10; tiers High (\>=80%), Medium (50-79%), Low (\<50%). All
ten criteria apply to both simulated and field studies (field studies
report turbine/operating conditions in place of rig velocity/geometry).

Results. Mean reporting completeness was 81% (median 80%) — somewhat
higher than for barotrauma (74%). Tiers: 20 High, 4 Medium, 1 Low.
Simulated-strike studies (10): 8 High / 2 Medium. Field studies (15): 12
High / 2 Medium / 1 Low. Criterion-by-criterion reporting:

| **Reporting element**                          | **Reported** | **Status** |
| ---------------------------------------------- | ------------ | ---------- |
| C1 Species + life stage + body size            | 96%          | Strong     |
| C3 Strike velocity / operating condition       | 96%          | Strong     |
| C4 Impactor geometry / structure               | 96%          | Strong     |
| C5 Strike location / orientation               | 88%          | Strong     |
| C8 Holding / recovery & delayed mortality      | 84%          | Strong     |
| C9 Controls (handling/tag; live-vs-euthanized) | 84%          | Strong     |
| C2 Sample size (n) per treatment               | 80%          | Adequate   |
| C7 Injury-scoring protocol                     | 64%          | Gap        |
| C10 Statistical / dose-response model          | 64%          | Gap        |
| C6 Collision metric explicitly defined         | 60%          | Major gap  |

Collision studies report the physical strike conditions (velocity,
geometry, location) well, but four in ten do not explicitly define a
collision metric, and a third under-report the injury-scoring protocol
and the statistical model — limiting cross-study synthesis.

# 6\. Major problems & gaps

1.  Collision metric is often implicit. Only 60% explicitly define a
    metric (strike probability, L/t, strike-velocity threshold,
    mutilation index), so 'strike injury' is reported in incomparable
    ways across studies.

2.  No standardized injury taxonomy or strike-location scheme. Injury
    scoring (C7, 64%) and body-region/orientation conventions differ
    between labs, so 'mortal strike' is not comparable.

3.  Lab single-velocity strikes vs real velocity distributions. Rigs
    deliver one controlled strike; a real runner imposes a distribution
    of velocities, locations and probabilities. Few studies bridge rig
    dose-response to in-turbine strike-probability distributions.

4.  Strike-probability models rest on strong, rarely-validated
    assumptions. Random arrival/orientation and no active avoidance are
    standard; CFD/DEM particle models add geometric realism but treat
    fish as inert particles with little field validation.

5.  Surrogacy and morphology are under-controlled. Body shape and length
    drive strike outcome, yet salmonid surrogates are widely reused for
    untested, differently-shaped species (Saylor 2020; Saylor 2019).

6.  Field studies cannot isolate collision. Field injuries blend strike
    with barotrauma, shear and grinding; without paired exposure data,
    the collision-specific signal is uncertain.

7.  Statistics/dose-response under-reported (64%), and
    immediate-vs-delayed mortality and live-vs-euthanized handling are
    treated unevenly (Brackley 2018 shows euthanized fish can misstate
    live outcomes).

8.  Non-turbine and non-blade collisions are thin. Impeller, screw,
    wall/draft-tube and plunge-pool impacts are far less studied than
    Kaplan/Francis blade strike.

# 7\. Recommendations & next steps for the community

## 7.1 Adopt a minimum reporting standard for collision studies

| **\#** | **Required element**                                                                                            | **Why**                                                  |
| ------ | --------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| 1      | Species, life stage, and body size (length & mass, ranges)                                                      | Length & body shape drive strike probability and outcome |
| 2      | Strike/impact velocity (lab) or runner speed + operating point (field), with the strike radius                  | Velocity is the primary dose                             |
| 3      | Impactor geometry: blade thickness, leading-edge shape/slant (lab) or runner type/diameter/blade number (field) | Geometry governs injury at a given velocity              |
| 4      | Strike location AND orientation (controlled or observed), by a defined body-region scheme                       | Outcome is location-dependent                            |
| 5      | Explicit collision metric with formula (e.g. strike probability; L/t; mutilation index)                         | Ends incomparable reporting                              |
| 6      | Standard injury taxonomy + scoring method (necropsy/X-ray/observation), with observer blinding                  | Comparable injury data                                   |
| 7      | Sample size per treatment and the full treatment matrix                                                         | Power and re-analysis                                    |
| 8      | Holding/recovery conditions and delayed-mortality window (e.g. 48-96 h)                                         | Separates immediate from latent mortality                |
| 9      | Controls: handling/tag/sham AND, where relevant, live-vs-euthanized                                             | Removes confounds                                        |
| 10     | Statistical model / dose-response form, with open data and code                                                 | Reproducible inference                                   |

## 7.2 Standardize the core conventions

  - Agree a common strike-injury taxonomy and a body-region/orientation
    scheme shared with the barotrauma injury catalogue.

  - Report strike VELOCITY DISTRIBUTIONS (and strike probability), not
    just a single rig velocity, so lab dose-response maps onto real
    runners.

  - Define strike probability consistently and state its assumptions
    (arrival, orientation, avoidance).

## 7.3 Close the evidence gaps

  - Couple rig dose-response to CFD/DEM strike-probability distributions
    and validate against field passage at matched conditions.

  - Test morphologically diverse, non-salmonid and non-temperate
    species; quantify the body-shape effect rather than assuming
    surrogacy.

  - Extend beyond Kaplan/Francis blade strike to impeller,
    Archimedean-screw, structure and plunge-pool impacts.

  - Move particle/DEM models toward behaviourally-informed fish
    representations, and report validation against live-fish strike
    data.

  - Standardize live-vs-euthanized and tag-control practice, and always
    report delayed mortality.

*Method note: the 48-paper collision set and per-criterion scores were
produced by full-text screening and automated detection of reporting
elements, then reviewed. Quantitative landmarks attributed to a named
study were read from that source. Reproducibility tiers index reporting
completeness, not scientific quality; Low/Medium ratings should prompt a
look at the paper (extraction gaps can miss reported items in older or
non-English papers).*
