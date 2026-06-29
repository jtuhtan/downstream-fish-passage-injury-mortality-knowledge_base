**Fish Passage Injury & Mortality  
State of the Art**

*A mechanism-based synthesis of a 229-paper downstream-passage library
(1928–2026)  
Quantitative claims verified against 37 key papers; see the extraction
spreadsheet ('Confidence' column)*

# 1\. Scope & corpus

This synthesis covers 229 publications on downstream fish passage and
the injury and mortality it causes — passage through hydropower
turbines, pumps, Archimedean screws, weirs, spillways, and
bypass/fish-friendly structures (1928–2026). Headline quantitative
claims below were checked against the original papers; 37 key empirical
studies are marked 'Verified' in the companion spreadsheet. Other cell
values remain text-mined first-pass estimates.

| **Study type** | **Papers** | **Contribution**                                                             |
| -------------- | ---------- | ---------------------------------------------------------------------------- |
| Lab            | 75         | Controlled dose–response: pressure chambers, shear flumes, blade-strike rigs |
| Field          | 55         | Real-structure survival, telemetry, Sensor Fish, ecological assessment       |
| Numerical      | 48         | CFD, blade-strike & particle models, BioPA / bio-hill charts                 |
| Review         | 38         | Syntheses, overviews, meta-analyses                                          |
| Guidelines     | 13         | Standards & criteria (NEN 8775, German/Austrian/Dutch/Canadian guidance)     |

Mechanism coverage is dominated by barotrauma and shear, with blade
strike close behind (counts exceed 229 because most studies address
several mechanisms): barotrauma/pressure 84; shear 70; blade strike 53;
turbulence 42; entrainment/impingement 26; cavitation 26; gas
supersaturation 11; grinding 11.

How big is the problem? The best single estimate is from a global
meta-analysis of \>275,000 fish across 75 species (Radinger & van Treeck
2021): average hydropower-turbine fish mortality of 22.3% (95% CI
17.5–26.7%) after correcting for handling/catch effects — but with
large variation among turbine types, methods and taxa. Older syntheses
put direct turbine kill at roughly 3–30% depending on fish length and
turbine design (Amaral & Hecker 2011).

# 2\. Injury mechanisms

## 2.1 Barotrauma (rapid decompression) — verified landmarks

Barotrauma is the most intensively studied mechanism. The rapid pressure
drop near the runner (the 'nadir') over-expands swim-bladder gas,
causing emboli, swim-bladder rupture, exophthalmia and internal
haemorrhage. Susceptibility depends on the change relative to
acclimation, captured by the Ratio of Pressure Change (RPC = acclimation
pressure ÷ nadir) and its log form (LRP). The PNNL programme (Brown,
Carlson, Pflugrath, Stephenson, Colotelo) established 'simulated turbine
passage' in hyper/hypobaric chambers; Brown et al. (2012) showed injury
is driven mainly by Boyle's-law gas expansion rather than Henry's-law
gas exsolution, and McKinstry et al. (2007) replaced raw mortality with
a 'mortal injury' endpoint.

| **Metric / question**                    | **Verified value**                                                                        | **Source**            |
| ---------------------------------------- | ----------------------------------------------------------------------------------------- | --------------------- |
| Acclimation depth ceiling (juv. Chinook) | Neutral buoyancy only to \~4.6–11.6 m; deeper = higher risk                               | Pflugrath 2012        |
| Precautionary pressure threshold         | Keep exposure pressure ≥ \~70% of acclimation pressure (Murray cod, silver perch)         | Boys 2016 (piecewise) |
| Eggs & larvae                            | Highly vulnerable; injuries near 100% at low pressure; keep ≥ \~40% surface pressure      | Boys 2016 (How low)   |
| RPC dose–response (Neotropical)          | 50% swim-bladder rupture at RPC ≈ 1.75 (pacu) – 2.2 (piracanjuba)                         | Kerr 2023             |
| Lamprey tolerance                        | No injury at 146.2→13.8 kPa, where \~97.5% of juv. Chinook would be injured/killed        | Colotelo 2012         |
| American eel tolerance                   | Resilient at 172 kPa acclimation; barotrauma not a major concern                          | Pflugrath 2019        |
| Tag effect                               | Tag presence + LRP are the strongest predictors of mortal injury (tags inflate mortality) | Carlson 2012          |

