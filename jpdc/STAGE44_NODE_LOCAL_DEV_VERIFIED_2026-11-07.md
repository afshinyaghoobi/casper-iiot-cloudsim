# Stage44 node-local causal hotspot MISSION scheduling DEVELOPMENT results VERIFIED (2026-11-07)

## Actual engineering evidence
Pre-outcome fixed hypothesis and prospective source seeds `jpdc/STAGE44_NODE_LOCAL_REGIME_PREREG_2026-11-07.md`, commit `49d357e2bb245ba43e5ee3474b9ddf238b7f26c5`. New `jpdc/causal_node_regime_selector_stage44.py`, adversarial `jpdc/test_causal_node_regime_stage44.py`, isolated source `jpdc/independent_physical_node_local_regime_stage44.py` and runner `jpdc/run_stage44_node_local_development.py`. Original source E42 Git blob sha `34256ca7bff46f911cf20e8b94278fbd09175746` frozen and E4.6 unchanged.

**Real GitHub Actions [42430050383](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42430050383) SUCCESS** both development source seeds97 and98, causal unit including one-node diluted network shift, exact original Stage6 PRED_GREEDY and CASPER_FULL JSON parity, exact frozen Stage38 MISSION-only and Stage42 global regime policy JSON parity, repeat byte identical. Original Stage3 80k calibration per source seed; scenarios S2 hidden compute40%-loss and S3 hidden network50%-loss, six policies ×12k jobs each per scenario, **288,000 DEPENDENT task-policy outputs**, source development scientific n2 seeds (not independent validation).

## Changed structural mechanism, NOT just threshold tuning
Stage42 global regime detector misses NETWORK opportunities due to all-node ratio pooling. Stage44 learns FIRST12 CPU and FIRST12 E2E network completion badness per node as frozen per-node reference; recent LAST12 of each per node; badness actual/nominal>=1.5; node alert >=5 of12 bad and >=.25 greater than historical baseline. At each task arrival compute current 21 nominal predicted end-to-end latencies, choose six smallest with node-index tie break; NETWORK mode if >=1 of those six nodes flags NETWORK and no node of six flags CPU; otherwise original FULL. CPU evidence ONLY AFTER FINISH, network E2E evidence ONLY AFTER delivery. NORMAL/HIGH always original FULL. MISSION NETWORK mode uses fixed earlier 2ms-nominal-bounded Stage38 feedback route, E2E-only or CPU+E2E ablation. No oracle scenario, hidden affected node set, task index threshold or future duration in selection. No hard deadline/safe uncertainty certification or mathematical novelty claimed.

## Verified DEVELOPMENT outcomes only (post task-index>=10000 MISSION misses)
| Seed | Shock | Post MISSION n | GREEDY | CASPER_FULL | old Stage38 ungated | old Stage42 global gated | NEW Stage44 node E2E | NEW Stage44 node combined | Stage44 NETWORK dispatches / all12k | MISSION NETWORK decisions |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|97|S2 CPU40-loss|94|9|5|4|5|5|5|0|0|
|98|S2 CPU40-loss|97|5|1|3|1|1|1|0|0|
|97|S3 NET50-loss|94|0|0|0|0|0|0|1865|74|
|98|S3 NET50-loss|97|6|6|3|3|3|3|1961|93|

No S2 change to FULL; S3 97 has zero MISSION misses with any tested method, so its NETWORK activation has NO actual deadline benefit in that seed. S3 seed98 node methods save3 MISSION misses vs FULL, identical to old global Stage42 and ungated Stage38 in that seed; no unique superiority. The candidate masks CPU danger in this small dev cohort; n2 cannot prove robustness, significance or innovation. The node-local E2E and CPU+E2E variants have equal POST MISSION missed-deadline counts across these four dev scenario-seed arms. Do not call CPU feedback essential.

## Scientific next step
Fixed Stage44 algorithm and its observable evidence policy MUST be frozen before a NEW independent source cohort. If proceeding, preregister untouched seeds 901–908 with all eight mandatory, S2/S3, original FULL and Stage42 global as controls plus Stage44 E2E and combined. Primary paired source-seed MISSION missed-deadline comparisons, detector rate/reliability and mean wait; every result including adverse retained. Reusing prior held-out 601–608,701–708,801–808 after method changes would be improper. Original Python strict FCFS vs Java CloudSimPlus8.5.7 SpaceShared queue parity FAILED 9.1214ms>5ms and no published modern DFAQ-LB/AUHS executable algorithm reproduced. Six user-supplied 2026 FGCS/JPDC articles already in bibliography; no more PDFs needed yet.
