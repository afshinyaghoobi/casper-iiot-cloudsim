# S3 stratum-specific trend directions are not identified (2026-10-28)

## Data and reproducibility
The original verified `s3_all30_by_seed.csv` from successful GitHub Actions run 40517387076 was used (SHA256 `78fd57691aa3fabd7a3d84fddac28903c66b173f7165def809b7ec374685321c`). This analysis is a deterministic reanalysis of 90 seed-window rows; no simulation rerun or E4.6 edits.

Executable: `jpdc/s3_stratum_direction_identification.py`. Reproduce after downloading the exact original run artifact:

```bash
python3 jpdc/s3_stratum_direction_identification.py s3_all30_analysis/source/s3_all30_by_seed.csv
```

## Derivation
For each seed-window, affected miss count `x` must be an integer in `[max(0,m-(n-a)), min(a,m)]` where `n` is all candidate count, `a` affected count and `m` total misses. A group's admissible rate interval follows by division by its group count. For the change Wb-Wa, the sharp feasible limits are `[lower_b-upper_a, upper_b-lower_a]`; measurements in separate windows are unconstrained beyond the published marginal counts. Empty group denominators are omitted from seed-specific directional classification (not counted as decreases).

## Results: aggregated miss-rate change intervals (percentage points)
| Group | W0 to W1 | W1 to W2 | W0 to W2 |
|---|---|---|---|
| affected | [-20.3260, +17.6599] | [-17.6599, +14.6039] | [-20.3260, +14.6039] |
| unaffected | [-8.8065, +7.6899] | [-7.6895, +6.3765] | [-8.7919, +6.3624] |

## Direction identification among seed pairs
| Group | Comparison | Identified decrease | Identified increase | Ambiguous | Undefined (empty stratum) |
|---|---|---:|---:|---:|---:|
| affected | 0 to 1 | 0 | 0 | 29 | 1 |
| affected | 1 to 2 | 0 | 0 | 28 | 2 |
| affected | 0 to 2 | 0 | 0 | 28 | 2 |
| unaffected | 0 to 1 | 1 | 0 | 29 | 0 |
| unaffected | 1 to 2 | 0 | 0 | 30 | 0 |
| unaffected | 0 to 2 | 1 | 1 | 28 | 0 |

## Scientific implications and stop rule
Despite lower overall candidate miss rates in later task-index windows, **neither affected nor unaffected aggregate stratum-specific direction is identified** using the archived marginals. This demonstrates a genuine identification gap, not a statistically nonsignificant effect. These bounds are algebraic rather than confidence intervals. Need actual stratum miss counts to claim subgroup trends, estimate standardization, or interpret adaptation mechanisms. The separate parity-gated 30-seed instrumentation workflow remains the empirical gate; no verified result from it is claimed.

No evidence here establishes nominal 99% conformal coverage, SOTA superiority, cross-generator transfer, causality or algorithmic novelty. E4.6 remains frozen.
