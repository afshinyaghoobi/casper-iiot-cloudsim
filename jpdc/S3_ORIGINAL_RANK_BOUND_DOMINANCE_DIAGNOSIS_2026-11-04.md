# JPDC rank-2/3 activation diagnosis on original decision trace — 2026-11-04

## Status and dataset
This is a POST-HOC DESCRIPTIVE mechanism audit of the **already generated** original CloudSim S3 seed40 HIGH trace, workflow 41779874971, artifact 13298343053 (3090 MISSION records, two policies sharing 1545 mission task indices). It is not a preregistered out-of-sample hypothesis test, independent efficacy trial, or validation of adaptive online feedback in a second simulator. Its purpose is to explain why the previously verified cross-language run saw zero rank2/3 assignments.

## Formula reconstructed independently from original Java-recorded inputs
For the three lowest-latency eligible predicted nodes (with health alarms excluded), recompute each rank-wise upper conformal bound
`U_r = prediction[node_r] + eta * qRank[r] * (3 + 0.1 * prediction[node_r]) * sigmaMultiplier[node_r]`.
The frozen Java policy selects the **first** rank where `U_r <= deadline`, otherwise defaults to rank1 with no certificate. Python independently recomputes and requires exact node, rank and certificate parity for every original mission task.

## Genuine original-trace results — local executable independent analysis
| Measurement | CASPER_FULL | CASPER_HEALTH_STATIC |
|---|---:|---:|
| MISSION records | 1545 | 1545 |
| Original certificates | 1298 | 1482 |
| Rank2 U below Rank1 U | 0 | 0 |
| Rank3 U below Rank1 U | 0 | 0 |
| Rank2 feasible when Rank1 infeasible | 0 | 0 |
| Rank3 feasible when Rank1 infeasible | 0 | 0 |
| **Minimum U2 − U1 (ms)** | **+1.5852998581** | **+1.4167475470** |
| **Minimum U3 − U1 (ms)** | **+2.1830101941** | **+1.1244049131** |

Observed pattern frequency `(rank1, rank2, rank3)` where 1 denotes upper bound <= task deadline:
- CASPER_FULL: 111:1056, 110:45, 101:12, 100:185, 000:247.
- CASPER_HEALTH_STATIC: 111:1343, 110:52, 101:1, 100:86, 000:63.

There were **zero** tasks with rank1 infeasible while a later rank was feasible. Thus, **for this specific original dataset, the ranked selection branch was structurally dominated at evaluation time**: if any of the next two candidates met its bound, the first candidate already met its own. This is stronger than the original descriptive all-rank1 count and is a valuable LIMITATION for the manuscript. It is not proof of universal rank domination across other seeds/scenarios or alternative calibration/health states.

The source data reported rank calibration q-values approximately `[1.32,1.66,1.54]` for both policies, but the q values alone do not prove domination without the node-specific predicted times and sigma multipliers. The positive bound-gap measurements above use all those inputs.

## Reproducibility and source separation
- New committed standard-library `jpdc/audit_original_rank_dominance.py`, commit `767a2377528f1abf20c3690c4874a5a527435147` consumes the **unchanged original** `instrumented.log`; no new scientific CloudSim simulation, no data filtering or tuning.
- The full 3090-record original artifact was downloaded, and an independent local verbose script `/mnt/data/audit_policy_rank_dominance.py` was actually executed against its raw `instrumented.log`; it found the results above. The compact committed script must be CI-tested on the exact archived artifact before claiming its own successful execution.
- The original run 41779874971 remains correctly labelled a PASS of *conditional Java-vs-Python selection and certificate logic* (all 3090 tasks); this rank audit should not inflate it into independent policy efficacy.

## Scientific next step
Study rank utilization across a **predefined** untouched selection of scenarios/seeds using original frozen workload science, not by tuning deadlines, calibration or eta until rank2 appears. If observed ranked branches remain unexercised, be explicit in JPDC that rank-aware calibration does not empirically choose alternative candidates in these workloads. More consequential for publication is out-of-sample independent policy-level validation in another simulation framework.

The original strict independent Python FCFS queue fidelity test remains **FAILED** at max error 9.1214 ms > original 5 ms gate. Registered disjoint S2/S3 holdout p=.0625 and exploratory four-seed factorial p=.125 remain nonsignificant. E42/E4.6 are immutable.
