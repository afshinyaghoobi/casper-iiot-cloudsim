# SIMPAT Paper A — independent editor-facing desk-rejection risk and minimum viable scope, 2026-11-18

**Immutable author-approved exact title:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation.
**Current manuscript examined in full:** [v2.0](SIMPAT_MANUSCRIPT_V20_EIGHT_NEW_INPUT_PREDICTION_2026-11-18.md), about 8,450 whitespace-delimited words and eleven Results subsections (5.1–5.11).
**Target:** *Simulation Modelling Practice and Theory*, https://shop.elsevier.com/journals/simulation-modelling-practice-and-theory/1569-190X. **No actual submission.**

## What the target journal says, versus what we can substantiate

The journal's published aims solicit substantial original contributions in modelling and simulation, including methodology for validation/verification, experimental design, sensitivity analysis, simulator environments, and applications such as cloud, fog, edge and IoT. Applied modelling articles should transparently explain model development, implementation and validation (with real data when relevant). The user-locked title and native simulator focus are **topically in scope**, but *scope match is not originality*. The publisher's journal page does not, on its own, verify that a **short communication/technical note** manuscript type is currently selectable on this journal's live submission form. Do NOT claim that such article type exists as an accepted option before checking the exact active submission instructions.

**Key editor's question:** What new generalizable simulation-science procedure, validation insight or falsifiable principle is established beyond (a) using documented SpaceShared event/eligibility paths, and (b) contrasting the output of a known nonequivalent event-independent analytical FIFO model? If this cannot be answered in 2–3 evidence-graded sentences, the manuscript is likely a technically reproducible *case study* with insufficient significance for a full SIMPAT original article. Do not replace that question with number of tests, Word count or successful GitHub CI.

## Source-backed hard evidence and claim strength

| Empirical component | Evidentiary status | Real contribution | Strict upper limit |
|---|---|---|---|
| Original A1 6 source-fixture jobs/event cases | Verified native code, same-control trace and callbacks | Executed older-WAIT / younger-EXEC states in two named fixed conditions | Neither real CPU-start evidence nor a broken FIFO software contract |
| Native method-level promotion instrumentation | Six fixed cases, 33 method calls/10 with actual WAIT→EXEC before/after change | Separates native direct admission and deferred waiting promotion in *executed method paths* | Paths are already documented in official API |
| Native end-of-update added waiting rescan | Predeclared treatment on **preknown** two positives (both flip), original byte-identical control, 4 negative fixtures no new bypass | *Local intervention sufficiency for a state ordering in these known configurations* | Modified scheduling semantics; not independent causal decomposition, library patch or efficiency improvement |
| A2 native 24 conditions/288 tasks | Correct versioned Java provenance, 49.0961ms descriptive mean abs waiting gap, max across cases 246ms, synthetic +25/+50 classification differences86/288 and107/288 | Quantifies divergence for specified reference model and test fixtures | No IoT arrivals or physical deadline ground truth; original reference intentionally differs from native |
| A2 posthoc service-duration oracle | Native reported duration differs from requested250/288; still up to154ms maximum within-case after hindsight substitution | Demonstrates important *measurement construct/confound* | Uses after-completion native duration; noncausal hindsight, not valid prospective service oracle |
| A3 arrival/submit clock | Native 288/288 same logged clock in defined configuration | Rules out one narrower apparent origin confound for fixed setting | No universal simulator timestamp theorem |
| Posthoc 51-point deadline sweep | Source-verified, mathematical interval equivalence | Shows arbitrary threshold changes sign of descriptive PE-group model disagreement (e.g.25ms: 27 vs59;75ms:64 vs22) | Threshold identity is elementary and analysis posthoc |
| New eight prereg synthetic inputs | Native untreated 8 cases/24 tasks, byte-identical repeat | Before-submit state predicate P: TP2/FP0/TN6/FN0 **on fixed new fixtures** | Source state P may be tautological implementation check, not an independent input-only predictor |
| New input-only event-gap prediction | Predeclared before run | **FAILED**: 5ms vs1µs both1/4 positive | Cannot claim higher interval causes the queue state |
| Earlier 30k parity and Stage65 gates | Explicit negative history | No suppressed negative original work | Both FAIL unchanged |

