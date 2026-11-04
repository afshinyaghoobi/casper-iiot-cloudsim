# JPDC native eight original E42 policy modes — verified development expansion (2026-11-04)

## Predeclared scope
Original E42 frozen Git blob SHA `34256ca7bff46f911cf20e8b94278fbd09175746`; E4.6 unchanged. Development protocol `jpdc/NATIVE_ALL_EIGHT_POLICIES_DEVELOPMENT_PREREG_2026-11-04.md` was committed BEFORE executing any eight-mode experiment, commit `0112b43e064369c0d43fcdf5ae0e649a95ac5ab0`.

This extends the **independently executing Python physical strict-FCFS native CASPER engine** to the entire set of eight frozen E42 policy flag combinations. Python independently generates original task arrivals and 21 node specs; E17 adaptive feedback, node health, stochastic original-model physical CPU/network and quantiles from native completion-driven 80k Stage3 calibration, and all queues are generated and maintained inside Python. **No Java original event, outcome, calibration score or decision is used as simulation input.** It does not claim CloudSimPlus SpaceShared scheduler parity, YAFS, or external industrial deployment.

## Exact policy feature matrix

| Policy | CP | Ranked | E17 adaptive | Node health | Eligible nodes |
|---|---|---|---|---|---|
| CLOUD_ONLY | No | No | No | No | 18..20 |
| EDGE_FIRST | No | No | No | No | 0..11 |
| PRED_GREEDY | No | No | No | No | 0..20 |
| GLOBAL_CP | Yes | No, uses qGlobal for all candidate ranks | No | No | 0..20 |
| RANKED_CP_STATIC | Yes | Yes | No | No | 0..20 |
| CASPER_ADAPT_NO_HEALTH | Yes | Yes | Yes | No | 0..20 |
| CASPER_HEALTH_STATIC | Yes | Yes | No | Yes | healthy of 0..20 |
| CASPER_FULL | Yes | Yes | Yes | Yes | healthy of 0..20 |

The original E42 first-feasible top3 bound, qGlobal vs qRank, rank1 uncertified fallback, no-eligible fallback, health masks, sparse normal probe only under health policies, and adaptive feedback only under two adaptive policies are independently implemented. CP-inapplicable family/abstention/false-cert rates are marked null rather than posing as measurements of those baselines.

Files:
- `jpdc/independent_casper_deployment_stage4.py`, expanded at commit `20416b195f8eb0aff5a80ac1d452e277986dbd9b`.
- `jpdc/test_native_eight_policy_semantics.py`, commit `2012d2493bee8eb81d1868e114ed9807f3685aac`.
- `jpdc/run_native_all_eight_policies_development.py`, commit `ec2d23b0c87c0a49271acd2aa2c850995cc92e80`.
- CI `.github/workflows/jpdc-native-eight-policies-development-once.yml` commit `07c9f06a465eedf85c7c0e34bc63e16081ad16cd`.

## Actual successful CI
**Real GitHub Actions run 41912345904 SUCCESS**, job `126862925240`, raw result artifact **13362907059**. Original registered matrix used **known development** seed index 50, independently generated 80k physical calibration, original S2_HIDDEN_COMPUTE_40LOSS and S3_HIDDEN_NETWORK_50LOSS, 12k native physical task executions each of all eight policies. Total **16 scenario-policy runs / 192000 task-policy observations**. The CI verified original E42 SHA, 8 original mode semantics, original Stage4 decision fixtures, 16-run task and state conservation, previous 3-policy regression identical MISSION miss counts, and **byte-identical complete repeat of all 16 native simulations**.

Observed logs:
- `JPDC_NATIVE_EIGHT_POLICY_DECISION_UNIT_PASS` including original eligible node sets, original GLOBAL_CP qGlobal vs ranked qRank distinction, synthetic rank2/rank3 rescue, health-only alarm exclusion, all-excluded fallback.
- `JPDC_NATIVE_STAGE4_POLICY_UNIT_PASS` (earlier rank2/rank3 CP and native E17 calibration tests unchanged).
- `JPDC_NATIVE_ALL_EIGHT_DEVELOPMENT_MATRIX_PASS`.
- `JPDC_NATIVE_ALL_EIGHT_FULL_MATRIX_BYTE_REPRODUCIBLE_PASS`.
- `JPDC_NATIVE_ALL_EIGHT_EVIDENCE_AUDIT_PASS`.

### All actual Stage4 native physical MISSION deadline misses — development seed 50, original 12k tasks

| Policy | S2 compute degradation | S3 network degradation |
|---|---:|---:|
| CLOUD_ONLY | 190 | 248 |
| EDGE_FIRST | 397 | 354 |
| PRED_GREEDY | 19 | 25 |
| GLOBAL_CP | 19 | 25 |
| RANKED_CP_STATIC | 19 | 25 |
| CASPER_ADAPT_NO_HEALTH | 19 | 25 |
| CASPER_HEALTH_STATIC | 18 | 25 |
| CASPER_FULL | 18 | 25 |

Every policy had exactly **617 MISSION tasks** (including both pre- and postchange events), and each policy's observed chosen rank was **rank1 for every MISSION**. Rank2 and rank3 paths were tested using deliberately designed synthetic feasibility snapshots, but NEVER observed in actual fixed Stage4/8-mode workload; no efficacy contribution attributable to rank selection can be concluded. Actual S2 alarm transition count was 1 under HEALTH_STATIC/FULL, no S3 health alarms. Adaptive `eta>1` dispatches occurred for both CASPER_ADAPT_NO_HEALTH and FULL: 6027 under S2, 7907 under S3. There is **no persuasive comparative benefit** in the development results; static and full were tied in deadline outcomes.

## Statistical and scientific limitations
The completed independent engine is native Python, not YAFS and not equal to CloudSim Plus SpaceShared scheduling. The independently registered original Java→Python FCFS fidelity test run41773297282 **FAILED** max wait 9.1214ms against original maximum allowed 5ms; this new clean-room physical engine is valid under its *own* explicitly documented nonpreemptive FIFO semantics but does not change the old gate.

Original separately registered S2/S3 confirmatory 10-seed exact sign test p=.0625 **nonsignificant**; original exploratory four-seed factorial p=.125 **nonsignificant**. New eight-policy seed50 results are purely development evidence and do not justify a new p-value, causal claim or improved generalization.

## Next experimental milestone
Reserve a wholly untouched seed-level evaluation, after all eight native policy semantics and 30k task scale are frozen, with independently computed 80k calibration per seed. Predefine a single primary paired metric and comparison and preserve zero/tie treatment in exact sign testing; report effect sizes and seed-level confidence intervals, no p-hacking. Before executing holdout, decide whether 30k full-scale source sequence and actual rank 2/3 physical branch coverage should be inspected in separate clearly labeled **development seeds**, not leak confirmatory outcomes.

Original run: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41912345904
Raw artifact: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41912345904/artifacts/13362907059
