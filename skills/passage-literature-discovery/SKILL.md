---
name: passage-literature-discovery
description: >-
  Find publications and other sources that are MISSING from the downstream fish
  passage injury/mortality knowledge base, rank them by how important they are,
  and connect each to the framework's themes (barotrauma, collision, shear, and
  the exposure-pathway / outcome-timing axes). Use this skill WHENEVER the user
  wants to grow or audit the collection: "what papers are we missing", "what
  should we add next", "find gaps in the bibliography", "snowball the
  references", "suggest sources to acquire", "is the corpus complete", or before
  starting a new mechanism module (to seed it with the right literature). It
  reads the existing collection and proposes a ranked, theme-tagged acquisition
  list - it never adds copyrighted PDFs, only bibliographic candidates.

# Passage literature discovery (gap-driven)

## What this skill is for
The knowledge base will only ever be as good as its corpus. This skill audits the
*current* collection and produces a **ranked, theme-tagged list of works to add**,
so growth is evidence-based rather than ad hoc. The primary, default method is
**citation snowballing**: works cited by many papers already in the collection,
but not yet in it, are almost always important and missing.

## When to use it
Whenever the user wants to extend or sanity-check coverage — explicitly ("what
are we missing?", "snowball the refs", "suggest additions") or implicitly (before
opening a new mechanism module, or after a gap matrix shows thin/empty cells).

## Core method — citation snowballing (default)
Run `scripts/discover_candidates.py <pdf_folder> <repo>/data -o candidates.csv`.
It:
1. extracts the **reference section** of every included PDF (`pdftotext`);
2. parses reference entries into `(first-author surname, year)` keys with a
   short title snippet;
3. counts, for each cited work, **how many distinct collection papers cite it**;
4. drops works already in the collection — both by `(author, year)` against
   `data/corpus.csv` AND by **title-signature** match (to remove co-authors of
   papers you already have, which is the main false-positive source);
5. tags each candidate with the **mechanism themes** of the papers that cite it
   (barotrauma / collision / shear), and
6. ranks by citation frequency (an in-corpus proxy for importance).

Treat the output as a high-quality first pass. Author/year are reliable; the
**title is approximate** (parsed from messy reference text). Short titles follow
a fixed, citeable schema — **ISO 4 / LTWA** (see `references/title_abbreviation.md`)
— applied by `scripts/iso4_abbreviate.py`; the ISO-4 form is PROVISIONAL until the
canonical title is resolved (Crossref/OpenAlex), then recomputed. Resolve the full
citation + DOI before adding (see "Resolving & adding", below).

## Other methods (optional extensions)
The snowball is internal and needs no web. When broader discovery is wanted, the
same ranking/tagging applies to candidates found by:
- **External search** — WebSearch / Crossref / Semantic Scholar / OpenAlex
  queries aimed at the framework's *gap cells* (from
  `outputs/Cross_mechanism_gap_matrix.xlsx`): e.g. taxa with zero studies
  (gobies, sculpins, livebearers), under-covered timing (latent, indirect), or
  mechanisms not yet modularised (grinding/abrasion, gas supersaturation/GBT).
  If a scholarly-search MCP connector is available, prefer it over raw web search.
- **Key author / venue tracking** — follow the prolific authors, labs and
  journals already dominant in `data/corpus.csv` to catch newer or missed papers.

## Reference files
- `references/ranking_rubric.md` — how to prioritise candidates.
- `references/candidate_schema.md` — output columns.
- `references/title_abbreviation.md` — the ISO 4 / LTWA title-abbreviation schema.

## Ranking
See `references/ranking_rubric.md`. In short: importance is proxied by
**times-cited-within-the-collection** (primary), then **recency**, with a
**gap bonus** when a candidate connects to an under-covered theme/taxon/timing.
Priority tiers: High (>=10 citing papers), Medium (7-9), Low (5-6).

## Connecting candidates to the framework
Every candidate carries `themes` (which mechanisms' papers cite it) so it slots
straight into the framework. When you can infer them from the title/snippet, also
note the likely **taxon / family_group**, **study_environment** and
**outcome_timing** so the candidate maps onto all three axes — this is what makes
a suggestion actionable (it says not just "add this" but "this fills *that* gap").

## Output
Write `data/candidate_additions.csv` per `references/candidate_schema.md`
(rank, priority, author, year, times_cited, themes, title_as_cited,
short_title_iso4, example_citing, notes) and a short prose summary in `reviews/`.
Short titles use the ISO 4 / LTWA schema (`references/title_abbreviation.md`).

## Resolving & adding (hand-off to the review skill)
1. Resolve each chosen candidate to a full citation + DOI (external lookup).
2. Acquire the PDF locally (never commit it).
3. Add it via the `passage-injury-mortality-review` skill: a `corpus.csv` row,
   an `extraction.csv` row, the relevant mechanism register/scorecard, and the
   `axes_exposure_timing.csv` row.
4. Log the addition in `CHANGELOG.md` (documentation is part of the change).

## Principles
- **Bibliography only — never PDFs.** Candidates are metadata to acquire, in
  keeping with the repo's no-PDF policy.
- **Importance is what the field cites.** The collection's own reference lists are
  the most honest signal of what matters; snowballing exploits that.
- **Verify before adding.** Parsed titles are approximate; confirm author, year,
  title and DOI before a candidate becomes a corpus row.
- **Document the run.** Record when discovery was run, the threshold used, and
  what was added, so coverage growth is auditable.
- **Standardise titles.** Short titles follow ISO 4 / LTWA (the journal-
  abbreviation standard), never ad-hoc truncation — applied to the resolved
  canonical title. See `references/title_abbreviation.md`.
