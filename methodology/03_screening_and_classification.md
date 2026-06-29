# 3. Screening & classification

## Study-type classification
Each paper is assigned one primary study type:
- **Review** — literature/systematic reviews, syntheses, frameworks.
- **Lab** — controlled experiments (pressure chamber, shear flume, blade-strike rig).
- **Field** — in-situ studies at real structures (survival, telemetry, Sensor Fish).
- **Numerical** — CFD, blade-strike/particle models, BioPA/bio-hill charts.
- **Guidelines** — standards/criteria (e.g. NEN 8775, agency guidance).
- **Misc** — presentations, datasets, tangential engineering, supplements.

Classification reads the title, abstract and methods (not the reference list,
which mentions everything). When automated, categorical fields are detected from
the title + early text to avoid reference-list noise.

## Mechanism tagging
Papers are tagged with one or more injury mechanisms from
`data/vocab/mechanisms.csv`. Tag what the study **measures**, not every mechanism
its introduction lists. Reviews and CFD papers legitimately span several.

## Topic screening (e.g. barotrauma)
For a focused sub-review, screen the whole corpus by full-text term density
(for barotrauma: `barotrauma`, `decompression`, `swim bladder`, `nadir`,
`RPC`/ratio-of-pressure-change) plus a title screen, then sub-classify the hits
(live-fish lab / live-fish field / modeling / review / guideline / foundational).
