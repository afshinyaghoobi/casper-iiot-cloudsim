# JPDC S3 pre-shock task-level negative control — 2026-11-03

## New independent check
Using original successful physical S3 GitHub Actions run 41719553340 (artifacts seed40 13272215535, seed41 13271273184, seed42 13270784276, seed43 13272485400), performed a deterministic **within-seed pre-shock placebo / negative-control comparison** of baseline, LOW and HIGH mask assignments. This test was conducted on previously generated original `mission_network.csv` traces, not on the processed four-seed summary.

## Verification result: PASS
Across all four seeds, pre-shock MISSION task indices were identical in all three arms and every task matched **exactly as strings**, including task index, selected node, nominal network delay, realized network delay, network multiplier and end-to-end latency. For the two intervention arms compared against baseline:

| Seed | Identical pre-shock mission task IDs | Exact arm-to-baseline task comparisons |
|---|---:|---:|
| 40 | 514 | 1028 |
| 41 | 477 | 954 |
| 42 | 513 | 1026 |
| 43 | 505 | 1010 |
| **Total** | **2009** | **4018** |

No mismatching task, routing node, nominal/realized network delay, multiplier or end-to-end latency was observed pre-shock for CASPER_FULL.

Reproducible Python standard-library script `jpdc/pre_shock_negative_control.py` commit `330979bfa129c1a3a3dd4c3b91af0fccaf0de5c6`. Download the four original physical workflow artifacts to the same directory as `github-actions-artifact-<id>.zip`, and run `python3 jpdc/pre_shock_negative_control.py DIRECTORY`. Local run successfully printed all four seed passes and `PASS 2009 ... 4018 ...`.

## Scientific significance and limitations
This exact **pre-intervention invariance** provides a useful falsification/implementation-consistency check: choosing the affected mask did not change *observed* pre-shock CASPER_FULL mission-task routing or latency in these four replicates. The difference between LOW and HIGH observed postshock is therefore less plausibly an artifact of unexpected pre-shock changes **in these recorded variables**.

Do not confuse a negative control with independent assignment of masks, full state equivalence across every policy, causal proof, or validation under a second simulator. The HIGH/LOW masks were deliberately selected using pre-shock placement frequencies, which limits external validity; per-task equality does not create 2009 independent experimental seeds. The factorial inferential n remains four, exact two-sided sign p=.125; the independent registered S2/S3 holdout p=.0625 remains nonsignificant. E42/E4.6 are untouched.

## Next
Execute/check the previously committed compact raw-actions auditor on downloaded original archives and record its own result; pre-register a distinct trace-replay/independent-simulator validation protocol before looking at outcomes. No repeated p-value fishing.
