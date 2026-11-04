# JPDC first preregistered independent native eight-policy 10-seed holdout — VERIFIED 2026-11-04

## Outcome upfront: completed and NOT statistically significant

The first fully preregistered native-Python 10-seed S2/S3 holdout **completed SUCCESS**, preserving every seed and the unchanged original primary analysis. Across ten reserved scientific seed indices **60–69**, the preregistered primary measure (equal-weight seed-average S2/S3 postchange MISSION deadline-miss rate of PRED_GREEDY minus CASPER_FULL) was **+0.0032083124668819615** (CASPER +**0.3208 percentage points** on average, descriptively). The preregistered **exact two-sided sign test p = 1.000**, with **five positive seeds, four negative and one exact tie (effective n=9)**. Thus **NO statistically supported superiority** in the native independent model (alpha .05). Do not transform these data into a positive efficacy claim. A fixed PRNG 10,000-resample seed-paired descriptive bootstrap 95% interval for mean benefit is **[-0.003060346399035438, +0.009882285010326505]** (in percentage points **[-0.3060, +0.9882]**), which includes zero. Median benefit +0.0005045408678102936 (+0.05045 percentage points).

### Original first registration, then real runs — auditable chronology
1. BEFORE any holdout run, the exact original protocol `jpdc/NATIVE_EIGHT_POLICY_HOLDOUT_PREREG_2026-11-04.md` was committed **`a7e992403d4a82ea787f3144d15b1a3950039dde`**, declaring all 10 untouched seeds (excluding earlier development indices 40–44/50–51), full independent 80k calibration per seed, S2 and S3 original hidden shock, 30k deployment per policy, every eight frozen original E42 policies, a SINGLE primary FULL-vs-GREEDY equal-weight seed-level contrast, exact two-sided sign test with exact-zero ties excluded, no dropout or seed substitution, 10000 fixed-PRNG bootstrap and secondary mechanism reporting only. This was *not* preregistered after seeing holdout.
2. The per-seed fail-closed `jpdc/run_native_eight_holdout_seed.py` was committed `d8b9c56f677f9422bdb3821d8912bdcd3c70a2a9`. The primary statistical analyzer `jpdc/analyze_native_eight_holdout.py` was committed `3ae610afb6fcce2caf0146992134a5d989d10ba4`. The corrupt/duplicate/missing cohort rejection and exact sign test fixture suite `jpdc/test_native_eight_holdout_statistics.py` was committed `7156afd5c1a7823fcb7bd9c3ce9997b5f7a6fff6`. Thus source, statistic, test thresholds and seed selection were frozen **before** any result.
3. **Original GitHub Actions run 41920321822 COMPLETED SUCCESS**, source commit `8d2885b542aabe15012fdf7ef53db22b71dddf48`. Original frozen E42 git blob was checked `34256ca7bff46f911cf20e8b94278fbd09175746`, original E4.6 not edited. Frozen-gate CI passed; all 10 GitHub Actions seed jobs completed SUCCESS; **160** scenario-policy runs ×30k = **4,800,000 task-policy executions**, and 10 separately native independent 80k calibrations = 800,000 original-model calibration task executions. Source model RNG, hashed CPU stochastic noise, network shocks, physical strict FIFO queue completion/latency, ranked conformal calibration, 21-node health and E17 policy feedback are all independently computed in Python; no Java output is fed in.
4. Within original run `41920321822`, **seed60** calibration+16 full-scale policy simulations were independently repeated and its complete result JSON was **byte-identical**. The **preregistered-analysis** job succeeded ONLY after all 10 seed artifacts were present, producing original artifact **13367565614**. It printed `JPDC_NATIVE_HOLDOUT_COMPLETE_PREREGISTERED_ANALYSIS_PASS` and `JPDC_NATIVE_HOLDOUT_ORIGINAL_PREREGISTERED_PRIMARY_INFERENCE_PASS`.
5. A SEPARATE subsequent purely reporting workflow downloaded the **immutable original results** and did **NOT** rerun the experiment, change data, or recalculate a new hypothesis: real run **41920792886 SUCCESS**, archived report artifact **13366842219**. Reporting-only logs verified original sign p, ten per-seed effects, fixed bootstrap interval, native original rank utilization and descriptive comparisons. All inferential conclusions are from original preregistered analysis and unchanged.

## Every prespecified scientific seed effect (GREEDY minus FULL; percentage points)
Positive = lower MISSION postchange miss rate under CASPER_FULL.

| Original seed index | Difference (percentage points) | Direction |
|---:|---:|---|
| 60 | -0.1599 | CASPER worse |
| 61 | 0.0000 | tie |
| 62 | -0.6931 | CASPER worse |
| 63 | +1.5432 | CASPER better |
| 64 | -1.3000 | CASPER worse |
| 65 | +0.1009 | CASPER better |
| 66 | -0.1035 | CASPER worse |
| 67 | +0.1499 | CASPER better |
| 68 | +1.4344 | CASPER better |
| 69 | +2.2364 | CASPER better |

All ten effects were used; zero effect removed only from the sign test denominator according to the *original* protocol and remains in mean and bootstrap.

