# JPDC novelty and original-contribution gate — evidence-first assessment, November 4, 2026

**Decision: NO-GO for a second *new-algorithm* claim on current evidence alone; CONDITIONAL GO for methodological systems analysis if presented as such.** This is an internal research gate, not an editorial decision. A full side-by-side of the FGCS CASPER manuscript and a complete JPDC methods draft has **not** been performed: the repository contains the executable CASPER system and analysis notes, not both full final article texts. Consequently all originality claims relative to exact FGCS publication wording are **provisional** until that comparison.

## 1. Originality baseline: what is already part of CASPER

The existing CASPER execution model already contains task criticality/deadline-aware decisions; nominal heterogeneous 21-node latency prediction and virtual queue; calibrated conformal global/rank quantiles and first-feasible top-three candidate selection; E1.7 adaptive residual-based uncertainty scaling; node-health monitoring; bounded sparse probes; abstention/certification; original 8 policy/ablation modes; and synthetic IIoT/cloud-edge degradation experiments. These are **not novel simply because they were reproduced in Python or retested at 30k tasks**.

Original E42 frozen Git blob `34256ca7bff46f911cf20e8b94278fbd09175746` and frozen E4.6 are unchanged. This is an important reproducibility constraint, but the absence of source changes also makes it implausible that current work demonstrates a **new scheduler algorithm** beyond the frozen CASPER framework.

## 2. Claim-by-claim novelty audit

| Candidate JPDC claim | Evidence currently available | Is it genuinely a new algorithm beyond frozen CASPER? | Claim gate |
|---|---|---|---|
| A new conformal-aware CASPER scheduler | Existing E42 includes rank quantiles, first-feasible routing and E17 adaptive eta | No new mechanism demonstrated | REJECT |
| A new rank-aware uncertainty allocator | Rank-aware CP and risk split already in frozen CASPER | Not established | REJECT |
| A novel health-aware fallback/probe mechanism | Native Python faithfully ports original health/probe mechanisms | No | REJECT |
| An independently executing cross-language physical simulation | Real Python strict FCFS 21-node event engine, native stochastic service and calibration, all 8 policies; CI verified | New **validation artifact**, not new dispatch algorithm | ACCEPT, correctly framed |
| External simulator reproducibility / YAFS validation | Python is a custom native event engine using the same generative task/node/source model; physical CloudSim queue differs | Not established | REJECT |
| Demonstrably better deadline-miss performance under hidden faults | Native prereg 10 seeds60–69: FULL-minus-GREEDY equivalent benefit mean +0.3208 percentage points, two-sided sign p=1.000, 95% descriptive seed bootstrap [-0.3060,+0.9882] pp | No reproducible population superiority | REJECT |
| Improved certificate reliability due to E17 under induced network exposure | Original Java S3 HIGH descriptive false certificates 33 vs 3, abstentions 11 vs 125, misses 44 vs 45 per 1000; exploratory interaction p=.125 | Evidence of **mechanistic tradeoff**, not new E17 or confirmed general benefit | ACCEPT with qualification |
| Exposure-aware *causal* diagnosis of shift mechanisms | LOW/HIGH deliberately chosen pre-shock route masks, 4 seed controlled experiments; exposure varied strongly | Analysis method/diagnostic may be useful, but selected extreme masks not representative and not a new routing policy | CONDITIONAL |
| Rank2/rank3-driven causal scheduling benefit | Actual native holdout CASPER_FULL rank2=39, rank3=0; no same-state rank1 counterfactual | Not shown | REJECT |
| Distribution-free finite-sample guarantee under arbitrary drift | Observed adaptive eta and empirical conformal metrics; hidden nonexchangeable shifts not covered by a demonstrated proof | No | REJECT |
| Broad workload generalization / real IIoT evidence | Native Python reimplements same synthetic generator and shock logic | No | REJECT |

## 3. What a JPDC contribution could legitimately be

### Path A — systems-methodology paper (no algorithm novelty claim)

**Working framing:** *When Adaptive Certificates Do Not Improve Deadline Completion: Exposure-Aware Evaluation of Cloud–Edge Scheduling under Hidden Resource Degradation*.

