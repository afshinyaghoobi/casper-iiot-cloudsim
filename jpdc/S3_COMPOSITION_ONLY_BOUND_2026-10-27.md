# JPDC S3: two-stratum composition-only bound — executed 2026-10-27

Source: successful run 40517387076, artifact 12739924675, file `s3_all30_by_seed.csv` (SHA256 `78fd57691aa3fabd7a3d84fddac28903c66b173f7165def809b7ec374685321c`). Script: `jpdc/s3_composition_only_bound.py`. Exactly 90 observations: 30 seeds × 3 task-index windows. No E4.6 edits or new simulator runs.

## Mathematical premise
If q is the affected candidate share, r the miss rate, and the two stratum-specific miss risks p_A and p_U are **unchanged** across windows (and common across seeds for pooled comparison), then r = q p_A + (1-q) p_U, so |delta r| <= |delta q|. This is a restrictive algebraic sensitivity model **not** a null-hypothesis test. Other composition changes, changing stratum risks and varying seed weights invalidate the premise.

| Contrast | Pooled Δmiss (pp) | Pooled Δaffected-share (pp) | Maximum two-stratum composition magnitude (pp) | Residual beyond bound (pp) | Seed pairs violating analogous within-seed inequality |
|---|---:|---:|---:|---:|---:|
| 0→1 | -0.783333 | +0.178764 | 0.178764 | 0.604569 | 14/30 |
| 1→2 | -0.922411 | -0.029693 | 0.029693 | 0.892718 | 12/30 |
| 0→2 | -1.705744 | +0.149071 | 0.149071 | 1.556673 | 18/30 |

The changing affected share **alone** cannot reproduce these pooled changes *under the fixed-common-two-strata assumption*. It does not rule out other forms of composition or time-varying risk, nor demonstrate CASPER adaptation or causality.

Reproduce:

```bash
gh run download 40517387076 --repo afshinyaghoobi/casper-iiot-cloudsim --name jpdc-s3-all30-windowed-summary --dir s3_all30_analysis/source
python3 jpdc/s3_composition_only_bound.py s3_all30_analysis/source/s3_all30_by_seed.csv
```

No claims of 99% coverage, family-wise success, statistical superiority, external generalization, or novelty. Next meaningful data collection requires affected/unaffected candidate **misses** per seed and window and a policy parity test.
