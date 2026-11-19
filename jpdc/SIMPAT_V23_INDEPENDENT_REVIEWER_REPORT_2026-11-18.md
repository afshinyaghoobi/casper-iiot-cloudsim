# Independent field-specific reviewer assessment — SIMPAT manuscript v2.3

**Review date:** 2026-11-18  
**Manuscript:** `SIMPAT_MANUSCRIPT_V23_EDITORIAL_FOCUS_DRAFT_2026-11-18.md`  
**Exact unchanged title:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation  
**Reviewer perspective:** simulation modelling, distributed systems, queueing measurement and computational reproducibility. **Internal independent critical assessment, NOT actual peer review, editor decision, author-approved revision, or recommendation issued by SIMPAT.**  
**Recommendation for internal submission gate:** **HOLD / not yet ready for full-length original-research submission**. This is not a prediction of the journal's official decision.

## Overall assessment

The manuscript clearly reports a version-specific comparison of native CloudSimPlus 8.5.7 SpaceShared timing measurements against a separately defined m-server FIFO reference. Provenance is unusually explicit for such a study: the 24 deterministic A2 cases, 288 completed jobs, A3 timestamp-origin check, A1 passive tracing, rescan control/treatment and eight additional hand-designed fixtures are documented, and 14 primary/derived files are retained in Git with an SHA256 manifest. The writing correctly avoids treating analytical FIFO as physical ground truth, acknowledges retrospective audits, and reports the failed input-only event-gap hypothesis.

The problem is not that the fixed observations are necessarily invalid. Rather, the study lacks a clearly demonstrated **original, transferable simulation-modelling contribution** of the sort sought by SIMPAT. Prior work already analyzes simulation versus analytical models, timing/resource-duration fidelity and CloudSim-family limitations. The paper's interesting exact-version observational evidence is narrower than a novel method or independently validated general diagnosis. A more concise article could be a useful reproducible case study, but a confirmed journal-specific short-paper category or editorial endorsement has not been established.

## Major comments (within reviewer field; ordered by scientific importance)

**M1. The original contribution remains insufficiently separated from documented stock semantics and prior model validation (Sections 1, 2, 6).** Version-specific WAIT/EXEC observations and a capacity-matched FIFO comparison are real, but neither the waiting-list promotion mechanisms nor mismatches between intentionally different models establish a new method. State precisely which *scientific question becomes answerable* because of this work and which result goes beyond published API behavior and the CloudSim validation literature. Do not claim a transferable validation framework without an independently tested rule. Evidence: official CloudSimPlus 8.5.7 SpaceShared/Abstract API documentation, Zakarya/Gillam (2019), Vondra/Šedivý (2017), Mechalikh et al. (2025). **Submission-blocking unless authors can articulate a credible incremental original contribution.**

**M2. The native/FIFO timing gap is not causally attributed to event-phase ordering (Sections 3, 5.4, 5.5, 5.8–5.10, 7).** The analytical reference deliberately omits native event scheduling and uses requested rather than native-reported service. A3 removes one clock-origin alternative in this configuration, yet 250/288 jobs have different reported execution durations. The retrospective service swap is after-outcome sensitivity, not a decomposition of causality. The two A1 known-case rescan successes do not isolate the cause of the entire 24-case A2 discrepancy. The present manuscript largely acknowledges this, but the study's claimed mechanism must remain bounded; if the author seeks a general mechanistic claim, independently designed intervention evidence is required. **Blocking for broad mechanism claims; not blocking if scoped explicitly as a case study.**

**M3. Independent validation for IoT scheduling implications is absent (Title, Abstract, Sections 4, 6–9).** All 24 A2 conditions are deterministic CPU-only single-VM fixtures, with only one/two VM PEs, no network, no IoT trace, and no physical timing reference. The title's “Implications for IoT Scheduling Simulation” is defensible only as a *methodological caution*, not as an evaluated IoT system. Keep the exact author-locked title but clarify that the IoT implications are conditional on using the same constructs, and avoid implying empirical generality. For stronger applicability claims, an external reference or independently chosen modelling configuration would be necessary. **Blocking only for unsupported external-validity claims; important in editor's overall relevance decision.**

