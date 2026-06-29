# 5. Reproducibility rubric (live-fish studies)

A transparent, auditable checklist that measures **reporting completeness** —
whether a study reports enough to be reproduced. It is not a verdict on
scientific quality. Applied to live-fish studies and recorded in
`data/<mechanism>_reproducibility_scorecard.csv`.

## Criteria (C1–C10)

| # | Element |
|---|---|
| C1 | Species + life stage + body size (length/mass) reported |
| C2 | Sample size (n) per treatment reported |
| C3 | Acclimation pressure / depth reported |
| C4 | Acclimation duration reported |
| C5 | Exposure pressure profile / nadir quantified |
| C6 | Pressure-change metric (RPC/LRP/ratio) explicitly defined |
| C7 | Injury-scoring protocol defined (which injuries; necropsy/X-ray/observation) |
| C8 | Holding/recovery time & delayed-mortality window reported |
| C9 | Controls (handling/tag/sham) reported |
| C10 | Statistical model / dose–response reported |

## Scoring
- Each criterion is **reported (1)** or **not (0)**.
- **Field-passage studies:** C3 and C4 (chamber acclimation) are **Not
  Applicable** and excluded from the denominator.
- Score = reported ÷ applicable. Tiers: **High ≥ 80%**, **Medium 50–79%**,
  **Low < 50%**.

## Application notes
- Criteria are detected automatically from the extracted text, then reviewed.
  Treat Low/Medium as "check the paper", since OCR/extraction gaps (older or
  non-English papers) can miss reported items.
- This rubric is for barotrauma-relevant live-fish studies; an analogous rubric
  can be defined per mechanism (e.g. strike velocity & blade geometry for
  blade-strike studies).

## Known limitation
The rubric scores **internal** reproducibility (one study's reporting). It does
not measure **external** reproducibility (independent replication), which is the
deeper gap — most species rest on a single study.
