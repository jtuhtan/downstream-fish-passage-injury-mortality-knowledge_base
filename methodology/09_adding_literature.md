# 9. Adding new literature (end-to-end workflow)

How a candidate work goes from "cited but missing" to a fully screened, verified
member of the collection. This is the repeatable process distilled from the build
sessions; refine it as the base grows.

## Stages

1. **Discover.** Run the discovery skill
   (`skills/passage-literature-discovery/scripts/discover_candidates.py`) to mine
   works cited by the collection but not in it → `data/candidate_additions.csv`,
   ranked by in-collection citation frequency and tagged to mechanism themes.

2. **Resolve metadata.** For each candidate, clean `title_as_cited`, and fill:
   - `journal` — the publication (blank for reports/theses/books).
   - `doi_or_url` — DOI (as `https://doi.org/…`) or a stable URL if open access.
   - `candidate_link` — a Google Scholar search link (always works as a finder),
     upgraded to a direct open-access PDF link where one is found.
   Resolve via Crossref/OpenAlex where reachable, otherwise web search; recompute
   `short_title_iso4` from the canonical title with `iso4_abbreviate.py`.
   Record provenance/uncertainty in `notes`.

3. **Acquire (human-in-the-loop).** Claude cannot fetch paywalled/binary PDFs.
   Download targets land in `<library>/_candidates_to_check/`, named with the repo
   convention `YYYY_FirstAuthor_StudyType_ShortTitle.pdf`. You (or Claude via the
   Claude-in-Chrome extension, for open-access items only) populate this folder,
   then review each PDF for correctness/version.

4. **Vet & stage.** Move the PDFs you want to add into
   `<library>/_candidates_accepted/`. Delete wrong/duplicate files.

5. **Ingest (Claude, next pass).** For everything in `_candidates_accepted/`:
   - confirm/repair the filename (repo convention);
   - move it into the correct study-type folder
     (`Review/Lab/Field/Numerical/Guidelines/Misc`);
   - add a row to `data/corpus.csv` (citation_key, year, first_author, title,
     study_type, doi, local_filename);
   - add a `Mined` row to `data/extraction.csv` (run
     `scripts/extract_passage_data.py` on the new file). **Note:** that script
     reads `Category` from the containing folder name, so after extracting from a
     temp folder, overwrite each new row's `Category` from the corpus
     `study_type` before merging (otherwise the study-type chart drops them);
   - re-screen for barotrauma / collision / shear and update the registers,
     reproducibility scorecards and `axes_exposure_timing.csv`;
   - remove the item from `data/candidate_additions.csv` (or mark `added <date>`);
   - de-duplicate (md5 + title check) against the existing corpus.

6. **Verify.** Run the offline verification tool
   (`tools/verification/verify.py`, `methodology/08_verification_protocol.md`) to
   confirm the new rows against their PDFs (Mined → Verified).

7. **Rebuild & document.** Regenerate artefacts and the dashboard, update the
   reviews, bump the version and CHANGELOG:
   ```
   python scripts/build_outputs.py
   python scripts/build_dashboard.py
   ```

## Guardrails

- **No PDFs in the repo** (copyright). PDFs live only in the local library; the
  staging folders (`_candidates_to_check/`, `_candidates_accepted/`) are inside the
  library, not the repo.
- **Document as you go** — every rule/decision into `methodology/`, `CHANGELOG.md`
  and the affected vocab in the same change.
- **Resolve before adding** — never add a row whose DOI/canonical title is unknown;
  resolve it first (stage 2).