**M4. RQ3's phase-state predictor has a serious circularity and small-design limitation (Sections 1, 5.11, 6, 7).** The P rule uses the execution list immediately before admission, which is closely related to stock free-PE/eligibility decisions. TP2/FP0/TN6/FN0 in eight chosen fixtures is a descriptive match, not independent predictive accuracy. The separate input-only H fails (one positive of four per event-gap group). The manuscript correctly reports this, but making the RQ3 “confirmation” a headline scientific contribution risks overweighting an implementation-adjacent rule. Consider treating this as a supporting diagnostic and emphasize the negative H result in Results/Discussion, not as evidence of model generalization. **Blocking for general classifier claims, otherwise a framing revision.**

**M5. The principal outcome measures need a clearer construct-validity argument, not just numerical agreement (Sections 3.2–3.3, 5.2–5.7).** Maximum absolute waiting-gap measures waiting-clock differences, whereas synthetic +25/+50ms classification disagreements measure threshold crossings in completion models. A lower maximum waiting difference can accompany more threshold disagreements (e.g., BURSTY_S0_1US P1 vs P2). This descriptive counterexample is defensible but the retrospective deadline sweep and posthoc service oracle should be segregated from preregistered A2 evidence. Neither metric validates physical deadline reliability or algorithm quality. The manuscript already includes caveats; add a concise decision-oriented distinction between “model discrepancy”, “realism/validity” and “application performance” instead of repeating long caveats. **Important interpretation issue; not new experiments by default.**

**M6. Full-text length and result hierarchy dilute the scientific contribution (Sections 5.1–5.11 and 6).** There are eleven Results subsections encompassing original A2, A1, A3, retrospective margin/threshold sensitivity, known-fixture intervention and small added fixtures. This chronological depth can resemble multiple weak mini-contributions instead of one coherent scientific argument. Keep RQ1 primary, RQ2 a bounded event-phase explanation and RQ3 as one confirmatory/negative diagnostic; move execution histories, per-case trace transcripts, posthoc threshold grids, extended calibration descriptions and CI provenance detail to supporting material while retaining links and all negative outcomes. The current v2.3 improved Introduction/Discussion but did not yet consolidate Section 5. **Major editorial-restructuring recommendation; must not remove raw auditability.**

## Minor comments

**m1. Numerical boundary convention:** clearly state `> 1e-8 ms` late-margin tolerance, especially for archived rows exactly at a nominal +25-ms boundary. Avoid silently switching between strict threshold and tolerance-inclusive language.

**m2. Unit and origin consistency:** ensure all millisecond/second conversions and cloudlet arrival, scheduler-submit, start-wait, execution duration and finish callback definitions are stated once in a table or model-definition paragraph. A3 matching at logged precision does not establish universal equality of origins.

**m3. Prior-art verification limits:** avoid presenting the full publisher paper of Vondra/Šedivý (2017) as directly examined; earlier comparison used the accessible publisher abstract/synopsis. Bibliographic and closest-work claims should be human-verified against accessible primary sources before submission.

**m4. Package completeness:** ensure the manuscript and supplementary package have stable source/data links, exact pinned commit, verified figure/table integrity, finalized author metadata, CRediT roles, funding/conflicts and separated research-method AI versus manuscript-preparation AI declarations. A Git mirror is not an independently deposited DOI archive; no DOI is currently claimed.

## Strengths and scientific boundaries

- Exact version and Java native experiments are documented; provenance tracking mitigates expiring GitHub Actions artifacts.
- All 288 A2 jobs completed, prespecified A2 grid retained; distinct A3 origin measurement helps constrain one confound.
- The important 250/288 native-reported service discrepancy is not hidden.
- A1 intervention is clearly in-sample, not represented as independent stock scheduler correction.
- Negative RQ3 spacing result and earlier project-specific failure gates remain visible.
- The reference FIFO is correctly framed as a declared model, not universal truth.

## Editorial recommendation

**Do not submit v2.3 as-is as a full original SIMPAT article.** The high-priority blocker is the lack of demonstrably significant novelty beyond version-specific diagnostics; the second is hierarchy/positioning of evidence. A *bounded simulator measurement case-study* presentation with complete supplementary archive is accurate but still requires the journal to accept the contribution or manuscript type. Do not manufacture novelty, statistical significance or new IoT validation. If a full research article is required, the next research step must be independently predeclared, genuinely distinguishing model or validation method (or external validity source), not another near-duplicate synthetic grid.

**Actual action status:** No Java experiment, no DOI, no author final approval, no journal submission. Keep title and all A1/A2/A3 results, source files and the separate CASPER Program B unchanged.
