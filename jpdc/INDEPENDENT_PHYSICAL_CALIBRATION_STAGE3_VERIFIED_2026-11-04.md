# JPDC Stage 3 — native independent physical calibration on original-model workloads (verified 2026-11-04)

## New technical contribution and provenance

The previous verified clean-room native Python physical stochastic engine simulated original-model source-generated workloads, original deterministic service noise and compute/network shocks but only baseline policies (Stage 2 success run 41899450893). The new Stage 3 goes beyond Java-sourced calibration score replay by generating the **complete S0 calibration workload and the actual physical completion times, CPU wait and realized service entirely inside Python**, then computing original-model mission conformal residual scores and tier health thresholds from those *native* physical outcomes.

**Protocol was committed before execution:** `jpdc/INDEPENDENT_PHYSICAL_CALIBRATION_STAGE3_PREREG_2026-11-04.md`, commit `5906a4d1e60402b512019146af4b0ac93322eca9`, fixed seed indices 50 and 51, 80k calibration tasks per seed, 10k burn-in, original MISSION rank-shuffle allocation and original sparse NORMAL probe cadence. E42 git blob SHA `34256ca7bff46f911cf20e8b94278fbd09175746` and original E4.6 never changed. No Java-generated calibration service times, residual scores, qRank, qGlobal or health-tier thresholds are used as inputs.

- New independently executing calibration event simulator: `jpdc/independent_physical_calibration_stage3.py`, commit `9ff2b24894948f4a69c58280e5a066c5787f989e`.
- Registered fixed seed matrix driver: `jpdc/run_independent_calibration_stage3.py`, commit `2016ee8b1f988f839daee3a366d8cc0c07cf9175`.
- Independent adversarial/small-scale tests: `jpdc/test_independent_calibration_stage3.py`, commit `3f5b5a66ec59069822798b90c9f6b53be492a3de`.
- Real CI workflow: `.github/workflows/jpdc-independent-physical-calibration-stage3.yml`, commit `a8fabce8d501cb11a75f1cb0827f69b5814942c9`.

### Actual GitHub Actions and evidence
**REAL GitHub Actions run 41906886928 SUCCESS**, with artifact **13361690352**. Its logs show:
- `JPDC_NATIVE_CALIBRATION_STAGE3_UNIT_PASS`: independent small-run mission-rank and service-ratio conservation, actual sparse probes and malformed sample rejection.
- `JPDC_NATIVE_PHYSICAL_CALIBRATION_STAGE3_PASS`: both original-source-model 80k-event calibration runs finished and every physical task was dispatched/completed exactly once, each postburnin service ratio and all mission nonconformity scores derived from native Python physical completion.
- `JPDC_NATIVE_STAGE3_FULL_CALIBRATION_BYTE_REPRODUCIBLE_PASS`: repeated **full two-seed 80k calibration matrix**, with byte-exact normalized JSON output.
- `JPDC_NATIVE_STAGE3_INDEPENDENT_CALIBRATION_QUANTILE_AUDIT_PASS`: finite quantiles, group conservation and complete results verified.

The reported **160,000 calibration tasks** are the total in a single two-seed matrix (80k per seed). The identical second matrix execution is a reproducibility rerun, not an additional independent experimental replication.

| Physical calibration metric | Seed index 50 | Seed index 51 |
|---|---:|---:|
| Scientific seed | 4202202650 | 4202202651 |
| Native Python task arrivals/completions | 80000 / 80000 | 80000 / 80000 |
| Postburnin service ratios | 70000 | 70000 |
| Postburnin MISSION nonconformity scores | 3419 | 3575 |
| Independent calibration ranks 1/2/3 | 1140 / 1140 / 1139 | 1192 / 1192 / 1191 |
| Independent qRank[1] | 1.1639370670471874 | 0.9021160123660767 |
| Independent qRank[2] | 1.68628546687794 | 1.3174003661486557 |
| Independent qRank[3] | 2.548828407791089 | 2.0085003812552262 |
| Independent qGlobal | 0.8560106655051337 | 0.6928342768190033 |
| Tier ratio sample counts 0/1/2 | 2402 / 54345 / 13253 | 595 / 53498 / 15907 |
| Tier qhat thresholds 0/1/2 | 1.3261312650938832 / 1.2704683624777615 / 1.279733984766549 | 1.2971690117703178 / 1.2620622680956846 / 1.270307553623448 |
| Sparse probes actually selected | 639 | 641 |

Original-model calibration logic independently implemented: original 48-bit seeded JavaRandom workload + calibration rank shuffle, 21 independently generated node specs, 50ms virtual-queue telemetry driven by independent physical next-free, MISSION postburnin top-three rank routing, other task greedy/probe routing, sparse original NORMAL budget, native stochastic source service noise, strict nonpreemptive FIFO physical queues, finish-time service/nominal ratios, exact original qhat alpha [.006,.003,.001] rank, .01 global and per tier.

## Scientific boundary
**Established:** the first complete *native-physics* independent calibration stage within the Python event-driven simulator. No original Java physical completion or residual score input is needed to estimate the numerical qRank and tier health thresholds inside this engine, unlike prior real Java-event conditional qhat replay.

**Not established:** complete independent CASPER adaptive ranked deployment / certificate, E17 feedback+health/probe lifecycle in deployment, same numerical CloudSim calibration or queue equivalence, YAFS runtime evaluation, superiority to baselines or a new statistically significant scientific holdout. The qRank and health thresholds in this independent strict FCFS engine differ appropriately from original CloudSimPlus SpaceShared physics. The original prespecified Java-vs-Python chronological FCFS physical queue transfer test `41773297282` remains **FAILED**, max 9.1214ms wait error > predeclared 5ms; this new independent calibration does not retrospectively repair that gate.

The previously registered ten-seed S2/S3 holdout exact sign p=.0625 and exploratory four-seed factorial sign p=.125 remain NONsignificant. Rare original actual rank2 selection on S3 seed indices 41–44 (14 policy-task decisions, with actual on-time task outcomes in postselection exploratory followup) remains evidence of code-path usage, not a rank1 counterfactual improvement.

## Next technical gate
Implement full original-model CASPER ranked eligible-node selection, health alarm handling, E17 dual-memory adaptive eta, sparse probes and certificate/abstention outcomes in the independent Python physical event deployment. Its calibration source must be **Stage3 native qRank, qGlobal, health thresholds and raw mission reference scores**, not copied Java original scores. A new predeclared never-before-used seed/scenario policy-vs-baseline holdout should then be run at seed-level sample units. Beware that today's Stage3 summary exports only aggregate q/tier and counts; for E17 constructor the independent calibration engine must safely expose the actual native raw mission reference-score sequence in a separate auditable internal artifact or new in-memory interface, with science invariance and no Java imports.
 
### Provenance
- CI run: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41906886928
- Original artifact: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41906886928/artifacts/13361690352
