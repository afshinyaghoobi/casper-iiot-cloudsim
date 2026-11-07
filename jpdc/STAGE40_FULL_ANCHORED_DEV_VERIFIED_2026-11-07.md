# JPDC Stage40 CASPER_FULL anchored MISSION feedback — verified dev seeds93–94, 2026-11-07

Pre-outcome protocol `jpdc/STAGE40_FULL_ANCHORED_MISSION_E2E_PREREG_2026-11-07.md` (commit `3ef75e282989c395e154958ec2242dc386023294`). Original FGCS E42 blob SHA `34256ca7bff46f911cf20e8b94278fbd09175746` unchanged, E4.6 frozen. New original-CASPER_FULL-anchored reranker `jpdc/casper_full_anchored_reranker_stage40.py`, isolated native strict-Python-FCFS source `jpdc/independent_physical_full_anchored_stage40.py`, causal unit, run code/workflow and all prior policy parity. Feedback at CPU finish and E2E delivery ONLY; qrank/E17/health and original background routing preserved. MISSION switches only within original top3 eligible CASPER_FULL family, qrank-screened, nominal chosen+2ms, both fresh E2E >=8 reports per-node (last32 and <=5000ms) and at least1ms corrected-score advantage; optional CPU+E2E additionally min4 fresh CPU finishes per node; no future truth. Hard safety/90% class coverage **never** claimed.

**Real GitHub Actions [42405082241](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42405082241) SUCCESS**, both new DEVELOPMENT source seeds93 and94, each 80000 calibration tasks and 2 hidden shock scenarios, 5 policies ×12000 source tasks per scenario; 240000 DEPENDENT task-policy samples, scientific DEV n2. Original baseline Stage6 exact JSON parity in all 8 original scenario-policy arms, frozen Stage38 mission-only policy exact parity in4 arms, source output repeat byte-identical, causal unit pass.

| Seed | Scenario | POST MISSION denominator | PRED_GREEDY misses | Original CASPER_FULL misses | Stage38 old Mission-only combined misses | NEW FULL-anchored E2E misses | NEW FULL-anchored CPU+E2E misses |
|---:|---|---:|---:|---:|---:|---:|---:|
|93|S2 CPU40%-loss|100|5|2|5|**2**|2|
|94|S2 CPU40%-loss|121|11|9|9|**9**|9|
|93|S3 NET50%-loss|100|8|7|6|**6**|6|
|94|S3 NET50%-loss|121|15|15|14|**15**|15|

S2 Stage40 E2E produced ZERO switches both seeds; CPU+E2E produced0 seed93 and1 seed94 (no miss count change). Original FULL choices preserved effectively. S3 Stage40 E2E mission switches **12 seed93**, **8 seed94**; CPU+E2E same switches12,8, no extra deadline-miss benefit. Availability of usable fresh evidence is not a guaranteed bound. This is **slightly encouraging**, but total net S3 benefit is ONE MISSION task across two DEV source seeds, and S2 parity is plausible because no network signal generates rerouting. No meaningful statistical hypothesis test from n2 and no "new algorithm superior" claim. The changed node can still disrupt future queues and downstream tasks despite original CP screen.

These are all native stochastic strict Python FCFS results; original preregistered Python-vs-Java CloudSimPlus SpaceShared queue parity FAILED max wait discrepancy9.1214ms>5ms and remains unaddressed.

**Decision:** Freeze Stage40 unchanged and independently examine on a new source-seed cohort. If S2 no-harm and S3 evidence of benefit fail, do not promote as final JPDC method. Six uploaded 2026 FGCS/JPDC references staged in `jpdc/references_2026_six_uploaded.bib` and Related Work draft, but original algorithms not reproduced.
