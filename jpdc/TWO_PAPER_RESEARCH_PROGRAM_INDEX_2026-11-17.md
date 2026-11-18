# LATEST AUTHOR DECISION — SIMPAT PRIMARY + IoT-CONTEXT TITLE (2026-11-18)

**Program A first-paper journal selected:** Elsevier **Simulation Modelling Practice and Theory (SIMPAT)**, NOT JPDC (now backup/unsuitable unless distinct distributed impact). [Author's selected-venue decision and accuracy guardrails](SIMPAT_PRIMARY_VENUE_AND_TITLE_DECISION_2026-11-18.md). New [working manuscript v0.7](SIMPAT_MANUSCRIPT_V07_IOT_CONTEXT_2026-11-18.md) now titled **Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation**. User asked to include IoT or IIoT: **IoT allowed ONLY as an implications/application context**; exact current tests are one VM, CPU-only, fixed synthetic arrivals, **no actual IoT or industrial IoT dataset/network**; therefore **IIoT NOT scientifically justified in title without new distinct evidence**. SIMPAT official scope includes IoT, cloud/fog/edge and model V&V, but journal also published the closer edge-simulator comparison *Quality matters: A comprehensive comparative study of edge computing simulators*; must compare before submission. v0.6 all-24 source table/SVG static QA PASS, 288 fixed jobs, max246ms, mean abs49.0961ms, deadline disagreements86/288 and107/288, posthoc service oracle residual154ms, A3 clock origin0ms in 288/288. Old strict30k Java↔Python parity FAIL and Stage65 safety FAIL unchanged. **Paper not submitted**; conditional internal Dec20. Next actual work: focus closest SIMPAT precedent, author-approved publication compliance, no arbitrary extra simulation. **Program B remains RESERVED and NOT STARTED**, potential IIoT-specific future work requires separate actual IIoT evidence.

---

# LATEST 2026-11-18 — MANUSCRIPT v0.6 DURABLE PAPER PACKAGE QA PASSED

[Publication-format working manuscript v0.6](JPDC_A_JOURNAL_FACING_MANUSCRIPT_V06_2026-11-18.md) now embeds the **full 24-condition A2 Table 1**, [durably committed editable vector Figure 1](figure_a2_24_case_native_vs_fifo_2026-11-18.svg) and [stable original audited 24-row CSV](manuscript_a2_primary_24_cases_2026-11-18.csv), cleaned internal placeholder labels. Source original A2 ZIP independently rehashed against SHA256 1d29943e5e48d27f65eed186df23ff22d3dd7bdab381ebe63fca88dba1e3bb4b. Original audited fixed 288 job-condition wait MAE=**49.0960972223ms**; across24 case max range24–246ms, synthetic deadline classification disagreements86/288 (+25ms),107/288(+50ms). These are *two models' discrepancies*, not physical ground-truth error or performance gain. [New static paper QA CI run44324159517](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44324159517) **SUCCESS**, 24 source rows matched manuscript/CSV/SVG exactly, check code [here](audit_a2_manuscript_v06_package.py). [Submission readiness / evidence-tier report](JPDC_A_V06_JOURNAL_PACKAGE_CHECKPOINT_2026-11-18.md) records remaining concrete obstacles: nearest primary-paper full text, truly sufficient JPDC originality for single VM CPU-only evaluation, author affiliations/declarations, journal file formatting and venue. **NO JOURNAL SUBMISSION HAS OCCURRED.** A1/A2/A3 original studies frozen verified; posthoc service oracle250/288 mismatched, worst154ms; A3 exact clock origin288/288 matching. Old 30k Java/Python FCFS gate FAIL and Stage65 safety FAIL unaffected. Conditional Dec20 internal target; no open-ended native experiments. Future independent Program B remains RESERVED/NOT STARTED.

---

# 2026-11-18 EDITORIAL CHECKPOINT — MANUSCRIPT v0.5, EVIDENCE-TIERED PRIOR ART, VENUE GO/NOGO

**Program A real state:** [manuscript v0.5](JPDC_A_COMPLETE_WORKING_MANUSCRIPT_V05_2026-11-18.md) now accurately titled *Arrival and Execution-Time Accounting in CloudSimPlus 8.5.7 SpaceShared Scheduling: A Reproducible Reference-Model Comparison* (one VM, CPU-only), includes bounded 288-job results, posthoc service accounting and A3 288-job clock equality, doesn't imply evaluated real multi-node cloud-edge. [Evidence-graded specific prior-art report](JPDC_A_FULLTEXT_EVIDENCE_GRADED_PRIOR_ART_2026-11-18.md) read Sallo/Kecskemeti 2023 open FULL publisher article 'Other simulators' section (that paper's tested CloudSim ignored trace submission time, not transferable to native 8.5.7); Vondra2017 and Zakarya/Gillam2019 FULL TEXT NOT obtained here, publisher summary/abstract only; already establish category overlap on duration inaccuracies and analytical validation. This is a real potential JPDC novelty weakness, not solved by writing more papers or arbitrary experiments. [NEW Venue GO/NOGO](JPDC_A_VENUE_GO_NOGO_MINIMUM_PACKAGE_2026-11-18.md): **NOT YET READY for JPDC submission**; JPDC lacks proven distributed-systems-level contribution with current isolated 1VM 12-job synthetic cases; SMP&T and Journal of Simulation are more directly method-fit candidate venues (official scopes checked), NOT submissions/guaranteed acceptance. Conditional internal Dec20 manuscript target remains, not acceptance promise. **Next:** shortest legitimate full-text checks and manuscript formatting/final author approval/venue choice, not more unneeded simulator runs. A1/A2/A3 provenance frozen and original parity FAIL/Stage65 FAIL preserved. Program B separate research RESERVED, NOT STARTED.

