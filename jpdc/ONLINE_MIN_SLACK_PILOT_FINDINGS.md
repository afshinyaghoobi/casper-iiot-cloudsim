# Online minimum feasible slack: three-seed diagnostic (negative result)

## Reproducibility
Branch: jpdc-seed0-repro-20261024.
GitHub Actions run: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/40224697724
All 3 jobs succeeded, 45 rows each (9 policies x 5 scenarios), 135 total.
Patch: jpdc/online_min_slack_patch.py.
Original immutable E4.6 is not modified.

## Method
For each incoming task, choose the eligible node with the smallest nonnegative (deadline minus predicted latency). If none is predicted feasible, choose the minimum predicted latency node. This method uses no DAG precedence and is NOT HEFT. It is a newly defined heuristic; do not attribute it to published literature.

## Three-seed descriptive means: late deadline violation rate (proportions)
|Scenario|CASPER_FULL|PRED_GREEDY|ONLINE_MIN_FEASIBLE_SLACK|
|---|---:|---:|---:|
|S0|0.001333|0.001333|0.044000|
|S1|0.018667|0.017333|0.016000|
|S2|0.026667|0.036000|0.100000|
|S3|0.024000|0.022667|0.316000|
|S4|0.060000|0.062667|0.417333|

## Interpretation and safeguards
This is a negative result for the newly defined online heuristic on these settings, especially S3 and S4. Do not present the heuristic as representative of online scheduling literature or as an established strong baseline. With only 3 seeds, these estimates are exploratory and not statistically validated. The method intentionally minimizes feasibility margin and may be fragile under hidden shocks.

## Next steps
1. Prefer an independently validated, literature-faithful online scheduling baseline, with specification, deterministic unit tests, and identical information budgets.
2. Keep existing PRED_GREEDY, CASPER_FULL, and deadline-capacity-preserving heuristic for transparent internal ablation comparisons.
3. Only run full 30-seed tests for a defensible comparator after algorithmic fidelity checks; publish negative pilots rather than discarding them.
4. Avoid naming an online dispatch rule HEFT without a true DAG scheduling benchmark.
