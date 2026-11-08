# JPDC Stage47–48 queue-externality-gated NodeLocal scheduler: independently VERIFIED mixed/negative incremental value (2026-11-07)

## Provenance and scientific sample
Stage47 structure preregistered BEFORE any DEV results `jpdc/STAGE47_CAUSAL_QUEUE_EXTERNALITY_GATE_PREREG_2026-11-07.md` commit `97610d8077a422c882ba890d7cda4378e15559eb`. It was motivated by an explicitly POSTHOC Stage46 frozen source forensic where seed903 NodeLocal saved2 MISSION misses but added5 vs original FULL (net+3) and seed901 NodeLocal saved4, added0. Stage47's pure `jpdc/queue_externality_gate_stage47.py` gates candidate issue-time health, nominal +2ms vs original FULL, predicted virtual FCFS backlog no increase vs FULL, delivered positive corrected-score improvement>=3ms, corrected candidate<=deadline−2ms, original FULL nominal<=deadline. Stage44 NodeLocal causal CPU/E2E detector unchanged; NORMAL/HIGH and rejected MISSION always original FULL. Accepted MISSION route remains uncertified: NOT a real queue externality upper bound or hard deadline guarantee. E42 frozen original blob `34256ca7bff46f911cf20e8b94278fbd09175746`, E4.6 and older Stage6/42/44 sources untouched.

[Verified Stage47 development GitHub run42433569355](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42433569355) succeeded seeds99,100 S2/S3, 6 policies×12000=288000 DEPENDENT task-policy obs, source DEV scientific n2. Both S2 new combined matched FULL6/99 and6/108; S3 seed99 FULL5 vs combined5, seed100 FULL3 vs combined2, only one miss improvement. New combined also **TIED frozen old Stage44** for all DEV source scenario-seeds. Preregistered DEV gates S2 no harm, S3 strict mean gain vs FULL and at least one S3 accepted switch passed; no separate proof.

Stage48 genuine scientific new fixed source seed cohort preregistered BEFORE any seed results `jpdc/STAGE48_EIGHT_SEED_QUEUE_GUARD_HOLDOUT_PREREG_2026-11-07.md`, git commit `2f0bacf077f917faa60469106d66b20b2d6817a4`. Exactly eight fresh independent source seeds **1001–1008**, 80000 original Stage3 calibration each, original S2 hidden CPU40%-loss and S3 hidden network50%-loss, 6 policies×12000 arrivals/scenario/seed => **1,152,000 DEPENDENT task-policy observations, independent scientific n8 source seeds**. Per seed original PRED_GREEDY/CASPER_FULL exact Stage6 JSON parity, original Stage42 global and Stage44 node-local JSON exact parity, E42 frozen SHA guard and NodeLocal causal units pass. All 8 scientific jobs mandatory, no cherry-picking, source jobs not treated iid.

[**Actual GitHub Actions full Stage48 run 42433839742**](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42433839742) **SUCCESS all 8 independent source jobs and complete aggregated audit**, `JPDC_STAGE48_COMPLETE_EIGHT_SEED_ORIGINAL_SOURCE_DEADLINE_AUDIT_PASS`. Runner `jpdc/run_stage48_queue_guard_independent.py`, complete audit `jpdc/audit_stage48_queue_guard_independent.py`, workflow `.github/workflows/jpdc-stage48-eight-seed-queue-guard.yml`.

## Original source POST MISSION misses, full eight seed matrix

| Scientific source seed | POST MISSION n | S2 CASPER_FULL | S2 Stage47 combined | S3 CASPER_FULL | S3 frozen Stage44 NodeLocal combined | S3 Stage47 queue-guard combined | S3 accepted queue-guard MISSION route switches |
|---:|---:|---:|---:|---:|---:|---:|---:|
|1001|98|0|0|1|1|1|14|
|1002|109|1|1|2|2|2|5|
|1003|103|2|2|3|2|2|2|
|1004|99|0|0|0|0|0|0|
|1005|80|6|6|6|5|5|4|
|1006|97|6|6|10|9|**10 (worse than Stage44)**|11|
|1007|101|0|0|0|0|0|13|
|1008|99|2|2|10|6|6|7|
|**Pooled descriptive, dependent task counts**|**786**|**17**|**17**|**32**|**25**|**26**|**56**|

