# S3 paired temporal audit — executed results (2026-10-27)

## Provenance
- Original S3 all-candidate aggregation: GitHub Actions run **40517387076**, artifact **12739924675**.
- Input: `s3_all30_by_seed.csv`, SHA256 `78fd57691aa3fabd7a3d84fddac28903c66b173f7165def809b7ec374685321c`.
- 90 rows = 30 seeds (4202202600–4202202629) × 3 windows; checked all seed/window keys.
- Independent local Python reproduction of `jpdc/analyze_s3_paired_temporal.py` statistical procedure, using `random.Random(20261027)`, 20,000 bootstrap replicates.
- These are **executed** calculations, not hypothesized results. New GitHub Actions workflow execution status was not verified when recording these results.

## Descriptive pooled data
| Window | Candidates | Misses | Pooled miss rate | Unweighted mean seed miss rate |
|---|---:|---:|---:|---:|
| 0 | 30273 | 1863 | 0.0615399861 | 0.0605419649 |
| 1 | 30108 | 1617 | 0.0537066560 | 0.0521815599 |
| 2 | 29742 | 1323 | 0.0444825499 | 0.0445198203 |

## Seed-paired changes
Reported differences are window B minus window A (negative means lower miss rate). Bootstrap percentile confidence intervals resample **entire seed pairs**, not individual candidates.

| Contrast | Equal-seed mean difference (percentage points) | 95% bootstrap CI (pp) | Seed decreases / increases / ties | Two-sided exact sign-test p (unadjusted) |
|---|---:|---:|---|---:|
| 0→1 | -0.836041 | [-1.514157, -0.285341] | 23 / 7 / 0 | 0.00522288 |
| 1→2 | -0.766174 | [-1.528450, -0.134621] | 19 / 9 / 2 | 0.08715855 |
| 0→2 | -1.602214 | [-2.442059, -0.883118] | 25 / 5 / 0 | 0.000324914 |

**Important disagreement:** The unadjusted sign test for 1→2 does NOT reject at 0.05, even though the exploratory bootstrap CI for mean change excludes zero. They test different quantities (sign prevalence vs mean difference). Do not report all contrasts as significant or promote them to pre-registered confirmatory tests. Three comparisons were inspected; no multiplicity-controlled significance claim is made.

## Reproduction
```bash
gh run download 40517387076 --repo afshinyaghoobi/casper-iiot-cloudsim --name jpdc-s3-all30-windowed-summary --dir s3_all30_analysis/source
sha256sum s3_all30_analysis/source/s3_all30_by_seed.csv
python3 jpdc/analyze_s3_paired_temporal.py s3_all30_analysis/source/s3_all30_by_seed.csv
```
Compare generated output to `jpdc/S3_TEMPORAL_PAIRED_RESULTS_2026-10-27.json`.

## Scientific interpretation and boundaries
This audit independently confirms that mean seed-level candidate Miss rates are lower in later S3 windows of these 30 synthetic seeds, particularly 0→2. It does not identify a causal benefit from increasing eta. The exact start/end and construction of each window, changes in candidate composition, and instrumentation parity of late FWC/DVR against frozen E4.6 still need code-level verification. Measurements are **candidate-level**, not family-wise coverage; S3 undercoverage remains. Neither 99% coverage nor generalization nor SOTA superiority nor algorithm novelty is established.

No original E4.6 code or frozen reference tag was changed.
