# Ranking rubric — which missing items to add first

The goal is to order candidate additions by expected value to the knowledge base.

## Primary signal: times-cited-within-the-collection
How many distinct papers already in the corpus cite the candidate. This is an
honest, in-domain proxy for importance: if 12 of our papers cite a work we don't
have, it is almost certainly foundational and worth adding. Priority tiers:

| Tier | Citing papers in collection |
|---|---|
| **High** | >= 10 |
| **Medium** | 7 - 9 |
| **Low** | 5 - 6 |

(The default threshold for inclusion in the list is >= 5; lower it to surface a
longer tail, raise it to focus on the essentials.)

## Secondary signals (tie-breakers / adjustments)
- **Recency** — among equally-cited works, prefer newer ones (faster-moving
  sub-topics); but do not discard historical classics, which often anchor a
  mechanism (e.g. early pressure/decompression and turbine-strike papers).
- **Gap bonus** — raise priority when a candidate connects to an UNDER-covered
  part of the framework (a family_group with few/no studies, an under-measured
  outcome timing such as latent/indirect, or a mechanism not yet modularised
  such as grinding/abrasion or gas supersaturation). Cross-check against
  `outputs/Cross_mechanism_gap_matrix.xlsx`.
- **Source type** — peer-reviewed primary studies and authoritative reviews rank
  above textbooks/methods references (e.g. a stream-hydrology or surgery text
  cited only for methods is low value to THIS framework even if frequently cited).
- **Breadth of citing themes** — a work cited across several mechanisms
  (barotrauma + collision + shear) is often a cross-cutting review worth adding.

## What NOT to over-weight
- Raw citation counts from outside the collection (a paper can be globally famous
  but irrelevant here). Stay anchored to in-collection citation.
- A single high-citing paper that is actually a co-author's listing of a work you
  already have — the title-signature dedup should catch these; spot-check the top
  of the list.