## Descriptive secondary scenario summary (10 seeds, original 30k tasks/policy)

| Scenario | Policy | Mean seed-level postshock MISSION miss rate | Total ALL MISSION deadline misses across ten seeds | Mean postshock certificate issuance rate |
|---|---|---:|---:|---:|
| S2 compute loss | PRED_GREEDY | **3.282722%** | 367 | 0 |
| S2 compute loss | CASPER_HEALTH_STATIC | **2.557971%** | 299 | 93.8534% |
| S2 compute loss | CASPER_FULL | **2.557971%** | 299 | 92.9462% |
| S3 network loss | PRED_GREEDY | **6.130041%** | 647 | 0 |
| S3 network loss | CASPER_HEALTH_STATIC | **6.213129%** | 655 | 96.8654% |
| S3 network loss | CASPER_FULL | **6.213129%** | 655 | 87.9553% |

The original total MISSION misses include both pre/postshock tasks and are **not** the primary metric, which is restricted to postshock original MISSION cohort. Raw original postshock rates in immutable artifact are authoritative. Scenario-specific S2 benefit is 0.72475 percentage points; S3 difference is **-0.08309 percentage points** (worse for FULL), both descriptive and not multiplicity-controlled inferential claims. FULL vs HEALTH_STATIC has the same aggregate MISSION miss counts/rates in these scenario summaries despite altered E17 certification percentages: do not imply E17 improved actual missed deadlines.

### Mechanism branch utilization from original untouched holdout
20 original full-scale runs per policy (10 seeds ×2 shock scenarios; ~29462 MISSION tasks/policy):
- CASPER_FULL: **29,423 rank1, 39 rank2, zero rank3**; actual rank2 decision logic is now seen on genuinely native simulated 30k deployment trajectories (unlike previous 12k development cells).
- CASPER_HEALTH_STATIC: **29,453 rank1, 9 rank2, zero rank3**.
- CASPER_ADAPT_NO_HEALTH: **29,399 rank1, 63 rank2, zero rank3**.
- RANKED_CP_STATIC: **29,452 rank1, 10 rank2, zero rank3**.
- CLOUD_ONLY, EDGE_FIRST, PRED_GREEDY and GLOBAL_CP: 29,462 rank1 each; no rank2/3.
- S2 FULL **60 health detector alarm transitions** across the ten runs; S3 FULL zero observed. FULL eta>1 in **163288 S2 dispatches and 246153 S3 dispatches**, showing active E17 paths; no evidence this improved deadline-miss rates. Positive rank2 branch usage is a code-path observation, **not** rank1 counterfactual efficacy, nor statistically significant superiority.

## Critical interpretation and limits
The completed native Python system is a **genuinely independently executing physical strict FIFO discrete-event simulator**, with independently generated calibration reference scores, workload, service noise, virtual queue telemetry, and eight original-model policies. It is still a *reimplementation of the same generative experiment*, NOT an independent workload distribution/industrial dataset and **NOT YAFS**. It deliberately differs from original Java CloudSimPlus SpaceShared task-admission behavior. The *previous* separately preregistered Java-to-Python strict chronological FCFS physical fidelity gate (original run41773297282) remains **FAILED**: max wait error 9.1214ms > fixed5ms. Neither new success nor native original-like source computations retroactively change that classification.

Original separate frozen confirmatory S2/S3 Java holdout exact sign p=.0625 **NONSIGNIFICANT**, earlier exploratory factorial exact sign p=.125 **NONSIGNIFICANT**, unchanged. This new fully independent native holdout **also does not show statistically supported FULL-vs-GREEDY improvement** (p=1.0). Report all three without selective emphasis. Despite positive average paired effect in native model, it is small, heterogeneous and not significant. Do not mine the held-out data for a new primary endpoint, seed subset, or alternative significance test. Additional counterfactual rank2 mechanism probes on the now-seen seeds are exploratory and must be labeled; new untouched seeds would be needed for any new confirmatory claim.

## Evidence
- Preregistered protocol and fixed exact analysis source: `jpdc/NATIVE_EIGHT_POLICY_HOLDOUT_PREREG_2026-11-04.md`, `jpdc/analyze_native_eight_holdout.py`.
- Original all-ten-seed SUCCESS workflow: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41920321822
- Immutable original primary + all-eight secondary artifact: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41920321822/artifacts/13367565614
- Archived reporting-only workflow: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41920792886
- Reporting original-output archive: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41920792886/artifacts/13366842219

## What to do next
Write JPDC results as methodological validation with measured limitations; do not reframe these nonsignificant efficacy results as positive. Evaluate/strengthen actual novelty rather than just numerical parity. Consider external implementation in YAFS or independently sourced workload traces, and a separately preregistered new scientific hypothesis if an improved algorithm genuinely adds an original technical mechanism. Do not tune original frozen CASPER simply to create rank3. Review a potential mismatch in original `family_covered` counterfactual diagnostics (strict FCFS vs CloudSim queue admission) before claiming empirical conformal coverage. No additional claims without new validated data.
