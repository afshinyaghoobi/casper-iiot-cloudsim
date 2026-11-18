# SIMPAT Program A — DIRECT FULL-TEXT near-venue comparison & bibliography correction (2026-11-18)

**Exact author-approved title:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation.

**Provenance:** Publisher metadata at https://www.sciencedirect.com/science/article/pii/S1569190X24001564 and **full paper author-uploaded text** available publicly via https://www.researchgate.net/publication/386084832_Quality_matters_A_comprehensive_comparative_study_of_edge_computing_simulators, uploaded by coauthor Charafeddine Mechalikh 2024-11-27, directly examined 2026-11-18. Publisher landing-page full text returned HTTP 403, but author-available full text DOES EXIST; supersedes earlier handoff note "full text unavailable" for this one paper. Copyright respected: analytical summary only, no article reproduction.

## Full-text checked related work
**Charafeddine Mechalikh, Abd El Heq Silem, Zahra Safavifar, Fatemeh Golpayegani (2025),** *Quality matters: A comprehensive comparative study of edge computing simulators*, **Simulation Modelling Practice and Theory 138, 103042**, DOI **10.1016/j.simpat.2024.103042**.

### Direct-text, section-specific findings
- **Abstract, §2 and §6:** evaluates **24 different edge simulator tools**, develops literature/tool classification and evaluation criteria for functional/non-functional properties. Categories include fidelity-relevant *realism*, scalability, reliability, maintenance, software quality, usability/extensibility; tools measured with documentation, code metrics and runtime benchmark considerations.
- **§5.1.2:** CloudSim Plus is explicitly included in cloud/edge lineage and described for software architecture, event listeners, resource and network modeling, extensions and maintainability. The paper describes **CloudSim Plus in general**, not source-locked 8.5.7 SpaceShared callback behavior.
- **§6.4 software quality & performance:** tables include language, files, classes, code smells, duplication, bugs/coverage and runtime/scalability thresholds. Here "execution time" denotes **simulator benchmark execution time** or benchmark responsiveness, not necessarily a Cloudlet's getTotalExecutionTime() or per-Cloudlet queue waiting metric.
- **§8 conclusion/future directions:** quality, completeness, modeling capability and fair simulator comparison/benchmarking are core takeaways.

### Controlled side-by-side difference
| Dimension | Mechalikh et al. 2025 | Present A1/A2/A3 | What can be claimed |
|---|---|---|---|
| Unit | 24 **simulation tools** | 24 **conditions of one versioned runtime**, 288 completed CPU tasks | The number 24 is coincidental and denotes entirely different units |
| Primary evaluation | framework quality, features, software/scalability/maintenance | source-defined wait/execution/accounting and descriptive model disagreement | Different measurement target and protocol |
| CloudSimPlus specificity | cloud framework/tool-level taxonomy and attributes | actual v8.5.7 SpaceShared Java code callback trace and original frozen logs | More specific empirical program for defined internals |
| Comparator | cross-tool descriptors and quality benchmarks | simple non-native event-independent m-server FIFO and explicit after-completion service oracle | An analytical *reference-model sensitivity*, not a superiority comparison |
| Real IoT systems | discusses simulator applicability to IoT and edge | no sensor traces or IoT network, one VM | "Implications for IoT scheduling simulation" ONLY contextual |
| Novelty caution | shows simulator benchmarking and comparative quality work was done | quantifies a new narrow discrepancy in exact predeclared fixed scenarios | Specific measurement evidence, not an invented new methodology |

**Conclusion of this direct full-text audit:** no exact duplication of this A1/A2/A3 data/path/metric was found in the author-available paper sections inspected. However, this is not a global first-in-literature proof, nor does it establish SIMPAT full-article acceptance merit. The much closer CATEGORY rivals remain Vondra et al. 2017 (job-duration accounting), Zakarya/Gillam 2019 (mathematical/analytic validation) and potential queue-semantics work still to check. This targeted reading allows upgrading the Mechalikh reference from *abstract-only* to *full author-uploaded text inspected*.

## Concrete primary bibliographic error found and fixed for next manuscript
Previous draft [1] began "R. Buyya et al." while publisher original paper DOI **10.1002/spe.995** lists **R. N. Calheiros** FIRST, followed by R. Ranjan, A. Beloglazov, C. A. F. De Rose, and R. Buyya; *Software: Practice and Experience* 41(1):23–50, 2011. Correct both bibliographic entry and prose citation (Calheiros et al. [1]). Publisher record: https://onlinelibrary.wiley.com/doi/full/10.1002/spe.995 .

## Current journal compliance from publisher, 2026
- Official scope (https://shop.elsevier.com/journals/simulation-modelling-practice-and-theory/1569-190X) demands significant novelty in simulation methods or applications, accepts IoT/cloud/edge settings and prioritizes transparent model development and verification, including actual data for applied claims. This paper has synthetic CPU-only one-VM data, so do NOT claim general IoT deployment validation.
- Elsevier GenAI journal policy (https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals), updated June2026: use of AI to write/edit code must be explained in Methods; a separate **human-approved** AI manuscript-preparation declaration belongs immediately **before References**; data-derived reproducible plots permitted with method transparency. Authors must review and take responsibility. Don't insert false human approval.
- Before actual submission, confirm current exact SIMPAT author instructions in Editorial Manager / Guide for Authors, approval, authorship, conflicts, prior FGCS overlap disclosure, any permanent data-availability archive.

**No experiments added or native claims changed.** A1/A2/A3 results remain exactly frozen and verified; pre-existing 30k parity and Stage65 safety FAIL still unchanged. Program B separate and not started.
