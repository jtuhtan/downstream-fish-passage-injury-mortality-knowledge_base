**Fluid Shear & Strain-Rate Injury in Downstream Fish Passage  
Metrics, Protocols & the Reproducibility of Live-Fish Studies**

*A state-of-the-art assessment of 36 shear papers (12 live-fish studies
scored)  
Companion to the workbook 'Shear\_metrics\_reproducibility.xlsx'*

# 1\. Purpose & scope

Fluid shear — injury caused by steep velocity gradients rather than by
impact or pressure change — is the third major downstream-passage injury
mechanism alongside collision and barotrauma. Where two adjacent parcels
of water move at very different speeds (the boundary of a submerged jet,
a draft-tube shear layer, a spillway plunge), a fish spanning that
gradient is stretched, its eyes, opercula and gills torn. This document
and its companion workbook catalogue the shear metrics in use and how
each is calculated, describe the protocols used to generate shear data
on live fish, and assess how reproducible that evidence base is, before
identifying gaps and next steps.

Definition. We treat shear as fluid-shear / strain-rate injury, indexed
primarily by the STRAIN RATE (s^-1). Turbulence is the closely-related
exposure and is included where studies link it to injury or behaviour.
Shear is distinct from blade-strike collision and from pressure-change
barotrauma.

Scope. All 228 analysed papers were screened for shear relevance
(full-text density of shear / strain-rate / turbulence / jet /
shear-stress terms plus title screening); 36 shear-relevant papers were
retained. Of these, 12 are live-fish studies, all controlled laboratory
jet/flume experiments, and these form the reproducibility assessment.
The remaining 24 (CFD shear-field models, Sensor-Fish field exposure,
reviews and guidelines) are catalogued for metric coverage but not
scored.

# 2\. The shear evidence base — small and lab-bound

| **Role**                                          | **Papers** | **What it provides**                                                             |
| ------------------------------------------------- | ---------- | -------------------------------------------------------------------------------- |
| Live-fish SIMULATED (lab jet/flume)               | 12         | Controlled dose-response between strain rate / jet velocity and injury/mortality |
| Field exposure (Sensor Fish, no live-fish injury) | \~5        | Measured shear EXPOSURE during real passage (not isolated injury)                |
| Modeling (CFD shear field)                        | \~11       | Predicted shear-stress / strain-rate fields (no live fish)                       |
| Reviews / guidelines                              | \~8        | Synthesis of shear injury and adopted thresholds                                 |

The single most important structural finding is that the live-fish shear
evidence base is small and almost entirely a LABORATORY product,
dominated by one apparatus and lineage: the Pacific Northwest National
Laboratory submerged-jet programme (Neitzel, Deng, Richmond, Colotelo,
Pflugrath) and a few Alden/hydrokinetic flume studies (Jacobsen; Doyle).
There is effectively NO field live-fish shear set: in the field, shear
is measured as EXPOSURE with Sensor Fish, but live-fish injury cannot be
attributed to shear in isolation because real passage mixes shear with
strike, barotrauma and turbulence.

# 3\. Shear metrics and how they are calculated

The workbook's 'Metrics catalogue' gives the full list; the essentials:

| **Metric**                           | **Calculation**                                                                           | **Notes**                                                                                            |
| ------------------------------------ | ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Strain rate                          | Mean velocity gradient dU/dy across the shear layer (from nozzle velocity & jet geometry) | Primary dose; value depends on the length scale and where computed - not comparable across apparatus |
| Jet / nozzle velocity                | Set exit velocity into still water (e.g. 6.35-cm jet, 3-22.9 m/s)                         | Velocity is not strain rate; geometry-specific                                                       |
| Shear stress                         | tau = mu x (dU/dy)                                                                        | Often CONFLATED with strain rate; a different quantity (Pa)                                          |
| Acceleration                         | Motion-tracked or Sensor-Fish accelerometer                                               | Best predictor of eye/opercle injury in Deng 2005; links lab & field                                 |
| No-observed-effect / onset threshold | Lowest strain rate (or velocity) at which an injury class appears                         | Apparatus- and definition-specific                                                                   |
| Injury-specific dose-response        | Logistic P(injury) \~ strain rate/velocity                                                | Injury taxonomies differ between labs                                                                |

