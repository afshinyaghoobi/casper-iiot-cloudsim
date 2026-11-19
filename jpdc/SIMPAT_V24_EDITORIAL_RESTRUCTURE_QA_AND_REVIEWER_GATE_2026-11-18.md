# SIMPAT v2.4 — editorial restructuring QA and reviewer gate

**Exact title preserved:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation

**Working manuscript:** `SIMPAT_MANUSCRIPT_V24_RQ_STRUCTURED_EDITORIAL_DRAFT_2026-11-18.md` (Git blob `f92c34ea58a11cb32833bb457835add70aa10ae1`).  
**Supplement:** `SIMPAT_V24_SUPPLEMENTARY_EXTENDED_RESULTS_2026-11-18.md` (Git blob `0b4a3e2f9b0ef67cc0a3321d35025cea71528cf8`).  
**Frozen prior draft:** `SIMPAT_MANUSCRIPT_V23_EDITORIAL_FOCUS_DRAFT_2026-11-18.md`.  
**Internal critical assessment:** `SIMPAT_V23_INDEPENDENT_REVIEWER_REPORT_2026-11-18.md`.

## Changes and cross-file static verification

- Main Results now has **three RQ-labelled subsections**, down from eleven. RQ1 presents A2 native/FIFO results and A3/retrospective confounds; RQ2 summarizes A1 observed mechanism and known-fixture rescan; RQ3 summarizes eight held-input native fixtures and the failed input-only event-gap hypothesis.
- Seven formerly long subsections (§5.1 and §§5.6–5.11) were preserved as **verbatim body content** in Supplementary S1–S7, including method-trace timings, event order, posthoc sweep, executed control/treatment and negative outcomes.
- Original full primary 24-case A2 Table 1 and Figure 1 path remain in the main draft. Fixed 24 cases / 288 jobs, synthetic deadline model disagreement **86/288** (+25ms) and **107/288** (+50ms), 250/288 reported service differences, after-completion oracle residual **154 ms**, A3 source-time equality, A1 method calls 33/10, and RQ3 negative 1/4 vs 1/4 are retained. The original A2 method sections and the twelve-item bibliography were checked byte-identical between the two drafts.
- No old A1/A2/A3 native Java outputs, source data files, SHA manifests or source-hash run records changed. No fresh Java runs or claimed DOI.
- Existing manuscript's `## 5. Results` block dropped from 30,654 to 13,934 characters. Whole main draft dropped from 68,512 to 51,792 characters, while Supplementary is 21,738 characters. This is redistribution and editorial compression, **not a reduction or concealment of experiment coverage**.
- Static follow-up read from GitHub confirmed 3 main Results subsections, 7 supplementary sections, 1 main figure, and 12 main references. All three main-to-supplement links point to the exact actual new supplement path. **No new end-to-end GitHub CI was run for v2.4**; manual and programmatic content checks are not publisher production proof.

## Reviewer response matrix

| Prior major issue | v2.4 disposition |
|---|---|
| M1 novelty / overlap with prior V&V | **UNRESOLVED substantive submission blocker**: no new independent modelling method established |
| M2 cause of native/FIFO discrepancy | **SCOPED, not resolved causally**: A1 local mechanism distinct from A2 residual; current framing truthful |
| M3 real IoT external validation | **LIMITATION EXPLICIT**, not solved by editorial revisions |
| M4 potentially circular state predicate | **DOWN-WEIGHTED**, failed H retained; not general predictor |
| M5 metric construct confusion | **IMPROVED**: different wait and synthetic completion-classification constructs grouped under RQ1 |
| M6 scattered eleven-subsection Results | **STRUCTURALLY ADDRESSED**: main RQ hierarchy; complete supporting observations preserved |
| m1 numeric endpoint tolerance | **STILL NEEDS FINAL AUTHOR CHECK**, including threshold equality cases |
| m2 units and origins | **EXISTING DEFINITIONS RETAINED**, final proofread needed |
| m3 full-text closest prior art | **PARTIALLY VERIFIED**: source-access caveat remains |
| m4 declarations and journal package | **NOT FINALIZED**: authors, AI-method/manuscript disclosures, overlap, portal type, external DOI optional |

## Overall disposition

v2.4 is an **editorial candidate for author and independent reviewer scrutiny**, **NOT submission-ready** as a full SIMPAT original research paper. Scientific novelty and journal article-type fit remain under HOLD, regardless of formatting. Do not create a new algorithm, physical validation, or result in response to the editorial review. Original user-selected title is unchanged; reserve independent CASPER Program B.
