# JPDC S3 chronological-window and composition audit (2026-10-27)

## Source and exact window semantics
- Research branch: `jpdc-seed0-repro-20261024`; E4.6 immutable.
- Instrumentation source: `jpdc/s3_all_candidate_patch.py`; experiment run 40517282086; aggregation 40517387076.
- This source specifies: post-shock mission-critical task indices [10000,16667), [16667,23334), [23334,30000). The candidate array is counted for each family member at the relevant task index. Thus windows are **task-index partitions**, not equal-size candidate cohorts, nor necessarily equal wall-clock durations.
- Data artifact ID 12739924675, `s3_all30_by_seed.csv`, SHA256 `78fd57691aa3fabd7a3d84fddac28903c66b173f7165def809b7ec374685321c`. 90 seed-window rows.
- New executable analysis: `jpdc/s3_temporal_composition_audit.py`. Only aggregate reanalysis; no new simulator execution.

## Executed unweighted seed-level measurements
| Statistic | W0 | W1 | W2 |
|---|---:|---:|---:|
| Mean candidate miss rate | 0.060541965 | 0.052181560 | 0.044519820 |
| Mean affected-candidate share | 0.304601475 | 0.305472454 | 0.302088974 |
| Mean eta | 2.310184072 | 2.424615857 | 2.422561894 |
| Seeds with window-average eta exactly 3 | 0 | 19 | 19 |

## Paired within-seed diagnostics
| Contrast | Mean Δ miss rate (pp) | Mean Δ eta | Mean Δ affected share (pp) | Seeds with unchanged eta | Seeds with falling miss and non-increasing eta |
|---|---:|---:|---:|---:|---:|
| W0→W1 | -0.836041 | +0.114432 | +0.087098 | 0 | 0 |
| W1→W2 | -0.766174 | -0.002054 | -0.338348 | 19 | 15 |
| W0→W2 | -1.602214 | +0.112378 | -0.251250 | 0 | 1 |

Across W1→W2, the seed-level Pearson correlation between change in miss rate and change in affected share is **-0.002074**, while correlation with change in eta is **-0.710037**. These are ecological associations, not causal estimates and not adjusted for all possible confounders. Particularly, affected *share* is not sufficient to standardize candidate misses without misses split by affected/unaffected strata.

**Interpretation:** Temporal decrease in miss rate continues despite no increase in average eta in 25 of 30 seeds during W1→W2 (19 unchanged, 6 decreased); 15 of these 25 also exhibit decreasing miss rate. This disproves a simplistic statement that all temporal reductions require a rising eta, but does not identify any causal mechanism.

## Reproduce
```bash
gh run download 40517387076 --repo afshinyaghoobi/casper-iiot-cloudsim --name jpdc-s3-all30-windowed-summary --dir s3_all30_analysis/source
sha256sum s3_all30_analysis/source/s3_all30_by_seed.csv
python3 jpdc/s3_temporal_composition_audit.py s3_all30_analysis/source/s3_all30_by_seed.csv
```

## Limits and next instrumentation requirement
No 99% coverage, superiority, novelty, cross-generator generalization, or mechanistic causal claim follows. A credible composition-adjusted result needs per-seed × window × affected-status **candidate counts and miss counts**, plus an explicit instrumentation-parity check against the original frozen policy for S3 late FWC/DVR. Those counts are *not* present in the previously archived aggregate CSV and cannot be reconstructed from it. A separately instrumented run would be needed, without editing E4.6.