Verified quantitative landmarks (sources read directly): juvenile
Chinook (93-128 mm) in a 6.35-cm submerged jet showed onset of minor /
major / fatal injury at nozzle velocities of 12.2 / 13.7 / 16.8 m/s,
with opercle injury appearing at \~12.2 m/s and eye injury and loss of
equilibrium at \>=16.8 m/s; whole-body acceleration predicted injury
better than velocity (Deng 2005). In a later submerged-jet study, minor
and major injury onset occurred at \~15.2 and \~21.3 m/s (Deng 2010).
Two Mekong species were injured at strain rates up to \~1185 s^-1,
gouramis being more susceptible than iridescent sharks (Colotelo 2018).
American eel showed NO injury at severe shear (strain rate \>800 s^-1),
confirming eel resilience and pointing to strike/grinding rather than
shear as their main turbine risk (Pflugrath 2021). The PNNL programme
established strain rate as the standard exposure index and the
submerged-jet apparatus subsequently reused across these studies
(Neitzel 2000, 2004).

# 4\. Protocols used

## 4.1 Simulated shear (laboratory jet / flume)

The dominant design introduces a live fish into a submerged,
high-velocity water jet entering still water (or a controlled flume
shear layer), at a set nozzle velocity from which a strain rate is
computed, with the fish's introduction orientation (head- vs tail-first)
controlled, then holds and examines the fish for shear-typical injuries
- eye injury, operculum damage, gill damage, bruising, and loss of
equilibrium - against a low-velocity reference control. High-speed video
and motion tracking (Deng 2005) link kinematics (acceleration) to
injury. Variants include hydrokinetic flume studies (Jacobsen 2012) and
multi-stressor pumped-storage simulations that include a shear component
(Doyle 2020, 2022).

## 4.2 Field exposure (not live-fish injury)

In the field, shear is characterised as EXPOSURE using autonomous Sensor
Fish that record acceleration and pressure during real passage (Boys
2018; Martinez 2019, 2020; Fu 2016). These quantify the physical shear
environment and feed CFD/biological-response models, but they do not
measure live-fish shear injury and so are not part of the
reproducibility scoring.

# 5\. Reproducibility assessment

Method. Each live-fish shear study was scored against a 10-element shear
reporting checklist (C1-C10; see workbook 'Legend'). Score = reported /
10; tiers High (\>=80%), Medium (50-79%), Low (\<50%).

Results. Among the 11 machine-readable studies, mean reporting
completeness was 94% (11 High; one further study, Neitzel 2004, is a
scanned PDF with no extractable text and could not be machine-assessed -
shown as Low and flagged for manual scoring). This is the highest of the
three mechanisms assessed (barotrauma 74%, collision 81%, shear 94%).
Criterion reporting:

| **Reporting element**                           | **Reported** | **Status** |
| ----------------------------------------------- | ------------ | ---------- |
| C1 Species + life stage + size                  | 100%         | Strong     |
| C3 Exposure quantified (velocity / strain rate) | 100%         | Strong     |
| C4 Shear-field characterization                 | 100%         | Strong     |
| C5 Introduction orientation / entry             | 100%         | Strong     |
| C6 Shear metric explicitly defined              | 100%         | Strong     |
| C8 Holding/recovery & delayed mortality         | 100%         | Strong     |
| C7 Injury-scoring protocol                      | 91%          | Strong     |
| C10 Statistical / dose-response                 | 91%          | Strong     |
| C9 Controls (reference / low-velocity)          | 82%          | Adequate   |
| C2 Sample size (n) per treatment                | 73%          | Gap        |

The shear literature reports its methods unusually well - because it is
small, recent, and methodologically homogeneous (one apparatus, one core
lineage). High internal reproducibility here is therefore a double-edged
result: the studies are individually replicable, but the base is narrow
and inbred.

