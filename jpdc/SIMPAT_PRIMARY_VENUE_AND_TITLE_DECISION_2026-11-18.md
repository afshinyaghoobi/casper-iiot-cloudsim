# PRIMARY JOURNAL SELECTED: Simulation Modelling Practice and Theory (SIMPAT) — 2026-11-18

**User decision:** The first Program A paper now targets **Simulation Modelling Practice and Theory** (Elsevier), official journal https://shop.elsevier.com/journals/simulation-modelling-practice-and-theory/1569-190X. JPDC and other venues remain alternatives, not simultaneous targets. Research scope remains bounded; do not run arbitrary extra experiments merely to inflate stage counts. **Submission has NOT happened.**

## Working manuscript and chosen title

[New SIMPAT-oriented manuscript v0.7](SIMPAT_MANUSCRIPT_V07_IOT_CONTEXT_2026-11-18.md):
**Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation**

**Naming rationale:** The journal's *current publisher scope* explicitly includes IoT, cloud/fog/edge simulation, verification/validation, model comparison and experimental design (Elsevier source https://shop.elsevier.com/journals/simulation-modelling-practice-and-theory/1569-190X). The simulations themselves comprise **ONE VM**, one/two PEs, fixed synthetic CPU-only jobs: this does NOT justify an unqualified claim of *Industrial Internet of Things* (IIoT), industrial production, field validation, or a fully evaluated IoT network. “Implications for IoT Scheduling Simulation” denotes evaluation relevance, and the abstract/limitations must explicitly explain the *absence of empirical IoT trace/network validation*. The original v0.6 paper remains unchanged at [v0.6](JPDC_A_JOURNAL_FACING_MANUSCRIPT_V06_2026-11-18.md).

**Alternative conservative titles** if the final direct prior-art check judges even the IoT implication too stretched:
1. *Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: A Reproducible Reference-Model Study* — most literally faithful to current data.
2. *Event-Time and Queue-Accounting Sensitivity in CloudSimPlus 8.5.7 SpaceShared Scheduling: A Reproducible Study* — version and mechanism central.
3. *Queue-Wait and Execution-Time Semantics for IoT Scheduling Evaluation: A CloudSimPlus 8.5.7 Case Study* — more prominent IoT but needs the explicit contextual limitation in first paragraph.

**Do not use in the current title:** `Industrial IoT`, `IIoT`, `IIoT-optimized scheduling`, `real-time industrial cloud-edge networks`, `simulator bug`, `validated on actual IoT workloads`, or `first-ever`.

## Relevant journal-specific literature — stronger novelty screen

Besides the existing CloudSim/accuracy papers (Vondra 2017; Zakarya & Gillam 2019; Casanova 2014; Sallo & Kecskemeti 2023), **this target journal has itself published**:
- *Quality matters: A comprehensive comparative study of edge computing simulators* (2024/2025 journal paper; publisher https://www.sciencedirect.com/science/article/pii/S1569190X24001564), evaluates simulator properties with code/repository and documentation checks. Main risk: merely comparing simulators/limitations is no new novelty; difference is our single-runtime per-event actual Java trace and explicit FIFO reference recurrence. Full text specifics and authors/year must be verified before final metadata/citation.
- *A modular configuration-based rapid verification and validation framework combining analytical and simulation methods for intelligent manufacturing systems* (publisher https://www.sciencedirect.com/science/article/abs/pii/S1569190X25000711), very close **methodological category** (analytical + simulation V&V). No claim this is the same application/code without reading full text.
- *Probeless and decentralised multi-criteria decision support for IoT computation offloading* (publisher https://www.sciencedirect.com/science/article/pii/S1569190X26000419) shows IoT scheduling domain relevance, but it is a true offloading-policy study; our study does NOT introduce/validate such policy.
- *Modelling federated learning workflows for the cloud-to-edge continuum* (publisher https://www.sciencedirect.com/science/article/pii/S1569190X26000821) involves much richer network topologies/heterogeneous workloads; highlighting this is a reminder our fixed CPU single-VM case needs a methodology-specific rather than a broad end-to-end IoT novelty claim.

## Evidence preserved / scientific outcome, independent from venue

A1 version 8.5.7 native six-case eligibility callback observation verified, A2 prospective 24 cases/288 jobs verified, 24-case max-wait differences 24–246ms, equal-weight descriptive mean abs over all 288 job-condition observations 49.0961ms, synthetic +25/+50ms deadline disagreements 86/288 and 107/288, A2 service-duration posthoc 250/288 discrepant and max oracle residual154ms, A3 Datacenter arrival and scheduler submit time aligned in 288/288 native fixed cases. New [journal-facing v0.6 data/figure CI PASS](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44324159517) with [stable 24-cell data](manuscript_a2_primary_24_cases_2026-11-18.csv), [Figure1 SVG](figure_a2_24_case_native_vs_fifo_2026-11-18.svg). **Old Java↔Python 30k strict-FCFS parity FAIL and Stage65 safety FAIL remain unchanged**. Neither A1/A2/A3 nor new IoT title demonstrates observed real-world IoT deadline, policy improvement, CloudSimPlus defect or isolated causal factor.

## Next precise submission gates (bounded)

1. Verify exact citation metadata and closest journal precedent paper *Quality matters*, plus selected closest full-text works where accessible. Avoid claiming full-text review from abstract.
2. Audit changed IoT framing against actual methods, scope and author-approved narrative; keep IIoT out of first-paper title.
3. Adapt final author manuscript to current Elsevier/SIMPAT Guide for Authors and declarations, proper author list/affiliations, AI assistance disclosure, conflict/funding/data statements. Verify current rules at filing time, not stale 2019 archived guide. Check all references and exact overlap treatment vis-à-vis submitted FGCS CASPER manuscript.
4. Reuse archived original A2 native results and journal v0.6 permanent table/figure. No new arbitrary simulations; only if a critical validity question emerges.
5. Submit *only* after author sign-off and actual originality gate. Internal December 20, 2026 target **conditional**; no guaranteed acceptance.

**Program B separate future IIoT/risk-aware scheduling paper** remains reserved, not started. Its eventual title may legitimately use IIoT if it incorporates independent industrial assumptions/data and evidence; do not conflate with Program A.