---

# LATEST VERIFIED PROGRAM A CHECKPOINT — A3 VALIDATED AND MANUSCRIPT v0.4 (2026-11-17/18)

**User goal: submit minimum defensible paper, no unnecessary scope expansion.** [Working manuscript v0.4](JPDC_A_COMPLETE_WORKING_MANUSCRIPT_V04_2026-11-17.md), [exact native wait/time-origin audit](JPDC_A3_NATIVE_TIME_ORIGIN_VERIFIED_2026-11-17.md), [successful genuine A3 Java CI run44228414078](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44228414078). Exact publisher CloudSimPlus 8.5.7 source defines `getStartWaitTime = getStartTime - dcArrivalTime`; this could have introduced FIFO-origin mismatch because A2 reference uses `cloudletSubmitInternal` clock, BUT a SAME-WORKLOAD 24-case / 288-job new native source check found 0/288 differing datacenter-arrival vs scheduler-submit timestamps (maximum abs0ms). New A3 extra logs stripped match fresh uninstrumented A2 original log byte-for-byte; full augmented trace repeat PASS. Original max wait discrepancy 246ms remains. Initial A3 run44228241419 FAIL due to nondeterministic order of **two finish listener logging callbacks**, fixed by emitting both records in same listener; never erase failed run. Source run44228012730 PASS and successful A3 artifact14394061608 ZIP SHA256 6e23f0979d9c6bb1b91d21f098ca707efe3e7b465c94e7749d5e97765661775a independently rehashed. This rules out clock origin difference only for this fixed A2 design, NOT causal attribution of residual to scheduler branch. Native-duration posthoc analysis250/288, worst154ms still valid. A1/A2 remain completed, previous original 30k Java↔Python parity FAIL, original Stage65 safety FAIL. **Next focus: manuscript originality / closest prior art / journal suitability and author-approved submission package; no more exploratory simulator work.** Full paper still NOT submitted; target Dec20 conditional. **Program B still RESERVED / NOT STARTED.**

---

# LATEST WORK: JPDC ORIGINALITY PRIOR-ART GATE AND MANUSCRIPT v0.3 — 2026-11-17

