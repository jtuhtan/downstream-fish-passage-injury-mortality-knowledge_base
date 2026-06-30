# Figure digitization — protocol & provenance

The most valuable relationships (dose–response curves) usually exist *only* as
figures. Extracting them is legitimate and high-value — but only if done
reproducibly, with provenance and error recorded. Hand-eyeballed points are not
acceptable.

## Tooling
Use a real digitizer, not estimation: **WebPlotDigitizer** (web/desktop) or the
Python `plotdigitizer`/`engauge` equivalents. The skill records *that* a figure was
digitized and stores the resulting points; the tool is the operator's choice but must
be named in the row.

## Protocol
1. **Identify** the figure and exactly what it plots: x = predictor (+ unit + scale),
   y = response (+ unit), and the series (species/condition) if multiple curves.
2. **Calibrate axes** from at least two labelled ticks per axis. **Respect log
   axes** — set the digitizer to log for any log-scaled axis (barotrauma RPC, strike
   probability, and shear figures are frequently log). Getting this wrong silently
   corrupts every point.
3. **Extract** each data series separately. Capture marker points; for a fitted line,
   sample enough points to reconstruct the curve, and also record the fitted equation
   if the paper gives one (→ `equations.csv`).
4. **Capture error bars** if present (as `response_uncertainty`).
5. **Sanity-check** against any value stated in the text (e.g. an LD50 in prose
   should match the curve). Mismatch → re-check calibration.

## Storage
- Save the extracted points to `data/figures/<citation_key>_fig<N>.csv` with columns:
  `series, x, x_unit, y, y_unit, y_err, x_scale(lin|log), notes`.
- Add a header comment recording: source `citation_key`, figure number, digitizer
  tool + version, who digitized, date, and the axis calibration points used.
- In `stressor_response.csv`, the relationship row(s) for this figure set
  `extraction_method = digitized_figure` and `digitized_points_file` to that path,
  with `source_location = Fig N`.

## Provenance & honesty rules
- **Digitized ≠ reported.** Always tag the method; never present digitized points as
  if read from a table.
- **Record the operator and tool.** Digitization is a measurement with error; it must
  be attributable and repeatable.
- **Never invent points** beyond the plotted range, and never "clean" outliers.
  Extrapolation belongs in a model row with an explicit domain-of-validity note, not
  in digitized data.
- **Re-digitization should reproduce** within a small tolerance; if it doesn't, the
  calibration (often a missed log axis) is wrong.
- **No figure images are committed** — only the extracted numeric points (consistent
  with the repo's no-PDF / metadata-only policy). The figure stays in the source PDF.

## Copyright & digitization (legal basis)

Digitization here extracts **numeric data points (facts)** from a figure — it does **not** copy
the figure. Copyright protects the figure as *expression* (the rendered image), not the underlying
measurements, which are facts and not copyrightable (US: *Feist*; EU: idea/expression dichotomy).
Extracting and recording those values for analysis is standard meta-analysis practice and is
consistent with the repo's no-PDF / metadata-only policy. Rules that keep it clean:

1. **Never store or commit the figure image** (no scans/screenshots) — only the extracted numeric
   points. The figure stays in the source PDF; any render made for digitization is a throw-away
   working file, never committed.
2. **Attribute** every digitized dataset to its source (`citation_key` + figure number) and record
   provenance (`extraction_method = digitized_figure`, plus tool / operator / date).
3. **Legal basis:** as a research organisation we rely on the **EU DSM Directive (2019/790)
   Art. 3 text-and-data-mining exception** — which **cannot be overridden by publisher terms** for
   research — together with the facts-not-copyrightable principle. Keep extractions
   **proportionate** (the points needed for analysis) so the EU *sui generis* database right is not
   engaged on a substantial part.
4. **Prefer the primary data** when it exists — author-provided underlying data, supplementary
   files, or data-repository deposits (often CC-licensed / public-domain) — and cite that instead
   of digitizing. Ask the authors when in doubt.

This is general US/EU reasoning, **not legal advice**; jurisdictions and individual agreements vary.

## Provisional visual extraction (interim tier)

Tool-calibrated digitization (WebPlotDigitizer) is the standard. When a quick interim read is needed
to seed the pipeline, a **provisional visual extraction** may be recorded **only if clearly flagged**:
`extraction_method = digitized_figure`, `confidence = Mined`, and a note
`provisional visual read — verify with WebPlotDigitizer`. Provisional points must be replaced by a
calibrated extraction before any quantitative claim relies on them, and never carry
`confidence = Verified`. Prefer **table-extracted** values and **published model coefficients** over
visual reads wherever they exist — they are exact and need no digitization.
