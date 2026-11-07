# JPDC scheduling-first Stage39 — eight independent seed holdout VERIFIED, mixed and NOT statistically confirmed (2026-11-07)

## Scientific design and strict provenance
Stage37/38 pilot learned from 2026 user-uploaded FGCS/JPDC engineering/heuristic papers and moved the project from abstract guarantees to actual **MISSION deadline miss** outcomes. Frozen Stage38 MISSION-only CPU/E2E scoring is a strictly observable-only heuristic with +2ms nominal mission route budget; NORMAL/HIGH always source PRED_GREEDY. Source CPU labels only enter AFTER actual CPU FINISH and network errors only after E2E delivery. No oracle hidden affected-node mask or future outcome at dispatch, no hard-deadline or 90% uncertainty guarantee.

Stage39 fixed scientific seed cohort and retention thresholds preregistered **BEFORE any seed601–608 outcomes**, `jpdc/STAGE39_EIGHT_SEED_MISSION_SCHEDULING_HOLDOUT_PREREG_2026-11-07.md`, commit `fa24e0734a7ebf57896d60cad9fb433337af3852`. Eight NEW independent synthetic source seeds601–608, original Stage3 80k physical source calibration per seed, two source scenarios hidden CPU40%-loss S2 and network50%-loss S3, seven immutable original/scheduler policies ×12k tasks per arm = **1,344,000 dependent task-policy observations, scientific n=8 source seeds**. No seed exclusions/threshold tweaks; all policy versions frozen before outcomes. All original PRED_GREEDY/CASPER_FULL source outputs exact Stage6 JSON parity in 32 scenario-seed original arms; E42 original Git blob `34256ca7bff46f911cf20e8b94278fbd09175746`, E4.6 untouched.

[Actual GitHub Actions complete independent holdout 42357317014](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42357317014): **SUCCESS** 8/8 independent physical source jobs and all-or-nothing `JPDC_STAGE39_ALL_EIGHT_PREREG_SOURCE_SEEDS_PAIRED_AUDIT_COMPLETE_PASS`. First attempted GitHub YAML [42357274622](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42357274622) **FAILED BEFORE jobs** because unquoted YAML step name containing colon; YAML-only fix, no scientific code/seed modification. Aggregate code `jpdc/audit_stage39_eight_seed_holdout.py` computes exact two-sided seed-level sign tests on *non-tied* paired count differences. Does not treat 1.344M jobs as independent samples.

## Primary S2 compute shock, every source seed
| Source seed | POST MISSION tasks | PRED_GREEDY misses | CASPER_FULL misses | CPU+E2E feedback all classes misses | MISSION-only CPU+E2E misses |
|---:|---:|---:|---:|---:|---:|
|601|92|6|3|6|5|
|602|101|4|1|4|2|
|603|88|6|4|3|4|
|604|117|4|4|2|3|
|605|84|0|0|0|0|
|606|96|0|2|2|0|
|607|89|0|0|0|0|
|608|112|5|3|6|5|
|**Pooled dependent counts; NOT independent inference**|**779**|**25**|**17**|**23**|**19**|

MISSION-only combined minus CASPER_FULL seed-level differences **[+2,+1,0,-1,0,-2,0,+2]**. Mean **+0.25 missed deadlines per seed (WORSE)**, two seeds better, three worse, three ties; exact two-sided sign p=**1.0**. Predeclared (a) no mean harm vs FULL FAIL, (c) at most2 seeds worse FAIL (3/8). Thus the candidate fails **CPU-shock retention** despite beating GREEDY total 19 vs25. This is NOT robust superiority to original CASPER_FULL.

Full source seed means E2E latency S2: PRED_GREEDY51.6743ms, CASPER_FULL52.1183ms, MISSION-only combined51.6693ms. Overall mean latency advantage does NOT establish mission deadline noninferiority; actual POST MISSION count is worse than FULL. Mission-only source routing changed zero background tasks as asserted in all8 source seeds.

