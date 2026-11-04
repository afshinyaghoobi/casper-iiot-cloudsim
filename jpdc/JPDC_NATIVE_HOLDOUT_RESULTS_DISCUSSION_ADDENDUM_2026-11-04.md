# JPDC manuscript addendum — independent native simulation and preregistered ten-seed holdout
*Drafted November 4, 2026. American English. Evidence-grounded Results and Discussion copy; not a claim of publication readiness.*

## Results: independently executed native Python validation

### Cross-implementation design and scope

To assess whether the proposed online scheduling mechanisms could execute outside the original Java runtime, we built an independently executing discrete-event implementation in Python. The Python program generates workload arrivals and task attributes, heterogeneous node specifications, noise-perturbed service times, and compute/network degradation from the preregistered scientific seeds. It independently computes calibration outcomes from task completions rather than importing Java residuals: each seed receives 80,000 calibration tasks (10,000 burn-in), and the native completion events determine the ranked conformal quantiles, the global quantile, and node-tier health thresholds. The deployment engine also implements its own virtual-queue predictions, health alarms, feedback to the E17 adaptation mechanism, and eight baseline/ablation policy variants.

The physical queue model is **a nonpreemptive, single-server FIFO queue at each of 21 nodes**. This design is distinct from the original CloudSim Plus SpaceShared queue implementation. Earlier direct queue-fidelity testing found a maximum waiting-time discrepancy of 9.1214 ms against a preregistered 5 ms criterion, and forensic event review demonstrated an instance of a newly submitted task overtaking an older waiting task in the Java runtime. Consequently, the two implementations are not physically equivalent. The Python experiments provide a cross-language **independent implementation under explicitly different queue semantics**, not a YAFS replication or validation against real industrial traces.

Prior to observing any of the confirmatory native-Python results, we fixed ten previously unused seed indices (60–69), two hidden-degradation scenarios, the eight scheduling policies, the primary outcome, and the statistical test. Each seed had one independently executed 80,000-task calibration. Each scheduling policy was evaluated on 30,000 deployment tasks under both a 40% compute-capacity loss at affected nodes (S2) and a 50% bandwidth loss (S3), beginning at task index 10,000. The study therefore includes **160 policy-by-scenario simulations and 4,800,000 task-policy executions**, with ten independent seeds as the analysis units. Within a seed and scenario, policy comparisons use the same source-generated workload; individual tasks are not treated as independent experimental replicates.

### Preregistered primary comparison

The primary endpoint was the post-change MISSION-task deadline-miss rate. We compared CASPER_FULL against PRED_GREEDY and, for each seed, equally weighted the difference in miss rates (greedy minus full) across S2 and S3. A positive difference means fewer missed deadlines under CASPER_FULL. Inference used the preregistered *two-sided exact sign test* at alpha = 0.05; exact-zero ties were excluded from the sign-test denominator but retained when computing the average effect.

Across the ten seeds, five differences favored CASPER_FULL, four favored PRED_GREEDY, and one was an exact tie. The seed-level mean difference was **+0.3208 percentage points** in favor of CASPER_FULL, and the median was **+0.0505 percentage points**. The **two-sided exact sign-test p-value was 1.000**, which does not support a statistically significant reduction in missed deadlines. A secondary, prespecified descriptive seed-level bootstrap yielded a 95% percentile interval for the mean difference of **[−0.3060, +0.9882] percentage points**, including zero. The bootstrap interval does not replace the designated exact test. The observed effect was small and heterogeneous; the higher value of the mean relative to the median reflects variation across the seeds, not consistent superiority.

| Seed index | Difference in post-change miss rate (greedy minus full, percentage points) |
|---:|---:|
| 60 | −0.1599 |
| 61 | 0.0000 |
| 62 | −0.6931 |
| 63 | +1.5432 |
| 64 | −1.3000 |
| 65 | +0.1009 |
| 66 | −0.1035 |
| 67 | +0.1499 |
| 68 | +1.4344 |
| 69 | +2.2364 |

No seed was excluded or replaced after results were inspected. All ten seed jobs and the prespecified aggregate-analysis job completed successfully; seed 60 was additionally rerun end-to-end and produced a byte-identical output artifact. This is a reproducibility check, not an additional independent observation.

### Scenario-level outcomes and certification behavior

The following secondary summaries average *per-seed post-change MISSION miss rates*, giving each seed equal weight. The counts of missed deadlines are provided separately for **all MISSION tasks, including pre-change arrivals**, and therefore should not be used as denominators for the primary post-change endpoint.

| Scenario | Policy | Mean post-change MISSION miss rate | All-MISSION deadline misses across ten seeds | Mean post-change certificate issuance rate |
|---|---|---:|---:|---:|
| S2 compute loss | PRED_GREEDY | 3.2827% | 367 | Not applicable |
| S2 compute loss | CASPER_HEALTH_STATIC | 2.5580% | 299 | 93.8534% |
| S2 compute loss | CASPER_FULL | 2.5580% | 299 | 92.9462% |
| S3 network loss | PRED_GREEDY | 6.1300% | 647 | Not applicable |
| S3 network loss | CASPER_HEALTH_STATIC | 6.2131% | 655 | 96.8654% |
| S3 network loss | CASPER_FULL | 6.2131% | 655 | 87.9553% |

In S2, the average post-change miss rate was descriptively **0.7248 percentage points lower** under CASPER_FULL than under PRED_GREEDY. In S3, it was **0.0831 percentage points higher** under CASPER_FULL. These are exploratory scenario-specific summaries and were not subjected to separate confirmatory tests. CASPER_FULL and CASPER_HEALTH_STATIC had identical aggregate deadline-miss outcomes in these two scenario summaries, even though E17 adaptation changed certificate issuance; thus these results do not establish a deadline-completion benefit attributable to E17.

