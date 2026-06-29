# Contributing

Thanks for helping keep this knowledge base current and trustworthy.

## Golden rules

1. **Never commit PDFs or other copyrighted full text.** Add a bibliographic
   row (with DOI) and extracted/derived data only. `*.pdf` is git-ignored.
2. **`data/` (CSV) is the source of truth.** Excel/Word files in `outputs/` and
   `reviews/` are generated; edit the CSVs (or the scripts), not the artefacts.
3. **Cite the source.** Every extracted value should be traceable to a
   `citation_key` that exists in `data/corpus.csv`.

## Adding a new paper

1. Add a row to `data/corpus.csv` (`citation_key`, year, first author, title,
   study_type, DOI, local_filename). Use the key convention `YYYY_FirstAuthor`
   (append `b`, `c`… to disambiguate).
2. Add a row to `data/extraction.csv` following the schema in
   [`methodology/04_extraction_schema_and_vocab.md`](methodology/04_extraction_schema_and_vocab.md).
   Use the controlled vocabularies in `data/vocab/`.
3. If it is a barotrauma study, also add it to `data/barotrauma_register.csv`
   and, if it exposes live fish, score it in
   `data/reproducibility_scorecard.csv` using the rubric in
   [`methodology/05_reproducibility_rubric.md`](methodology/05_reproducibility_rubric.md).
4. Set `Confidence = Mined` for an automated/first-pass row, or `Verified` once
   you have read the paper and checked the values.
5. Open a pull request describing the source and what you changed.

## Bulk updates

To re-mine a batch of PDFs, run
`python scripts/extract_passage_data.py <folder> -o data/extraction_new.csv`
and reconcile against the existing table (see
[`methodology/06_update_protocol.md`](methodology/06_update_protocol.md)).

## Review standards

- Keep claims falsifiable and attributed.
- Preserve disagreement in the literature rather than averaging it away.
- For barotrauma, always pair a threshold with its metric, units, species, life
  stage and acclimation assumption.
