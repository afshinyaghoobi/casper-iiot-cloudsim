# JPDC S3 temporal seed-paired audit — 2026-10-27

## Provenance
- Original experimental action: 40517282086 (30 original seeds, S3, all instrumented candidates).
- Verified aggregate action: 40517387076, successful, source commit 3e48afca160fc33441a72fdce5cd7ec94d5b65ed.
- Exact immutable input: artifact `jpdc-s3-all30-windowed-summary`, ID 12739924675, CSV `s3_all30_by_seed.csv`, from aggregate action above.
- Audit script: `jpdc/analyze_s3_paired_temporal.py`.
- Workflow: `.github/workflows/jpdc-s3-paired-temporal.yml`.
- Frozen E4.6 and its tag are not modified.

## Already verified descriptive results (not a new experiment)
| Window | Candidates | Misses | Candidate miss rate | Mean eta |
|---|---:|---:|---:|---:|
| 0 | 30273 | 1863 | 0.0615399861 | 2.3051200227 |
| 1 | 30108 | 1617 | 0.0537066560 | 2.4181394562 |
| 2 | 29742 | 1323 | 0.0444825499 | 2.4297433186 |

Descriptive pooled absolute change window 0 to 2: -1.7057436197 percentage points. Candidate mix and count change by window, and exact window construction has **not** yet been audited against the instrumentation source, so do not label them as equal-duration temporal thirds or claim adaptation.

## New reproducible analysis
Reads exactly 90 CSV rows representing 30 seeds × 3 windows, validates full seed/window coverage, exact nonnegative counts, and unique keys. Calculates per-seed candidate miss rate, pairs window changes within each seed, reports equal-seed-weight mean changes (percentage points), 95% percentile seed-cluster bootstrap intervals (20,000 replicates with fixed RNG seed 20261027), and an exploratory two-sided exact sign test. Retains observed per-seed dependency. Three contrasts: 0→1, 1→2, 0→2.

**Execution/results status:** Script and workflow were committed; no computed paired estimates are stated here until the new workflow's artifact has been retrieved and verified. No assertion of test significance is warranted from pooled rates. Multiple exploratory contrasts are not confirmatory claims.

## Run
Workflow automatically triggers on the research branch when the workflow/script changes. It explicitly retrieves the original successful run's CSV instead of repeating simulation. Reproduce locally with:

```bash
gh run download 40517387076 --repo afshinyaghoobi/casper-iiot-cloudsim --name jpdc-s3-all30-windowed-summary --dir s3_all30_analysis/source
python3 jpdc/analyze_s3_paired_temporal.py s3_all30_analysis/source/s3_all30_by_seed.csv
```

Output: `s3_all30_analysis/s3_paired_temporal_audit.json`.

## Interpretation safeguards
- Not a causal test: the temporal window assignment is observational, not randomized.
- No claim of nominal 99% conformal coverage in S3 or family-wise calibration.
- Not evidence of SOTA superiority, generalization beyond the simulator, or a novel algorithm.
- Paired seed bootstrap needs reasonable between-seed independence; shared synthetic generator remains a limitation.
- Audit instrumentation parity with frozen S3 output (late FWC, late DVR) and code-level temporal-window semantics remain unverified future gates.