Two important nuances. First, the field's workhorse assumption — that
barotrauma follows the static Boyle's law — has been directly
challenged: Kerr et al. (2023) show a dynamic (Modified
Rayleigh–Plesset) model diverges from Boyle's law near zero nadir
pressure and under liquid tension, implying static chamber thresholds
can mis-state real risk. Second, the common shorthand that 'physostomes
(open swim bladder) are more tolerant' holds for eel and lamprey but is
not universal: Zitek et al. (2026) found physostomous cypriniform larvae
and juveniles among the most barotrauma-sensitive groups tested, and
observed lower mortality under partial-load operation. Susceptibility is
therefore species- AND life-stage-specific, not reducible to bladder
type alone.

## 2.2 Fluid shear — verified landmarks

Shear injury arises where steep velocity gradients (shear layers, jets,
draft tubes, spillway plunge) tear at body surface, eyes, opercula and
gills. The exposure metric is the strain rate (s⁻¹), operationalised in
the PNNL submerged-jet apparatus (Neitzel 2000). Injury severity rises
with jet velocity / strain rate and with fish size and orientation; eye
and operculum injuries appear first, and acceleration predicts injury
better than velocity alone.

| **Finding**                              | **Verified value**                                                          | **Source**     |
| ---------------------------------------- | --------------------------------------------------------------------------- | -------------- |
| Injury onset (juv. Chinook, 93–128 mm)   | Opercle injury \~12.2 m/s; eye injury/equilibrium loss ≥16.8 m/s jet        | Deng 2005      |
| Minor/major injury onset (submerged jet) | Minor \~15.2 m/s; major \~21.3 m/s                                          | Deng 2010      |
| Mekong species                           | Injury rose with strain rate to \~1185 s⁻¹; gourami \> shark susceptibility | Colotelo 2018  |
| American eel                             | No injury at strain rate \>800 s⁻¹ (immediate or 48 h) — shear-resistant    | Pflugrath 2021 |

Comparison trap: strain rate (s⁻¹) is not shear stress (Pa); the two are
frequently conflated in secondary literature.

## 2.3 Blade strike — verified landmarks

Blade strike is direct mechanical impact by a runner blade. Mortality
rises with strike velocity, fish length, thinner blades, and strike
location/orientation; engineering responses (blunt, slanted leading
edges) reduce it.

| **Finding**                                   | **Verified value**                                                                            | **Source**       |
| --------------------------------------------- | --------------------------------------------------------------------------------------------- | ---------------- |
| Strike severity drivers                       | Midbody \> head \> tail; lateral \> dorsal/ventral; thinner blades & higher velocity worse    | Bevelheimer 2019 |
| Leading-edge geometry (rainbow trout, 10 m/s) | 98% survival at 30° slant vs 26.8% at 90° (L/t=2); 200-mm fish 68% vs 7.9% by strike location | Amaral 2020      |
| Body shape                                    | Anguilliform eel resists strike; laterally-compressed bluegill highly susceptible             | Saylor 2019      |
| Surrogacy                                     | Salmonid surrogacy for untested species is unreliable; size & morphology matter               | Saylor 2020      |
| Novel runner (white sturgeon)                 | Higher survival through a thick, slanted fish-friendly runner vs conventional                 | Zillig 2025      |
| Overall                                       | Blade strike often the primary kill mechanism (3–30%); blunter/slower = safer                 | Amaral 2011      |

## 2.4 Turbulence, cavitation, grinding, gas supersaturation

  - Turbulence — disorients fish and increases strike/shear exposure;
    usually studied with shear/behaviour (Cada; Odeh).

  - Cavitation — vapour-bubble collapse; in this corpus mostly
    turbine-engineering (Avellan; Escaler) rather than direct fish
    injury.

  - Grinding / abrasion / pinch — fish crushed in narrow gaps
    (runner–hub, screw–trough); for American eel, the likely dominant
    injury route alongside strike (Pflugrath 2021).

  - Gas supersaturation / GBT — total dissolved gas from spillway
    plunge; distinct from barotrauma; depth modulates the effect
    (Morris; Watson).

# 3\. Cross-cutting findings

## 3.1 Species & life-stage sensitivity

The evidence base is salmonid-centric: juvenile Chinook and rainbow
trout/steelhead dominate (Chinook 57 studies, rainbow 34), with Atlantic
salmon, American shad and European/American eel well represented.
Tolerance ordering is mechanism-specific: eel and lamprey are highly
barotrauma- and (for eel) shear-tolerant (Colotelo 2012; Pflugrath 2019,
2021), yet eel remain vulnerable to blade strike and grinding. The
blanket 'physostomes are tolerant' rule fails for cypriniform
larvae/juveniles, which Zitek (2026) found highly sensitive. Juveniles
are by far the most-tested stage (74 studies); eggs and larvae (Boys
2016) are under-studied despite high vulnerability.

