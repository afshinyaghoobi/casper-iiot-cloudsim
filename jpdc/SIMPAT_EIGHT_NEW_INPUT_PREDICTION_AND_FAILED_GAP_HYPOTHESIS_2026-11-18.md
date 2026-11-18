# SIMPAT A1 — PREDECLARED eight-new-input passive Java prediction audit, verified results (2026-11-18)

**Exact user title:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation.
**Journal:** Simulation Modelling Practice and Theory. This is an **out-of-previous-six-fixture** controlled synthetic test, NOT a random representative holdout sample, IoT trace, simulator defect test or full scientific novelty demonstration.

## Preregistration, new experiments, provenance
- **Before the first native Java execution**, froze [four new parameter families × two event gaps (8 cases)](SIMPAT_A1_EIGHTCASE_UNSEEN_INPUT_PREDICTION_PREREG_2026-11-18.md), immutable prereg commit **80b6de95ef7922cecb226ce2c686e22a7642c274**. Input families H_A,H_B,H_C,H_D with distinct times/services from original A1; each uses 1μs and5ms minimum-event gap, single VM/PE, 3 Cloudlets per case. These fixtures were *designed with knowledge of prior phenomenon*, but their exact outputs were not inspected before freezing.
- [Native Java17/CloudSimPlus8.5.7 passive runner](../src/main/java/org/casperiiot/jpdc/NativeV857IndependentEightCaseTrace.java), [independent source-event parser](audit_simpat_a1_eightcase_unseen_predictor.py). Original SpaceShared and library source unchanged; no rescan intervention was used in these **held-back** cases.
- [Real GitHub Actions run44391376042 SUCCESS](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44391376042), **artifact14469051199** (original and duplicate native logs, 8-case audited JSON and SHA list), GitHub archive reported SHA256 **32b1c0cb6509c75bf6ecb005973af2e5b235510cdd034b6821cb66d909fcc824**. Downloaded artifact and inspected all individual case statuses. Original native source log SHA256 **c4bd49c77c488626fb027831bc8704b34db53f0d34845e1f01fc278ca3438c02**. **8/8 cases each have all three jobs complete (24 jobs), and first/repeat Java logs are byte-identical**.

## Predeclared P (trace-only, BEFORE next submission)
The predictor was defined before the Java run using earlier *source-native event phase* state. Given an UPDATE with job0 EXEC/job1 WAIT and job1 eligibility FALSE, the same update ends EXEC empty / WAIT job1; no intervening promotion takes job1 out of WAIT; then at job2 SUBMIT BEFORE, EXEC still empty and job1 WAIT. **P never accesses job2 ELIGIBILITY or SUBMIT AFTER to define prediction**. Outcome label was defined separately as job2 direct admission into EXEC while job1 remains WAIT on the corresponding SUBMIT AFTER.

**Results on all frozen eight conditions, including negative cases:**

| New original-native case | P before job2 admission | Actually younger job2 admitted EXEC while older job1 WAIT? |
|---|---|---|
| H_A_1US | false | no |
| H_A_5MS | false | no |
| **H_B_1US** | **true** | **yes** |
| **H_B_5MS** | **true** | **yes** |
| H_C_1US | false | no |
| H_C_5MS | false | no |
| H_D_1US | false | no |
| H_D_5MS | false | no |

**Predeclared descriptive confusion: TP2, FP0, TN6, FN0.** Original six fixtures were not part of this eight-case table. This supports a **version-specific local association / consistency across new deterministic fixtures**. It is NOT a population accuracy estimate, confidence interval, independent physical scheduler validation or proof of a novel predictive algorithm: P includes the *before-submit state* with free EXEC and older WAIT, and the documented SpaceShared capacity-suitability check may make the outcome nearly a direct implication of implementation semantics.

## A PREDECLARED HYPOTHESIS FAILED — do not hide
The independently preregistered weaker **input-only** directional prediction that **5MS** minimum event gap would produce *more* old-WAIT/new-EXEC cases than **1US** in these four matched new families is **FALSE**: **1/4** for 5MS vs **1/4** for 1US. The two observed positives occur in H_B under **both** event-gap settings. Thus it is incorrect to generalize from original six scenarios that only a coarse 5ms event gap can produce the source-list anomaly. Merely setting the simulator minimum-event gap does not alone predict the event-phase state.

## Scientific limitations and decision
- The new input fixtures were frozen before measurement but chosen to test a previously observed pattern, not sampled from real IoT/IIoT. Eight correlated deterministic configurations and three tasks/case are insufficient to claim generalized predictive reliability or a novel simulation-method theorem.
- P was defined using event observables immediately before the label, rather than entirely from input parameters, and may be a near-tautological restatement of an already documented native direct-PE admission contract. Its 8/8 descriptive agreement should **not** become “100% accuracy” in abstract or conclusion.
- Strongest actual contribution is now **bounded reproducible warning**: event-phase state and job admission can depart from a simplifed event-independent FIFO queue abstraction; a pre-submit phase predicate is a useful instrumentation check across these defined fixtures. This differs from asserting CloudSimPlus is wrong.
- The **independent input-only 5MS-more-often hypothesis failed**, limiting claims about event discretization.
- No experimental attribution of entire original A2 24-condition native-vs-FIFO discrepancy or physical IoT measurements; original A2/A3 unchanged. Old strict30k Java/Python parity FAIL and Stage65 safety FAIL remain. Program B separate RESERVED/NOT STARTED.

**SIMPAT full-length scientific GO/NO-GO = HOLD**. Some original simulator-source phase observations and a controlled in-sample rescan are meaningful but source behavior is largely documented; a significant new method or real-world empirical relevance still not established. Publication paperwork and author approvals are independently pending.
