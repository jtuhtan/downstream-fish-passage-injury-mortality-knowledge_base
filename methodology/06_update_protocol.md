# 6. Update protocol

How to keep the knowledge base current and re-cut releases.

## Adding papers (incremental)
1. Hydrate the new PDF(s) locally; name them per
   `01_corpus_acquisition_and_naming.md`.
2. `python scripts/extract_passage_data.py <folder> -o data/extraction_new.csv`.
3. Reconcile `extraction_new.csv` into `data/extraction.csv`:
   - de-duplicate against existing `citation_key`s;
   - add corresponding rows to `data/corpus.csv` (with DOI).
4. Verify the high-value rows (set `Confidence = Verified`).
5. If barotrauma-relevant, update `data/barotrauma_register.csv` and (if
   live-fish) `data/<mechanism>_reproducibility_scorecard.csv`.

## Re-building artefacts
- Excel/Word in `outputs/` and the synthesis in `reviews/` are generated from
  `data/`. Re-run the build scripts in `scripts/` after data changes; never
  hand-edit the artefacts.

## Releasing
1. Update `CHANGELOG.md` with what changed.
2. Bump the version in `CITATION.cff` (MAJOR.MINOR.PATCH):
   - PATCH — corrections; MINOR — new papers/fields; MAJOR — schema/rubric change.
3. Tag the release (`git tag vX.Y.Z`) and attach generated artefacts.

## Suggested cadence
- Rolling PRs for individual papers.
- A tagged release on a regular schedule (e.g. quarterly or biannual), or when a
  meaningful batch of new studies has been verified.

## Provenance & auditability
Every value is traceable to a `citation_key`; every editorial decision
(dedup, classification, verification) is captured in the CHANGELOG or PR history.