## 3.2 Fish size

Larger fish face higher blade-strike probability and mortality (length
relative to blade spacing; Amaral 2020, Bevelheimer 2019), while
barotrauma scales with swim-bladder physiology and acclimation rather
than length. Interpret size mechanism-by-mechanism, not as a single
vulnerability axis.

## 3.3 Structure / turbine type

Kaplan turbines are the most-studied structure (62 studies), then
spillways (44), Francis (40) and pumps (38). Field comparisons show
conventional Kaplan plants can be most harmful (up to \~83% mortality;
Mueller 2022), whereas Very Low Head turbines (Tuononen 2020: only 1.16%
of entrained fish killed) and purpose-built fish-friendly runners
(Zillig 2025; Watson) are markedly safer. Small, well-bypassed projects
can reach 77–97% total passage survival (Amaral 2018). Pumps/pumping
stations form a distinct sub-literature where strike and shear dominate
over barotrauma (van Esch; Pan; Bierschenk).

# 4\. Methods landscape

| **Approach**                                   | **Strength**                                             | **Blind spot / assumption**                                                       |
| ---------------------------------------------- | -------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Lab (chamber / flume / strike rig)             | Clean dose–response for one mechanism                    | Single-mechanism; assumes acclimation/neutral buoyancy; apparatus ≈ real turbine  |
| Field (mark–recapture, telemetry, Sensor Fish) | Integrates all mechanisms at a real structure            | Tag/handling burden (Carlson 2012); immediate vs delayed; representativeness      |
| Numerical (CFD, blade-strike, BioPA)           | Maps the full exposure field; compares designs pre-build | Predicts exposure not biology unless coupled to dose–response; idealized geometry |

The integrative frontier couples CFD exposure distributions (pressure,
shear, strike) to lab dose–response via BioPA / bio-hill charts
(Richmond 2015; Romero-Gomez) and validates against field tests;
Tomanova (2023) updated Francis-turbine mortality formulae (peripheral
speed, diameter, fish size; r=0.89 vs observed). Sensor Fish and
balloon-tag recovery bridge lab and field by measuring the physical
exposure live fish experience.

# 5\. Key assumptions & where they are contested

  - Static Boyle's-law barotrauma vs dynamic decompression — challenged
    by Kerr (2023).

  - Neutral buoyancy at acclimation depth — standard, but wild fish at
    an intake may not be neutrally buoyant, changing RPC (Pflugrath
    2012).

  - Cross-species surrogacy — salmonid thresholds are widely reused but
    repeatedly shown not to transfer (Saylor 2020; Pflugrath 2018; Zitek
    2026).

  - Physostome tolerance as a rule — true for eel/lamprey, false for
    cypriniform larvae (Zitek 2026).

  - Sensor Fish / biomimetic ≈ live fish (Saylor 2021); CFD exposure ≈
    biological dose — only via a validated dose–response model.

  - Immediate ≈ total mortality — delayed (48–96 h) and tag effects can
    substantially change the number (Carlson 2012).

# 6\. Research gaps & recommendations

  - Broaden beyond salmonids: eggs/larvae, eels, lamprey, cyprinids and
    non-temperate species relative to their exposure.

  - Resolve Boyle's-law vs dynamic barotrauma with rate-varying (not
    just magnitude-varying) experiments.

  - Standardise reporting: pair every threshold with metric, units,
    species, life stage and acclimation depth (the extraction schema
    enforces this).

  - Strengthen CFD exposure-to-response coupling and independent field
    validation of BioPA/bio-hill predictions.

  - Quantify combined/sequential exposure (strike + shear + barotrauma)
    rather than single mechanisms.

  - Expand delayed-mortality and sub-lethal endpoints beyond immediate
    survival.

  - Build matched-condition comparisons of novel fish-friendly designs
    (VLH, screw, shaft, Natel/Alden runners) vs conventional turbines.

*Provenance: figures attributed to a named study above were read from
that paper and are marked 'Verified' in the extraction spreadsheet (37
studies). Corpus-level counts come from automated text mining of all 229
PDFs and should be treated as close estimates. Remaining unverified
cells in the spreadsheet (Confidence = 'Mined') should be checked before
citation.*
