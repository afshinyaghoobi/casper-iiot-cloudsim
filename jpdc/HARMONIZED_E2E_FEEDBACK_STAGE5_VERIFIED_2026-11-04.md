# JPDC Stage 5: harmonized end-to-end feedback timing VERIFIED (development seed81, 2026-11-04)

## What changed, and why
The original independent Python Stage4 CASPER_FULL has E17.observe(score) called at physical CPU-service completion, while the NEW_NETWORK_RESIDUAL method implemented in the earlier seed80 network risk pilot observes network delay only at a **later** independently scheduled end-to-end timestamp (CPU finish + network delay). This creates a measurable pre-dispatch information asymmetry. Under this Stage5 protocol, **both adaptive E17 score feedback and network residual feedback are withheld until the same end-to-end event timing**, while CPU-specific NodeHealth may be updated upon physical CPU service completion (because its measured service time is already observable). Strict FIFO physical CPU remains unchanged; this is **not packet-level network transport** and not equivalent to original CloudSimPlus SpaceShared.

Before any new run, `jpdc/HARMONIZED_E2E_FEEDBACK_STAGE5_PREREG_2026-11-04.md` registered **previously unused but DEVELOPMENT-only scientific seed index81** (seed81 now exposed), one independent original-model 80k native physical calibration, S2 hidden compute and S3 hidden network scenarios, 12000 tasks × three policies PRED_GREEDY, CASPER_FULL, NEW_NETWORK_RESIDUAL => six 12k scenarios/policy runs / **72,000 task-policy outcome observations**, with mechanical no-early-feedback tests, baseline original physical engine regression and full byte-identical rerun; **no p-value or efficacy claim**. This is not an untouched new statistical holdout or a replacement for seed80.

### Technical realization

Standalone alternate physical engine `jpdc/independent_harmonized_e2e_feedback_stage5.py` (commit `6f4cc4ac5c3e2474a436a0960072793b2072d481`) was generated as a **new separate file**, leaving the prior seed80 engine, original Stage4 policy and frozen E42/E4.6 unchanged. Event heap ordering: CPU service finish kind0, fully observed end-to-end feedback kind1, new arrival kind2. At CPU finish the physical server is freed and next node queue job starts, service-health state may update, but **NO E17 score and NO new network-excess observation** is supplied to policy. E17 receives only MISSION score exactly once in kind1 E2E feedback and the new policy's node risk likewise observes completed network feedback in kind1. E2E event is scheduled at `CPU_finish+actual_network_ms`; explicit fail-closed guards ensure no premature feedback, exactly 12000 CPU finishes, 12000 E2E callbacks, 12000 network observations and, under FULL, exactly one E17 observed feedback per MISSION. Stable event tie ordering and strict FIFO queue conservation preserved.

Original independent E17 reference remains native Stage3 fully independent calibration scores, not original Java data. Source `jpdc/run_harmonized_e2e_feedback_stage5.py` (commit `cb0570db600334e6480070065aec86d2091d24ca`) compares greedy physical outcomes against the earlier unchanged Stage4 independent simulator for each S2/S3 scenario and prints old vs harmonized FULL E17 eta>1 decision counts and physical outcomes without interpreting divergence as automatically beneficial. Unit `jpdc/test_harmonized_e2e_feedback_stage5.py` (commit `dded4378efa638e525cc0a63ab8b55f197cf763e`) verifies source event placement and an actual 10010-task physical E2E feedback smoke test; this source check does not constitute independent second-simulator transport semantics. Workflow `.github/workflows/jpdc-harmonized-e2e-stage5-once.yml` (commit `74dc8475817f6a481b7b3ff72bc5b7785ee8ade2`) ran original frozen source check and repeated the **entire fixed six-arm result** byte-identically.

**REAL GitHub Actions run 41966056585 SUCCESS**, job127043208374, raw data artifact **13387302669**. Marks: `JPDC_STAGE5_E2E_FEEDBACK_TIMING_UNIT_PASS`, `JPDC_STAGE5_UNCHANGED_GREEDY_ORIGINAL_PHYSICAL_PARITY_PASS` (both scenes), `JPDC_STAGE5_HARMONIZED_E2E_COMPLETE_PHYSICAL_PILOT_PASS`, `JPDC_STAGE5_HARMONIZED_FULL_MATRIX_BYTE_REPRODUCIBLE_PASS`, `JPDC_STAGE5_ORIGINAL_E2E_HARMONIZATION_EVIDENCE_AUDIT_PASS`.

An *additional read-only* archive workflow `.github/workflows/jpdc-stage5-archived-feedback-report.yml` (commit `34ffd742ef2756ea60e701bd5e0d91d378a510a8`) downloaded the exact original artifact, did **not** rerun or alter science, and emitted old-vs-new E17 counts. **REAL GitHub Actions run41966192044 SUCCESS**, job127043624742, marker `JPDC_STAGE5_IMMUTABLE_ARTIFACT_DIAGNOSTIC_AUDIT_PASS`.

