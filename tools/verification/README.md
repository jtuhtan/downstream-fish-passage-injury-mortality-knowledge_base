# Offline verification tool

A small, self-contained tool for **confirming the source-of-truth data against the
original PDFs**, one paper at a time. It runs entirely on your own machine — no
internet, no installation (Python 3 standard library only) — because it needs your
local PDF library, which is not part of this repository.

It shows each paper's **PDF on the left** and an **editable form of every extracted
field on the right**. You read the paper, confirm or correct each field, and mark
the row **Verified**. The tool writes your changes back to `data/extraction.csv`
and records who verified it and when in `data/verification_log.csv`.

## Why this exists

Every extraction row is either **Mined** (machine-extracted, unchecked) or
**Verified** (a human confirmed it against the source PDF). See
[`methodology/08_verification_protocol.md`](../../methodology/08_verification_protocol.md)
for the rules. As of this writing **all rows are Mined** — this tool is how they
become Verified.

## Run it

```
python tools/verification/verify.py
```

Your browser opens at `http://127.0.0.1:8000`. On first run you'll be asked for:

1. **PDF folder** — the local library root that contains the study-type subfolders
   (`Review/`, `Lab/`, `Field/`, `Numerical/`, `Guidelines/`, `Misc/`). The tool
   finds each PDF at `<PDF folder>/<study_type>/<local_filename>` using
   `data/corpus.csv`.
2. **Your initials** — recorded as the verifier.

These are saved to `tools/verification/config.json` (git-ignored, so your local
path never gets committed). A template is in `config.example.json`.

## What you do per paper

- Read the PDF on the left.
- For each field on the right: leave it if correct, or edit it if wrong.
- **Confirm & mark Verified** — saves edits and sets `Confidence = Verified`.
- **Flag uncertain (stay Mined)** — if the paper doesn't let you confirm it; add a
  note. The row stays Mined and the flag is logged.
- **Skip** — move on without changing anything.

Progress is saved after every paper, so you can stop and resume any time; the tool
always jumps to the next still-Mined row.

## Outputs (committed to the repo)

- `data/extraction.csv` — updated field values; `Confidence` flipped to `Verified`.
- `data/verification_log.csv` — append-only provenance: `citation_key, verifier,
  date, action, fields_changed`.

After a verification session, rebuild the artefacts and dashboard:

```
python scripts/build_outputs.py
python scripts/build_dashboard.py
```

---

## `verify_models.py` — verifying the dose–response MODELS (coefficients)

A second verifier, for the **fitted-model coefficients** in
`data/dose_response_models.csv` (barotrauma / blade-strike / fluid-shear `b0/b1/…`).
Verifying a coefficient is a faster job than reading a whole paper — you jump to one
table and compare a few numbers — so this tool is optimised for that:

```
python tools/verification/verify_models.py      # opens http://127.0.0.1:8010
```

- **Jumps the PDF to the coefficient table** — searches the paper's text for your
  `b0/b1` values and the `source_location` table, and opens the PDF at that page.
- **Compute-and-compare** — shows the extracted coefficients, the derived landmark
  (E50 / S50 / V50 / A50 / RPC50), a **live curve**, and the source snippet, so
  verifying = "do these match the table?".
- **Batches by paper** and is **keyboard-driven**: `V` verify · `F` flag · `N` next.

It resolves each model's PDF via `data/vocab/source_pdf_map.csv` (which links the
stressor-response citation keys to the corpus) plus a recursive filename search under
your **library root** (asked once, stored in the git-ignored `config.json`). Needs the
`pdftotext` binary (`sudo apt install poppler-utils` on Debian/Ubuntu). Marking
Verified writes `confidence = Verified` back to `dose_response_models.csv` and logs to
`data/model_verification_log.csv`.
