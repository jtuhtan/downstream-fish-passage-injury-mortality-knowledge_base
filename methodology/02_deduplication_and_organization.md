# 2. Deduplication & organization

Libraries accumulate duplicates (same paper saved twice; conference vs journal
versions; copies inside topic subfolders). De-duplication is done in two passes.

## Pass 1 — exact duplicates
- Compute an MD5 hash of each PDF's bytes.
- Group by hash; keep one canonical copy (prefer the shallowest folder / largest
  file), move the rest to `_Duplicates_review/`.

## Pass 2 — near-duplicates
- Normalise filenames (strip accents/punctuation, lowercase) and group by
  `year + author + title-prefix` AND by title-only (to catch the same paper
  saved under different years/author spellings).
- Inspect candidate groups by reading the first page of each (publisher,
  authors, year) and decide which single version to keep. Typical cases:
  - journal vs accepted-manuscript/preprint  → keep the published version;
  - online-first vs final issue              → keep the final;
  - mis-attributed first author              → keep the correctly-named copy;
  - conference talk vs journal article       → keep the citable article.
- Never hard-delete: move discarded copies to `_Duplicates_review/` with a note
  so decisions are auditable and reversible.

## Organization
- Sort canonical PDFs into study-type folders (Review / Lab / Field / Numerical /
  Guidelines / Misc). This folder is the `study_type` field and a sanity check on
  the mined methodology.
- Keep a manifest of every move (old path → new path → reason).
