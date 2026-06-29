---
name: passage-injury-mortality-review
description: >-
  Systematically review and extract structured data from fish-passage
  injury-and-mortality literature (downstream passage through hydropower
  turbines, pumps, screws, weirs, spillways and bypasses). Use this skill
  WHENEVER the user wants to scan, screen, synthesize, or compare a body of
  passage / barotrauma / blade-strike / shear / turbine-mortality papers, build
  a literature-extraction spreadsheet, map mechanisms-thresholds-species-life
  stages-fish sizes-study parameters, or write a state-of-the-art synthesis of
  what is known about fish injury and mortality during passage. Trigger even
  when the user only says things like "organize these turbine fish papers",
  "what are the barotrauma thresholds", "compare blade-strike studies", "make a
  review matrix of these PDFs", or "summarize the state of the art on passage
  mortality".
---

# Passage literature review — injury & mortality

## What this skill is for

Researchers studying downstream fish passage accumulate large, messy PDF
libraries. The questions they actually need answered are comparative and
cross-cutting: *Which injury mechanism does each study address? What thresholds
were reported, in what units? Which species, life stages and fish sizes were
tested? Was it a lab, field, or CFD study, and with what parameters and sample
sizes? What did it actually conclude about injury or mortality?*

This skill turns a folder of passage papers into (1) a **structured extraction
spreadsheet** (one row per study) and (2) a **state-of-the-art synthesis
report** organized by mechanism. It encodes the domain's vocabulary so the
extraction is consistent across hundreds of papers.

## When to use it

Use it whenever the user points at a set of passage / turbine-mortality /
barotrauma / blade-strike / shear publications and wants them read, organized,
compared, or synthesized — whether they say "skill" or not. Also use it to
extend an existing extraction with newly added papers.

## Core workflow

Follow these steps. Steps 2–3 can be done with the bundled script for breadth,
then refined by reading the papers that matter most.

1. **Gather the corpus.** Identify the PDFs to review. If they are organized by
   study type (review / lab / field / numerical), record that — it is a useful
   column and a sanity check on the mined "methodology" field. Note that
   cloud-only files (e.g. OneDrive placeholders) must be downloaded locally
   before their text can be read.

2. **Mine structured fields (breadth).** Run
   `scripts/extract_passage_data.py <folder> -o extraction.csv`. It runs
   `pdftotext` on every PDF and applies the controlled vocabularies in
   `references/` to populate the schema columns. It is precision-leaning:
   categorical fields (mechanism, species, life stage, structure) are detected
   from the title + abstract + early text to avoid picking up everything that
   intros and reference lists happen to mention; numeric fields (pressure
   ratios, kPa, strain rate, mortality %, sample size, fish size) are mined from
   the full text. Treat the output as a high-quality first pass, not gospel.

3. **Curate the rows that matter (depth).** Open the key empirical papers
   (especially lab dose–response and field survival studies) and verify or
   correct: the *primary* mechanism, the exact threshold values and units, the
   tested species/stage/size, sample sizes, the headline injury/mortality
   result, and the study's main hypothesis/assumption. Mark each row's
   confidence (mined vs. verified). Read `references/extraction_workflow.md` for
   how to read a passage paper quickly and what to look for.

4. **Build the spreadsheet.** Use the `xlsx` skill. One row per study, columns
   per `references/schema.md`, plus a legend sheet explaining the controlled
   vocabularies. Freeze the header, enable filters, and keep list-valued cells
   semicolon-separated so they filter cleanly.

5. **Write the synthesis.** Use the structure in "Synthesis report structure"
   below. Ground every quantitative claim in specific rows; never invent
   thresholds. Where the literature disagrees (it often does — e.g. Boyle's-law
   vs. dynamic barotrauma models), present the disagreement rather than
   averaging it away.

## Reference files (read as needed)

- `references/mechanisms.md` — the injury-mechanism taxonomy with the physical
  cause, typical evidence, and how to recognize each in a paper.
- `references/metrics_thresholds.md` — the metrics and units used for each
  mechanism (ratio/log-ratio of pressure change, nadir pressure, strain rate,
  strike velocity/probability, TDG %), with reported threshold landmarks and the
  traps in comparing them.
- `references/schema.md` — the exact extraction columns, allowed values, and
  formatting conventions.
- `references/study_templates.md` — what parameters to capture for each study
  type (lab pressure-chamber, shear-flume, blade-strike rig; field
  survival/telemetry/Sensor Fish; CFD/numerical), and the assumptions each
  type tends to bake in.

## Synthesis report structure

ALWAYS use this template so successive reviews stay comparable:

```
# Fish passage injury & mortality — state of the art
## Scope & corpus (n papers, date range, study-type mix)
## Injury mechanisms (one subsection each)
   - definition & physical cause
   - what the studies tested and found
   - reported thresholds (table: metric, value, species/stage, source)
   - agreements, disagreements, open questions
## Cross-cutting findings
   - species & life-stage sensitivity (who is most vulnerable, and why)
   - fish-size effects
   - structure/turbine-type comparison
## Methods landscape (lab vs field vs CFD: strengths, blind spots, sample sizes)
## Key assumptions & where they are contested
## Research gaps & recommendations
```

## Principles

- **Mechanisms are the spine.** Injury/mortality during passage is driven by a
  small set of physical mechanisms (blade strike, barotrauma, shear,
  cavitation, turbulence, grinding, gas supersaturation, entrainment). Organize
  everything around them.
- **Thresholds are only comparable within a metric.** A "ratio of pressure
  change" is not a "nadir pressure"; a strain rate in s⁻¹ is not a shear stress.
  Keep units explicit and never compare across metrics silently.
- **Lab ≠ field ≠ CFD.** Each answers a different question and carries different
  assumptions (acclimation depth, neutral buoyancy, surrogacy, idealized
  geometry). Capture the study type and its parameters, not just the result.
- **Preserve disagreement.** This is an active field; surfacing contested
  assumptions is more useful than a false consensus.
