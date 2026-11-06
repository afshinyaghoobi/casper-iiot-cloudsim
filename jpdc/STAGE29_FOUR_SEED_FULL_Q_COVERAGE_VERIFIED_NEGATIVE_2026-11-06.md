# JPDC Stage29 — prospective four-seed FULL q calibration validation VERIFIED NEGATIVE (2026-11-06)

## Provenance: protocol before new independent seed results
Protocol `jpdc/STAGE29_FOUR_SEED_FULL_Q_VALIDATION_PREREG_2026-11-06.md`, committed `5a1d767b397d5765a08ac28c5d1a3ca35f2d04f8` **before new results**, explicitly froze source seeds **501, 502, 503, 504** (not present in previously summarized Stage12–28 experiment reports; repository-wide past-use exclusivity not independently audited), two scenarios S2 hidden CPU 40% loss and S3 hidden network 50% loss, both frozen PRED_GREEDY and CASPER_FULL, 80k calibration per seed and 12k deployment jobs per policy/scenario. No optional stopping or seed/threshold adjustments; prior development seeds83–90,301–308 never reused as prospectively independent confirmation.

Original physical source `jpdc/independent_physical_cpu_nonnetwork_trace_stage27.py` and Stage28 `jpdc/causal_nonnetwork_calibration_stage28.py`, `jpdc/replay_stage28_archived_full_q.py` used **without algorithm changes**. Central signed empirical FULL q intervals conditional on class and queue telemetry age: rolling last200 CPU-finish-delivered scores, min40 for available, empirical signed lower/upper order stats 5% and 95%. At CPU finish the signed q score is exactly `(actual CPU finish - dispatch) - (dispatch predicted WAIT + dispatch predicted CPU)`, never network delay; no future task truth enters dispatch. `certified=False` for every interval. Original Stage6 physical policy output JSON equality checked for ALL 16 arms. Original FGCS E42 blob `34256ca7bff46f911cf20e8b94278fbd09175746` and E4.6 untouched.

Actual [GitHub Actions four-seed CI 42280672176](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42280672176): **SUCCESS**: matrix seed501/502/503/504 4/4 successful, all per-seed complete source and Stage6 exact parity, independent aggregate job success `JPDC_STAGE29_ALL_FOUR_SEEDS_COMPLETE_COHORT_AUDIT_PASS` and original per-seed source provenance artifacts. Complete frozen cohort 4 seeds × S2/S3 × PRED_GREEDY/CASPER_FULL ×12000 = **192,000 dependent task-policy evaluations**, scientific **n=4 independent source seeds**, not n=192k independent. A CI PASS is the success of the faithfully executed *negative scientific validation*, not 90% calibration adequacy.

## Preregistered S2 PRED_GREEDY 90% operational adequacy gates — FAILED

For all four independent seeds and all 2000 postshock tasks per S2 PRED_GREEDY arm, empirical total q interval coverage and HIGH/MISSION subgroup (conditional on interval issued):

| Seed | S2 post all | S2 post HIGH | S2 post MISSION |
|---:|---:|---:|---:|
|501|90.20%|89.13%|83.00%|
|502|84.40%|83.33%|59.82%|
|503|85.65%|85.42%|69.90%|
|504|82.65%|75.25%|40.66%|
|**Mean of four seeds**|**85.725%**|**83.2846%**|**63.3459%**|
|**Pass at least 90% of four**|**1/4**|**0/4**|**0/4**|

MISSION per-seed denominators are NOT equal: the shared source workload yielded 100,112,103,91 postshock MISSION jobs for seeds501..504 respectively (406 MISSION jobs total across 4 scientific replicates). Never pool job-level MISSION proportions and call it four independent guarantees. S2 Greedy 4-seed postshock 8000 tasks yielded **1142** interval violations and zero postshock abstentions; post HIGH 1176 tasks with **198** violated; post MISSION 406 tasks with **147** violated.

## All other policies/scenarios — retain full negative picture

| Scenario | Policy | Seed-level mean POST all | Seed-level min POST all | Mean POST HIGH | Mean POST MISSION |
|---|---|---:|---:|---:|---:|
|S2 CPU|PRED_GREEDY|85.725%|82.650%|83.2846%|63.3459%|
|S2 CPU|CASPER_FULL|89.7125%|89.450%|91.3664%|84.8508%|
|S3 network|PRED_GREEDY|90.350%|89.450%|91.1812%|88.0635%|
|S3 network|CASPER_FULL|90.350%|89.600%|91.1812%|87.7887%|

Even S2 CASPER_FULL MISSION undercovered on **every seed** (83.00%,86.61%,87.38%,82.42%). S3 both algorithms average around90.35% postshock overall but MISSION means 88.06% and87.79%, no coverage guarantee. Pre-shock cohort mean overall coverage roughly89.91% (GREEDY),89.96% (FULL), reflecting intrinsic finite-sample signed order stats/exchangeability/nonstationarity, not a validated 90% risk certificate.

All 16 arms achieved Stage6 exact policy parity. Each arm 12000 jobs; intervals issued for about 11637 or 11638 tasks, with sparse initial abstentions (aggregate across seeds: 1450 per scenario/policy). Those abstentions are *not covered* and must be tracked separately in any decision-safe model.

## Science and method implications
1. The severe S2/compute nonstationarity result is **independent-seed negative evidence** for using a simple historical central 90% `q` interval as a trustworthy input to a hard-deadline route certificate, particularly MISSION. Stage24 requires genuine sound externally provided bounds to prove conditional latency dominance. It must **NOT** be physically deployed using Stage28 rolling estimates as if they were guaranteed.
2. The numerical interval is descriptive and empirically evaluated; this work provides no deterministic or distribution-free sequential conditional coverage theorem. Source family and queue outcomes are not proven exchangeable. A 4-seed mean is not a 95% CI. Future new algorithms must explicitly treat source-dependent CPU state changes, residual telemetry age, false alarms, detection delay, risk budgets, and fallback behavior. Do not tune after viewing these four validation seeds and call the same cohort confirmatory.
3. Java CloudSimPlus v8.5.7 SpaceShared versus native Python strict FCFS preregistered cross-simulator queue parity remains **FAIL**: max wait difference 9.1214009ms >5ms. Stage18–21 source-level event timing diagnosis did not repair parity. Still no external real workload/Java performance validation.
4. Stage23 network-only robust rule on one seed88 S3 16 MISSION misses vs CASPER_FULL33, S2 robust14 vs FULL9; **development only**. Stage16 prior Stage15 n8 S3 superiority p=.375 NOT significant, S2 adverse. Stage17 probe ablation n2 saw no miss-count benefit. No JPDC acceptance prediction or claim of new methodological novelty. Prior delayed feedback and hard deadline scheduling literature must be contrasted.

## Next research decision
Treat Stage28 quantile model as **falsified for the prespecified S2 operational coverage target** in the sampled source cohort. Preserve all original data and fail markers. Next method step should formulate a genuinely changed but theoretically clear *change detection + abstention/risk-budget* policy, with an observable-only detector and explicit CPU label delivery delays, preregister false-positive/detection-lag/cost metrics, test causality and after that evaluate a NEW disjoint seed cohort and stronger baselines, not repurpose the four seeds for confirmatory tuning. Also require cross-queue-model assessment, published method comparisons and external traces before JPDC submission.
