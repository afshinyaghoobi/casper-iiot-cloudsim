# CASPER JPDC — prespecified unmodified rank activation screen, seeds 41–44 (2026-11-04)

## Key result: rank 2 activates in real unmodified E45 workloads

An **a priori fixed four-seed mechanism screen** was registered before execution in `jpdc/S3_RANK_UTILIZATION_FROZEN_SEEDS_41_44_PREREG_2026-11-04.md` (commit `e6f2f6d50296d0c7da6fd14d8de192c3e4b6307c`). It explicitly chose *all* consecutive seed indices 41, 42, 43, 44, fixed S3_HIDDEN_NETWORK_50LOSS and the fixed six-node HIGH mask [9,12,14,15,17,18]. Frozen E42 Git blob `34256ca7bff46f911cf20e8b94278fbd09175746` and E4.6 were not modified. Workload, deadlines, calibration, confidence levels, eta policy and routing rule were NOT tuned to force multi-rank operation. Each seed used 80,000 calibration samples and 30,000 deployment tasks, eight policies, Java generated E45 and observational MISSION policy decision trace for FULL and HEALTH_STATIC. This is a mechanism coverage screen, **not a new performance superiority or statistical significance claim**.

**REAL GitHub Actions run 41782270007 finished SUCCESS in all four independent matrix jobs**, with both `JPDC_FROZEN_RANK_UTILIZATION_SCREEN_PASS` and `JPDC_FROZEN_RANK_SCREEN_OFFICIAL_COHORT_PASS` per seed. The second check validates independently reconstructed MISSION counts against original full eight-policy official CSV. Python independently recalculates the same rank-based node, certificate, and deadline-feasible conformal bounds using recorded Java *inputs*; zero decision parity failures.

| Seed | MISSION tasks per policy | FULL rank1 | FULL rank2 | STATIC rank1 | STATIC rank2 | Both rank3 | FULL rank2 rescues | STATIC rank2 rescues |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 41 | 1481 | 1472 | **9** | 1481 | 0 | 0 | **9** | 0 |
| 42 | 1488 | 1488 | 0 | 1488 | 0 | 0 | 0 | 0 |
| 43 | 1535 | 1535 | 0 | 1535 | 0 | 0 | 0 | 0 |
| 44 | 1479 | 1475 | **4** | 1478 | **1** | 0 | **4** | **1** |
| **Total** | **5983 per policy** | **5970** | **13** | **5982** | **1** | **0** | **13** | **1** |

In 14 actual Java MISSION decisions across both policies, rank1 upper bound did **not** meet deadline but rank2 bound did, and Java selected rank2, independently reproduced by Python. These are **deadline-feasibility certificate rescues**, not proof that task *realized* deadlines succeeded or that the policy outperformed baselines. The same mission workload is evaluated under both policies; do not treat 11,966 policy-task events as independent experimental replications. Independent seed sample is four.

## What explains activation differences (descriptive)

Let `U_r=pred_r + eta*qRank_r*(3+0.1*pred_r)*sigmaMultiplier_r` for the rth eligible node, ordered by predicted latency. Rank2 rescue requires `U_1 > deadline >= U_2`; rank3 rescue would also require rank2 infeasible if using the first-feasible decision rule.

Seed 41:
- FULL: **499** MISSION tasks with `U2 < U1`, 9 rank2 deadline rescues; STATIC: **214** tasks `U2 < U1`, zero rescues.
- Minimum `U2-U1` FULL **-6.14946856ms**, STATIC **-1.48520200ms**; `U3` never fell below `U1`.

Seed 42 and seed 43:
- All MISSION records under both policies had `U2>=U1` and `U3>=U1`, zero rank2/3 rescue/selection.

Seed 44:
- FULL: **468** tasks with `U2 < U1`, 4 rescues; STATIC: **176** with `U2 < U1`, 1 rescue.
- Minimum `U2-U1` FULL **-2.95053823ms**, STATIC **-0.91899949ms**; `U3` never fell below `U1`.

The recorded q-rank relation is `qRank[2] < qRank[1]` (second candidate's quantile below first's) in seeds 41 and 44, while `qRank[2] >= qRank[1]` in seeds 42 and 43. Rank3's q was >= rank1's in all four seeds. This is a contextual explanation, not a sufficient universal causal or mathematical condition: node-specific predicted latency and sigma multiplier matter.

The previously audited **seed40** had 1545 MISSION decisions/policy, all rank1; in that seed rank2/3 upper bounds exceeded rank1 for all observed tasks. This earlier seed40 was intentionally excluded from the fixed new 41–44 screen, so it cannot contaminate the prespecified seed selection.

## Scientific interpretation and limits

- The conclusion **"ranked selection is never used"** is demonstrably false across unmodified seeds. Rank2 is empirically exercised **but rare**; rank3 remains unobserved in these five examined S3 HIGH seeds.
- The contribution should be phrased carefully: rank-aware bound/certification can occasionally cause a genuine rank2 fallback under original workloads; the primary documented effect remains reliability/certification and selective abstention, not demonstrated broad rank switching.
- No comparison of rank2 and rank1 *actual* deadline outcomes has been carried out here. Avoid equating bound-feasibility rescue with realized deadline improvement.
- This screen used a single **instrumented** E45 run per new seed, not paired instrumented-vs-uninstrumented controls. Previous seed40 observational noninterference was verified, but do not claim per-seed noninterference was separately repeated here.
- These cross-language replays condition on Java-recorded 21-node predictions, calibrated qRank, eta, health state and task deadlines. They do not constitute independent simulation of feedback, predictor, queue mechanics, physical workload or full CASPER policy.
- Registered S2/S3 disjoint holdout exact sign test p=.0625 remains nonsignificant. Earlier exploratory four-seed mask/eta factorial exact sign p=.125 remains nonsignificant. Do not reclassify this mechanism screen as statistical confirmation or pursue a posthoc p-value.

## Evidence and reproducibility

- Frozen protocol: `jpdc/S3_RANK_UTILIZATION_FROZEN_SEEDS_41_44_PREREG_2026-11-04.md`, commit `e6f2f6d50296d0c7da6fd14d8de192c3e4b6307c`.
- Independent seed-aware detailed policy rank screen: `jpdc/screen_rank_utilization_unmodified.py`, commit `cde095f55af1dbd8907caff64d60d6e37221555c`.
- Actual matrix workflow: `.github/workflows/jpdc-s3-frozen-rank-screen-41-44.yml`, commit `3ee67e6a35f28cf72ec37666d26672af373845d4`.
- **All-jobs SUCCESS** https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41782270007.
- Saved original source artifacts for seed41 `13299876493`, seed42 `13299607377`, seed43 `13299343912`, seed44 `13299099239`, containing log, exact source SHA, results CSV, screen JSON, validation output.

## Next scientifically valuable work

1. Without modifying frozen E42/E4.6, inspect the **14 original rank2 selected task outcomes** separately using observed completion/deadline logger if needed, explicitly distinguishing feasible predicted upper bounds from actual observed success. Pre-register any comparisons; seed-level n remains four.
2. Implement genuinely independent policy-state simulation/health and E1.7 feedback in another framework (e.g. YAFS) and evaluate out-of-sample on an unmodified, prespecified input schedule. That is a distinct uncompleted claim.
3. If revising JPDC text, report this rank2 activation as evidence of code-path usage with all limitations, not as proof of general efficacy.
