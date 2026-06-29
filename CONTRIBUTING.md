# Contributing

Thanks for helping keep this knowledge base current and trustworthy.

## Golden rules

1. **Never commit PDFs or other copyrighted full text.** Add a bibliographic
   row (with DOI) and extracted/derived data only. `*.pdf` is git-ignored.
2. **`data/` (CSV) is the source of truth.** Excel/Word files in `outputs/` and
   `reviews/` are generated; edit the CSVs (or the scripts), not the artefacts.
3. **Cite the source.** Every extracted value should be traceable to a
   `citation_key` that exists in `data/corpus.csv`.
4. **Document as you go.** Any new rule, vocabulary, schema column or coding
   decision must be recorded in the same change — in `methodology/`,
   `CHANGELOG.md`, and the affected `data/vocab/` file. A change isn't done until
   it's documented.

## Adding a new paper

1. Add a row to `data/corpus.csv` (`citation_key`, year, first author, title,
   study_type, DOI, local_filename). Use the key convention `YYYY_FirstAuthor`
   (append `b`, `c`… to disambiguate).
2. Add a row to `data/extraction.csv` following the schema in
   [`methodology/04_extraction_schema_and_vocab.md`](methodology/04_extraction_schema_and_vocab.md).
   Use the controlled vocabularies in `data/vocab/`.
3. If it concerns a mechanism with a module, add it to the matching register
   (`data/barotrauma_register.csv`, `data/collision_register.csv`,
   `data/shear_register.csv`) and, if it exposes live fish, score it in that
   mechanism's `*_reproducibility_scorecard.csv` using the rubric in
   [`methodology/05_reproducibility_rubric.md`](methodology/05_reproducibility_rubric.md).
4. Code the two cross-cutting axes in `data/axes_exposure_timing.csv`
   (`study_environment`, `location_during_passage`, `outcome_timing`,
   `delayed_window_h`) with the vocabularies in `data/vocab/` — see
   [`methodology/07_axes_exposure_and_timing.md`](methodology/07_axes_exposure_and_timing.md).
5. Set `Confidence = Mined` for an automated/first-pass row, or `Verified` once
   you have read the paper and checked the values.
6. Open a pull request describing the source and what you changed.

## Bulk updates

To re-mine a batch of PDFs, run
`python scripts/extract_passage_data.py <folder> -o data/extraction_new.csv`
and reconcile against the existing table (see
[`methodology/06_update_protocol.md`](methodology/06_update_protocol.md)).

## Review standards

- Keep claims falsifiable and attributed.
- Preserve disagreement in the literature rather than averaging it away.
- Always pair a threshold with its metric, units, species and life stage (and,
  for barotrauma, the acclimation assumption) so values stay comparable.
