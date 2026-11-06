# JPDC Stage27 — causal CPU+WAIT full nonnetwork residual source pilot VERIFIED (2026-11-06)

## Registration and exact successful provenance
Prospective pre-outcome protocol `jpdc/STAGE27_CPU_AND_TOTAL_NONNETWORK_TRACE_PREREG_2026-11-06.md`, commit `70b2f84a5052d3846fbf9d055147764d2201a6aa`. Exact frozen E42 Git blob `34256ca7bff46f911cf20e8b94278fbd09175746`, old E4.6 and original Stage6 untouched.

- [Native physical Stage27 run 42269844289](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42269844289): **SUCCESS**, exactly 80k source calibration, one development seed90, S2/S3 x two frozen arms PRED_GREEDY and CASPER_FULL, 12k tasks/arm, 48k dependent task-policy labels (scientific n=1, not n48k). Full source policy JSON **exact Stage6 parity** for all four arms and entire trace repeated **byte-identically** `JPDC_STAGE27_SOURCE_TRACE_BYTE_REPRODUCIBLE_PASS`. No policy routing intervention.
- [Independent original-artifact-only forensic audit 42270153066](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42270153066): **SUCCESS**, validates exact arithmetic for **all 48k saved CPU and queue labels** and class-conditioned post-shock extreme residuals. No new source simulation, no output exclusion. Marker `JPDC_STAGE27_IMMUTABLE_NONNETWORK_DECOMPOSITION_AUDIT_PASS`.

## Exact zero-network-error decomposition observed only at CPU finish
At dispatch, `predicted_wait=vq.predicted_backlog(j,now)` before original `vq.on_dispatch`; `predicted_cpu=work/capacity*12` is original nominal service prediction, which does **not** incorporate shock masks or future hashed noise. At CPU FINISH, actual waiting=start−arrival and actual CPU=CPUfinish−start. Then
`q_wait = actual_wait - predicted_wait`
`q_cpu = actual_cpu - predicted_cpu`
`q_nonnetwork = q_wait + q_cpu = (CPUfinish - arrival) - (predicted_wait + predicted_cpu)`.
All 48k identities verified at tolerance 1e-8ms. This is the entire modeled nonnetwork error term in the native strict-FCFS source, not including E2E network delay. Dispatch policy never receives future CPU service or wait. CPU finish label must **never** be passed to an E2E network observer.

## All preregistered POST-task-index10000 numbers (each 2000 tasks, one seed90)

| Scenario | Frozen policy | CPU error signed MEAN ms | WAIT error signed MEAN ms | Total q signed MEAN ms | CPU ABS p95 ms | WAIT ABS p95 ms | TOTAL ABS p95 ms | TOTAL ABS p99 ms |
|---|---|---:|---:|---:|---:|---:|---:|---:|
|S2 hidden CPU|PRED_GREEDY|5.28382|2.63335|7.91717|18.78268|18.79368|**32.57932**|46.89684|
|S2 hidden CPU|CASPER_FULL|0.54631|0.10128|0.64759|3.26936|1.42247|**3.80822**|9.38929|
|S3 hidden network|PRED_GREEDY|0.17919|0.08961|0.26880|2.63398|1.88317|**3.05404**|5.61864|
|S3 hidden network|CASPER_FULL|0.19208|0.09362|0.28569|2.68144|1.91159|**3.21661**|6.52423|

PRE-shock source index0–9999 total q absolute p95 is around 3.15ms (GREEDY) and 3.19ms (FULL), and CPU signed mean ~0.195ms (GREEDY), ~0.198ms (FULL) in both frozen scenarios. Post S2 GREEDY differs sharply from S3, and post S2 FULL better controls bulk q but not all extreme tails.

## Relevant independent archived tail inspection
On S2 postshock PRED_GREEDY, original artifact shows very high total q outliers repeatedly on **node 16** (e.g. index11210, qtotal +65.06183ms = WAIT +28.87264 + CPU +36.18920; index11196 +61.93022ms on same node). Postshock task-class counts for |q_total|>10ms: NORMAL440/1584, HIGH151/315, MISSION8/101. This is **descriptive exposure/selection**, not evidence the scheduler was causally harmed by node16 or an oracle hidden shock mask.
Postshock S2 CASPER_FULL has rarer extreme CPU prediction errors (e.g. index11266 node1 CPU +150.63071ms, WAIT 0; index10005 node1 CPU +95.03504ms WAIT 0), despite much smaller p95 q. No outlier excluded. This highlights that good 95th-percentile bulk latency uncertainty may coexist with severe fat-tail events; do not imply guaranteed hard deadlines.

## Critical claim boundaries and decision
1. The full native *nonnetwork* error is now OBSERVED and its decomposition checked. **NO predictive calibration on future data, probabilistic error guarantee or prospective cross-source coverage** is established for `q_nonnetwork`; Stage24 controller still uses externally supplied bounds and is not physically evaluated. Stage26 rolling signed intervals covered WAIT-only, not qtotal. Need separate prequential model and untouched seed-level validation before feeding source-specific intervals to any risk-aware scheduler.
2. The source S2 task-index shock creates task-dependent compute rate change on hidden affected nodes, whereas S3 creates network-only change. The large S2 GREEDY q contrasts reflect source-dependent regime/context; not real factory trace validation or proven transferable system dynamics.
3. Strict Python-FCFS vs Java CloudSimPlus 8.5.7 SpaceShared queue parity remains **FAILED** with registered max wait error9.1214ms>5ms. Stage18–21 library explanation did not repair cross-engine parity. No independent Java validation.
4. Earlier Stage23 seed88 robust network-only algorithm S3 MISSION misses16 vs CASPER_FULL33 but S2 robust14 vs FULL9; ONE DEVELOPMENT seed, not reliable efficacy. Stage16 original Stage15 guarded 8-seed S3 superiority test p=.375, S2 harm; Stage17 probe ablation had no miss benefit on n2. These negative facts remain.
5. This is reproducible descriptive science, not independently demonstrated novelty of robust intervals or a JPDC-ready new scheduling policy.

## Next methodological experiment
Prospectively register a **causal prequential full qtotal** calibration/validation design with separate unobserved independent scientific seeds and robust distribution shift checks. Full q scores must arrive only at CPU finish, model must explicitly include task class, telemetry age and potential compute-fault inference (without oracle masks or hidden scenario truth). Report MISSION subgroup calibration, outliers, repeated seeds and both S2/S3; avoid assuming aggregate 90% error coverage suffices for hard-deadline safety or using source seed90 retrospectively as fresh confirmation. Formal robust dominance proof must identify whether intervals are deterministic assumptions or statistical risk bounds, and distinguish PRED_GREEDY abstention from guarantee. Stronger published baselines and alternative queue models still required.