## Primary S3 network shock, all eight source seeds
| Source seed | POST MISSION tasks | PRED_GREEDY | CASPER_FULL | CPU+E2E all classes | MISSION-only CPU+E2E |
|---:|---:|---:|---:|---:|---:|
|601|92|1|1|1|1|
|602|101|2|2|0|0|
|603|88|1|1|1|1|
|604|117|9|9|7|6|
|605|84|10|10|4|3|
|606|96|5|4|3|3|
|607|89|0|0|0|0|
|608|112|0|0|0|0|
|**Pooled dependent counts**|**779**|**28**|**27**|**16**|**14**|

MISSION-only combined minus CASPER_FULL seed differences **[0,-2,0,-3,-7,-1,0,0]**. Mean **-1.625 misses per seed (IMPROVED)**, four source seeds better, zero worse, four ties; exact **two-sided sign p=.125**, NOT statistically significant at p<.05. Predeclared S3 strict mean improvement PASS, at most2 seeds harm PASS, but directional significance criterion FAIL. The sample is small, with four ties. This is promising within native source, not independently proven superiority across real workloads or alternate engines.

Mean overall E2E S3: PRED_GREEDY51.9558ms, CASPER_FULL52.4318ms, MISSION-only combined51.9485ms. Mean overall wait S3: FULL2.2350ms vs mission-only combined2.2725ms (slightly worse); do not hide this tradeoff.

## Ablation insight and incomplete claim
- S2 MISSION-only CPU and MISSION-only combined produce EXACT SAME deadline counts on all8 seeds (both19 total) because network feedback did not alter this CPU-shock exposure enough. Full all-class combined total23 (worse than MISSION-only19), indicating that background routing intervention can impact mission outcomes; this is an observation, not a proved decomposition.
- S3 network-only historical E2E penalty alone has pooled19 POST MISSION misses, original CASPER_FULL27; all-class combined16; MISSION-only combined14. CPU-only MISSION has pooled26 (very little gain over FULL27). Thus delivered E2E network feedback seems crucial under S3, and limiting background routing may help. But no p<.05 seed-level directional result for MISSION-only combined vs FULL.
- Original Stage29–36 negative calibration and risk bounds remain; Stage37–39 do NOT use Stage28 signed q intervals as certified. No safety certificate is produced.
- Existing native Python strict FCFS versus original Java CloudSimPlus8.5.7 SpaceShared registered parity **FAIL** (max wait discrepancy9.1214ms>5ms). Nothing here repairs or bypasses this. No real IIoT trace or cross-queue validation.

## Preregistered retention decision (explicit)
S2 non-harm gate FAIL; S2 at most2 harmful seeds gate FAIL; S3 improvement PASS; S3 <=2 harmful seeds PASS; S2 exact sign p<.05 FAIL; S3 exact sign p<.05 FAIL. Therefore **DO NOT promote current candidate to a submission-ready JPDC scheduler**. This is a completed negative/mixed independent validation, not a code failure. Do not tune on seeds601–608 then reuse them as untouched holdout.

## Concrete next method research direction, separate from publication claims
Build a scheduling method that explicitly starts from **original CASPER_FULL mission candidate and health screening**, rather than PRED_GREEDY; then apply CPU-finish and E2E-delivered feedback to *break ties or rank candidates* only when deadline slack and observation freshness support it, with different sources of error separated. Compare against genuine executable baseline versions and price interference effects, not just observational interval coverage. Investigate and repair/characterize cross-queue simulator semantics or use a distinct engine before strong JPDC claim. New policy requires NEW source development cohort and separate untouched confirmation. User supplied six FGCS/JPDC papers are in `jpdc/references_2026_six_uploaded.bib` and actual Related Work draft `jpdc/RELATED_WORK_MANUSCRIPT_DRAFT_SCHEDULING_FIRST_2026-11-07.md`, but **published original schedulers not directly reproduced**.
