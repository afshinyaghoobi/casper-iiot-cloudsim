# SIMPAT v1.9 — Contract-aware editorial GO/NO-GO and consistency checkpoint (2026-11-18)

**Exact user-approved title:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation
**Journal:** Simulation Modelling Practice and Theory (Elsevier)
**Current paper:** [v1.9](SIMPAT_MANUSCRIPT_V19_SOFTWARE_CONTRACT_AND_LIMITATIONS_2026-11-18.md). No submission.

## Official 8.5.7 API read and technical implications

- [SpaceShared exact official 8.5.7 Javadoc](https://javadoc.io/static/org.cloudsimplus/cloudsimplus/8.5.7/org/cloudsimplus/schedulers/cloudlet/CloudletSchedulerSpaceShared.html) describes exclusive PE use, WAIT for Cloudlets that cannot run, and no consideration of submitted Cloudlet priorities. It does not state an unconditional global FIFO admission guarantee across all native event callback phases.
- [SchedulerAbstract exact 8.5.7 Javadoc](https://javadoc.io/static/org.cloudsimplus/cloudsimplus/8.5.7/org/cloudsimplus/schedulers/cloudlet/CloudletSchedulerAbstract.html) explicitly documents waiting-list promotion, finding a suitable waiting Cloudlet with sufficient free PE capacity, and promotion called by updateProcessing.
- The exact version 8.5.7 source JAR was previously SHA256 verified: 8d3efcacfc661b2f1e018e279761fc4ae1e5584a770b2022d20930568688966c. Original source code paths detailed in [source mechanism audit](NATIVE_V857_SOURCE_MECHANISM_AUDIT_VERIFIED_2026-11-17.md).
- These paths and eligibility tests are KNOWN IMPLEMENTATION SEMANTICS, not an invented algorithm or an automatically proven bug. See [source/contract comparison and exact prior-manuscript issue list](SIMPAT_OFFICIAL_V857_SCHEDULER_CONTRACT_AND_MANUSCRIPT_AUDIT_2026-11-18.md).

## Actual four scientific manuscript corrections in v1.9

1. Original 24-case **A2** did not directly record all internal WAIT-promotion callbacks; later six-case **A1** DID record those methods and added intervention. Old v1.8 Threats text improperly implied no promotion method was instrumented in the entire paper; corrected.
2. Old “one-PE” wording for all experiments was false because A2 includes **one and two PEs**; fixed.
3. Conclusion now acknowledges completed A1 method-level trace and controlled rescan, while identifying unresolved A2-wide causal decomposition and independent external validity.
4. Reference [6] now links both actual exact-version API classes, not just SpaceShared; Discussion and Threats explicitly distinguish published API contract from measured execution and modified treatment.

## Published evidence vs original work
| Topic | Established status | What is NOT established |
|---|---|---|
| Direct admission/wait promotion paths | Existing documented methods; A1 native methods dynamically executed | Discovery of a new algorithm |
| Original exact-event A1 anomaly | Recorded in 2 of 6 known deterministic cases, with four negative controls | Globally violated FIFO contract or CloudSimPlus defect |
| Preregistered after-update rescan | Executed native Java, original byte-exact CONTROL, treatment repeats, observed anomaly removed in both PREKNOWN positive cases | Independent holdout, physical IoT correctness, isolated internal root cause |
| Immediate next callback time | Original and treatment return values match at all 12 added calls | Entire downstream scheduling/event times are identical |
| A2 FIFO discrepancy | 24-case, 288 synthetic CPU tasks, source-verified quantitative model difference | Physical deadline error, all discrepancies attributed to promotion |
| Publication novelty | Reproducible version-pinned implementation-level finding and local state intervention | A new generalizable SIMPAT-size simulation methodology |

**Actual new static QA:** [GitHub Actions run44388832724 SUCCESS](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44388832724) enforces locked title, 12 numbered sources, unmodified A2 source, and removal of stale methodological contradictions. First run44388702794 failed due to checker erroneously comparing uppercase A1/A2 literals against lowercase manuscript text; fixed checker only, not science.

## Scientific verdict

**HOLD actual full SIMPAT submission.** The stock event paths are documented and the positive treatment modifies native queue processing in known fixtures, so neither the method existence nor the removal of observed list behavior proves a new general method or bug. A strong technical case study is possible, but a full paper claiming novelty or general IoT validity is not currently supported. The strict 30k Java/Python fidelity gate FAIL and Stage65 safety FAIL remain unchanged, and independent CASPER Program B remains reserved.

**Single conditional next research question, not yet an experiment:** before new simulation, define a source-based eligibility-phase predicate and freeze an independent previously unseen input set and positive/negative controls. Prediction should be about whether the old-WAIT/new-EXEC event phase occurs BEFORE seeing any new results; report success AND failure. A merely documented trivial behavior is not sufficient novelty. Do not expand grid or write a universal theorem from preknown cases.

**Additional unavoidable pre-submission gates:** all coauthor identities/affiliations/CRediT and final approval, FGCS CASPER overlap/status, accurate author-approved Elsevier generative AI manuscript AND Methods disclosure, funding/conflicts, genuine immutable code and original-data archive, exact current journal guide. No invented acknowledgments or promises.
