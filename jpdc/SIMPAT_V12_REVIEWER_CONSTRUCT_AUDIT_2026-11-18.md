# SIMPAT A1–A3 reviewer-style claim and construct audit — 2026-11-18

**User-approved exact title:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation
**Manuscript examined:** [v1.1](SIMPAT_MANUSCRIPT_V11_QUEUE_PRIOR_ART_2026-11-18.md). This is **internal editorial assessment**, NOT actual external refereeing, endorsement, or a journal decision.

## Evidence-graded methodological concerns, ranked

### M1 — Model-to-model contrast must NOT be reported as simulator error (high importance, addressed in v1.2 wording)
The comparator is **event-independent earliest-free-server analytical FIFO**, while Java CloudSimPlus 8.5.7 SpaceShared is event-driven, maintains WAIT/EXEC lists, and has its own service accounting. Source API describes the SpaceShared scheduler, waiting lists, and updates (https://javadoc.io/static/org.cloudsimplus/cloudsimplus/8.5.7/org/cloudsimplus/schedulers/cloudlet/CloudletSchedulerSpaceShared.html ; https://javadoc.io/static/org.cloudsimplus/cloudsimplus/8.5.7/org/cloudsimplus/schedulers/cloudlet/CloudletSchedulerAbstract.html). Neither recurrence is privileged as physical ground truth. Therefore Δ(wait) and synthetic deadline disagreements measure **model construct non-equivalence**, not correctness, unfairness or software defect. Manuscript already acknowledges this; ensure all abstract/figure captions/conclusion obey.

### M2 — “Execution time” mixes requested CPU service, native completed runtime, and wall-clock callback intervals (high, remaining partial)
A2 original analytical comparator uses **requested p_j**; hindsight replaces p_j with **native total execution** obtained *after* completion. For 250/288 jobs these differ >1e-6 ms. Yet this substituted native metric is not independently established as the **service demand a hypothetical FIFO server would experience**, and cannot identify a causal component. Worst gap 246→154ms is NOT an isolated 92ms effect. Existing report [retrospective A2](JPDC_A2_NATIVE_SERVICE_ORACLE_RETROSPECTIVE_VERIFIED_2026-11-17.md) is source. Correct words: “reported duration” rather than “ground-truth CPU service time”, explicitly mark diagnostic non-causal.

### M3 — Event list membership is not a proven physical execution start; native waiting-time clock audited only for fixed conditions (high, addressed)
The A1 “later-submitted in EXEC list while earlier WAIT” occurs in two of six cases. It is not proof of actual CPU start, universal FCFS violation, callback error, or deadline policy rank reversal. A3 source/native 24-case audit establishes **dcArrivalTime = observed scheduler submit timestamp in 288/288 at logged precision** and *source-defined wait = startTime-dcArrivalTime* in the fixed setup; not general for all brokers/versions. Retain exact 54 eligibility callbacks and passive instrument control.

### M4 — No external IoT experiment (high, unresolved scientific applicability)
A2 has 24 *designed conditions* ×12 one-PE CPU tasks on **one VM with one/two PEs**, no sensor traces, network, hardware/field validation, factory network or actual deployed deadline; fixed +25/+50ms are thought-experiment thresholds. “IoT” in exact user-selected title is *implications for evaluation*, not IoT dataset proof. Publisher [official SIMPAT scope](https://shop.elsevier.com/journals/simulation-modelling-practice-and-theory/1569-190X) expects significant methodological novelty and transparent real validation where appropriate. No author can claim physical IoT correctness. A stronger actual IoT evaluation would be a real scientific addition, but **do not launch one merely to manufacture publishable numbers without an approved preregistered question**.

### M5 — Statistical independence and retrospective effects (moderate, documented)
The 3 timing variants per family are deterministic; 288 jobs are correlated within 24 fixed fixtures. Report totals and within-case max descriptively, not p values, CIs or population proportions. 86 and107 classification disagreements are **disagreements of two models** across artificial thresholds, not 86/288 observed missed physical SLAs. After-completion hindsight uses the same A2 trace, not independent replication.

### M6 — Closest SIMPAT published precedents materially narrow novelty (high, cannot resolve by prose alone)
Zakarya/Gillam2019 already validate modified CloudSim with analytical/statistical models plus traces/testbed; Vondra/Šedivý2017 SIMPAT already use queue-network autoscaling model to address CloudSim limitations; Mechalikh et al2025 SIMPAT fully compared 24 simulator tools. Specific exact-version callback, service/clock and explicit FIFO recurrence remain new *executed observations*, but novelty of **a full-length methodology paper is not yet established**. Sources and access tiers documented in [SIMPAT direct prior art](SIMPAT_DIRECT_ZAKARYA_AND_VONDRA_PRIOR_ART_2026-11-18.md). Don't claim literature first or physical simulator bug.

### M7 — Researcher-facing reproducibility and truthful publication declarations (moderate, partial)
A2 original run44215741883 and output ZIP SHA256 1d29943... remain evidence; 24-case source table/SVG directly pinned, static CI passed. GitHub Actions artifacts may expire: journal data availability ought to list an immutable persistent **release/archived repository DOI if actually created**, not an invented DOI. FGCS CASPER exact status should be verified by corresponding author (existing manuscript wrongly states “submitted” as an unconditional fact), cross-paper overlap and attribution need human audit. Elsevier AI-related actual tool(s), use during source code and manuscript development, author responsibility, CRediT/funding/conflicts/permissions all must be factually approved; do not state approved yet.

## Practical go/no-go assessment
- **Scientific reproducibility within the chosen simulator fixture: supported** by A1/A2/A3 and independent code/data consistency checks.
- **First-in-literature/meaningful new simulation methodology: not demonstrated** by current 12 references; closest prior studies have stronger validation.
- **Journal formatting / technical readiness: progressing**, not sufficient alone.
- **Recommendation before user-approved actual submission:** keep preparing bounded author-review version; **HOLD** blanket “submit ready” status. Decide whether a meaningful simulation-model *principle* can be isolated that is not a tautology of comparing two knowingly non-equivalent models. If not, pursuing a narrower technical-note-type outlet may be more defensible. No fabricated causal evidence or unnecessary stage expansion.

## Concrete manuscript adjustments authorized by currently verified evidence
1. Repair original FGCS manuscript editorial status to “separate earlier CASPER study/manuscript” unless author verified submission.
2. Use consistent “model disagreement at synthetic thresholds” and “after-completion duration diagnostic” language.
3. Add explicit construct-level limitation: model differences are expected if two defined models differ; empirical contribution is **quantifying their gap** for *exact fixed scenarios*, not proving an unexpected bug.
4. Update data availability to distinguish persistent git source vs potentially expiring Actions archive.
5. All original A1/A2/A3 numbers and title frozen; no new experiments requested.

**Next gate:** conduct scientific GO/NO-GO review against important SIMPAT precedents; final author and journal requirements. Program B preserved, not started. Old 30k cross-runtime parity FAIL and Stage65 safety FAIL unchanged.
