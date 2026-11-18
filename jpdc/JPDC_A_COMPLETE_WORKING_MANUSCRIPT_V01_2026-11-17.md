# DRAFT — Event-Granularity and Queue-Admission Semantics in Cloud–Edge Scheduling Simulation: A Reproducible Cross-Model Study

**WORKING MANUSCRIPT v0.1, 2026-11-17.** NOT SUBMISSION-READY. This is a scientifically scoped author-editable full-outline draft grounded in the project’s current verified measurements, not a literature-vetted final article. No invented literature citations, no claimed journal acceptance or field deployment. Author must independently approve all claims and prepare final bibliography, figures, tables, acknowledgments and declarations.

## Abstract

Discrete-event simulation is frequently used to evaluate online cloud–edge schedulers, but comparisons can depend on the semantics of task arrival, event updates, admission, and execution-list accounting. We investigate how these semantics affect queue-level evaluation in CloudSimPlus 8.5.7 relative to an explicitly defined event-independent capacity-matched FIFO reference. First, we instrument a six-case, three-task native Java microexperiment and observe 54 dynamic execution-eligibility callbacks. Two cases show a later-submitted task admitted to the execution list while an earlier-submitted task remains on the waiting list; exact reruns and uninstrumented reference execution reproduce the same queue observations. Second, we perform a preregistered full-factorial study of two synthetic arrival families, three deterministic timing variations, two minimum-event intervals, and one- versus two-PE scheduling: 24 native cases and 288 completed Cloudlets. An independent parser recomputes the corresponding one- or two-server FIFO reference from observed native submission timestamps. Across the 24 cases, maximum within-case absolute differences between native-reported waiting time and the reference range from 24 to 246 ms. The two models disagree on deadline classification for 86 of 288 tasks at a fixed submission-plus-25-ms threshold and 107 of 288 at a submission-plus-50-ms threshold. These findings establish configuration-dependent model discrepancies for the tested synthetic scenarios; they do not establish a CloudSimPlus bug, physical-CPU start times, real-world deadline prevalence, or a scheduling-policy performance gain. We discuss implications for reproducible, model-conditional cloud–edge scheduling evaluation.

**Keywords (draft):** discrete-event simulation; cloud–edge scheduling; queue semantics; CloudSimPlus; reproducibility; model fidelity.

## 1. Introduction

Deadline-aware dispatch is commonly studied through simulated cloud–edge computing environments, where a scheduling decision interacts with job arrivals, CPU capacity, queue admission and event processing. A basic methodological question is whether a queue abstraction used to estimate waiting time has the same operational meaning as the queue states and timing reported by a particular discrete-event simulator. If not, comparisons that differ only in timing or simulator event cadence can disagree even before evaluating a new scheduling algorithm.

This manuscript addresses that question with a deliberately narrow reproducible simulator-semantics study. It does not propose a replacement for the original CASPER algorithm, and it does not assert a universal FIFO violation by CloudSimPlus. Instead, it explicitly defines a capacity-matched event-independent FIFO reference and evaluates whether native Java CloudSimPlus 8.5.7 SpaceShared observations match that reference under controlled, fully disclosed CPU-only workloads.

Our intended contributions are (i) an instrumented same-source native queue-admission study with concrete callback evidence and an uninstrumented control, (ii) a preregistered multi-condition comparison of native queue-wait and deadline classification against an explicit FIFO reference, and (iii) a reproducibility and limitations protocol that avoids treating artificial queue assumptions as physical ground truth. The empirical scope is fixed synthetic workloads, not factory telemetry.

**AUTHOR TO COMPLETE:** Position these contributions against peer-reviewed prior work on discrete-event simulation semantics, CloudSimPlus SpaceShared scheduling, simulation model validity and cloud–edge performance evaluation. Include direct primary references and a properly attributed original-CASPER-vs-this-study differentiation table. No unsupported priority/novelty claim until this search is complete.

## 2. Related work and originality boundary

**TODO — FULL CITED SECTION REQUIRED.** This paper is distinct in research question from the earlier FGCS CASPER scheduling study: the latter presents the algorithm and its uncertainty-based/feedback-related mechanisms, whereas the present work evaluates native simulator event and queue semantics against an explicitly constructed reference. The earlier manuscript already discusses some shortcomings of one-step queue estimates and feedback limitations; these are background, not new contributions here. Cite the earlier FGCS paper using its actual publication status (submitted manuscript if still under review) and use the complete full-text overlap audit before final submission.

Identify primary source documentation/papers for CloudSimPlus, SpaceShared, discrete-event timing and reproducible simulation. Avoid citing repository CI as a substitute for methodological literature. Benchmark exact software versions, not unspecified current source versions.

## 3. Models and measurement definitions

### 3.1 Native simulator

We run Java 17 with the published CloudSimPlus 8.5.7 binary. Each simulator case has a single SpaceShared VM with either one or two processing elements (PEs), sufficient host capacity and CPU-only one-PE Cloudlets. The native scheduler generates its own event updates and reported start-wait accounting. We record actual submit callback order and timestamps, the execution and waiting lists immediately surrounding task submission, the completion callback clock, native reported wait, and native total execution duration.

