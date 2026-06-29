# Candidate-additions schema (`data/candidate_additions.csv`)

One row per suggested work to add. Bibliographic only — no PDFs.

| Column | Content |
|---|---|
| `rank` | 1 = highest priority (by the ranking rubric) |
| `priority` | High / Medium / Low (citation-frequency tier) |
| `first_author` | Cited work's first-author surname (as parsed) |
| `year` | Publication year |
| `times_cited` | Number of distinct collection papers that cite it |
| `themes` | Mechanism themes of the citing papers, e.g. `barotrauma(11); shear(2)` |
| `title_as_cited` | Title text as parsed from the citing paper's reference list — verbatim, APPROXIMATE (verify) |
| `short_title_iso4` | ISO-4 / LTWA short title (see `references/title_abbreviation.md`). PROVISIONAL until the canonical title is resolved, then recompute |
| `example_citing` | A few `citation_key`s of collection papers that cite it |
| `notes` | Free text (e.g. "already in library uncatalogued", "methods textbook", resolved DOI) |

## Conventions
- `first_author` + `year` are the reliable identifier; `title_as_cited` is a
  hint, not a citation. Resolve the full reference + DOI (Crossref/OpenAlex)
  BEFORE adding to `corpus.csv`, then recompute `short_title_iso4` from the
  canonical title with `scripts/iso4_abbreviate.py` (ISO 4 / LTWA).
- Once a candidate is acquired and added, remove it from this file (or mark
  `notes = added <date>`), so the list always reflects what is still outstanding.
- Keep the file sorted by `rank`.

## Resolution provenance (2026-06-29)
- The 11 **High**-priority candidates were resolved to canonical titles and their
  `short_title_iso4` recomputed via `scripts/iso4_abbreviate.py`. DOIs verified for
  3 (Rummer 2005 `10.1577/T04-235.1`; Mathur 1996 `10.1139/f95-206`; Larinier 2008
  `10.1007/s10750-008-9398-9`). The rest are pre-DOI / grey literature (book
  chapter, PhD dissertation, technical reports, 1957 German journal) — flagged in
  `notes` with status. Medium/Low candidates remain `(pending canonical resolution)`.
- **Tooling note:** the intended Crossref/OpenAlex REST pass was run but those JSON
  APIs are not reachable from this build's sandbox (Crossref timed out; OpenAlex
  returned empty). Resolution therefore used `WebSearch` to confirm canonical
  titles + DOIs, then the ISO-4 abbreviator. When run in an environment with direct
  API access, prefer Crossref `query.bibliographic` / OpenAlex `search` keyed on
  `first_author`+`year`+`title_as_cited`, then `iso4_abbreviate.py` on the returned
  canonical title.
