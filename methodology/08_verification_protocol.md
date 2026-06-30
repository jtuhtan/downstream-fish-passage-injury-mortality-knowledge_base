# 8. Verification protocol (confirming data against the source PDFs)

Every row in `data/extraction.csv` carries a `Confidence` flag:

- **Mined** — populated automatically by `scripts/extract_passage_data.py`
  (`pdftotext` + controlled-vocabulary regex). Fast, broad, **unchecked**.
- **Verified** — a person opened the original PDF and confirmed (or corrected)
  the row field-by-field using the offline verification tool.

This document defines how a row becomes Verified so the process is consistent and
repeatable by anyone.

## Status

As of v0.11.0 **all rows are `Mined`**. Earlier ad-hoc verification flags were
reset because they predate this formal, PDF-in-hand protocol. Rows become Verified
only by running the tool below.

## Tool

`tools/verification/verify.py` — an offline, dependency-free local web app
(see [`tools/verification/README.md`](../tools/verification/README.md)). It runs on
the verifier's own machine because it needs the local PDF library (PDFs are never
committed). It displays the PDF beside an editable form of every field and writes
results back to the CSVs.

## Procedure (per paper)

1. Open the next `Mined` row; read its PDF.
2. Check each field against the paper and apply the field rules below: leave it if
   correct, correct it if wrong, blank it if the paper does not support it.
3. Choose an outcome:
   - **Verified** — the row now faithfully reflects the paper. Sets
     `Confidence = Verified`.
   - **Flag uncertain** — the paper cannot confirm the row (e.g. it is an abstract,
     a non-primary source, or the detail is genuinely absent). The row stays
     `Mined`; record why in the note.
4. The tool logs `citation_key, verifier, date, action, fields_changed` to
   `data/verification_log.csv` (append-only provenance).

## Field rules (what "confirmed" means)

- **Only what the paper itself reports.** Do not infer from other papers, the
  abstract of a citing work, or domain knowledge. If it isn't in this PDF, it isn't
  verified.
- **Mechanism(s)** — the injury mechanism(s) the study actually investigates
  (controlled vocabulary in `data/vocab/mechanisms.csv`), not every mechanism it
  mentions in the introduction.
- **Species / Life stage / Fish size** — as tested; use scientific names where the
  paper does; keep size units as reported (mm/cm, g).
- **Thresholds/metrics** — exact numeric values and units as stated (e.g. ratio of
  pressure change, log10 ratio, kPa, strain rate s⁻¹). Copy the number, don't round.
- **Mortality/survival** — the headline outcome with its denominator/conditions.
- **Sample size (n=)** — the number of live fish (or model runs) actually used.
- **Turbine/structure** — the device/structure studied (Kaplan, bulb, screw,
  barochamber, jet/flume, spillway, etc.).
- **Methodology** — lab / field / numerical and the essential setup.
- **Outcome summary** — one neutral sentence of what the study concluded.
- **Notes** — caveats, ambiguities, page references.
- Leave a field **blank** rather than guess; blank-but-verified is information.

## After a session

Regenerate derived artefacts so everything stays consistent:

```
python scripts/build_outputs.py     # outputs/ workbooks + reports
python scripts/build_dashboard.py   # docs/index.html (Verified count updates)
```

Commit `data/extraction.csv`, `data/verification_log.csv`, and the regenerated
`outputs/` and `docs/` files together, with a message noting how many rows were
verified.

## Scope note

This protocol governs the per-paper extraction in `extraction.csv`. The
cross-cutting axes (`axes_exposure_timing.csv`) carry their own confidence flag and
are out of scope here; if they need the same PDF-in-hand treatment, extend this
protocol rather than inventing a parallel one.