S2 pooled GREEDY30 vs FULL17, old global Stage42 17, Stage44 NodeLocal17, both Stage47 guard versions17; ALL eight source seeds tied Stage47 vs FULL; S2 network-regime gate calls 0 in all8 seeds; no CPU harm in this particular cohort.

S3 pooled GREEDY33, original FULL32, global Stage42 26, frozen Stage44 NodeLocal combined25, Stage47 E2E-only26, Stage47 combined26. Stage47 combined vs FULL source differences [0,0,-1,0,-1,0,0,-4]: paired seed mean **−.75 MISSION misses/seed**, **3 better,0 worse,5 ties**, two-sided **exact sign p=.25**, NOT significant at.05. The S3 discrepancy vs prior NodeLocal comes from source seed1006 (NodeLocal9 vs new guard10), where denying some issue-time candidate switching worsened one actual deadline outcome. Therefore more conservative queue gating did not yield better actual source MISSION deadline resilience.

S3 for all 8 Stage47 combined gate: source MISSION NETWORK-mode calls by seed [97,108,97,17,70,96,78,58], accepted switches [14,5,2,0,4,11,13,7]. Seven of eight seeds actually switched>=1; one seed1004 had zero. Note gate calls are not accepted switches; most unchanged proposals not active intervention. Strict model source result had no independent queue simulator/real trace.

## Predeclared criterion results: keep all negative findings
Combined Stage47:
- S2 mean no harm vs FULL PASS, <=2 harmed source seeds PASS, S2 NETWORK-mode false-issue fraction <=1% PASS.
- S3 strict mean benefit vs FULL PASS (26 vs32), at most2 harmed source seeds PASS (0).
- S3 <=2 harmed source seeds vs prior Stage44 PASS (1); at least one actual switch in >=6/8 PASS (7/8).
- **S3 no worse mean vs frozen Stage44 NodeLocal FAIL** (**Stage47 26 vs Stage44 25**, one source seed worsened).
- **S3 directional exact sign p<.05 FAIL** (.25), S2 exact sign not applicable/all ties.
- Stage47 E2E-only produced same pooled S3 misses26, no demonstrated CPU+E2E aggregate MISS improvement.
This is a completed **negative incremental value** result for added queue gate: do not promote this as a new stronger JPDC scheduling contribution or claim a hard externality guarantee.

## Stronger publication decision
Stop repeatedly building/validating small threshold-based StageX heuristics without new external validation evidence. Existing six user-supplied 2026 FGCS/JPDC accepted articles already BibTeX referenced and Related Work drafted; no new PDFs are currently needed. A higher-leverage next workstream is **queue model fidelity and fair reproducible baseline comparison**: original native Python strict FCFS vs original Java CloudSimPlus8.5.7 SpaceShared queue WAIT parity previously FAILED registered max deviation **9.1214009ms>5ms**. Examine exact state/queue semantics, instrument differences, compare on small fixed task traces with independently reproducible runs, and run a second physical queue discipline or real trace once well-defined. Also implement an explicitly **DFAQ-LB-inspired** (not falsely the author original) congestion-responsive comparator and a deadline heuristic with frozen method descriptions. Only after a source-independent fair performance case is strong should a JPDC manuscript claim be broadened.

Stage48 seed1001–1008 are now SPENT for algorithm selection; any changed future method requires NEW source development and untouched holdout independent seeds. Older holdout seeds601–608,701–708,801–808,901–908 also spent; source DEV seeds91–100 spent. No 90% conformal future coverage proof, no journal acceptance forecast, no real-factory or cross-engine claims.
