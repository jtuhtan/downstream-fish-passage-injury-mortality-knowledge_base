# Candidate additions — gap-driven literature discovery

Works **cited by many papers already in the collection but not yet in it**, found
by citation snowballing (see the `passage-literature-discovery` skill). They are
ranked by how many collection papers cite each (an in-corpus proxy for importance)
and tagged with the themes of the citing papers. Full list:
[`data/candidate_additions.csv`](../data/candidate_additions.csv).

**38 candidates remaining** (8 High, 8 Medium, 22 Low priority). Of the original 72, many have since been added to the collection or removed as invalid — see `data/candidate_additions.csv` and `data/candidate_removals_log.csv`.

## Top priority (High: cited by >=10 collection papers)

| Cited by | First author | Year | Themes | Approx. title |
|---|---|---|---|---|
| 15 | Carlson | 2008 | barotrauma(12); shear(2); collision(1) | Data overview for sensor fish samples acquired at Ice Harbor, John Day |
| 14 | Turnpenny | 1998 | collision(7); shear(3); barotrauma(1) | Mechanisms of fish damage in low-head turbines: An experimental apprai |
| 14 | Cada | 1997 | collision(4); barotrauma(2); shear(1) | Shaken, not stirred: the recipe for a fish-friendly turbine. p. 374-38 |
| 14 | Cramer | 1964 | barotrauma(11); shear(1) | “Passing fish through hydraulic turbines.” Trans. Am. Fish. Soc. 92(3) |
| 13 | Turnpenny | 1992 | shear(5); collision(5); barotrauma(1) | Experimental studies relating to the passage of fish and shrimps throu |
| 11 | Rummer | 2005 | barotrauma(10); shear(2) | Pysiological effects of swim bladder overexpansion and catastrophic de |
| 11 | Turnpenny | 2000 | collision(5); shear(2); barotrauma(2) | A UK guide to intake fish-screening regulations, policy and best pract |
| 11 | Mathur | 1996 | collision(6); barotrauma(5); shear(1) | a. Turbine passage survival estimation for Chinook salmon smolts (Onco |
| 11 | Harvey | 1963 | barotrauma(6); collision(3); shear(1) | Pressure in the early life history of sockeye salmon. Doctoral dissert |
| 10 | Larinier | 2008 | barotrauma(5); shear(2); collision(2) | Fish passage experience at small-scale hydro-electric power plants in  |
| 10 | Raben | 1957 | collision(6); shear(2); barotrauma(2) | a): Über Turbinen und ihre schädliche Wirkung auf Fische. Zeitschrift  |

## How to read this
- **Author + year are reliable; the title is an approximate parse** of messy
  reference text — resolve the full citation and DOI before adding.
- A standardised **ISO 4 / LTWA short title** (`short_title_iso4`) is included in
  the CSV — the same standard used for journal abbreviations (e.g. *J. Biol.
  Chem.*); see `../skills/passage-literature-discovery/references/title_abbreviation.md`.
  It is provisional until the canonical title is resolved, then recomputed.
- `themes` = the mechanism modules whose papers cite the work, so each candidate
  slots straight into the framework.
- Many High items are the field's foundational/classic works (turbine-strike,
  early decompression/pressure biology, gas-supersaturation reviews, UK turbine
  and screening studies). Adding these strengthens the citation backbone.
- Note: **Monten 1985 'Fish and turbines'** is already present in the library as a
  .zip but was never catalogued in the corpus — catalogue it rather than re-acquire.
- A few frequently-cited entries are methods textbooks (stream hydrology, surgery)
  cited only for technique — low value to THIS framework; deprioritise.

## Next step
Resolve chosen candidates to full citations + DOIs (external lookup), acquire the
PDFs locally (never commit them), then add via the `passage-injury-mortality-review`
skill (corpus + extraction + mechanism register + axes rows) and log in CHANGELOG.
