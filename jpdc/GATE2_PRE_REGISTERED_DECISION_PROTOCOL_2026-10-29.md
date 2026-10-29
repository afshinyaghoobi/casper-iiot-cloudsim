# Gate 2 — prospective decision protocol (2026-10-29)

This document is written **before** confirmed access to any completed deadline-feasible seed-zero CloudSim result. It records decision rules to reduce post-hoc selection.

## Pilot integrity gate (required)
- A successful Actions job and downloadable `jpdc-deadline-feasible-seed0` artifact.
- `before.csv`: 8 original policies × 5 scenarios; `after.csv`: same 40 plus 5 new rows; scenario/seed exactness.
- All original **scientific** fields must agree exactly before/after. `mean_mapper_us` may differ because wall-clock measurement is nondeterministic.
- Complete 30,000 tasks and expected runtime markers, no service parity failure.
- If any gate fails, debug; do not interpret outcomes.

## Descriptive pilot outcomes
Preselect `late_dvr` (primary), `p99_late_latency_ms` (tail-latency), and `mean_mapper_us` (runtime cost). Report all five scenarios and all pairwise contrasts of deadline-feasible policy vs `PRED_GREEDY` and `CASPER_FULL`. Report adverse findings and tradeoffs, including S3.

One seed is an **engineering smoke test**, not hypothesis testing. No p-values, confidence intervals, statistical superiority or causal mechanism claims from the pilot.

## Decision to scale
If pilot integrity passes and all five scenario rows have valid finite outcomes, proceed to a **precommitted 30-seed paired experiment** regardless of whether seed zero performs better. This avoids choosing a favorable seed. Do not tune parameters on the result. Report scenario-wise paired differences, confidence intervals and a clearly specified multiple-comparison correction. Separately preserve a disjoint holdout for confirmation.

If the new policy is functionally indistinguishable from `PRED_GREEDY` under the workload, report redundancy and prioritize an external literature-faithful independent-task comparator. Do not relabel the control SOTA.

## Main comparison boundaries
- Fixed E4.6 tag remains unchanged; experiments patch only generated E45.
- Controls sharing `fixedSigma` with CASPER are mechanistic ablations, **not** independent external baselines.
- The task workload has no DAG edges, so HEFT is not an equivalent online independent-task competitor.
- In-distribution heldout seeds are **not** a test of cross-generator generalization.
- Do not claim nominal 99% coverage under S3 hidden network shocks, novelty or broad superiority.

## Current blocker
No verified completed GitHub Actions run ID is accessible via the connector's available methods. The commit-run endpoint returns an empty list but does not comprehensively list push-triggered runs. GitHub public URL access also failed. Manual `workflow_dispatch` may not be offered for a workflow only present on a nondefault branch; if absent, use an ordinary push-triggered run or explicitly configure a default-branch dispatcher after reviewing repository protections.

## Next evidence-bearing action
Identify run ID and download actual artifacts before further parameter or outcome analysis. Never substitute synthetic unit data for simulation results.
