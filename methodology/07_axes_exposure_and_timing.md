# 7. The three-axis framework: mechanism x exposure pathway x outcome timing

Each study is described along three orthogonal axes so it can be queried by
*what injures the fish*, *how/where it was exposed*, and *when/what kind of
outcome was measured*.

| Axis | Question | Where it lives |
|---|---|---|
| **Mechanism** | What physically injures the fish? | `data/extraction.csv` + per-mechanism registers |
| **Exposure pathway** | In what setting, and at what physical location, was the fish exposed? | `data/axes_exposure_timing.csv` |
| **Outcome timing** | When and in what form was the outcome measured? | `data/axes_exposure_timing.csv` |

Exposure pathway and outcome timing are **cross-cutting, per-study attributes**,
coded ONCE per study in a single join table keyed by `citation_key`, so a study
in several mechanism registers is never coded twice.

## Axis 2 - Exposure pathway (two fields)

The exposure pathway separates *the test setting* from *where the fish actually
was* when exposed - these are different questions and a study with one does not
imply the other.

### `study_environment` (controlled vocab: `data/vocab/study_environment.csv`)
The setting in which the study was conducted - the apparatus or the real
structure. Examples: **Lab - barotrauma chamber**, **Lab - shear jet/flume**,
**Lab - blade-strike rig**, **Physical model / test rig**, **Field - Kaplan
turbine**, **Field - pump / pumping station**, **Field - Archimedean screw**,
**Numerical / CFD model**, **Review / synthesis**, **Guideline / standard**.

### `location_during_passage` (controlled vocab: `data/vocab/location_during_passage.csv`)
The physical location at which the injurious exposure occurred. Multi-valued.
- **Lab apparatus** -> the exposure site: *Remained in barochamber*, *In shear
  jet/flume*, *At strike plate / blade (rig)*, *In lab apparatus (other)*.
- **Real structure / model** -> hydraulic-path component(s) in order: approach/
  forebay, intake, trash rack/screen, penstock, spiral/scroll case, stay vanes,
  wicket/guide gates, **turbine runner**, draft tube, tailrace; or spillway,
  plunge pool, bypass/sluice/gate, Archimedean-screw flight, pump impeller/casing.
- **Whole-route (not localised)** -> real passage where injury cannot be tied to
  a component (e.g. balloon-tag/recapture survival of whole-turbine passage). This
  is the honest default for most field live-fish survival studies.
- **Modelled flow path** / **Various / not applicable** -> models without a named
  component / reviews & guidelines.

Why two fields: `study_environment` tells you *what hardware or apparatus* the
result pertains to (and how controlled it is); `location_during_passage` tells
you *where in the machine* the injury arises - which is where mitigation is
applied. A barotrauma chamber and a large Kaplan turbine can study the same
mechanism (pressure), but the chamber's location is "remained in barochamber"
while the turbine's is "turbine runner / draft tube" - and only the latter
localises the real risk. CFD studies are the most localisable (they resolve
individual components); field live-fish survival studies are the least.

## Axis 3 - Outcome timing
Multi-valued (controlled vocab: `data/vocab/outcome_timing.csv`): **Immediate**
(<= ~1 h), **Delayed** (defined window; max recorded in `delayed_window_h`),
**Latent / long-term** (> ~1 week), **Sublethal** (injury/physiological/
behavioural), **Indirect** (e.g. post-passage predation), **Not reported**. A tag
means the study *reports or addresses* that outcome class, not that it is the
primary endpoint.

## How the axes are coded (repeatable)
1. **Scope.** Currently the union of the barotrauma, collision and shear
   registers (120 studies). New studies are coded when added.
2. **Automated first pass.** Controlled-vocabulary regex over the PDF text, with
   guards against introduction/reference noise: categorical fields are read from
   the **title + abstract/early text**; lab studies take an apparatus-based
   `study_environment`/`location`; field survival studies default to
   **Whole-route (not localised)** unless they target a specific component
   (spillway, screen/rack, bypass, screw, pump); `Indirect`/`Latent` timing tags
   fire only in an outcome context.
3. **Review.** Output is `confidence = Mined`; rows are spot-checked and flipped
   to `Verified`. Low-text (scanned) PDFs are flagged in `notes`.

## Known limitations
- Timing tags indicate coverage, not primacy, of an outcome class.
- `location_during_passage` for field live-fish survival is usually
  "Whole-route (not localised)" by design - real studies rarely localise injury.
- `study_environment`/`location` for reviews & models are coarse by nature.

## Extending
Add new studies to `data/axes_exposure_timing.csv` with the same vocab; when a
new mechanism module is added, its register's `citation_key`s are folded in so
every study carries all three axes.