## Original seed81 development results (all 6 × 12000 physical outcomes)

| Scenario | Policy | All MISSION deadline misses | Postshock MISSION miss rate | Positive completed network-excess observations | Postshock damaged-node dispatches | NEW risk reroutes from same-trajectory greedy | eta>1 dispatches |
|---|---|---:|---:|---:|---:|---:|---:|
| S2 compute loss | PRED_GREEDY | **0** | 0 | 0 | 333 | 0 | 0 |
| S2 compute loss | CASPER_FULL | **0** | 0 | 0 | 16 | 0 | **7002** |
| S2 compute loss | NEW_NETWORK_RESIDUAL | **0** | 0 | 0 | 333 | **0** | 0 |
| S3 network loss | PRED_GREEDY | **0** | 0 | 351 | 351 | 0 | 0 |
| S3 network loss | CASPER_FULL | **0** | 0 | 349 | 349 | 0 | **7035** |
| S3 network loss | NEW_NETWORK_RESIDUAL | **0** | 0 | **11** | **11** | **483** | 0 |

During S3 NEW network-risk operation, **1974 task arrivals** encountered a nonzero observed penalty; the network-risk policy selected a different physical node than same-state nominal GREEDY at **483 arrivals**. Its postshock damaged-node dispatch count of 11 was descriptively lower than the separately simulated PRED_GREEDY count 351 (different future queue trajectories; NOT a controlled per-task causal counterfactual). The same policy did not activate risk under S2 compute-only degradation, exactly matching GREEDY's 333 affected-node dispatches.

**Crucial limitation:** in seed81 all six 12k runs had **zero MISSION deadline misses**. The absence of missed deadlines means this fixed development seed cannot discriminate policy deadline efficacy at all. Do not claim zero missed deadlines proves safety, rank superiority or formal calibration reliability; this is a stress-insensitive cohort for the primary outcome. No retrospective seed substitution or threshold tuning allowed.

### Direct old vs harmonized FULL timing comparison (from original archived artifact)

| Scenario | Original E17 eta>1 dispatch count (CPU-time observed) | Harmonized E17 eta>1 dispatch count (E2E-time observed) | Difference | Native FULL MISSION miss count changed? | FULL 21-node dispatch histogram changed? |
|---|---:|---:|---:|---|---|
| S2 | 6997 | **7002** | +5 | No (0 vs 0) | No |
| S3 | 7033 | **7035** | +2 | No (0 vs 0) | No |

Thus harmonizing the observable E17 feedback time **did change the adaptive state path** slightly, but not physical dispatch allocation or Mission deadline outcomes on this fixed seed at this horizon. This is a documented mechanism/timing repair, **not evidence of improved scheduling efficacy**.

## Interpretation and next requirements

1. Stage5 fixes the **E17 vs network residual late-feedback timing asymmetry within this new model**, while health CPU feedback appropriately stays earlier. It does **not** implement physically distinct upstream transfer + CPU queue + downstream transfer or network congestion. Since nominal network duration is fully placed *after CPU* for observation, original end-to-end decomposition remains stylized and there is not yet a realistic second transport model.
2. NEW network penalty learns only from selected nodes. Its pronounced avoidance can reduce further observations of damaged nodes (informational starvation/selection bias). Next development study should **formally preregister sparse unbiased network-only exploration and/or confidence expiration** while measuring true coverage and exploration cost, without using hidden affected-node IDs as pre-dispatch inputs.
3. Even with matched observation timing, the two controllers use **different information types and feedback sample sizes**: E17 sees MISSION-only normalized E2E residuals, NEW sees all task criticalities' node-local network residuals. This is an intended policy design difference, not a matched-information comparison. Do not call the controllers statistically or information-theoretically equivalent.
4. Existing scientifically registered native 10-seed CASPER_FULL vs PRED_GREEDY exact two-sided sign p=1.000 nonsignificant, Java disjoint sign p=.0625 nonsignificant, four-seed factorial sign p=.125 nonsignificant unchanged. Old strict CloudSimPlus vs Python chronological FIFO physical queue fidelity gate **FAILED** max wait9.1214ms>predeclared5ms; native independent model is strict FIFO, NOT YAFS and not independently sourced industrial task arrivals.
5. Stage5 is **developer seed81 only**, as is seed80. Do not reuse 80/81 in a later untouched confirmatory set; do not change 32-slot network risk window, min8 warm-up and q90 after these already observed outcomes while describing such modified code as unchanged preregistered method.
6. The complete first FGCS manuscript already includes E17 adaptation and network-only fault blind spot; formal novelty against broader network-risk scheduling literature is not yet cleared. No new JPDC paper submission claim.

## Links
- Original Stage5: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41966056585
- Stage5 original raw artifact: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41966056585/artifacts/13387302669
- Archive read-only run: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41966192044
