# JPDC manuscript-ready Results and Discussion: reliability under realized network degradation

**Working draft, November 3, 2026.** This text synthesizes verified CloudSim evidence from the CASPER continuation branch. It is **not** a claim of acceptance-ready manuscript completeness or of independent implementation validation. All p-values are seed-level. The original E42/E4.6 science is untouched.

## Results

### Experimental design and outcome definitions

We studied the reliability of uncertainty-aware scheduling decisions in an event-driven CloudSim Plus implementation. Each deployment comprised 30,000 tasks, following 80,000 calibration samples. For the post-change tests, S2 reduced the effective compute capacity of affected nodes by 40%, whereas S3 reduced their effective network bandwidth by 50%. In S3, six of 21 nodes were selected as degraded. The same scientific seed and environmental scenario were used for paired scheduling-policy comparisons.

To isolate adaptive uncertainty scaling, we compared CASPER_FULL with an intervention that retained the same scheduling components but fixed the *effective dispatch-time* uncertainty multiplier, eta, at one. The intervention was applied to the generated E45 campaign only, not to the frozen scientific implementation. For each seed/scenario, we checked that other policies' scientific output columns remained unchanged and that the clamped CASPER_FULL outputs matched CASPER_HEALTH_STATIC, apart from mapper timing.

We distinguish four quantities. The false-certificate rate (`late_far`) counts certifications followed by missed deadlines, divided by **all** 250 late mission tasks per seed, not only certified tasks. The abstention rate (`late_air`) is the fraction of those mission tasks without a certificate. The deadline-violation rate (`late_dvr`) is the fraction missing the true deadline, regardless of certification. The family-wide coverage rate (`late_fwc`) evaluates whether conformal upper bounds cover counterfactual latencies of *all* ranked candidates; it must not be interpreted as the precision of the issued certificate. The independent experimental unit for the inference below is a **seed**, not an individual task.

### Exploratory matched S2/S3 comparison

In an initial matched exploratory cohort of ten seeds (indices 0, 1, 5, 7, 9, 13, 18, 21, 27, and 29), the S3 adaptive version produced 21 false certificates, compared with 80 for fixed eta, over 2,500 late mission tasks per arm. The adaptive version abstained 233 times versus 46, while deadline misses were 113 versus 112. The S3-versus-S2 interaction in false-certificate rate was -2.36 percentage points (two-sided exact sign p = .015625, exploratory Holm-adjusted p = .046875 for the three tested metrics). This apparent significance was fragile: excluding any of seven seeds made the multiplicity-adjusted p-value .09375. Accordingly, we treat the initial result as hypothesis-generating rather than conclusive.

### Separately preregistered disjoint holdout

Before running a disjoint holdout, we fixed ten new seed indices (30–39), defined the primary S3-minus-S2 paired interaction in late false-certificate rate, and specified a *two-sided* exact sign test with alpha = .05. In the S3 holdout, adaptive eta yielded 7 false certificates compared with 40 under fixed eta (2,500 late mission tasks per arm). Abstentions increased from 47 to 176. Deadline misses were 65 under adaptive eta and 63 under fixed eta. In the matched S2 condition, both versions produced zero observed false certificates, with deadline misses of 20 in each arm.

**The preregistered primary analysis was not statistically significant.** The seed-level mean S3-minus-S2 interaction in false-certificate rate was -1.32 percentage points, with five negative seed-level differences, five ties, and no positive differences (two-sided exact sign p = .0625). Although the direction reproduced the exploratory analysis, this did not meet the prespecified .05 threshold. The exploratory percentile-bootstrap interval [-2.60, -0.32] percentage points should not override that test. Nor should the original exploratory and holdout cohorts be pooled to retroactively label the result confirmatory.

| Disjoint holdout metric (2,500 late mission tasks per S3 arm) | Adaptive FULL | Fixed eta = 1 |
|---|---:|---:|
| False certifications | 7 (0.28%) | 40 (1.60%) |
| Abstentions | 176 (7.04%) | 47 (1.88%) |
| Deadline misses | 65 (2.60%) | 63 (2.52%) |
| Issued certificates | 2,324 | 2,453 |
| False certifications among issued certificates (descriptive, secondary) | 7/2,324 (0.30%) | 40/2,453 (1.63%) |