## Nearest published studies — concrete overlap
- Calheiros et al. (2011), DOI10.1002/spe.995 and Silva Filho et al. (2017), DOI10.23919/INM.2017.7987304: established simulator infrastructures.
- Sargent (2013), DOI10.1057/jos.2012.20: general validation principles are not novel here.
- Vondra, Šedivý and Castro, Wiley2017 DOI10.1002/cpe.3983: CloudSim-based service-duration/time calculation is an established issue (publisher metadata and abstract/synopsis).
- Zakarya & Gillam SIMPAT2019 DOI10.1016/j.simpat.2019.02.003: directly read accessible author manuscript; analytical/statistical comparison and some real traces/testbed are precedent. No generic “first CloudSim-vs-analytical accuracy audit” claim.
- Vondra & Šedivý SIMPAT2017 DOI10.1016/j.simpat.2016.10.005: queue-network CloudSim model, source tier only publisher abstract/synopsis; full PDF not read. Do not claim complete comprehensive gap search.
- Mechalikh et al SIMPAT2025 DOI10.1016/j.simpat.2024.103042: directly read author-posted full paper comparing 24 different simulator **tools**, not our 24 conditions.
- CloudSimPlus **exact version8.5.7 Javadocs** already document native `updateProcessing` waiting promotion and SpaceShared free-PE suitability. New experimental contribution is trace/measurement, not method discovery.

## Critical presentation and internal consistency risks

**1. Chapter-like Results:** eleven subsections, §5.6–5.7 posthoc threshold/metric descriptions, and §5.8–5.11 incremental A1 native mechanism observations and counterfactuals have accumulated in chronological order. They obscure three research questions and create a perception of an activity log, not a focused original result.

**2. Introduction outdated despite recent experiments:** v2.0 still calls evidence “(i) ... (ii) ... (iii) ...” but omits the now-completed A1 internal method-trace, in-sample treatment and eight new input sources. Reframe introduction around *evaluation construct / native event-phase mechanism / bounded independent-input robustness* and predeclare no full physical validation.

**3. Mixed preregistration statuses:** original A2 design and two original +25/+50 deadlines were prospectively specified; six-case observational anomaly was known before A1 mechanism treatment; new eight-case inputs and P/H were specified before *their first run* but selected using previously observed behavior; 51-point sweep and matched-pair interpretations were POSTHOC. Do not collapse these evidence levels into “all pre-registered”.

**4. Misleading positive-results framing:** 8/8 descriptive P vs labels does not give 100% population accuracy or independently known workload prediction. Predicated on immediate before-submit free-EXEC state that heavily constrains expected native admission; the **failed 5ms input-only hypothesis is central**, not a footnote.

**5. Source/report links are not archival guarantees:** GitHub Actions artifacts expire; published data availability should identify permanent frozen code+fixture commits and archive the full original native logs via a verified release or data repository. Do not invent DOI/Zenodo accession.

**6. Severe author/governance gates:** human-approved author order, affiliations, CRediT, conflicts, funding, exact FGCS CASPER overlap and status, accurate AI-assisted manuscript/code involvement, figure rights, ethics if relevant, full article author approval. No publisher submission initiated.

## Recommendation and bounded next step

**CURRENT: NO-GO for immediate full original research article submission to SIMPAT.** There is genuine reproducible evidence, including a clear intervention effect under pre-known conditions and a failure of a separate new-input hypothesis, but the main novel simulator-validation *principle* and cross-system/operational significance are not demonstrated. The risk is scientific, not merely language or formatting.

**Publication option A:** compress the evidence into one *source-pinned reproducible case study* with three questions (defined measurement constructs, executed event-phase behavior, limited robustness/negative test), one main summary table and a short diagnostic instrument. Ask editorial office or consult actual submission system whether a short communication or research note is formally available; publisher landing scope alone does NOT verify type acceptance.

**Publication option B:** if full SIMPAT research article required, design **one genuinely nontrivial independent test** with a new generalizable method/performance measure and a defensible empirical/physical ground-truth criterion *only after* the question and falsification gate are frozen. Do not repeat small synthetic sensitivity grids for publication optics.

**Publication option C:** keep verified artifact publicly reproducible as a software-methods technical report, redirect writing effort to independently novel research Program B **only with user authorization**; current Program B remains RESERVED/NOT STARTED.

**The locked exact title and original evidence must not be changed to make acceptance appear more likely.** This audit is internal scientific evaluation, not peer review by SIMPAT or an actual editorial opinion. Past original strict30k Java/Python parity FAIL and Stage65 safety FAIL unchanged.
