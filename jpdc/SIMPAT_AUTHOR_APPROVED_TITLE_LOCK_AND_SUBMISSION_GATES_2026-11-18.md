# SIMPAT Program A — AUTHOR-APPROVED EXACT TITLE LOCK and minimum submission protocol (2026-11-18)

**TITLE IS NOW USER-APPROVED AND LOCKED FOR PROGRAM A** (do not change without an explicit new user request):
**Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation**

**Target journal (selected):** *Simulation Modelling Practice and Theory* (Elsevier; ISSN 1569-190X), https://shop.elsevier.com/journals/simulation-modelling-practice-and-theory/1569-190X . User explicitly selected journal in preceding turn, then explicitly accepted this exact title. **No actual submission has occurred.**

**Source of currently verified scope:** official Elsevier publisher page inspected 2026-11-18. Explicitly covers simulation verification/validation, selection/comparison methods, IoT, computer systems, cloud/fog/edge, and requires significant contribution and transparent model development, implementation and validation/verification. Scope-fit does **not** establish publication novelty or ensure acceptance. Important: official page notes real-data validation for application studies; our work is a bounded CPU-only *synthetic simulator-accounting methods study*, not a validated real IoT deployment. Do not imply industrial hardware, physical queue ground truth or actual IoT empirical data.

**Current primary manuscript:** [SIMPAT v0.7](SIMPAT_MANUSCRIPT_V07_IOT_CONTEXT_2026-11-18.md), inherited independently checked all-24 A2 original table and durable SVG/CSV from journal-facing v0.6. Mandatory exact-title check must be applied to every future new manuscript revision and letter. V0.7 already starts with exact user-approved title, frozen title string in single source of truth here.

## Scientific claims permitted and scope boundaries

- A1: six native three-job cases in CloudSimPlus 8.5.7; instrumented 54 eligibility callbacks and admission-list observations, without universal proof of bug/CPU start.
- A2 preregistered: **24** fixed native configurations, **288** completed jobs, max within-case requested-service FIFO comparison gap 24–246ms; descriptive mean abs wait difference49.0961ms across these job-condition observations; synthetic deadline classification disagreements86/288 at submit+25ms and107/288 at submit+50ms.
- A2 **retrospective** after-completion service-oracle:250/288 reported execution durations differ; worst max discrepancy154ms, not a causal isolated effect; all24 case residuals>1ms.
- A3 source-verified `getStartWaitTime` definition and passive native real-Java 288/288 datacenter-arrival/scheduler-submit timestamps match for *fixed tested setup*, repeat control PASS.
- NO actual sensor network or IIoT workload, NO real-time IoT deployment validation, NO policy gain, NO proof of CloudSimPlus defect; generic simulator validity/CloudSim duration issues predate this work and overlap with published SIMPAT studies.

## Target-journal focused nearest publication risk

*Quality matters: A comprehensive comparative study of edge computing simulators*, **SIMPAT volume 138, article 103042, 2025** (publisher DOI **10.1016/j.simpat.2024.103042**). Search/index metadata identifies authors **Charafeddine Mechalikh, Abd El Heq Silem, Zahra Safavifar, Fatemeh Golpayegani**. Publisher abstract establishes broad comparative review of edge-simulation tools, software quality and modeling capabilities. **Full paper text NOT read in this continuation**: direct ScienceDirect fetch returned HTTP403. Thus cannot assert complete methodological non-overlap; our *hypothesized* distinction is same exact version native scheduler callbacks/clock-origin instrumentation and explicit FIFO-reference waiting/deadline classification, rather than multi-tool qualitative feature comparison. Direct full-paper comparison remains gate. Reference record to verify final citations: https://doi.org/10.1016/j.simpat.2024.103042 ; https://www.sciencedirect.com/science/article/pii/S1569190X24001564 .

Also preserve earlier findings: Vondra et al.2017 CloudSim duration correction; Zakarya & Gillam2019 analytical-vs-simulator accuracy; Sallo & Kecskemeti2023 open full paper differing trace submit handling. Full text of first two not read as of last audit. Avoid novelty claims already covered by these studies.

## Bounded next work; avoid unnecessary perfectionism

1. Keep *exact* approved title in all main files and any submission components.
2. Assess nearest SIMPAT publisher study (2025) and remaining direct papers; accurately label access limitations. Position exact quantitative, version-specific new evidence as a modest reproducible simulator evaluation, not broad priority.
3. Check SIMPAT-specific current Guide for Authors **at actual submission**, particularly publication format, originality/simultaneous submissions, highlights, data availability, CRediT, conflicts, funding, AI-use disclosure; separate author-supplied facts from model-generated drafts and do not invent affiliations/approvals.
4. Final visually inspect Figure1 at journal width, verify notation, PDF or LaTeX/Word package with original A2 evidence. Existing source experiment PASS and static cross-artifact QA PASS; don't launch more simulation without a specific scientific blocker.
5. Author/coauthor approve and submit *only then*. Target about 2026-12-20 is conditional **internal planning date**, not actual submission or review prediction. Manuscript v0.7 is not submitted.

**Program B** is separate and reserved (NOT started). It could use IIoT only if supported by independently designed IIoT evidence. Old 30k cross-runtime parity FAIL and Stage65 safety FAIL remain; no cover-up.