The last row uses a different denominator from `late_far` and is presented for interpretation, not as another inferential endpoint. Zero observed S2 false certificates does not establish zero underlying risk.

### Why identical nominal degradation creates different workloads

We audited actual mission-task placements for all ten original exploratory S3 seeds. Before the shock, we measured the fraction of mission tasks sent to the six nodes that would later be degraded. After the shock, we measured realized exposure: the fraction actually executed on degraded nodes. These seed-level quantities were strongly associated (Pearson r = .9970; Spearman rho = .9848), but this is descriptive and does not constitute independent confirmatory evidence. Realized exposure ranged from zero in seed 7 to 94.0% in seed 18, despite identical nominal network-retention settings.

In seed 7, no post-change mission task traversed a degraded node, and only 40/980 normalized completion scores exceeded that seed's reference threshold. In seed 18, 960/1,021 post-change mission tasks were assigned degraded nodes, and 965/1,021 normalized scores exceeded the corresponding reference threshold. Independent event-level reconstruction of the frozen E17 dual-memory detector confirmed that seed 7 never reached the 12-of-50 exceedance alarm threshold, while seed 18 first triggered it at mission task 10,165. Late eta was one and three, respectively. This establishes the *observed detector-state mechanism*, not a general causal explanation for every possible failure topology.

### Controlled location of degraded nodes

To distinguish nominal fault severity from actual exposure, we next performed an exploratory, paired physical-intervention experiment on four unused seed indices (40–43). For each seed, we measured baseline pre-change mission-task placements and selected two nonoverlapping masks of six nodes: the six least-used nodes (LOW) and the six most-used nodes (HIGH). We froze these masks before comparing outcomes. A location intervention therefore changed *which* nodes suffered the same nominal 50% bandwidth loss, without changing the number of degraded nodes or scientific seed.

Across the four seeds, average post-change mission-task exposure was 0.051% in LOW and 99.656% in HIGH. Mean added network delay increased from 0.0032 ms to 12.8762 ms, and mean late eta increased from 1.084 to 3.000. Under adaptive FULL, late deadline misses increased from 1/1,000 in LOW to 45/1,000 in HIGH. This comparison verifies that damage placement substantially changes realized stress; it must **not** be used to claim that adaptive eta improves deadline completion, because network exposure itself was changed.

We subsequently held each seed-specific LOW or HIGH mask fixed and separately intervened on adaptive versus fixed eta. Sixteen full CloudSim runs, with strict scientific-column parity checks, yielded the following descriptive results.

| Four-seed controlled-mask condition (1,000 late mission tasks per row) | False certificates | Abstentions | Family-wide covered cases | Deadline misses |
|---|---:|---:|---:|---:|
| LOW, adaptive eta | 0 | 14 | 992 | 1 |
| LOW, fixed eta = 1 | 0 | 11 | 990 | 1 |
| HIGH, adaptive eta | 3 | 125 | 835 | 45 |
| HIGH, fixed eta = 1 | 33 | 11 | 3 | 44 |

With the HIGH mask held constant, the adaptive intervention reduced false certificates from 33 to 3 per 1,000 late mission tasks (a descriptive 90.9% relative reduction), while abstentions increased from 11 to 125 and deadline misses remained virtually unchanged (44 versus 45). Effects under LOW were small. The seed-paired HIGH-minus-LOW interaction in false-certificate rate was -3.00 percentage points, with all four differences negative; however, the exact two-sided sign test gave p = .125. For abstentions, the interaction was +11.10 percentage points (p = .125). For deadline violations, it was +0.10 percentage points (p = 1). Thus these results support a **mechanistic tradeoff** but do not provide confirmatory population-level significance.

## Discussion

### Interpretation: certificate reliability is distinct from successful dispatch