The independently simulated trajectories also exercised several internal mechanisms without artificially activating their branches. Across 20 seed-by-scenario runs per policy, CASPER_FULL selected rank 2 on **39 MISSION tasks**, CASPER_HEALTH_STATIC on **9**, CASPER_ADAPT_NO_HEALTH on **63**, and RANKED_CP_STATIC on **10**. All remaining MISSION decisions in these four policies selected rank 1; **rank 3 was never selected**. The three uncalibrated baselines and GLOBAL_CP did not select ranks 2 or 3. These counts establish that rank-2 selection is a reachable path under the unmodified source-generated workload, but they do not establish that those tasks would have missed their deadlines under rank 1.

In S2, CASPER_FULL registered **60 total health-alarm transitions** across ten seeds; no health alarms were observed for CASPER_FULL in S3. The adaptive multiplier exceeded one on **163,288** S2 dispatches and **246,153** S3 dispatches under CASPER_FULL. These are process observations, not effect estimates. The observed increase in certification conservatism did not translate into a demonstrated improvement in the primary deadline-miss endpoint.

## Discussion: what has been validated, and what has not

### Replication of mechanisms versus superiority of outcomes

The native implementation can generate independent physical completion histories and run all eight policies without consuming Java-generated task outcomes or calibration scores. Agreement of individual mathematical components with the original frozen source was tested separately before the native whole-system experiments. The holdout adds evidence of reproducible, fully executable policy mechanisms under a clearly specified alternate queue engine. However, **successful cross-language execution must not be conflated with a validated performance advantage**. The preregistered native comparison was nonsignificant (p = 1.000), as was the earlier original-Java disjoint holdout of an S3-versus-S2 certification interaction (p = .0625). A separate four-seed exploratory mask-by-eta intervention also did not meet the two-sided .05 threshold (p = .125). These address different comparisons and must not be pooled or redefined after inspection.

Certificate issuance, false certification, abstention, family-wise upper-bound coverage and observed missed deadlines measure different properties. The availability of conformal upper bounds is not equivalent to a guarantee of deadline success after unanticipated distribution shift. Nor do the 39 rank-2 CASPER_FULL decisions provide causal evidence of improvement; that claim would require a defensible matched counterfactual under the same resource dynamics. The absence of rank-3 decisions is a mechanism-coverage limitation to report rather than a reason to tune or select seed subsets until it appears.

### Queue semantics, stress exposure and external validity

A second implementation using the same underlying source workload generator is **not an independent workload distribution**. Both the native and Java experiments rely on the synthetic task model and its seeded shocks. Moreover, FIFO queue semantics in Python differ from observed CloudSim Plus admission order; the earlier preregistered strict queue-fidelity gate failed. Consequently, any differences between Java and Python performance may reflect queueing assumptions as well as policy behavior. These experiments do not justify claims of exact cross-simulator performance parity, industrial deployment readiness, or robustness to network and computation failures outside the modeled scenarios.

The native S2/S3 results are consistent with a heterogeneous response to degraded resources, but no causal contribution of E17 adaptation to deadline improvement has been established. Scenario-specific effects are descriptive. A stronger external-validation program would use an independently sourced workload or a different simulator (for example, YAFS), prespecified physical queue and network dynamics, an untuned workload/shift distribution, and new reserved seeds or independent traces. Any redesigned policy or new primary endpoint should be evaluated on a disjoint confirmatory cohort rather than retrofitted to the present ten-seed holdout.

### Scope of the manuscript contribution

The defensible contributions currently supported by these experiments are **reproducible uncertainty-aware scheduling instrumentation, explicit separation of certification reliability from realized deadline compliance, analysis of degradation exposure, and a native cross-language execution study with a negative confirmatory performance result**. They do **not yet support** a broad claim that CASPER_FULL systematically reduces missed deadlines relative to PRED_GREEDY, nor a general theoretical conformal guarantee under arbitrary nonstationary service/network shifts. The manuscript's claims should be calibrated accordingly before journal submission.

---

## Evidence and audit notes (retain in repository, not necessarily in manuscript)

The registered study and Python script for the exact analysis were committed *before* the original GitHub Actions run: `jpdc/NATIVE_EIGHT_POLICY_HOLDOUT_PREREG_2026-11-04.md` commit `a7e992403d4a82ea787f3144d15b1a3950039dde`, and `jpdc/analyze_native_eight_holdout.py` commit `3ae610afb6fcce2caf0146992134a5d989d10ba4`.

Original completed evaluation: [GitHub Actions run 41920321822](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41920321822), original immutable scientific results artifact 13367565614. Secondary reporting downloaded **the same** existing results without new simulations: [run 41920792886](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41920792886), archived artifact 13366842219. Complete interpretive result report: `jpdc/NATIVE_TEN_SEED_ALL_EIGHT_HOLDOUT_VERIFIED_2026-11-04.md`.

Earlier complementary Java results and the original manuscript framing: `jpdc/JPDC_INTEGRATED_RESULTS_DISCUSSION_2026-11-03.md`; original E42 Git blob hash `34256ca7bff46f911cf20e8b94278fbd09175746`. Frozen E4.6 remains unmodified. The native Python simulator is NOT YAFS and does NOT erase the separately failed queue-parity test. No new p-values or alternate inference have been added in this addendum.
