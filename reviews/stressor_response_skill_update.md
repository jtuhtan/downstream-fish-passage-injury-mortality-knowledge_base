# Stressor–response: barotrauma re-run under the updated skill (old vs new)

This records what changed when the barotrauma stressor–response analysis was **re-run under the
updated `passage-stressor-response` skill**, compared with the original skill that produced the first
demonstrator. It is the audit trail for the methodology shift.

## 1. Method changes (the skill)

| Aspect | Original skill | Updated skill |
|---|---|---|
| Dose–response **curves** | figure digitization (curves left "pending") | **exact published coefficient tables**; digitize only figure-only data |
| Source strategy | per-study, paper-by-paper | **synthesis reports first** (PNNL Biological Response Models), then studies |
| Runnable models | none | **`data/dose_response_models.csv`** (b0/b1 → curves computed analytically) |
| QA on coefficients | none | **cross-check `RPC50 = exp(−b0/b1)`** against stated landmarks |
| Units | ad hoc | **standardized** (pressure→kPa, length→mm, mass→g; logged) |
| Assessment | none | **coverage matrix + thresholds tables** (`outputs/stressor_response_*.csv`) |
| PDF table extraction | — | documented gotchas (species-column shift; dropped decimals) |

## 2. Output changes (barotrauma)

| Metric | Original (demo) | Updated (this re-run) |
|---|---|---|
| Runnable dose–response models | 0 (pending digitization) | **46** |
| Species with modelled curves | ~4 (pending) | **~15** + European species/life-stages |
| Response types modelled | injury (pending) | injury · mortal injury · **immediate mortality** |
| Relationships (`stressor_response.csv`) | 15 (8-paper demo) | 44 |
| Equations (`equations.csv`) | 6 | 11 |
| Numeric threshold groups | 9 | 13 |
| Coverage cells (quantified-or-modelled / total) | — | **24 / 35** |
| Rows still "pending digitization" | several | **0** with coefficients available (3 reconciled) |

## 3. What the re-run did / found

1. **Ingested the PNNL "Biological Response Models" report** (Pflugrath et al. 2020, already in the
   corpus as `2020_Pflugrathc`) — its Tables 11–13 (Equation 12) gave **37 barotrauma logistic models**
   across ~15 species × injury / mortal injury / immediate mortality, all on the shared LRP axis.
2. **Coefficient cross-check passed for all 46 models** (`RPC50 = exp(−b0/b1)`), and validated the
   earlier extractions:
   - European grayling 0+: RPC50 = **10.3** ≈ paper's stated **10–12** ✓
   - Common nase 0+: RPC50 = **2.67** ≈ stated **2.7** ✓ (confirms the inferred b1 = 7.377)
   - Two **immediate-mortality** models (Murray cod RPC50 ≈ 84, silver perch ≈ 125) put 50% beyond the
     realistic RPC range — consistent with **low immediate mortality** (distinct from injury), not errors.
3. **Reconciled 3 relationship rows** (Brown 2012; Pflugrath 2018 ×2) from
   `digitized_figure / pending digitization` → `reported` — the curves are now held as **exact
   coefficients**, so no figure tracing is required.
4. **Re-ran the assessment**: coverage = 35 populated cells (24 quantified/modelled); 13 threshold
   groups; units re-verified (9 pressures already kPa, 0 conversions).
5. **Correctly still figure-only** (genuinely need digitization, no published equation): Stephenson
   Fig 3 (% vs nadir), Boys piecewise larval mortality, Doyle life-stage survival.

## 4. Net effect

The updated skill converted the barotrauma dose–response layer from a **sparse, digitization-pending
demo** (0 runnable curves, ~4 species) into a **verified ~15-species runnable model set built from
exact published coefficients**, with a coefficient-QA step that doubles as extraction validation — and
it did so by exploiting a single synthesis report that was already in the corpus. No figure tracing was
needed for the barotrauma curves; digitization is now reserved only for the handful of figure-only
datasets.