New [manuscript v0.3](JPDC_A_COMPLETE_WORKING_MANUSCRIPT_V03_2026-11-17.md) committed: explicit math of actual-submit-order capacity-matched FIFO m-server recurrence; verified 2017/2019/2018/2023 nearest simulator validation literature; appropriately narrower contribution language and 2019 authorship now verified (Zakarya & Gillam). [Specific prior-art matrix](JPDC_A_CLOSEST_PRIOR_ART_AND_NOVELTY_RISK_2026-11-17.md) documents **HIGH overlap** with Vondra et al. 2017 (CloudSim job-duration inaccuracies), Zakarya & Gillam 2019 (CloudSim against simplified analytical references), and Sallo/Kecskemeti 2023 (trace/arrival-time cross-simulator behavior). Exact version 8.5.7 SpaceShared API does NOT promise equality to analytical FIFO reference. Therefore do NOT call 246ms discrepancy proof of bug or novel general discovery. [Submission gate](JPDC_A_SUBMISSION_READINESS_CHECKPOINT_2026-11-17.md) remains **CONDITIONAL**; journal JPDC may require a more distinct distributed-system contribution. Next focus: direct nearest-full-paper comparisons, exact metrics/scientific claim audit and editorial fit; no exploratory simulation without decisive science question. Native runs A1/A2 remain verified, 30k Java↔Python parity FAIL, Stage65 safety FAIL. Program B next paper reserved/not started. User still wants bounded first-paper submission around Dec 20 only if valid.

---

# MANUSCRIPT-FOCUSED LATEST CHECKPOINT — 2026-11-17/18

**User goal:** bounded minimum scientifically defensible JPDC submission; no unnecessary expanding simulations. New [working manuscript v0.2](JPDC_A_COMPLETE_WORKING_MANUSCRIPT_V02_2026-11-17.md) now adds verified primary-reference first pass and corrects A2 native-service-duration confounding. New [posthoc A2 source experiment audit](JPDC_A2_NATIVE_SERVICE_ORACLE_RETROSPECTIVE_VERIFIED_2026-11-17.md) [CI run44216958536](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44216958536) PASSED on ORIGINAL spent 24-case Java log: 250/288 native-reported execution lengths differ from requested; original FIFO max abs wait gap246ms, hindsight reported-duration FIFO max154ms; **ALL24 cases residual>1ms**; synthetic deadline disagreement requested 86/288 at+25ms and 107/288 at+50ms, posthoc oracle58/288 and78/288. This does NOT isolate event callback causality or represent a deployable online oracle. [Verified original source-derivative table + vector SVG](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44217510468) [run44217510468] PASS, artifact14388253276, 24/24 cell CSV and deterministic repeat. [Initial primary literature and FGCS overlap screen](JPDC_A_RELATED_WORK_ORIGINALITY_SCREEN_2026-11-17.md) identifies 2017 CloudSimPlus, 2011 CloudSim, 2013 Sargent V&V and 2014 JPDC SimGrid simulation accuracy precedent; the qualitative notion “simulation models differ” is not automatically novel. [Focused submission GO/NOGO gate](JPDC_A_SUBMISSION_READINESS_CHECKPOINT_2026-11-17.md) now guides next work. **NEXT:** nearest prior-art comparison, scientific claim audit, final figure/format and author-approved submission package; do NOT run unrelated exploratory native trials. Original Java↔Python 30k fidelity FAIL and Stage65 independent safety FAIL persist. Program B future risk-aware scheduling research stays RESERVED/NOT STARTED.

---

# PROGRAM A MANUSCRIPT v0.1 NOW WRITTEN — 2026-11-17

[Integrated initial JPDC working manuscript](JPDC_A_COMPLETE_WORKING_MANUSCRIPT_V01_2026-11-17.md) has actual English Abstract, Introduction, Methods, A1/A2 Results, Discussion, Validity, Conclusion and reproducibility content grounded in frozen 24-cell source JSON. **DRAFT ONLY, NOT SUBMISSION READY**: related-work primary citations, exact FGCS-overlap/novelty audit, complete figures/tables, journal formatting and author verification remain. [A2 audited report](JPDC_A2_BOUNDED_GENERALIZATION_VERIFIED_2026-11-17.md): successful original native 288/288 Cloudlets, 24 conditions, wait max24–246ms, deadline disagreement86/288(+25ms),107/288(+50ms), independent artifact ZIP hash verified. **Next action: targeted literature/originality check, manuscript numeric figure/table generation and editorial readiness; no more gratuitous native simulations.** Program B reserved.

---

# A2 ACTUAL NEW NATIVE JAVA GENERALIZATION VERIFIED — 2026-11-17/18

