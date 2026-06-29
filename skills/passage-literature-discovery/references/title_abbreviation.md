# Title abbreviation — adopted standard (ISO 4 / LTWA)

We do **not** invent our own title shortening. Short titles in this framework
follow **ISO 4**, the international standard already used for journal-name
abbreviations (e.g. *J. Biol. Chem.*), via its controlled word list, the **LTWA**.

## The standard
- **ISO 4:1997** — *Information and documentation — Rules for the abbreviation of
  title words and titles of publications* (3rd ed.; first ed. 1972). Defines the
  rules for abbreviating title words.
- **LTWA (List of Title Word Abbreviations)** — the authoritative word→abbreviation
  list implementing ISO 4, maintained by the **ISSN International Centre (CIEPS)**,
  which ISO appointed as the ISO 4 **registration authority**. ~37,000+
  abbreviations across 60+ languages; updated periodically (latest 2024-02-26).
- **ANSI/NISO Z39.5** — the older US analogue (*Abbreviation of Titles of
  Periodicals*); ISO 4 / LTWA is now the de-facto international reference.

## Scope note (important)
ISO 4's native scope is **serial (journal) titles**. We use it two ways:
1. **Source / journal names → ISO 4 natively** (its intended use). Cite the
   abbreviated source per LTWA.
2. **Article / report titles → an ISO-4-style short title**: we apply the SAME
   LTWA word substitutions and ISO 4 rules to the article title. This is a
   documented *extension* of the standard (ISO 4 does not formally cover article
   titles) chosen specifically to reuse an established, citeable vocabulary rather
   than create ad-hoc abbreviations.

## Rules applied (from ISO 4)
- Omit articles, conjunctions and prepositions (e.g. *of, the, and, in, on, for,
  during*).
- A title consisting of a **single significant word is not abbreviated**.
- Substitute each remaining word using the LTWA (case-insensitive, with simple
  plural handling). **Words absent from the loaded LTWA are kept in full** — this
  is ISO 4-conformant (only listed words are abbreviated).
- Hyphenated compounds: abbreviate each component.
- Full stops mark abbreviations (LTWA values carry them); capitalization is not
  fixed by ISO 4 — we use Title Case for readability.

## Workflow — abbreviate the CANONICAL title, not a parse
Reference-list parses are noisy (they bleed journal names, pages, the next
reference). Therefore:
1. **Resolve** each candidate to its canonical metadata (Crossref / OpenAlex /
   DOI) — full verbatim title + source.
2. **Abbreviate** the canonical article title with `scripts/iso4_abbreviate.py`,
   and the source/journal natively per ISO 4 / LTWA.
3. Until a candidate is resolved, its `short_title_iso4` is **provisional**
   (computed from the parsed `title_as_cited`) and should not be cited.

## Implementation
- `scripts/iso4_abbreviate.py` — applies the rules above.
- `assets/ltwa_subset.csv` — a **subset** of the official LTWA (≈80 common
  scientific/aquatic/engineering words) for offline use; words not in it are kept
  in full. For full fidelity, download the complete LTWA and pass it via
  `--ltwa <file>` (two columns: word,abbreviation).
- Established alternatives (use if preferred): **AbbrevIso**
  (marcinwrochna.github.io/abbrevIso), the R package **abbrevr**, or a Python
  ISO 4 package — all consume the same LTWA.

## Worked examples (clean canonical titles)
| Full title | ISO-4 short title |
|---|---|
| Effects of hydraulic shearing actions on juvenile salmon | Effects Hydraul. Shearing Actions Juv. Salmon |
| Fish and turbines: fish injuries during passage through power stations | Fish Turbines: Fish Injuries Passage Power Stn. |
| Mechanisms of fish damage in low-head turbines: an experimental appraisal | Mechanisms Fish Damage Low-Head Turbines: Experimental Appraisal |
| A review of dissolved gas supersaturation literature | Rev. Dissolved Gas Supersaturation Literature |
| Decompression | Decompression (single word — not abbreviated) |

## How to cite the standard
- International Organization for Standardization. *ISO 4:1997, Information and
  documentation — Rules for the abbreviation of title words and titles of
  publications.* Geneva: ISO.
- ISSN International Centre (CIEPS). *List of Title Word Abbreviations (LTWA).*
  https://www.issn.org/services/online-services/access-to-the-ltwa/ ;
  searchable at https://portal.issn.org/ltwa
