# CASPER JPDC — independent calibration rank schedule and REAL CloudSim qhat verification (2026-11-04)

## Two new successfully executed cross-language calibration gates

### Gate 1 — independent calibration workload allocation and conformal quantile function
- Preregistered before execution: `jpdc/INDEPENDENT_CALIBRATION_RANK_QHAT_PREREG_2026-11-04.md`, commit `8677e2a07722aa91f189d5c69dcc9fb1003deb3d`.
- Python source-independent `java.util.Random.nextInt(bound)`, Java Collections.shuffle, original 80k calibration task-stream regeneration using calibration seed XOR `0xCA11B4A7`, mission task rank assignment using `seed ^ 0xA11CE77`, and `qhat` with (k=\lceil(n+1)(1-\alpha)\rceil) added to `jpdc/independent_workload_generator.py`, commit `b9a83394a7a4027409dd48f7747604a3f3da2b20`.
- Read-only frozen E42 Java reflection harness `jpdc/java_tests/OriginalCalibrationReferenceHarness.java`, commit `74076b63c2f91b7ac0eb389b460ba4c19e67936d`. Independently generated Python audit `jpdc/audit_independent_calibration_rank_qhat.py`, commit `c26b9347852429b465dce561c83697e8288eabe5`; later corrected sentinel recognition (not scientific values) in `0de50e9c2ae913dd930781209de557140b5cffab`.
- Original first workflow `41893671698` FAILED only because Python's reference parser accidentally excluded the Java completion marker `JPDC_CALIBRATION_REFERENCE_COMPLETE` from the filtered stream even though it had already matched **all 3501** rank allocations and **40** qhat fixtures. Corrected parser then reran same preregistered gate.
- **Real GitHub Actions run 41893849635 SUCCESS**, original artifact **13353419285**, exact original-code reference on seed index40/scientific seed4202202640. **All 3501/3501 post-burnin MISSION rank labels** assigned by independent Python generator/shuffle matched the frozen Java ranks; **40/40** independent conformal quantile edge-case fixtures matched the original qhat, including positive infinities for insufficient sample size. Deliberate rank-label mutation was rejected, `JPDC_INDEPENDENT_CALIBRATION_MUTATION_REJECTED_PASS`.

### Gate 2 — independent qRank/qGlobal/health threshold estimation using REAL CloudSim outcome scores
- Pre-execution protocol `jpdc/REAL_CALIBRATION_SCORES_INDEPENDENT_QHAT_PREREG_2026-11-04.md`, commit `50102a8ed251a96c96c385335c22ca6b3ef22647`.
- Purely observational generated E45-only source patch `jpdc/instrument_real_calibration_scores_generated_e45.py`, commit `ec383b3786e51e31b026b829b1d81b4014494885`, records 70k post-burnin actual service-to-nominal ratios, all post-burnin MISSION nonconformity scores, original rank assignments and selected node, and original **unrounded** qRank/qGlobal/tier threshold summaries. Doesn't change the original calibration formulas or scheduling.
- Independent Python scorer `jpdc/replay_real_calibration_quantiles.py`, commit `f529ae905092c466a0ace972c2b9a0422dc45e05`, independently regenerates the 80k calibration workload/rank labels, checks no missing/extra/duplicate records, checks each native score matches the correct independently assigned rank and task/node, reconstructs all quantiles from **raw Java-observed service and nonconformity samples**. Alpha = `[.006,.003,.001]` for qRank, `.01` for qGlobal and for tier health thresholds. No Java-produced q values consumed as estimator inputs.
- Paired 80k calibration / 30k deployment uninstrumented control and observational generated E45 simulation on original S3 HIGH seed40, affected mask [9,12,14,15,17,18]. Frozen E42 git blob SHA `34256ca7bff46f911cf20e8b94278fbd09175746` and E4.6 unchanged.
- **Real GitHub Actions run 41894270042 SUCCESS**, original artifact **13355212469**. `JPDC_REAL_CALIBRATION_SCIENTIFIC_PARITY_PASS`: every 8-policy official scientific summary field unchanged except non-scientific mapper timing. `JPDC_REAL_CALIBRATION_INDEPENDENT_QHAT_PASS`: all source quantities match Python re-estimates at <=1e-10ms. `JPDC_REAL_CALIBRATION_CORRUPTION_REJECTED_PASS`: malformed mission score record correctly rejected.

| Actual 80k calibration observation | Count or independently computed value |
|---|---:|
| Post-burnin service ratio samples | **70000** |
| Real mission nonconformity samples | **3501** |
| qRank sample counts | **1167 / 1167 / 1167** |
| Tier health sample counts | **757 / 56672 / 12571** |
| independent qRank[1] | **1.322830243267578** |
| independent qRank[2] | **1.6564031648878383** |
| independent qRank[3] | **1.539905477306746** |
| independent qGlobal | **0.9048799173085066** |
| tier health threshold 0 | **1.2838687972516774** |
| tier health threshold 1 | **1.269565143974892** |
| tier health threshold 2 | **1.27989658405091** |

## What independent means, and what still is not proven

**Now independent Python generation and cross-language validated:** original five-scenario 150k task workload and 21 nodes (run41889381945), zero-VQ-backlog 10500 nominal network/service/latency predictions (run41889848805), 80k original calibration task rank allocation, E42 qhat mathematical function, 3501 **REAL CloudSim-derived** MISSION qRank/qGlobal and 70000 service ratio-derived tier thresholds, and previous independent E17 state, node-health and virtual-queue state replay (runs41848215650,41873772600,41874289007).

**Not yet independent:** the physical service times, CloudSim VM scheduler behavior (including observed SpaceShared waiting task bypass), calibration *nonconformity score inputs* produced from those outcomes, true telemetry, full interdependent state/update event scheduling in an independent second engine, or policy-level generalized efficacy. Thus do not call this a complete independent CloudSim-vs-YAFS validation or a new performance holdout. Existing independently preregistered FCFS physical queue gate 41773297282 remains FAILED (max absolute wait 9.1214ms > original 5ms bound), original disjoint n10 S2/S3 sign p=.0625 nonsignificant and exploratory 4-seed factorial p=.125 nonsignificant, unchanged.

Previously reported rare genuine original rank2 route selections in four untouched S3 HIGH seed indices 41..44: 14 rank2 policy-task decisions, 14/14 selected tasks actually finished by deadline in a **post-selection** explanatory follow-up; no rank1 counterfactual, rank3 unobserved. Do not use as efficacy effect size.

## Next technical milestone
Integrate independent Python task generation + nominal predictor + rank calibration + E17/health/VQ state with **a separately specified discrete-event physical queue engine**, define explicit admission semantics, and test on new prespecified holdout seeds, including original baselines, before any claim about external policy performance. Be transparent about CloudSim SpaceShared bypass; do not retroactively soften original FCFS failure.

## Verified runs and artifacts
- Original rank/qhat formula success: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41893849635, artifact 13353419285
- Real original score quantile success: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41894270042, artifact 13355212469
- Independent original workload + nominal model success: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41889848805
