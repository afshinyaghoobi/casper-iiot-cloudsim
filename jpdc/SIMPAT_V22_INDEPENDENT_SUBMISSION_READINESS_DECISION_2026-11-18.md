# SIMPAT v2.2 — independent submission-readiness decision (2026-11-18)

**Exact title (unchanged):** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation

**Scope of this checkpoint:** Read-only review of existing v2.2 manuscript, source-provenance README, v2.2 checkpoint, prior-art comparison, and existing passing GitHub workflow run 44407124423. This is a scientific/editorial assessment, **not** newly run Java or independent re-computation of all original numerical results. No author's approval or publisher submission has occurred.

## Independently inspected evidence
- Current article: `jpdc/SIMPAT_MANUSCRIPT_V22_PERSISTENT_NATIVE_EVIDENCE_2026-11-18.md`.
- Source mirror and provenance: `jpdc/evidence/simpat_v857_original_2026-11-18/README.md`, archive commit `95424c68d8e3824c76c0a249cec6b0c5e3491184`.
- GitHub Actions run [44407124423](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44407124423): API reports `completed/success`, head SHA `1ea56a6591921c3d128487f95a4516ce2aa72b9e`; the one listed `frozen_original_provenance` job succeeded.
- Existing prior-art comparison: `jpdc/SIMPAT_DIRECT_ZAKARYA_AND_VONDRA_PRIOR_ART_2026-11-18.md`; publication-policy gate `jpdc/SIMPAT_PUBLICATION_DISPOSITION_PUBLISHER_POLICY_GATE_2026-11-18.md`.
- Official [SIMPAT scope](https://shop.elsevier.com/journals/simulation-modelling-practice-and-theory/1569-190X) requires significant contribution in modelling/simulation and encompasses validation, verification, simulation experiments, cloud/edge and IoT. Topic fit is not sufficient to establish originality.
- An accepted journal-specific **Short Communication** or **Technical Note** category has not been verified; general publisher/institutional article-type menus must not be represented as proof of SIMPAT availability.

## What can responsibly be claimed
1. **Reproducible bounded measurement:** For the frozen one-VM CPU-only synthetic workload, A2 compares source-reported waits to an independently *defined*, capacity-matched FIFO recurrence using actual native submission timestamps. Reported summaries: 24 deterministic conditions / 288 Cloudlets; per-case maximum absolute discrepancies 24–246 ms; artificial deadline-classification disagreement 86/288 at +25 ms and 107/288 at +50 ms.
2. **Confounding documented rather than denied:** A3 source-timestamp matching was 288/288 at logged resolution. Native-reported execution lengths differed from requested service for 250/288; the retrospective hindsight-service comparator retains up to 154-ms max waiting gap. The latter is not causal attribution or physical truth.
3. **Mechanism observed within bounded traces:** Previously known A1 six-case list-state bypass occurred twice and disappeared under a locally predeclared rescan treatment. The eight newly designed fixtures gave P TP2/FP0/TN6/FN0 **only for those chosen cases**; the directly source-observable P may approximate an existing admission test.
4. **Negative result preserved:** Predeclared 5-ms > 1-microsecond input-only event-gap hypothesis did not hold (1/4 in each group).

## Why full original-research submission remains HOLD
- **Novel modelling principle not yet demonstrated.** Existing literature covers simulator/analytical-model comparisons, CloudSim performance/fidelity, and queue-oriented simulation; the exact-version measurement niche does not establish a transferable new method by itself.
- **Comparator is deliberately not an oracle.** Measured discrepancy is a difference of specified software/analytical models, not established CloudSimPlus defect or real IoT deadline error.
- **External validity is deliberately absent.** No real IoT workload, independent physical timing/ground truth, multi-node network or general stochastic inference. Three deterministic variants are not independent population samples.
- **State-predicate circularity risk:** P's before-admission variables directly reflect implemented capacity/queue semantics. Small chosen fixtures cannot show general prediction accuracy.
- **Publication integrity unresolved:** journal-specific article type/author guide details; FGCS CASPER earlier-work status/overlap; authorship/CRediT and final approval; fully accurate AI-assisted methods versus manuscript declarations; external DOI archive if desired.
- Historical strict 30k Java/Python parity FAIL and Stage65 safety FAIL are not repaired by the SIMPAT archive.

## Decision and next bounded research action (no automatic new experiments)
**HOLD submission; keep v2.2 title, numbers, and negative results unchanged.** Treat this as a candidate *version-specific simulation-measurement/validation case study*, not as an already demonstrated broadly novel IoT scheduler or simulator fix.

Before more simulations, authors should state one precise, **falsifiable, non-tautological transferable modelling/validation contribution** and compare that claim explicitly with Zakarya & Gillam (2019), Vondra & Sedivy (2017), Mechalikh et al. (2025) and the official CloudSimPlus 8.5.7 semantics. If no independent method can be defended, prefer accurate limited-scope dissemination/alternative venue evaluation over artificially adding seeds or rebranding model disagreements as defects. If a genuinely new method is proposed later, freeze its protocol, independent outcome metric, appropriate validation reference, and null/failure criteria **before** generating new results.

No DOI, no author sign-off, no journal submission, no new native Java execution, and no separate CASPER Program B activity are claimed here.
