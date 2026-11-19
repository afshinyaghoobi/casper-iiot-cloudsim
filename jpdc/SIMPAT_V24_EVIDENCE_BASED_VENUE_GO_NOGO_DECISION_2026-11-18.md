# SIMPAT v2.4 — evidence-based submission GO/NO-GO decision

**Dated 2026-11-18.** Internal research/editorial decision, not a statement from SIMPAT editors. The user-approved exact title is **Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation**.

**Reviewed target manuscript:** `jpdc/SIMPAT_MANUSCRIPT_V24_RQ_STRUCTURED_EDITORIAL_DRAFT_2026-11-18.md`; Git blob `f92c34ea58a11cb32833bb457835add70aa10ae1`.  
**Supplement:** `jpdc/SIMPAT_V24_SUPPLEMENTARY_EXTENDED_RESULTS_2026-11-18.md`.  
**Earlier critical reviewer-style report:** `jpdc/SIMPAT_V23_INDEPENDENT_REVIEWER_REPORT_2026-11-18.md`.  
No new native Java runs, altered data, author declaration, journal communication or submission in this decision.

## Primary journal requirement actually checked on publisher website

The official Elsevier journal description at
https://shop.elsevier.com/journals/simulation-modelling-practice-and-theory/1569-190X
states that submissions must **significantly contribute to modelling and simulation** generally or to application areas. The stated topical coverage includes validation/verification methods, cloud/fog/edge simulation, IoT, simulation languages and applications. For applications, it calls for transparent modelling, implementation and validation/verification **with real data**. On topic fit alone, exact-version CloudSimPlus measurements and queue accounting are within scope. Topical fit does **not** establish sufficient contribution.

**Article-type verification:** Official journal-specific author submission menu or accepted `Short Communication` / `Technical Note` format **not independently confirmed** in this audit. Institutional read-and-publish coverage lists sometimes contain broad Elsevier types, but they do not demonstrate which manuscript types the SIMPAT portal currently offers. Do not state availability as a fact or submit under an invented type.

## Newly surfaced same-journal comparators (2026)

1. [CloudyGUI: A novel Python-based framework for auto-scaling and cloud workload analysis](https://www.sciencedirect.com/science/article/pii/S1569190X26000572), *Simulation Modelling Practice and Theory*, **September 2026**, **research article** as shown in search-accessible publisher metadata. Publisher snippets describe a new Python cloud simulation framework, workload-generation/prediction/autoscaling components and internal/external validation. The publisher full-text landing page returned HTTP 403 in this research session, **so this is metadata/abstract-level comparison only**.
2. [DriveNetSim: A simulation framework for mobility aware and learning based vehicular task offloading](https://www.sciencedirect.com/science/article/pii/S1569190X26000808), *Simulation Modelling Practice and Theory*, **November 2026**, shown as **research article** in search-accessible metadata, describes a modular vehicular-task-offloading simulator and reference to validation via prior case studies. Full text inaccessible in this session (HTTP 403). These are examples of other published research-article contribution types, **not an editor-prescribed minimum** and not conclusive evidence that a bounded version-specific audit is ineligible.
3. [Mechalikh et al., Quality matters](https://www.sciencedirect.com/science/article/pii/S1569190X24001564), **2025**, compares multiple simulator implementations; this is previous close topical precedent already explicitly separated from the present single-implementation 24-condition design.

Earlier closer direct model-validation overlap remains Zakarya/Gillam 2019 (analytical versus simulator plus external references) and Vondra/Šedivý 2017 (queue-network modelling), documented in `SIMPAT_DIRECT_ZAKARYA_AND_VONDRA_PRIOR_ART_2026-11-18.md`. The exact-version Cloudlet WAIT/EXEC timing niche is distinct but alone does not demonstrate a new transferable V&V method.

## Submission decision matrix

| Gate | Evidence | Disposition |
|---|---|---|
| Topical fit | Official scope includes cloud, edge, IoT and validation | **PASS** |
| Version-pinned data provenance | Original A1/A2/A3 logs and hashes committed; audited historical CI | **PASS within bounded conditions** |
| Numerical model comparison | 24 deterministic A2 conditions, 288 jobs; 86/288 and107/288 synthetic threshold disagreements | **PASS descriptive**, no accuracy inference |
| Source-level mechanism | A1 observed event admission states, in-sample rescan; A2 callback isolation incomplete | **BOUNDED / NOT GENERALIZED** |
| Claim of generalized algorithm or validation framework | BH1 two-control thought experiment did not establish independent novelty; no external model replication | **NO GO** |
| IoT field/hardware/second-model validation | None in current design | **NOT PRESENT** |
| Full original SIMPAT article scientific contribution | Reproducible narrow diagnostics versus known modelling/validation ideas | **NOT DEMONSTRATED** |
| Journal-specific short case-study type | No verified submission category or editorial invitation | **UNVERIFIED** |
| Author sign-off, FGCS overlap, AI/funding/conflict disclosures | Open author-dependent gates | **NOT READY** |

## What can actually be pitched to an editor

**Defensible:** An exact-version, reproducible measurement case study that distinguishes the native scheduler's reported queue state and time accounting from an explicitly named capacity-matched, event-independent FIFO reference; records a bounded phase-state list-level intervention; and preserves a failed hypothesis. All measurements are synthetic CPU-only single-VM, and external IoT relevance is a conditional methodological warning.

**Not defensible:** `novel general V&V framework`, `first proof of CloudSimPlus incorrect scheduling`, `validated real-world IoT deadline improvement`, `causal explanation of all A2 discrepancies`, or `100% universally accurate state predictor`.

## Firm, bounded next action

**NO-GO for direct full original-research SIMPAT submission of v2.4.** Do not keep incrementing manuscript versions or adding near-duplicate CloudSimPlus workloads merely to improve the count. The next efficient decision is a **short, truthful, author-reviewed presubmission suitability inquiry** (only if an official journal communication channel and its acceptance of inquiries can be confirmed), asking whether a reproducible, tightly scoped simulator semantics/measurement case study is an appropriate *article contribution* and which recognized submission category fits. An inquiry is not a guarantee of acceptance. If such an inquiry is not supported, the author should choose between a stronger independently validated science redesign or an alternative journal with a verifiable software measurement/experience-report article policy. Do not change venue or article title without author direction.

**Existing unchanged data:** A1 six known fixtures, A2 24/288, A3 288/288 same-clock checks, RQ3 eight inputs with P TP2 FP0 TN6 FN0 and negative 5ms>1us directional test (1/4 vs1/4), 250/288 native-reported service mismatches. Original strict30k Java/Python parity FAIL, Stage65 safety FAIL; CASPER Program B separate RESERVED/NOT STARTED. No DOI or submission is claimed.
