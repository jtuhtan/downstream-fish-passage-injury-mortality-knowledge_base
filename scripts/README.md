# Scripts

- `extract_passage_data.py` — run `pdftotext` + controlled-vocabulary mining over
  a folder of PDFs and write a first-pass `extraction.csv`. Usage:
  `python extract_passage_data.py <folder_with_pdfs> -o data/extraction.csv`
  (also bundled in `skill/scripts/`).

Build scripts that regenerate the Excel/Word artefacts in `outputs/` from the
CSVs in `data/` are added as the build is formalised; until then artefacts are
produced from `data/` and committed under `outputs/`.

Requirements: see `requirements.txt`. `pdftotext` (Poppler) must be on PATH.
