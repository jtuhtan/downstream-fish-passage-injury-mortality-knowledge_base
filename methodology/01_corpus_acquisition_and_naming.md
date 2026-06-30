# 1. Corpus acquisition & naming

## Acquisition
- Publications are collected locally (e.g. a reference-manager or folder of PDFs).
  **PDFs are never committed** (copyright). Only their metadata enters the repo.
- For every paper, record a DOI where available; `scripts/extract_passage_data.py`
  and the corpus builder mine DOIs from the first pages as a fallback.

## Authoritative titles (read from the PDFs)
Titles are read from the PDF itself, not inferred from filenames or reference
parses: the embedded `pdfinfo` **Title** metadata when it is a sane title, else a
**largest-font, top-of-page-1 heuristic** (via `pdftohtml -xml`), with journal
mastheads stripped, all-caps normalised, and noisy tails (e.g. "Abstract",
author/affiliation lines) trimmed. Each candidate is flagged by confidence
(`same` / `improved` = superset of the prior title / `likely` / `review` /
`keep-current`) and **reviewed against a manifest before being applied** to
`corpus.csv`. The audit trail lives alongside the PDFs as
`title_scan_manifest.csv`. Titles flagged `review` are low-confidence and may
contain extraction errors — fix them in the manifest and re-apply.

## File-naming convention
Local PDFs use a sortable, parseable convention:

```
YYYY_FirstAuthor_StudyType_ShortTitle.pdf
```

- `YYYY` — publication year (use `20XX`/`200X` if unknown) so a directory sorts
  chronologically.
- `FirstAuthor` — surname, particles joined (e.g. `vanEsch`, `BenAmmar`),
  hyphens kept (`Romero-Gomez`).
- `StudyType` — Review / Lab / Field / Numerical / Guidelines / Misc (this also
  matches the file's parent folder).
- `ShortTitle` — the **ISO 4 / LTWA short title** of the paper, made
  filename-safe (see below). This is the same standard used for the
  `short_title_iso4` field in `data/candidate_additions.csv`, so titles are
  abbreviated identically wherever they appear.

### ShortTitle: ISO 4 / LTWA, filename-safe
The title is abbreviated with `skills/passage-literature-discovery/scripts/iso4_abbreviate.py`
(ISO 4:1997 + LTWA; see that skill's `references/title_abbreviation.md` for the
standard and citations), then sanitised for filesystems:

1. Abbreviate the canonical title (drop articles/prepositions/conjunctions;
   substitute listed words via LTWA, e.g. *Hydraulic→Hydraul.*,
   *Physiological→Physiol.*; single-word titles and unlisted words stay full).
2. Transliterate non-ASCII to ASCII (`ä→ae`, `ö→oe`, `ü→ue`, `ß→ss`, accents
   stripped) so names are portable.
3. Drop abbreviation periods (`Hydraul.→Hydraul`); remove `: ; , / \ ' " ( )`.
4. Replace spaces **and hyphens** with `_` (`Low-Head Turbines→Low_Head_Turbines`).
5. Collapse repeated `_`, keep only `[A-Za-z0-9_]`.

Source typos are preserved (the filename still matches its catalogued title), and
because the abbreviation is shorter than the full title the full path stays well
under OS limits. Within a study folder, identical results are disambiguated with a
trailing `_b`, `_c`, … . The exact ISO 4 token (with periods, for citation) is
the `short_title_iso4` field — the filename is the ASCII-safe rendering of it.

### Bulk renaming / re-deriving names
Names are re-derivable from `data/corpus.csv` (`year`, `first_author`,
`study_type`, `title`). To re-apply or audit the convention, generate an
old→new manifest, review it, rename in place, then sync `local_filename` in
`corpus.csv`. A worked manifest is kept alongside the PDFs as
`title_abbreviation_rename_manifest.csv`.

## Citation keys
The repository identifier for each paper is `citation_key = YYYY_FirstAuthor`
(append `b`, `c`, … to disambiguate same-year/author papers). Every data row
references a `citation_key` that exists in `data/corpus.csv`.

## Cloud-storage note
If PDFs live in a cloud-synced folder (OneDrive/Drive), files may be
"online-only" placeholders. Hydrate (download) them before text extraction;
renaming/moving works on placeholders, but reading their text does not.