# 6\. Major problems & gaps

1.  Strain rate is apparatus-specific and not standardized. Its value
    depends on the length scale and the point at which dU/dy is
    evaluated; reported strain rates are not directly comparable between
    the submerged-jet apparatus and other geometries, and almost never
    to real turbine shear fields.

2.  Shear stress and strain rate are conflated. CFD studies report shear
    STRESS (Pa) while live-fish studies report strain RATE (s^-1); the
    two are routinely treated as interchangeable in secondary literature
    though they are different quantities.

3.  The evidence base is narrow and lab-inbred. Twelve studies,
    dominated by one apparatus and one laboratory lineage, with few
    species and almost no eggs/larvae - so external (independent)
    reproducibility is essentially untested.

4.  No field live-fish shear evidence. Field work measures exposure
    (Sensor Fish) but cannot isolate live-fish shear injury, leaving the
    lab-to-field transfer of strain-rate thresholds unvalidated.

5.  Injury taxonomy and severity are not standardized across labs, and
    sample sizes are under-reported (73%).

6.  Mechanistic linkage is weak. Whether strain rate, shear stress, or
    acceleration is the true injury driver remains unsettled (Deng 2005
    favoured acceleration), yet most studies report only one.

7.  Old foundational work is hard to reuse. Key early reports (e.g.
    Neitzel 2004) survive only as scanned PDFs, impeding re-analysis.

# 7\. Recommendations & next steps for the community

## 7.1 Adopt a minimum reporting standard for shear studies

| **\#** | **Required element**                                                          | **Why**                                                                   |
| ------ | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| 1      | Species, life stage, and body size (length & mass, ranges)                    | Body length relative to the gradient governs exposure                     |
| 2      | Nozzle/flume geometry AND nozzle exit velocity                                | Defines the shear field; enables replication                              |
| 3      | Strain rate WITH the length scale and the location/method of computation      | Makes strain rate comparable between studies                              |
| 4      | Both strain rate (s^-1) and shear stress (Pa) where possible, kept distinct   | Ends conflation; enables CFD linkage                                      |
| 5      | Introduction orientation and entry point                                      | Outcome is orientation-dependent                                          |
| 6      | Standard shear-injury taxonomy (eye/operculum/gill/bruising) + scoring method | Comparable injury data                                                    |
| 7      | Sample size per treatment and the full velocity/strain-rate matrix            | Power and re-analysis                                                     |
| 8      | Holding/recovery conditions and delayed-mortality window                      | Separates immediate from latent mortality                                 |
| 9      | Low-velocity reference control                                                | Removes handling confounds                                                |
| 10     | Dose-response model + open data (incl. high-speed kinematics where used)      | Reproducible inference; resolves the strain-rate vs acceleration question |

## 7.2 Standardize the core conventions

  - Define and report strain rate with an explicit length scale (ideally
    fish-body scale) so values transfer between apparatus.

  - Always distinguish strain rate (s^-1) from shear stress (Pa); report
    both where feasible to link live-fish dose-response to CFD shear
    fields.

  - Agree a shear-injury taxonomy shared with the barotrauma and
    collision injury catalogues.

## 7.3 Close the evidence gaps

  - Broaden beyond salmonids and a single apparatus: test more species
    and life stages (especially eggs/larvae) and run cross-laboratory
    ring tests to measure external reproducibility.

  - Validate lab strain-rate thresholds against field exposure by
    coupling Sensor-Fish-measured shear fields to live-fish
    dose-response at matched conditions.

  - Resolve the injury-driver question (strain rate vs shear stress vs
    acceleration) with studies that report all three.

  - Digitise/OCR foundational scanned reports (e.g. Neitzel 2004) so the
    historical dose-response data can be re-analysed.

*Method note: the 36-paper shear set and per-criterion scores were
produced by full-text screening and automated detection of reporting
elements, then reviewed. Quantitative landmarks attributed to a named
study were read from that source. Reproducibility tiers index reporting
completeness, not scientific quality; one scanned study could not be
machine-assessed and is flagged for manual scoring.*
