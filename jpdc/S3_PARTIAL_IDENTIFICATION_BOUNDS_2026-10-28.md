# JPDC — sharp partial identification of S3 affected vs unaffected misses (2026-10-28)

## Input and execution
- Successfully aggregated original all-candidate run: 40517387076, artifact 12739924675, file `s3_all30_by_seed.csv`.
- Input SHA256: `78fd57691aa3fabd7a3d84fddac28903c66b173f7165def809b7ec374685321c`.
- 30 seeds × 3 task-index windows (90 verified unique rows).
- Local calculation executed against this original CSV; reproducible code: `jpdc/s3_partial_identification_bounds.py`. No new simulation, no alteration to E4.6.

## Method
For each seed-window with total candidates n, affected count a and total misses m, let x denote affected misses. Integer feasibility implies
`max(0, m - (n-a)) <= x <= min(a,m)`.
Sum these bounds over seeds within each window; bounds are *sharp* given per-seed-window marginals. Unaffected misses equal `m-x`. Group rates divide bounds by respective observed group count. No assumption that all misses fall into affected candidates, no independence or fixed miss risk assumption, and no confidence intervals.

## Verified observed aggregate and attainable ranges
| Window | n | affected n | total misses | affected misses range | affected miss rate range | unaffected misses range | unaffected miss rate range |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 30273 | 9141 | 1863 | 0–1858 | 0–20.326% | 5–1863 | 0.0237–8.816% |
| 1 | 30108 | 9145 | 1617 | 0–1615 | 0–17.660% | 2–1617 | 0.00954–7.714% |
| 2 | 29742 | 9025 | 1323 | 0–1318 | 0–14.604% | 5–1323 | 0.0241–6.386% |

Nonzero misses are **mathematically required** in the unaffected group in all windows because some individual seed-window groups have zero affected candidates but positive misses:
- seed 4202202623 W0: 2 misses, no affected candidate
- seed 4202202623 W2: 1 miss, no affected candidate
- seed 4202202607 W2: 4 misses, no affected candidate

This does not establish that unaffected candidates contribute substantially to aggregate undercoverage, because admissible upper ranges remain wide. The rates are **identification bounds**, not frequentist confidence intervals. The upper bounds declining over time do not establish temporal improvement in the actual stratum-specific rate; the true rates may lie anywhere within their respective bounds.

## Reproduction
```bash
gh run download 40517387076 --repo afshinyaghoobi/casper-iiot-cloudsim --name jpdc-s3-all30-windowed-summary --dir s3_all30_analysis/source
python3 jpdc/s3_partial_identification_bounds.py s3_all30_analysis/source/s3_all30_by_seed.csv
```

## Next evidence gate
A 30-seed instrumented S3 run must report exact affected/unaffected misses, verify seed-zero policy parity, verify 90-row legacy S3_ALL equality, and match original reference SHA. Until then, do not attribute changes to candidate mix or eta mechanism. No 99% coverage, causal, SOTA, external generalization or novelty claim is supported.