### 3.2 Defined FIFO reference (not a surrogate ground truth)

For each case, the reference takes the **actual observed native task submission timestamps** and their actual submission order. All jobs request one PE, and the reference has m identical FIFO servers, where m is the native VM PE count (1 or 2). At each submission in observed order, assign the job to the earliest available server, breaking a server tie by server index; set its start to the later of actual submission and that server’s next-free time, then advance that server by the task’s original requested CPU duration. FIFO reference waiting time is this computed start minus observed submission.

The reference intentionally omits native CloudSimPlus callback cadence and execution-time accounting. Therefore, a difference between the two traces indicates a **difference between model semantics as defined**, not a measured library defect or a proof that either model is the physically correct scheduler.

### 3.3 Waiting and deadline-classification outcomes

The primary per-case outcome is the maximum across 12 jobs of the absolute discrepancy between native reported waiting and reference waiting (milliseconds). Secondary outcomes are mean absolute and mean signed waiting differences. Deadline classifications are compared at two preregistered sensitivity thresholds: the actual observed native submit time plus 25 ms and plus 50 ms. Native finish is the CloudSimPlus finish callback time; FIFO finish is reference start plus requested service. The thresholds are synthetic analytical margins, **not observed IIoT service-level objectives**.

## 4. Experimental design and reproducibility

### 4.1 Six-case dynamic admission diagnosis

The microcase uses three fixed nominal CPU service requests of 8.099623, 4.730689 and 9.120283 ms, with the third nominal arrival offset at 4.0997406, 8.0997406 or 18.0997406 ms. Each is crossed with minimum event times 1 microsecond or 5 milliseconds. The native scheduler’s method-level execution-eligibility callback is logged by a passive subclass that invokes the original superclass method exactly once and records its returned decision; original admission and update callbacks are also logged. We compare the instrumented and original Java runs after filtering the added callback-only trace rows.

The [actual successful A1 CI run](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44214864810) yielded six complete cases, 18/18 finished jobs and 54 observed eligibility callbacks. A later-submitted job joined the native execution list while an earlier-submitted job remained waiting only in ORIGINAL_5MS and LATE10_5MS. The extra callback logger did not change the original source trace under this comparison. A method-level waiting-promotion callback was not directly instrumented; we therefore do not identify the unique causal branch responsible for all bypass observations.

### 4.2 Prospective 24-case generalization

The [frozen A2 protocol](JPDC_A2_BOUNDED_GENERALIZATION_PREREG_2026-11-17.md) predates the actual final successful A2 Java run. Two deterministic synthetic workload families are considered: STAGGERED (12 nominal arrivals every 3 ms) and BURSTY (four groups of three arrivals every 12 ms). Requested service durations are [8, 13, 5, 19, 7, 11, 17, 6, 14, 9, 16, 10] ms; the three predeclared variants adjust arrivals with fixed submillisecond jitter. These factors are crossed with minimum event intervals of 1 microsecond or 5 milliseconds and native VM capacities of one or two PEs. The resulting 2 × 3 × 2 × 2 factorial comprises **24 cases and 288 Cloudlets**. The three variants are *deterministic sensitivity configurations*, not independently sampled real workloads.

The [actual A2 Java CI run](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44215741883) completed 288/288 jobs and the native log reproduced byte for byte. Two separate Python implementations recomputed reference waiting and deadline classifications from the original native log and passed. Both earlier unsuccessful A2 CI attempts remain archived: one revealed a Java generic-type compile issue; another completed simulation but failed in CSV audit parsing. Those defects were corrected without changing the frozen experimental workload.

## 5. Results

### 5.1 Queue-admission transition and callback evidence

In the 5-ms original-arrival microcase, the native scheduler displayed EXEC=[] and WAIT=[1] immediately before a later task submission; after submission it displayed EXEC=[2] and WAIT=[1]. The later-arrival configuration produced the same class of direct-submit list-state transition. Other configurations did not produce that same overtaking signature. Direct method instrumentation confirmed 54 eligibility callback invocations across the six simulations, while preserving control traces. Execution-list membership must not be equated with precise physical CPU commencement.

### 5.2 Waiting-time discrepancies across the full factorial

The complete [verified A2 table](JPDC_A2_BOUNDED_GENERALIZATION_VERIFIED_2026-11-17.md) reports all 24 cells. Case-level maxima of absolute native-reported versus FIFO-reference waiting discrepancy ranged **24.0–246.0 ms**. The largest discrepancy (246 ms) occurred in the BURSTY_S2_5MS_P1 case. Across the 12 STAGGERED cells, the median of within-case maxima was **73.3055 ms** (range 24–171 ms); for the 12 BURSTY cells, the median was **87.0 ms** (range 25.005–246 ms). These summaries describe the designed fixed conditions and must not be interpreted as random-population estimates.

**FIGURE TODO:** a compact 2-family × 2-minEvent × 2-capacity grouped chart showing all three variants and their maximum waiting discrepancy; avoid omitting unfavorable/nonextreme cells.