Taken together, the studies suggest that the most defensible role of adaptive eta in this CloudSim configuration is *more conservative deadline certification when observed residual errors rise*. Both the disjoint holdout and the deliberately stressed mask intervention showed fewer incorrect certificates with adaptive eta, accompanied by more abstentions. They did **not** establish a corresponding reduction in deadline misses. Certificate reliability, certificate availability, counterfactual family coverage, and realized scheduling outcomes must therefore remain separate claims. A decrease in false certificates may partly reflect fewer issued certificates, rather than universal improvement in task execution.

### Why realized exposure belongs in the evaluation design

The original S3 failure mask did not guarantee that the workload actually used degraded nodes. Two nominally identical six-node damage scenarios could yield almost zero or near-total post-change mission exposure. The unusually high pre/post placement overlap suggests that a pre-change, seed-specific placement profile is useful for characterizing intended exposure *before* observing post-change outcomes. By contrast, realized post-change exposure is affected by policy decisions and should not simply be included as an ordinary exogenous adjustment covariate in causal comparisons.

The engineered LOW/HIGH masks provide a useful controlled contrast, but their extreme placements were chosen deliberately from the same seeds' baseline routes. Consequently, their effect sizes are **not** estimates of average performance for naturally sampled faults. Generalization to mixed and time-varying network failures, heterogeneous hardware, and other workload or simulator models remains untested.

### Statistical interpretation and limits

The original ten-seed analysis was exploratory and sensitive to single-seed exclusions. The separate ten-seed holdout was prospectively specified, but its primary two-sided test did not meet alpha = .05 (p = .0625). Four-seed mechanism studies were intentionally small; even four of four concordant nonzero signs yield p = .125 in a two-sided exact sign test. Task-level event counts are useful descriptive denominators but do not create hundreds or thousands of independent experimental units.

The intervention fixes effective eta at one while retaining feedback and other mechanisms; it should not be described as removing all adaptation. We also cannot infer a finite-sample distribution-free coverage guarantee under hidden nonstationary shifts from these experiments. FWC measures a counterfactual family-wide property within the simulator, not a universal safety guarantee. More independent simulation environments, broader shift regimes, and predeclared exposure-balanced validation would be required before making stronger generalization claims.

### Implications for the next JPDC experiment

The next incremental contribution should target external validity rather than repeatedly testing more seeds until one p-value crosses a threshold. A defensible design would use a workload trace and network-failure process defined independently of CASPER's prior results, with a prespecified comparison of adaptive eta, fixed eta, certificate coverage, abstention and deadline misses. A second simulator or well-documented trace-replay environment could test whether the exposure/certification tradeoff survives differences in arrival, queue and network semantics. Report both intended mask exposure (from a pre-change placement model) and realized policy-dependent exposure, keeping them conceptually distinct.

## Provenance and audit trail (not manuscript copy)

| Evidence | GitHub Actions run | Key registered source |
|---|---|---|
| Original exploratory S2/S3 paired seeds | 41510962554, 41511810120, 41516881350, 41517917953, 41520884581 | `jpdc/MANUSCRIPT_S2_S3_ETA_RESULTS_EVIDENCE_2026-11-02.md` |
| Preregistered disjoint holdout | 41524202008 | `jpdc/PREREG_S2_S3_DISJOINT_HOLDOUT_2026-11-02.md` |
| Original S3 exposure audit (10 seeds) | 41697794315; 41685852046 | `jpdc/EXPOSURE_AUDIT_10SEED_PROTOCOL_2026-11-03.md` |
| E17 detector independent replay | 41658004816 | `jpdc/S3_E17_FEEDBACK_DETECTOR_REPLAY_2026-11-03.md` |
| Controlled LOW/HIGH mask placement | 41719553340 | `jpdc/S3_CONTROLLED_MASK_EXPERIMENT_PROTOCOL_2026-11-03.md` |
| Controlled mask × eta intervention | 41724362605 | `jpdc/S3_MASK_ETA_FACTORIAL_PROTOCOL_2026-11-03.md` |

Provenance checks used the immutable E42 Git blob `34256ca7bff46f911cf20e8b94278fbd09175746` and a generated E45 intervention path. `E4.6` was not changed. This document is a drafted narrative, not a fresh simulation.
