# JPDC Stage25 — causal native FCFS queue WAIT-only residuals VERIFIED, seed89 (2026-11-06)

## Provenance and validation
Stage25 prospective trace protocol `STAGE25_QUEUE_WAIT_RESIDUAL_TRACE_PREREG_2026-11-06.md` committed before physical outcomes (commit `f6b7931b6218a05fdab29b97993cda55b58bad2c`). Exact original frozen E42 git blob `34256ca7bff46f911cf20e8b94278fbd09175746`. Stage25 source clone adds only an optional `queue_trace_hook` to `jpdc/independent_physical_queue_trace_stage25.py`; old simulator/FGCS untouched. Data captured at dispatch: VQ predicted backlog before `vq.on_dispatch`; actual service start stored; label emitted at **CPU FINISH** (not E2E) with `signed_wait_residual=actual_wait-predicted_backlog_at_dispatch`. No network loss enters this WAIT-only residual, and it is **not** full Stage24 additive q_j including CPU error.

Original [Stage25 physical run 42254782412](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42254782412) SUCCESS: 80k seed89 calibration, two scenarios S2/S3, two frozen policies PRED_GREEDY/CASPER_FULL, 12k tasks per arm, **48k dependent task-policy observations, scientific n=1**. All four policies **EXACT original Stage6 JSON parity**, 12k unique job labels/arm, complete causal arrival≤start≤CPU finish checks and source queue wait math, entire source matrix re-run byte identical. No routing changed. Additional [immutable-artifact-only stratified audit 42255041119](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42255041119) SUCCESS `JPDC_STAGE25_ARCHIVED_STRATIFIED_WAIT_RESIDUAL_AUDIT_PASS`, no new simulation, no tuning.

## Full preregistered summary (descriptive, seed89 only)

| Scenario | Policy | signed mean wait error ms | MIN signed ms | MAX signed ms | p95 ABS ms | p99 ABS ms | |error|>2ms count / 12000 |
|---|---|---:|---:|---:|---:|---:|---:|
|S2 compute|PRED_GREEDY|0.091765|-6.096139|17.566557|1.521887|3.566511|381|
|S2 compute|CASPER_FULL|0.071796|-6.096139|17.566557|1.504725|3.313859|360|
|S3 network|PRED_GREEDY|0.074378|-6.096139|17.566557|1.504725|3.313528|363|
|S3 network|CASPER_FULL|0.070793|-6.096139|17.566557|1.496065|3.305004|358|

Median signed WAIT prediction error = 0ms in all 4. These do **not** establish a deterministic bound; maxima reflect one source-generated seed only. The positive tail (17.5666ms) and negative residual (-6.0961ms) show signed correction may be valuable. Task type stratification suggests Normal has larger absolute errors than MISSION/HIGH in these source traces, but selection bias and service heterogeneity are uncontrolled.

## New post-hoc descriptive telemetry-age relation (original frozen data, NOT preregistered inference)
The 12,000 per-arm task opportunities split identically by last telemetry age because workload arrival times are shared: 0–10ms n=3692, 10–25ms n=3021, 25–50ms n=5287.

| S2 policy | telemetry age at dispatch | ABS error p95 (ms) | fraction |error|>2ms |
|---|---|---:|---:|
|PRED_GREEDY|0–10ms|0.125683|0.2709%|
|PRED_GREEDY|10–25ms|1.316488|1.9199%|
|PRED_GREEDY|25–50ms|2.197697|5.9202%|
|CASPER_FULL|0–10ms|0.135483|0.2709%|
|CASPER_FULL|10–25ms|1.314392|1.8868%|
|CASPER_FULL|25–50ms|2.105814|5.5419%|

S3 has similar trend: PRED_GREEDY p95 0.124368 →1.310972→2.109102ms, CASPER_FULL p95 0.117592→1.309925→2.094886ms. **No causal or generalization claim**: elapsed time correlates with queue dynamics, selection, node assignment and class; statistics are not independently replicated at seed level.

## Critical methodological boundaries
1. The E2E network residual observer cannot receive CPU finish labels. Source Stage25 labels are available at CPU finish, whereas source Stage10 network labels remain available only after E2E delivery. Stage24 `deliver_queue_envelope` only accepts externally validated error intervals and matching context; Stage25 descriptive residuals are NOT such intervals and must not be fed into it as if valid bounds.
2. Strong pre/post shock S2/S3 and all source task classes were retained; this is no new efficacy run for Stage24 and one scientific seed is not enough to claim distributional coverage, calibration, or statistically supported relationship.
3. Queue prediction residual is **WAIT-only**. Full nonnetwork q_j needed in Stage24 also includes CPU processing error unless separately modeled and bounded. Adding measured WAIT error to E2E residual or network shock is a double-counting hazard.
4. Source native queue is strict Python FCFS; original Java CloudSimPlus 8.5.7 SpaceShared queue fidelity **FAIL** registered max wait 9.1214009ms >5ms. A queue bound derived on native FCFS cannot silently generalize across engines.
5. Prior Stage16 Stage15 multi-seed primary S3 p=.375, S2 adverse; Stage17 probing n2 no MISSION miss changes; Stage23 Stage22 one seed88 S3 16 vs FULL33 but S2 14 vs FULL9. Preserve negatives; no JPDC superiority claim.

## Required next work
Before empirically deriving queue bounds, preregister a **chronologically causal** queue-calibration procedure with training and validation that never uses future CPU starts at dispatch, an explicit conditioning context (node class, source queue model, telemetry age, workload phase), independent calibration/evaluation seeds and block-aware coverage tests. Instead of pretending empirical p95/p99 are hard deterministic bounds, classify them probabilistically with **honest finite-sample limitations** and choose abstention fallback on insufficient sample size. Consider a theorem with explicit queue envelope assumption or separately calibrated risk levels and sensitivity. Then incorporate complete non-network CPU service error. Novel method must outperform credible hard-deadline and delayed-feedback alternatives under independent physical models before JPDC submission.
