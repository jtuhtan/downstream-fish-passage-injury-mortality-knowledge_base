# 1. Corpus acquisition & naming

## Acquisition
- Publications are collected locally (e.g. a reference-manager or folder of PDFs).
  **PDFs are never committed** (copyright). Only their metadata enters the repo.
- For every paper, record a DOI where available; `scripts/extract_passage_data.py`
  and the corpus builder mine DOIs from the first pages as a fallback.

## File-naming convention
Local PDFs use a sortable, parseable convention:

```
YYYY_FirstAuthor_StudyType_Title.pdf
```

- `YYYY` — publication year (use `20XX`/`200X` if unknown) so a directory sorts
  chronologically.
- `FirstAuthor` — surname, particles joined (e.g. `vanEsch`, `BenAmmar`),
  hyphens kept (`Romero-Gomez`).
- `StudyType` — Review / Lab / Field / Numerical / Guidelines / Misc.
- `Title` — cleaned title (Windows-invalid characters removed; length-capped so
  the full path stays well under OS limits).

## Citation keys
The repository identifier for each paper is `citation_key = YYYY_FirstAuthor`
(append `b`, `c`, … to disambiguate same-year/author papers). Every data row
references a `citation_key` that exists in `data/corpus.csv`.

## Cloud-storage note
If PDFs live in a cloud-synced folder (OneDrive/Drive), files may be
"online-only" placeholders. Hydrate (download) them before text extraction;
renaming/moving works on placeholders, but reading their text does not.
