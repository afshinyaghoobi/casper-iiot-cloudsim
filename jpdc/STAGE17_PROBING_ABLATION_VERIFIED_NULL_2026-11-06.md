# JPDC Stage17 — targeted no-active-probe ablation VERIFIED with NULL primary outcome (2026-11-06)

## Frozen provenance
Stage17 protocol was authored **before new results** at commit `cc1de0b0a0842d182ca25ade03fd28733f567667`: `jpdc/STAGE17_PROBING_ABLATION_PREREG_2026-11-06.md`. Frozen source-generated pilot [42187795512](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42187795512): successful **both** developmental seeds86 and87, each twice byte-identical, original CASPER_FULL and PRED_GREEDY exact Stage6 output parity, full guarded policy exact Stage15 original output parity (after removing only new observational diagnostic fields), fixed E42 original source hash. 2 seeds x 2 scenarios x4 policy arms x12000 =192,000 dependent task-policy outcomes, **scientific n=2**. This is **not** new confirmatory efficacy validation or independent n192000.

Second **immutable-artifact-only** forensic audit [42188302693](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42188302693) PASSED marker `JPDC_STAGE17_IMMUTABLE_TWO_SEED_ABLATION_AUDIT_PASS`. Comparison below reads original saved artifacts without rerunning physics or changing any parameter.

## Every preregistered contrast

| Seed | Scenario | CASPER_FULL MISSION misses | Guarded + probe | Guarded NO active probe | No-probe minus probe | Guarded probe attempts | Probe overrides changed chosen route |
|---|---|---:|---:|---:|---:|---:|---:|
|86|S2 compute|0|1|1|0|95|12|
|86|S3 network|0|0|0|0|95|12|
|87|S2 compute|5|4|4|0|95|16|
|87|S3 network|4|5|5|0|95|17|

No-probe changed neither PRE nor POST MISSION miss count in ANY of the four comparisons; guarded vs no-probe mean E2E latency and queue wait changed slightly. For transparency:

| Seed | Scenario | probe mean E2E ms | no-probe mean E2E ms | probe mean queue wait ms | no-probe mean queue wait ms | probe selection HHI | no-probe selection HHI |
|---|---|---:|---:|---:|---:|---:|---:|
|86|S2|45.062130|45.062635|2.870759|2.877452|0.367079|0.367370|
|86|S3|45.191415|45.187388|2.875827|2.881316|0.367654|0.367945|
|87|S2|50.369570|50.372248|1.398668|1.404211|0.326379|0.326654|
|87|S3|53.676838|53.680170|1.034612|1.040756|0.321872|0.322155|

HHI is sum of squared overall dispatch fractions across 21 nodes; here around 0.32–0.37 and near identical across policies. Absolute values indicate substantial routing concentration relative to a 21-node even distribution (HHI=1/21~0.0476), not proof this concentration caused misses. Actual changed probe routes were only 12–17 of 95 attempts, consistent with a small observed policy contrast despite 95 counted opportunities.

## Interpretation and decision
**No detectable miss-count benefit from explicit NORMAL active probing in these four specific developmental source scenarios.** This does not establish zero effect generally; low miss event counts and n2 are particularly weak. A causal ablation contrasts two dynamic routing policies on identical source workloads: different decisions alter future queue dynamics and E2E feedback. We must not treat future observations as identical replay or attribute every mean-wait difference to one task.

The current +2ms bounded freshness method is itself **not proven superior over CASPER_FULL** (Stage16 eight-seed primary p=.375, S2 tendency toward harm). The explicit probe add-on is *not a validated contribution* and should not be presented as essential. A defensible next research direction requires independent methodological novelty beyond freshness/probing, stronger queue-aware scheduling and cross-engine validation, and explicit limits of synthetic drift/measurement models.

## External novelty guardrail
2026 research, e.g. S. A. Hamid et al., "[Exploiting and Mitigating Staleness in Distributed Edge Offloading via Predictive Load Awareness](https://doi.org/10.3390/network6030069)," *Network* 6(3), highlights how some stale views can reduce synchronized migration/oscillation. 2025 IEEE TVT online hard-deadline work [10.1109/TVT.2025.3539885](https://doi.org/10.1109/TVT.2025.3539885) already addresses practical server-state acquisition. Prior delayed-feedback bandit cloud-edge work [10.1109/TSC.2025.3611379](https://doi.org/10.1109/TSC.2025.3611379) is a meaningful alternative baseline family. Further systematic review required.

## Stage18 priorities, no new efficacy claim
1. Stop seed-driven performance tuning. Use frozen Stage16 outcomes and Stage17 negative ablation to define a principled queue-aware decision objective that is NOT just empirical +2ms gating. State target counterexamples, observability conditions, costs and novelty.
2. Validate the competing Java CloudSimPlus SpaceShared vs Python strict-FCFS queue-admission semantics: original difference >5ms parity gate is unacceptable for claimed simulator equivalence. Either harmonize an explicit independent queue policy or report the two distinct domains honestly.
3. Integrate at least one externally informed workload or trace, broader fault severities, recovery and false alarm costs; pre-register separate evaluation before data. Distinguish CASPER FGCS original prior publication/submission and JPDC novelty rigorously.
