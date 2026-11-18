# Program A — Venue decision and minimal submission-quality package (2026-11-18)

**Status:** AUTHOR-DECISION PENDING. **Current evidence does NOT justify labeling the current version an already submission-ready full JPDC research paper.** This is a non-perfectionist scientific go/no-go rather than an instruction to run unlimited simulations. Original target December 20, 2026 remains an *internal conditional draft-delivery milestone*, not a required journal submission irrespective of quality.

## 1. Research question actually supported

**Bounded, evidence-backed:** How do native versioned CloudSimPlus 8.5.7 SpaceShared scheduling accounting and task-admission events differ from a separately defined event-independent, capacity-matched analytical FIFO server model under fixed 1VM synthetic conditions? What are the descriptive consequences for wait measurements and synthetic deadline classifications?

**Measured and auditable:** A1 actual six-case 18-job event tracing with 54 eligibility callback observations; frozen A2 native 24-cell 288-job full-factorial compared with an analytical recurrence (max within-case waiting gap 24–246ms; disagreements86/288+25ms,107/288+50ms); posthoc A2 native-reported service-duration diagnostic (250/288 duration differences; largest oracle-reference wait gap154ms); separate A3 288-job source+dynamic check (datacenter arrival equals native scheduler-submit clock in all fixed jobs). CI logs and artifacts linked in complete [v0.5 manuscript](JPDC_A_COMPLETE_WORKING_MANUSCRIPT_V05_2026-11-18.md) and [A3 verified report](JPDC_A3_NATIVE_TIME_ORIGIN_VERIFIED_2026-11-17.md). Original 30k Java/Python parity gate FAIL and Stage65 policy safety FAIL remain.

**Not supported:** a new CASPER method, simulator contract bug, policy rank reversal, physical field fidelity, independent randomly sampled IIoT outcomes, general v8.5.7 system equivalence or error source causally isolated to one path. Do not exaggerate simple 1VM tests as distributed multi-node architecture.

## 2. Evidence-graded closest work and novelty judgement

[Direct access-tier review](JPDC_A_FULLTEXT_EVIDENCE_GRADED_PRIOR_ART_2026-11-18.md) found:
- Vondra et al., 2017 already identify and address job-duration calculation inaccuracies in CloudSim/CloudAnalyst. Publisher detailed summary inspected, **full text not inspected** this continuation.
- Zakarya and Gillam, 2019 already compare CloudSim model accuracy with analytical/statistical models, abstract + institutional metadata only; **full text not inspected** this continuation.
- Sallo and Kecskemeti, 2023 open FULL publisher text explicitly reports their tested CloudSim trace simulator ignoring task submit times in a cross-simulator comparison, but does **not** use this exact 8.5.7 setup. Source section 'Other simulators' actually inspected.
- Casanova et al. 2014 JPDC SimGrid modeling/accuracy work establishes fidelity as an existing distributed-systems concern. This current continuation read publisher description/abstract-level information, not full paper.
- Exact CloudSimPlus 8.5.7 source and Javadoc do not guarantee identical outcomes under the deliberately different FIFO reference.

**Judgment: empirical version-specific observation is genuinely newly executed in repo, but whether it rises to a new substantial full-length JPDC contribution is UNSUBSTANTIATED.** Published precedents weaken any claim of generic novelty. More simulation cells won't automatically address this.

## 3. Recommended journal path (scope-based; no invented acceptance rates)

| Choice | Journal scope evidence | Fit to A1–A3 as currently written | Decision |
|---|---|---|---|
| **Journal of Parallel and Distributed Computing (JPDC)**, Elsevier, https://shop.elsevier.com/journals/journal-of-parallel-and-distributed-computing/0743-7315 | Original contributions on parallel/distributed theory, design, evaluation/use; includes cloud/edge/fog and performance | **Weak-to-conditional.** A single VM / 12-job synthetic simulator-semantics study lacks direct distributed architecture/policy result. | Hold journal-specific submission prep until a defensible non-trivial JPDC contribution/novelty rationale emerges. Do not press submit because of date target. |
| **Simulation Modelling Practice and Theory (SMP&T)**, Elsevier, https://shop.elsevier.com/journals/simulation-modelling-practice-and-theory/1569-190X | Official scope explicitly includes modeling, simulation validation/verification, sensitivity, experimental design, computing systems/edge/cloud simulation | **More directly aligned by subject** with semantics/construct validity; still expects original high-quality method or relevant evidence | Highest topical-fit alternative to assess using its current Guide for Authors and nearest papers; no assumption of automatic acceptance. |
| **Journal of Simulation**, Taylor & Francis / OR Society, https://www.tandfonline.com/tjsm ; https://www.theorsociety.com/ORS/ORS/Publications/Journals/JOS.aspx | Official description allows simulation theory/methods, practical studies, empirical controlled studies and technical notes | **Plausible more compact model-validation/technical-note framing**; contribution must meet editorial merit and specific article type | Second topical-fit alternative, not automatically preferred over SMP&T without final literature and author preference. |

**No switch of journal has been made**, and no simultaneous submission to multiple venues is planned.

## 4. Bounded remaining tasks (no extra science theater)

1. **Final source-claim review:** inspect Vondra 2017 and Zakarya 2019 full text where legitimately accessible; until then mark comparison as abstract/metadata only. Remove all first-in-literature claims. Ensure earlier FGCS manuscript’s policy and caveats remain separately attributed.
2. **Final manuscript:** clean internal notes/checklists out of submission copy, convert code/equations to journal format, position chart+24-cell table in manuscript (original CI artifact), include exact data/software archiving links and separate synthetic-only external-validity limitations.
3. **One author decision:** choose (a) JPDC only if there is an independently defensible distributed-systems contribution, or (b) more scope-compatible modeling/simulation venue while honestly describing size and novelty. A venue switch is not scientific failure.
4. **Author/editorial compliance:** authors/affiliations, funding/conflicts, AI policy, originality declaration, any editor-required data/code availability, and guide-for-authors checks.
5. **Freeze**: no further broad factorial grids, Google trace recovery campaigns, arbitrary stage numbers, alternative algorithm designs or simulated random significance tests before a specific validity-critical issue is identified.

## 5. Independent next paper remains reserved

Program B is *Risk-Aware Online Cloud–Edge Scheduling under Selective Feedback and Queue Uncertainty* with a separate genuinely new policy/risk model, independent source-seed training/holdout and overlap checks. See [future research roadmap](NEXT_PAPER_RISK_AWARE_SCHEDULING_RESEARCH_ROADMAP_2026-11-17.md). It is **NOT started**, and Program A's simulator study must not be recast as Program B's method contribution.

**Next chat continuation:** authorship-quality focused manuscript v0.6 and exact closest-paper full-text checks where available, then a venue GO/NO-GO decision. Do not initiate repository-wide new experiments without evidence of publication-critical necessity.
