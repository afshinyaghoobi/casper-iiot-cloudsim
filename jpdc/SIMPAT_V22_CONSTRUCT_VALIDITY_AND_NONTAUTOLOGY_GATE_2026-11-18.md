# SIMPAT v2.2 — construct-validity and non-tautology gate (2026-11-18)

**Locked title:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation

**Purpose:** Assess, using EXISTING recorded evidence, whether a journal-scale modelling-method claim can be justified. This is **not** an author-approved new contribution, not new native simulation, and not a change to the v2.2 manuscript or its numbers. It follows `SIMPAT_V22_INDEPENDENT_SUBMISSION_READINESS_DECISION_2026-11-18.md`.

## Grounding and precedence

- Official CloudSimPlus 8.5.7 API: [CloudletSchedulerSpaceShared](https://javadoc.io/static/org.cloudsimplus/cloudsimplus/8.5.7/org/cloudsimplus/schedulers/cloudlet/CloudletSchedulerSpaceShared.html) and [CloudletSchedulerAbstract](https://javadoc.io/static/org.cloudsimplus/cloudsimplus/8.5.7/org/cloudsimplus/schedulers/cloudlet/CloudletSchedulerAbstract.html). WAIT/EXEC admission and waiting-promotion methods are documented software behavior, not newly invented by this study.
- General verification/validation distinctions: [Sargent (2013), Verification and validation of simulation models](https://doi.org/10.1057/jos.2012.20). Model verification, conceptual validity and operational validity are not interchangeable.
- Target venue [Simulation Modelling Practice and Theory](https://shop.elsevier.com/journals/simulation-modelling-practice-and-theory/1569-190X): the field includes verification/validation and IoT, but significant contribution is required.
- Prior-art provenance and distinctions: `SIMPAT_DIRECT_ZAKARYA_AND_VONDRA_PRIOR_ART_2026-11-18.md` (Zakarya/Gillam 2019 and Vondra/Sedivy 2017); `SIMPAT_MECHALIKH_FULLTEXT_AND_CALHEIROS_BIB_AUDIT_2026-11-18.md` (Mechalikh et al. 2025).

## Measurement-construct audit

| Proposed construct | What is actually recorded/defined | Can support | Cannot support |
|---|---|---|---|
| Native start-wait | Simulator-reported `getStartWaitTime` and A3 arrival/submit source-time audit | Exact-configuration native wait measurement, 288/288 origin matches at logged resolution | Physical IoT response time or globally interchangeable time origins |
| Analytical FIFO waiting | m-server recurrence on actual submit clocks and requested service | Differences between TWO explicitly defined accounting models | Error of native scheduler, general FIFO-contract violation |
| Native execution duration | Simulator-reported `getTotalExecutionTime` after completion | Service-duration accounting sensitivity (250/288 differ; hindsight comparator max residual 154ms) | Actual CPU demand or online available service forecast |
| Synthetic deadline classification | Comparison of native completion callback and FIFO completion at submit+25/+50ms | Threshold disagreement of models (86/288 and107/288) | Real deadline-miss probability, QoS or SLA error |
| A1 WAIT/EXEC bypass | Executed list-state traces and specific instrumented callback paths | Two observed known-case native event-phase patterns and altered-rescan local intervention | Physical CPU start ordering, universally incorrect scheduler, independent broad causal mechanism |
| Before-submit predicate P | Frozen source-state conjunction in eight purposively chosen fixtures | Descriptive TP2 FP0 TN6 FN0 inside this exact set | Population classifier performance, new algorithm, predictive validation independent of stock admission logic |
| Event-gap hypothesis H | Four paired input families | Failed directional claim: 1/4 for 5ms and 1/4 for 1us | A generic event-gap monotonic effect |

## Three candidate contributions compared against a NON-TAUTOLOGY test

**C1. 'Native waits differ from an independently defined FIFO.'** Existing 24-case evidence: YES. Independent general modelling innovation: **NO**. Disagreement is expected when service/callback semantics are intentionally not identical. Treat as a bounded case observation.

**C2. 'A source-state predictor identifies an older-WAIT/younger-EXEC event.'** Existing eight-fixture evidence: descriptive YES. Independent generalizable prediction: **NOT ESTABLISHED**. P conditions on immediately pre-submit native WAIT/EXEC/free-capacity state, close to the direct admission implementation. Unseen workload design does not make this predictor model-independent. Predeclared input-only H failed. Treat as exact-version diagnostic.

**C3. 'A construct-validity protocol can tell whether a scheduling study's queue and deadline metrics are comparable across native event simulation and analytical reference.'** Concept: **plausible research question, not a validated or demonstrably new method**. To be a publishable original method it would need a formal decision rule that is (i) specified without reading the tested model's downstream label; (ii) applicable independently of CloudSimPlus v8.5.7 source internals; (iii) tested against meaningful alternative diagnostic explanations; and (iv) compared to existing V&V methods. The current data alone do not verify these properties.

## Explicit falsification requirements before claiming C3 as a contribution

1. **Operational definition predeclared:** Specify what 'semantics-compatible' means at the observable level (e.g., matching input clock origins, same capacity, explicitly comparable requested/native service lengths, and event-phase equivalence). Each check must have a reproducible pass/fail or 'not identifiable' result, not merely a generic checklist.
2. **Non-circularity:** The diagnostic must not use the actual disagreement outcome to choose its compatibility rule or the native post-admission label to predict that same label. Separate observation, decision rule and held-out evaluation.
3. **Independent comparison:** Evaluate whether the rule distinguishes a *known compatible* from a *known deliberately incompatible* reference under blinded, controlled conditions; when a physical/operational claim is made, a credible independent reference is mandatory. Current analytical FIFO cannot serve as physical ground truth.
4. **Transfer:** Apply the rule to a genuinely distinct scheduling/model configuration or modelling implementation *without reverse-engineering a new predicate from each outcome*. Without this, label C3 version-specific characterization, not general method.
5. **Failure criteria:** A rule that merely restates documented scheduler conditions, returns 'incompatible' whenever two different formulas are used without additional mechanistic insight, fails controls, or depends on posthoc thresholds **does not meet** an original-method novelty claim. Any null/negative findings must be preserved.
6. **Evidence independence:** Existing 24 deterministic A2 conditions, six preknown A1 fixtures, and eight purposively designed conditions are *not* statistically independent random population validation. No accuracy confidence interval or generalization claim should be inferred from their counts.
7. **Prior-art differentiation:** Before paper claims, demonstrate specific improvement over Sargent-style conceptual/operational validity and Zakarya/Gillam, Vondra/Sedivy, Mechalikh comparisons. Merely renaming those concepts is not novelty.

## Current evidence gate

| Gate | Finding |
|---|---|
| Reproducible exact-version simulator diagnostic | **PASS at archived-trace/CI level**; not an independent physical replication |
| Model-accounting difference measured | **PASS for frozen deterministic configurations** |
| Source-phase mechanism locally observable | **PASS within known A1 traces** |
| Input-only event-gap generalization | **FAIL (1/4 versus 1/4)** |
| State predicate independent of native implementation | **NOT ESTABLISHED** |
| New transferable V&V method | **NOT ESTABLISHED** |
| Physically grounded IoT validation | **NOT PRESENT** |
| Original-research SIMPAT go decision | **HOLD** |

## Actionable next decision

**Do not create 'method' claims or introduce a new name/acronym into the article just to make the work appear original.** First attempt a strictly documentary *design-only* operational rule and an explicit baseline comparator drawn from published V&V, then ask whether that proposal is genuinely non-circular. If it is not, stop this path and assess an honest software/simulation case-study venue instead. **No new simulations, altered title, modified manuscript, DOI, or submission in this step.** Preserve earlier strict 30k Java/Python parity FAIL and Stage65 safety FAIL. Reserved Program B remains untouched.