Potential contributions, all bounded by validated work:
1. An explicit experimental decomposition of **nominal fault severity, realized policy-dependent exposure, adaptive certification, abstention, and deadline outcomes**. The observed E17 adaptation can reduce incorrect certificates under deliberately high network exposure while increasing abstention **without** improving executed-task deadlines. This is a negative but informative systems finding.
2. Paired controlled fault-placement and fixed-eta interventions in the original Java CloudSim setting, distinguishing conditioning on observed exposure from deliberately intervening on a predeclared damage mask. State that HIGH/LOW masks were chosen from same-seed pre-shock route profiles, so estimates describe deliberately extreme stress settings, not random faults.
3. A separately executing **native Python** replica with original-model source generation, source-independent calibration/event physics, all eight policies and fail-closed ten-seed statistical reporting. **Different strict FIFO vs Java SpaceShared semantics remain a boundary, not cross-platform parity.**
4. Transparent negative confirmatory results, reproducibility artifacts and non-overclaiming methodology.

Potential strength: reproducible systems diagnosis of where confidence/certification separates from physical outcomes. Potential weakness: if reviewers expect a *new scheduling algorithm*, this may be judged an extension/re-evaluation of CASPER with limited novelty. Do not label it the second CASPER algorithm.

### Path B — a genuine follow-on dispatch mechanism (new work required)

**Research concept, NOT a demonstrated finding or claim:** a *state-aware exposure-regularized resource selector* that measures predicted degraded-path exposure and queue-network uncertainty jointly before ranking nodes, not merely scaling a conformal bound after observing failures.

Candidate decision model for a task t and node j:
`score(t,j) = nominal_latency(t,j) + lambda * independently-estimated_exposure_risk(t,j) + mu * predicted_queue_instability(t,j)`,
subject to a preregistered bound on missed deadlines or certificate risk. The risk terms **must be available before dispatch** from non-oracular telemetry; no post-outcome fault labels may enter the selector. Key technical development needed: define an observable exposure estimator with identifiability assumptions, derive a tractable constrained update (and complexity), evaluate against (i) PRED_GREEDY, (ii) fixed/ranked CP, (iii) original CASPER_FULL, and (iv) ablations dropping each new term. Show the technical difference in pseudocode/complexity from frozen E42. No tuning on previously tested 60–69 holdout. Use separate development/validation cohorts or independently sourced traces. Consider counterfactual shared-system interference: changing one dispatch changes every subsequent queue state; naive same-task counterfactuals are invalid unless carefully defined.

**This is not yet an invention validated in the repository.** Do not call it the current paper's contribution or promise that it improves performance. If its mathematical novelty is modest (a simple heuristic penalty), the work may still lack journal-level originality without deeper formal analysis.

## 4. Major scientific risks to resolve before submission

1. **Overlap and duplicate publication:** Compare the full first FGCS CASPER submission and any eventual published version, section-by-section and contribution-by-contribution. Explicitly cite/disclose the first work when appropriate, including shared algorithms and simulator. In repository alone, a complete side-by-side is unavailable.
2. **Nonsignificant results:** Original Java disjoint confirmation p=.0625 (not <.05); original exploratory factorial p=.125; new independent native FULL-vs-GREEDY primary p=1.000. Positive exploratory trends must not be described as significant or confirmed. Do not mine seed subsets or change primary endpoints.
3. **Certificate vs workload outcome:** false-certificate rate, conditional precision of issued certificates, abstention, family-wide coverage and actual deadline misses use different denominators. Report each correctly. E17 changed certificate availability substantially without demonstrating deadline improvements.
4. **Counterfactual interpretation:** full-family simulated predictions or candidate outcomes are not a causal no-interference comparison of rank1 vs rank2 when routing changes later queues. Actual rank2 occurs but no causal contribution to improvement established; rank3 absent.
5. **Physical model gap:** strict-FCFS Java→Python waiting-time fidelity test originally FAILED max9.1214ms >5ms. New Python standalone runs do not reverse it. The native environment is NOT YAFS, NOT independently sampled real-world workloads, and NOT CloudSim-parity.
6. **Simulation horizon / representativeness:** source-model task arrivals/deadlines/noise and six-node fixed fault masks have limited demonstrated external validity. Need novel workload/fault distributions for out-of-source claims.
7. **Inferential unit:** distinct scientific seed is experimental unit; 4.8 million simulated task-policy records are not independent evidence of efficacy. Small n=10 implies wide uncertainty.
8. **E4.6 artifact vs follow-on:** frozen E4.6 artifact may be an important appendix or method reference but is not itself a second contribution.