New real CloudSimPlus 8.5.7 full [24-case A2 run44215741883](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44215741883) **SUCCESS**, native 288/288 completed, byte-exact native repeat, independent source FIFO auditor **PASS**. Original ZIP artifact14387238746 independently downloaded, SHA256 **1d29943e5e48d27f65eed186df23ff22d3dd7bdab381ebe63fca88dba1e3bb4b**. [Detailed VERIFIED A2 report](JPDC_A2_BOUNDED_GENERALIZATION_VERIFIED_2026-11-17.md), 24-case max absolute native WAIT vs m-server FIFO case discrepancy ranges **24–246ms**, overall worst **246ms BURSTY_S2_5MS_P1**; deadline native/reference classifications differ **86/288** at nominal actual-submit+25ms and **107/288** at+50ms. These are deterministic SYNTHETIC, not independent real-world IIoT samples, nor CASPER gains or CloudSim bug proof. Earlier [A1 dynamic eligibility run44214864810](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44214864810) SUCCESS, 54 method callbacks; no waiting-promotion branch proof. Original 30k Java/Python strict-FCFS gate FAIL and Stage65 policy safety FAIL remain. **Program A next step changes to full manuscript writing and focused FGCS originality/related-work check, NOT more endlessly expanding simulations.** Program B future new policy paper still RESERVED. Initial A2 CI errors from Java generic type and parser row shape were corrected without changing frozen inputs; original failed runs retained.

---

# ACTIVE PROGRAM A UPDATE — NEW A1 JAVA ELIGIBILITY OBSERVED / A2 PROTOCOL FROZEN (2026-11-17)

New [A1 verified real Java CI evidence](JPDC_A1_DYNAMIC_ELIGIBILITY_CALLBACK_VERIFIED_2026-11-17.md): actual GitHub run [44214864810](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44214864810) SUCCESS, Java CloudSimPlus 8.5.7 six cases /18 completed; **54 dynamically observed canExecuteCloudletInternal callbacks**, two prior bypass cases repeated and passive new vs old harness output byte identical after stripping eligibility-only rows. A1 PARTIAL: WAIT-promotion callback path itself not yet dynamically instrumented. [A2 prospective 24-case protocol](JPDC_A2_BOUNDED_GENERALIZATION_PREREG_2026-11-17.md) newly COMMITTED before outcomes, but **A2 actual Java experiment NOT RUN**. Current highest value is implement/run A2 and then manuscript, not enlarge diagnostic scope. Original 30k parity FAIL and Stage65 safety FAIL unchanged. Program B still RESERVED; internal JPDC submission target December remains conditional.

---

# CASPER Research Program — Two Distinct Papers / Single Source of Truth

**Decision recorded:** 2026-11-17. **Research priority:** FINISH PROGRAM A; PRESERVE PROGRAM B FOR LATER.
This file is the starting point whenever ChatGPT context is lost or research resumes. A roadmap is NOT proof of completion, journal suitability or acceptance.

## Quick project table

| | PROGRAM A — NOW | PROGRAM B — LATER |
|---|---|---|
| Identity | Java CloudSimPlus event-granularity, queue-admission/strict-FCFS semantics and reproducible cloud-edge evaluation | NEW risk-aware online scheduling decision rule with selective / delayed feedback |
| Working title | *Event-Granularity and Queue-Admission Semantics in Cloud–Edge Scheduling Simulation: A Reproducible Cross-Model Study* | *Risk-Aware Online Cloud–Edge Scheduling under Selective Feedback and Queue Uncertainty* |
| Proposed journal | **JPDC**, suitability contingent on meaningful new systems-evaluation contribution | **TBD** after novel method and evidence; do not promise JPDC or another journal |
| Current state | Existing genuine Java six-case result and original v8.5.7 source audit VERIFIED; manuscript incomplete; new bounded generalization study NOT RUN | ROADMAP ONLY, NOT STARTED; candidates hypothetical; no new policy outcome |
| Frozen blockers / caveats | Java vs Python strict FCFS 30k 9.12140093294972ms >5ms FAIL; original Stage65 safety FAIL (do not suppress) | Must not recycle original FGCS CASPER, failed Stage64/65 or Program A's same experimental novelty |
| Plan | [A minimum-submittable plan](JPDC_MINIMUM_SUBMITTABLE_PAPER_PLAN_2026-11-17.md) | [B future full roadmap](NEXT_PAPER_RISK_AWARE_SCHEDULING_RESEARCH_ROADMAP_2026-11-17.md) |
| Schedule | Internal target Dec 15–20, 2026 if gates pass; fallback Dec 20, 2026–Jan 10, 2027 | Tentative ~6–10 weeks AFTER deliberate restart, dependent on viable method |
| Next action | Execute already-preregistered native method/callback trace, then bounded preregistered 2-workload-family study; write paper concurrently | NO execution until A package completed or explicit direction to switch |