### 5.3 Consequences for synthetic deadline classifications

With deadlines defined as native actual submit time plus 25 ms, the native and reference models disagreed on **86/288 paired job classifications**. At plus 50 ms they disagreed for **107/288**. These descriptive counts use repeated deterministic configuration variants; they are neither independent Bernoulli evidence for inferential testing nor evidence of field application deadline error.

**TABLE TODO:** show all 24 cells and both deadline disagreement counts from the verified A2 report; include the entire tested denominator and indicate the declared arbitrariness of the deadline thresholds.

## 6. Discussion

The observed differences are consistent with the general concern that discrete-event scheduler behavior is not interchangeable with an analytically defined event-independent FIFO service model. Native admission decisions, waiting-list promotion, service-accounting and event cadence may interact. However, this study does not isolate the unique causal contribution of each internal CloudSimPlus branch and does not establish that the library’s documented behavior is incorrect. Nor does passing a simulator trace audit imply that an abstract event reference models CPU hardware.

For cloud–edge scheduling studies, the practical implication is not to assume that an approximate queue-wait predictor is dynamically equivalent to a particular simulator merely because both employ one-PE tasks or use the label FCFS/SpaceShared. Report the actual event model, simulator version, task admission semantics, observed timing origin, independent reference definition and unresolved model differences. Uncertainty-aware routing performance cannot be inferred from this measurement study.

**AUTHOR TO COMPLETE:** Discuss comparable methodological work and why the present prospective 24-case matrix adds a distinct empirical answer beyond both existing CloudSimPlus documentation and FGCS CASPER. Check whether venue JPDC appreciates the measured systems-evaluation contribution; a different specialized journal may be preferable if novelty cannot be demonstrated.

## 7. Threats to validity

**Model construct.** Every workload is fixed and synthetic, with one-PE CPU-only tasks and no real network transfers, hardware contention, factory task traces, real deadline requirements or power measurements. The declared reference is an abstraction, and native-reported total execution differs from requested work under event processing.

**Internal attribution.** The extra passive eligibility method instrumentation does not visibly change old reference results, but a waiting-promotion callback was not instrumented. Separate sources of discrepancy—callback event granularity, admission timing, execution-length accounting—remain entangled. Neither the wait discrepancy nor the direct EXEC/WAIT observation alone identifies a defect.

**Statistical validity.** Three fixed timing variants per family are not independent source-level population draws. The 288 jobs belong to 24 designed, correlated simulator configurations and should not be treated as independent inferential replicates. Descriptive ranges and counts are appropriate; stronger confidence claims require a new sampling design.

**External validity and novelty.** No performance claim transfers to deployed edge devices or IIoT factories. This article is a simulator-methodology study, not a new CASPER scheduler paper. A distinct peer-reviewed related-work comparison and full overlap audit are required before submission.

## 8. Reproducibility and data availability

Original publicly auditable experiment descriptions, source commits, GitHub Actions runs and archived original outputs are tracked in the project repo [CASPER IIoT CloudSim](https://github.com/afshinyaghoobi/casper-iiot-cloudsim). The original completed A2 run ID is 44215741883, code commit 31a4acf167078ccbb255f01034630bca64ce40e8, archived artifact ID 14387238746, ZIP SHA256 1d29943e5e48d27f65eed186df23ff22d3dd7bdab381ebe63fca88dba1e3bb4b. Original native log SHA256 9fb08d07fe9741772b0de59a837046d0152362d3724da04daf02ccbc3d879391. The frozen code and source-archive verification ensure traceability within the documented environment, not general physical fidelity.

## 9. Conclusion

For the tested 24 synthetic CloudSimPlus 8.5.7 SpaceShared conditions, queue waiting and synthetic deadline classifications differ materially from an explicitly defined event-independent capacity-matched FIFO reference. The differences occur across controlled arrival patterns, event intervals and capacity settings, including cases without a directly observed admission-list bypass. The study illustrates why queue-model assumptions and native discrete-event scheduling semantics must be distinguished in reproducible cloud–edge evaluation. More precise attribution of waiting promotion and validation against independently sourced deployment workloads remain future research questions.

---

## Mandatory pre-submission author checklist

- [ ] Complete primary-literature related-work search and exact publisher references; remove all placeholders.
- [ ] Verify mathematical equations, exact simulator class contract and m-server semantics wording.
- [ ] Ensure a separate, genuinely original contribution relative to the full first FGCS manuscript and known literature.
- [ ] Create final 24-case figure and table directly from original verified JSON.
- [ ] Validate all 24 raw numbers and confirm source Git SHA, ZIP SHA, code/data links.
- [ ] Assess whether the article's contribution fits JPDC editorial scope; consider a more appropriate journal if not.
- [ ] Decide authors, approvals, journal declarations, ethics and AI-use disclosure under current policies.
- [ ] Write final cover letter, journal-specific submission files and formatting.
- [ ] Keep Program B risk-aware new scheduling method separate and unstarted.