## 5. Journal fit and current literature scan (preliminary, NOT exhaustive prior-art clearance)

The Journal of Parallel and Distributed Computing explicitly covers original research on distributed systems, including cloud/edge/fog, IoT algorithms, software environments and performance analysis:
- Elsevier official description, https://shop.elsevier.com/journals/journal-of-parallel-and-distributed-computing/0743-7315
- Recent JPDC cloud-edge scheduling work: Lei et al., *Adaptive container scheduling for serverless workflows in cloud-edge collaborative computing*, Journal of Parallel and Distributed Computing (October 2026), DOI 10.1016/j.jpdc.2026.105308, https://www.sciencedirect.com/science/article/pii/S0743731526000869
- Related uncertainty-aware scheduling precedent: *PRESAGE: Uncertainty-Aware Predictive Elastic Scheduling for Cloud Analytics and GenAI Inference*, IEEE Access (September 2026), https://ieeexplore.ieee.org/abstract/document/11694384/
- Related SLA-aware adaptive edge-cloud scheduler: Yamsani & Reddy, *SLA aware deep reinforcement learning for adaptive EdgeCloud task scheduling*, Scientific Reports (February 2026), https://www.nature.com/articles/s41598-026-40237-8

These sources establish **topic fit and a crowded neighboring problem space**, not an exhaustive proof of nonnovelty. They use different task settings/learning systems; cite them only after reading complete methods and checking genuine point-by-point novelty. The specific combined scheduling/CP literature needs a dedicated systematic search before a new technical contribution is claimed.

## 6. Decision and measurable next gates

**Current recommendation: DO NOT submit a second JPDC article as a new algorithm yet.** The native Python results demonstrate a valuable independently executable systems validation, but neither a distinct scheduler design nor supported deadline efficacy. A reframed *negative-results / exposure-and-certification systems methodology* paper is possible if its contribution is accepted by the target venue and duplication with first FGCS paper is resolved.

Action order:
- **Gate 1 (highest priority):** full first-paper vs second-paper overlap mapping, with duplicate equations, code-paths, baselines, figures, tables, claims and citations.
- **Gate 2:** choose exactly one honest paper identity (systems diagnosis versus genuinely new algorithm); write a 1-page contribution statement with falsifiable questions, never a menu of unsupported claims.
- **Gate 3:** if genuinely new algorithm, formalize the new decision rule, admissible information, complexity and relevant theorem/proposition *before* choosing new outcome analysis.
- **Gate 4:** externally distinct workload/fault trace or YAFS with own queue-semantic contracts, plus new preregistered seed/traces, zero leak of inspected indices (0–69 where used). Test both correct certification and physical deadline outcomes, including abstention cost.
- **Gate 5:** only after independent experiments, decide submission readiness on all evidence, including negative outcomes.

**Evidence constraints:** The original E42/E4.6 code is not changed by this document. The study must remain reproducible even if the original E1.7 mechanism proves primarily useful for withholding unreliable certificates, rather than improving dispatch completion.

## Exact provenance
- Original frozen E42 blob `34256ca7bff46f911cf20e8b94278fbd09175746`.
- Original-Java Results `jpdc/JPDC_INTEGRATED_RESULTS_DISCUSSION_2026-11-03.md`.
- Native ten-seed complete results `jpdc/NATIVE_TEN_SEED_ALL_EIGHT_HOLDOUT_VERIFIED_2026-11-04.md`, original run https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41920321822
- Native manuscript addendum `jpdc/JPDC_NATIVE_HOLDOUT_RESULTS_DISCUSSION_ADDENDUM_2026-11-04.md`; audit run https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41923518215
- Queue parity failure `jpdc/NEW_CHAT_CONTINUITY_2026-11-02.md`, original run https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41773297282
