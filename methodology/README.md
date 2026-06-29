# Methodology

This knowledge base is built by a documented, repeatable pipeline. Each stage
has its own file; together they let anyone reproduce the base from a folder of
PDFs or extend it with new papers.

## Pipeline overview

```
   PDFs (local, not in repo)
        │
        ▼
 1. Corpus acquisition & naming      01_corpus_acquisition_and_naming.md
        │   YYYY_FirstAuthor_StudyType_Title.pdf
        ▼
 2. Deduplication & organization     02_deduplication_and_organization.md
        │   md5 + near-dup detection; study-type folders
        ▼
 3. Screening & classification       03_screening_and_classification.md
        │   mechanism / study-type tagging
        ▼
 4. Extraction (schema + vocab)      04_extraction_schema_and_vocab.md
        │   one row per study  ->  data/extraction.csv
        ▼
 5. Reproducibility scoring          05_reproducibility_rubric.md
        │   live-fish studies  ->  data/reproducibility_scorecard.csv
        ▼
 6. Build artefacts & update         06_update_protocol.md
            reviews/, outputs/, releases
```

## Principles

- **Source of truth is text (CSV).** Binary artefacts (xlsx/docx) are generated,
  never hand-edited.
- **Two-tier confidence.** Every extracted row is `Mined` (automated first pass)
  or `Verified` (read and checked against the source).
- **No PDFs in the repo.** Only metadata, derived data and original summaries.
- **Tooling is reproducible.** The extraction logic lives in `scripts/` and in
  the `skill/` bundle, not only in prose.

## Reproducibility of THIS method

The pipeline was executed with `pdftotext` (Poppler) for text extraction,
Python (regex + controlled vocabularies) for mining, and openpyxl/python-docx
for artefacts. Automated steps are deterministic given the same inputs;
human verification is logged via the `Confidence` field and the CHANGELOG.