## Current-paper milestones and definition of DONE

| ID | Dates (planned) | Deliverable | Status as of 2026-11-17 |
|---|---|---|---|
| A0 | Nov 17 | Select narrow scientifically defensible paper scope; scope and FGCS overlap risks documented | PLAN RECORDED; final abstract/novelty table still pending |
| A1 | Nov 18–24 | Complete [dynamic native callback prereg](NATIVE_V857_DYNAMIC_ADMISSION_TRACE_PREREG_2026-11-17.md), new original Java run + independent auditor + evidence | NOT EXECUTED |
| A2 | Nov 18–24 | Freeze modest new generalization experiment (at least staggered/bursty arrivals, event gaps, 1/2 PE) including deadline margin and completion invariants BEFORE results | NOT REGISTERED |
| A3 | Nov 25–Dec 3 | Run new fixed matrix, independent audit, plots and effect sizes including negative cases | NOT EXECUTED |
| A4 | Dec 4–11 | Draft FULL JPDC manuscript, focused original-vs-FGCS contribution table, references, reproducibility | PARTIAL TEXT ONLY: [Stage68 draft](STAGE68_JPDC_MANUSCRIPT_VALIDITY_AND_NEGATIVE_RESULTS_DRAFT_2026-11-14.md) |
| A5 | Dec 12–18 | Numerical audits, coauthor approval, journal formatting / ethics / declarations and complete submission package | NOT STARTED |
| A6 | Dec 15–20 tentative | Author submits to JPDC only after scientific and originality go/no-go; if unmet, narrow/pivot rather than fabricate novelty | NOT SUBMITTED |

**Minimum publishable integrity:** define a distinct systems evaluation research question (not just three jobs); demonstrate credible controlled outcomes beyond original isolated case; transparently note model and cross-runtime differences; independently verify raw data; report all relevant negative results; no algorithm superiority or CloudSim bug claims. No demand to fix all Stage65 issues, ingest all 500 Google sources, obtain hardware or finish all future risk-aware policy ideas.

## Scientific separation and source-of-truth rules

1. **FGCS prior paper:** Original CASPER algorithm, uncertainty certificates, health/probes and several feedback limitations are preexisting. See [full-text overlap audit](FGCS_FULL_MANUSCRIPT_VS_JPDC_OVERLAP_AUDIT_2026-11-04.md).
2. **A:** independent *simulation/evaluation semantics* study; foreground methods/evidence of event timing, queue admission and reproducible model comparison; do not market original CASPER algorithm as new.
3. **B:** *distinct NEW online scheduling policy* with formal observable-information contract and independent prospective holdout; not a paper on the same Java microfixture with a different title.
4. Reuse background, infrastructure and citations with attribution; do not reuse same principal original result as two separate novelties, nor split one article unnaturally.
5. Use exact source/commit IDs and independent archived output checks for claims; distinguish code pushed from test actually run.
6. A negative outcome must remain negative. Never reinterpret failed original parity or Stage65 safety via retrospectively weakened gates.
7. No automatic transfer of manuscript title, results, unspent seeds or algorithm state from A to B. Freeze and independently document B's new experimental source split when B starts.

## Progress updates on GitHub

- Any significant completed step should update its ORIGINAL evidence report plus A or B roadmap status, with actual commit/run IDs, measured outcomes, and honest FAIL/PASS.
- At submission, freeze A's code/artifacts/manuscript references, record actual submission date and manuscript ID only if really obtained; change Program B status to ACTIVE only on an explicit research decision.
- Always read this index first, then [short handoff](CHAT_RESTART_HANDOFF.md), [long handoff](CURRENT_RESEARCH_HANDOFF.md), A plan and B plan.
- User's «ادامه» while A active: advance the **actual current-paper work**, not hypothetical B method performance and not endless provenance engineering. B roadmap is parked and protected from scope creep.
