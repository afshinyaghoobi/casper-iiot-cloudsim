# JPDC Stage39 independent eight-seed scheduling-first HOLDOUT preregistration (2026-11-07)

## Prospectively frozen before ANY new eight-seed source output
Stage37 seed91 actual MISSION deadline count mixed/adverse under naive CPU penalty. After explicitly retrospective Stage37b matched task analysis suggested background queue interference, Stage38 preregistered development seed92 with fixed **MISSION-only CPU/E2E feedback routing**. Source [Stage38 42356954652](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42356954652) SUCCESS: S2 MISSION-only combined POST misses2/100 vs GREEDY6, CASPER_FULL2, all-class combined3; S3 MISSION-only combined2/100 vs GREEDY5, FULL5, all-class combined2. **One developmental seed, selected after hypothesis generation, cannot establish superiority.** Freeze Stage38 source code, all CPU/network error thresholds, 2/5ms budget, estimator windows, and all workload setup NOW.

## Complete fixed scientific source cohort
Exactly eight new synthetic-source seeds **601,602,603,604,605,606,607,608**, unexamined in prior reported stages12–38; no claim exhaustive historical repo seed audit. Use original Stage3 80k calibration for EACH seed. Scenarios only S2_HIDDEN_COMPUTE_40LOSS and S3_HIDDEN_NETWORK_50LOSS, all original 12k tasks per policy, STRICT original Python FCFS source physics. Frozen candidate policies:
1 PRED_GREEDY
2 CASPER_FULL
3 NEW_CPU_FEEDBACK_ONLY
4 NEW_E2E_FEEDBACK_ONLY
5 NEW_CPU_E2E_FEEDBACK
6 NEW_MISSION_ONLY_CPU_FEEDBACK
7 NEW_MISSION_ONLY_CPU_E2E_FEEDBACK

8 scientific seeds ×2 scenarios×7 original-policy/frozen-candidate arms×12k dependent tasks = **1,344,000 dependent task-policy observations, scientific n=8 seeds**. Per scenario, postshock task_index10000..11999 MISSION job count is source-generated and shared across policy arms but may vary by seed. Never treat 1.344M dependent jobs as independent observations. Fail-fast=false and cohort aggregation must require 8/8 with no optional dropping of bad source seeds. Each seed original PRED_GREEDY/CASPER_FULL exact original Stage6 policy JSON parity and old Stage37 CPU/E2E policies frozen parity; new MISSION-only background changes 0, all units causal source CPU-finish/E2E feedback counts 12k.

## Primary outcomes frozen in advance
The PRIMARY scientific unit is the *independent source seed*. At each seed/scenario/policy report integer POST MISSION deadline misses and denominator, full MISSION missed deadline count, mean E2E, mean wait, per-class feedback reroute counts, CPU/E2E completions. Pair by seed/scenario with CASPER_FULL first, PRED_GREEDY second. Evaluate mission-only combined and mission-only CPU ablation, alongside all-class combined and the single-sensor ablations. For candidate minus baseline, negative paired miss difference means candidate improved. Report all 8 raw per-seed values, paired mean/min/max, counts candidate better/worse/ties and exact two-sided sign-test p-value calculated ONLY over non-tied seed outcomes; sign-test requires independent source seeds but does not assert task iid. Report any failure even if overall average improves.

Operational candidate retention gate: (a) **mean across eight S2 paired post MISSION misses vs CASPER_FULL <=0** (no average loss in compute shock), (b) S3 paired mean vs CASPER_FULL <0 (strict improvement in network shock), (c) no more than2/8 seeds worsened in either scenario. These are engineering decision rules, NOT acceptance criteria or false statistical guarantees. Separately require exact sign p<.05 to label a directional superiority finding at a scenario (otherwise "suggestive/insufficient" only). No tuning at all on the holdout seeds. If failed, permanently record as tested and choose NEW scientific seeds for any changed algorithm.

## Boundaries and explicit research posture
Source Python FCFS vs Java CloudSimPlus8.5.7 SpaceShared preregistered maximum queue-wait difference9.1214ms>5ms remains FAILED, so no cross-engine validation claim. Existing original E42 git blob `34256ca7bff46f911cf20e8b94278fbd09175746` and E4.6 untouched. No use of hidden affected-node identities or future source truth at dispatch. Actual source MISSION deadlines not conformal coverage. Six full-text user-uploaded 2026 FGCS/JPDC publications are staged in `jpdc/references_2026_six_uploaded.bib` and manuscript related-work draft, but **none of their published schedulers is claimed executed**. Independent holdout success would still require a credible reimplemented prior method and alternate queue/trace validation before submission.
