# JPDC S3 cross-bundle reproducibility audit — 2026-11-03

## Scope and material
Independent standard-library local audit of the two user-provided **processed** ZIP archives:
- `jpdc_s3_controlled_mask_4seed_2026_11_03(2).zip`, SHA-256 `08bf48d991a42032a3653f753d1af9fc4d91ad462823ffe92017759d56c68077`.
- `jpdc_s3_mask_eta_factorial_4seed_2026_11_03(2).zip`, SHA-256 `d69c9f03a0e7385d97f5cd76d896a0ec8bb203f6c0d596d3aae6b6ce2a98522b`.

The local independent audit completed **154 assertions PASS**, including four-seed cardinality, 72 cross-package metric matches for LOW/HIGH adaptive outcomes (9 metrics × 2 masks × 4 seeds), 16 factorial interaction checks, 16 independently recomputed pooled-count checks, four exact two-sided sign tests, 32 physical mask contrast checks, and 12 physical summary checks (plus cohort counts). The committed executable `jpdc/audit_s3_cross_bundle.py` implements the same key cross-package checks using ZIP parameters and Python stdlib.

Reproduction: `python3 jpdc/audit_s3_cross_bundle.py controlled_mask.zip mask_eta_factorial.zip`.

## Seed-level intervention robustness (additional numerical calculation)
Factorial interaction per seed defined `(adaptive−fixed)_HIGH − (adaptive−fixed)_LOW`.
A leave-one-seed-out sensitivity audit, dropping one of 40,41,42,43 each time, gave:

| Metric | Four-seed mean, pp | Leave-one-out range, pp | Exploratory exact two-sided sign p |
|---|---:|---:|---:|
| FAR | -3.00 | [-3.333, -2.533] | .125 |
| AIR | +11.10 | [+8.400, +13.067] | .125 |
| FWC | +83.00 | [+80.133, +87.600] | .125 |
| DVR | +0.10 | [0.000, +0.133] | 1.0 |

The signs and effect pattern for FAR, AIR and FWC are consistent under four one-seed exclusions *within this deliberately selected four-seed cohort*. This is **not** general robustness or confirmatory significance, and choosing extreme masks using pre-shock placements on the same seeds limits generalization. The preregistered independent 10-seed holdout primary result remains p=.0625 and NOT significant.

## Cross-package validation and scientific limits
All four adaptive LOW/HIGH seed rows in the factorial package agree with the independently archived physical controlled-mask outcomes across late FAR/AIR/DVR/FWC/eta and post FAR/AIR/DVR/FWC, within reported decimal rounding. Pooled counts and exact sign tests were recomputed rather than copied.

The delay precision ambiguity is resolved by unrounded derived values from the physical archive: LOW 0.003184597268205128 ms, HIGH 12.876242811949862 ms, difference 12.873058214681656 ms, correctly displayed as 12.8731 ms. Merely subtracting displayed four-decimal means gives 12.8730 ms; that subtraction is less precise.

**Boundary:** These are consistency checks on processed archive summaries, NOT raw CloudSim trace re-execution, independent simulator validation, nor evidence of statistically significant scheduling improvement. Under HIGH exposure, adaptive eta changes false certifications and abstentions while deadline violations are effectively unchanged. E42 and E4.6 were not modified.

## Next step
Obtain underlying GitHub Actions artifacts of 41719553340 and 41724362605 and test raw per-seed scientific outputs against these processed archives; independently assess manuscript originality relative to FGCS. Then define external trace-replay or second-simulator plan rather than conducting serial significance-seeking.
