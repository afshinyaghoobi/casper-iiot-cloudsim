# CASPER JPDC — actual outcomes of all observed rank2 selections (2026-11-04)

## Why this question was asked
The **prespecified four-seed mechanism screen** 41782270007 showed rank2 is actually used without tuning the frozen original algorithm: seed41 CASPER_FULL chose rank2 9 times, seed44 CASPER_FULL 4 times and CASPER_HEALTH_STATIC 1 time; rank3 remained unused. Those fourteen cases were rank1 predicted conformal bound infeasible and rank2 bound feasible, but the screen alone did not measure the actual deadline outcome of the selected task.

## Exact status: exploratory, post-selection, no rank1 counterfactual
We registered this follow-up **BEFORE running additional experiments** in `jpdc/S3_RANK2_OBSERVED_OUTCOMES_FOLLOWUP_PROTOCOL_2026-11-04.md` commit `0b1f597fa4b824944dbe262328e3502e9ac9d634`. Seed indices **41 and 44** were chosen because these were the two **already observed** activation seeds; not an independent random holdout. The code and outcomes are not a causal comparison with alternative rank1 routing. Do not use these observations to infer a statistical performance improvement or change existing preregistered efficacy claims.

Generated-only E45 sidecars `jpdc/instrument_policy_decision_generated_e45.py` and `jpdc/instrument_observed_outcome_generated_e45.py` log per-task decision node/rank/cert and native CloudSim observed actual network + queue wait + service total latency, deadline and missed deadline. `jpdc/audit_actual_rank2_outcomes.py` commit `d904d403a2367ce597d1b58a9b17e0841f5428f1` joins all missions, checks exact task/node/cert/eta/deadline agreement and prespecified rank2 counts, and produces a sorted record of every rank2 actual outcome. It also checks true latency physical decomposition.

## Real execution and results
**GitHub Actions run 41782683679: BOTH matrix jobs SUCCESS**. Original frozen E42 git blob `34256ca7bff46f911cf20e8b94278fbd09175746`, E4.6 unchanged, S3 HIGH original mask [9,12,14,15,17,18], each 80k calibration/30k deployment, original algorithms and deadline/calibration untouched. Both job logs showed:
- `JPDC_OBSERVED_OUTCOME_RECONCILIATION_PASS` (real MISSION actual outcomes agree with official eight-policy CSV).
- `JPDC_POLICY_DECISION_CROSS_LANGUAGE_PARITY_PASS` (independent Python selection/rank/certificate decisions match Java).
- `JPDC_RANK2_OBSERVED_OUTCOMES_JOIN_PASS` (all rank2 chosen task IDs observed; no duplicate/missing pairs).

| Seed | Policy | Rank2 selected | Actual deadline met | Actual deadline missed |
|---|---|---:|---:|---:|
| 41 | CASPER_FULL | 9 | **9** | 0 |
| 41 | CASPER_HEALTH_STATIC | 0 | 0 | 0 |
| 44 | CASPER_FULL | 4 | **4** | 0 |
| 44 | CASPER_HEALTH_STATIC | 1 | **1** | 0 |
| **Total** | | **14** | **14** | **0** |

Exact task IDs with observed on-time completion:
- seed41 CASPER_FULL: `11074, 13430, 15578, 15870, 16537, 17729, 19358, 26082, 29132`.
- seed44 CASPER_FULL: `13467, 14169, 14332, 22995`.
- seed44 CASPER_HEALTH_STATIC: `12444`.

Every one of these 14 selected tasks received a rank2 certificate and met its actual deadline under the original generated-E45 execution. This **does not establish that the same tasks would have failed at rank1**: the actual rank1 counterfactual outcome was not observed, and the policy state/queue could differ under an alternative routing decision.

Original artifacts (raw original logs, scientific CSV, every-task validator, rank2 outcome JSON):
- seed41 GitHub artifact **13299822515**.
- seed44 GitHub artifact **13300315011**.
- Both jobs https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41782683679, workflow `.github/workflows/jpdc-s3-observed-rank2-outcomes-41-44.yml`, source commit `3ef3a1b064ca3ae4809df76f385ebaa8b7bbf02e`.

## How to write this in JPDC without overclaiming
Recommended factual framing:

> In an untuned, four-seed S3 HIGH mechanism-coverage screen, the rank-aware CASPER decision rule selected rank 2 in 14 policy-task evaluations (13 FULL and one HEALTH_STATIC), after rank 1's conformal bound exceeded the task deadline but rank 2's did not. In a subsequent explicitly exploratory observed-outcome check of the two activating seeds, all 14 rank2-selected tasks completed by their deadlines. This demonstrates that rank2 selection can be exercised and can issue correct certificates under these observed workloads; it does not estimate a causal improvement relative to routing the same tasks to rank1 or generalize to rank3, which was not selected.

Do not claim 14 independent experimental replications: those are task-policy decisions across two activating seeds, which were chosen after screening. Do not quote a significance p-value here; it would be invalid.

## Remaining scientific limitations / next defensible work
- No empirical rank3 selection in seed40..44 S3 HIGH; only synthetic tests exercise rank3 code path.
- Cross-language policy parity conditions on Java-recorded model state; full independent YAFS/other simulation (including workload, predictions, feedback, health alarms, and queues) remains pending.
- Seed41/44 dual-sidecar runs were **not paired with uninstrumented science controls in this specific new workflow**; previous seed40 instrumented-vs-control parity was separately verified. The source has only observational print statements.
- Original independent strict chronological FCFS transfer gate **FAILED** max wait 9.1214ms > preregistered 5ms (41773297282), even though CloudSim VM scheduler bypass behavior later explained it.
- Disjoint previously registered S2/S3 holdout p=.0625 and earlier exploratory factorial p=.125 remain nonsignificant. Frozen E42/E4.6 untouched.
- If asking whether rank3 could activate, do not tune original paper to manufacture positive examples. A separate explicitly labeled **synthetic branch coverage** or carefully prespecified scenario-sensitivity study may test reachability, but do not mix synthetic outcomes with main real workload evidence.
