# SIMPAT v2.2 — independent behavioral validation gate (design only)

**Locked title:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation

**Status:** Research design / falsification checkpoint; NO new Java simulations or assertions of novelty. No manuscript changes. Designed after reading A1/A2/A3 reports, the exact v2.2 manuscript, and previous non-tautology gates on 2026-11-18. **This protocol is not claimed to be preregistered independently of prior observations.** It would be frozen *before any future study*; genuine novel inputs would have to be fixed after auditing contamination by the earlier case families.

## A. What is NOT an unresolved hypothesis

The previously observed 288-row arithmetic closure
`C_native - C_FIFO = (W_native - W_FIFO) + (S_native_reported - S_requested)`
is a bookkeeping identity conditional on matching recorded submit origins. Repeating it is not a genuinely independent or predictive test. The deadline-straddling identity likewise determines retrospective threshold classifications from postcompletion outcomes. Neither identifies native event-processing behavior or constructs a new validation method.

The A1 before-submit source-state predictor P (TP2, FP0, TN6, FN0 among eight purposively designed new fixtures) uses implementation-dependent, immediately preceding runtime queue state; its existing success cannot establish simulator-independent prediction or general accuracy. Previously attempted 5ms>1us input-only effect FAILED (1/4 vs 1/4), not to be dropped or rewritten.

## B. Single candidate testable claim, not yet adopted as an article contribution

**Hypothesis BH1 (behavior, not bookkeeping):** A *fixed, implementation-independent behavioral abstraction* that explicitly defines admission order, service accounting, server capacity and event timing will make predeclared predictions about `start/admission order and native-to-reference waiting` in conditions not used to specify it; these predictions will differ informatively from both (i) the current event-independent FIFO reference and (ii) the published stock 8.5.7 implementation rules. This is only a **candidate**. If the proposed abstraction merely copies the native 8.5.7 scheduler or relies on outcome-derived event lists, BH1 is circular and the project must not call it a new method.

**Null/failure scenarios:** no meaningful distinguishability between candidates on controls; model predictions only reproduce already available source conditions; observed behavior is not identifiable from available API instrumentation; passive hooks alter native timing; held-out predictions fail; or any performance discrepancy disappears when clock/service differences are controlled. Such outcomes are acceptable scientific negatives and terminate the novelty claim.

## C. Mandatory source-only feasibility gate BEFORE any experiment

1. Write down the proposed abstract model's **independent source of rules**; compare each rule to existing FIFO scheduling, published V&V techniques (Sargent 2013; Zakarya/Gillam 2019; Vondra/Sedivy 2017; Mechalikh et al. 2025), and official CloudSimPlus 8.5.7 behavior. Document **which rule is actually new** and why it is not just paraphrasing the implementation.
2. Provide a small manually reasoned **positive control** with matching admission and service rules and a **negative control** with deliberately different admission rules; specify observable expected classifications *without executing or looking at output*. Ensure control pairs are not drawn from A1 known positives or A2 previously audited cases.
3. State exactly which event-level observation can be independently recorded: submit order/clock, native callback start if truly supported, WAIT-to-EXEC transition, reported start-wait and finish clock, requested versus reported service. Do not infer physical execution start from EXEC membership.
4. Establish instrumentation fidelity against an unmodified original Java control under the same input; require native outcome bytes to match after stripping only explicitly declared passive trace lines. If this cannot be done, result is NOT_IDENTIFIED, not PASS.
5. Fix the exact version and artefact provenance: CloudSimPlus 8.5.7, Java17, frozen harness source and dependency hashes, primary native log and deterministic re-run, original result rows and SHA256SUMS. Separate native outputs from later retrospective calculations.
6. Specify quantitative pre-outcome prediction targets: for *every* predeclared case, compare exact first admission order and WAIT-to-EXEC transitions, plus waiting-time predictions within an independently justified time tolerance. **Do not use measured deadline disagreements or native postcompletion service as model inputs** when predicting behavior.
7. Freeze failed-case rules: partial completion, trace mismatch, unrecorded branch, timestamp ambiguity, or changed source hash => technical FAIL / NOT_IDENTIFIED, and preserve files. Do not tune offsets, exclude cases, or rewrite metrics after seeing results.

**STOP HERE unless rules 1–7 are independently satisfiable.** It is better to document NO GO than to run another near-duplicate synthetic grid.

## D. Distinctiveness test — without this, even a positive experiment is not publishable novelty

- Compare against the *correct* published-stock SpaceShared model (not an imagined unconditional FIFO guarantee) and an explicit analytical FIFO baseline. Demonstrate a specific question neither baseline nor established V&V check already resolves.
- A valid new model should make some **differential prediction in a predeclared control** where both baseline predictions are specified. If all models always predict the same outcome, or the proposed model only asserts 'different constructs are different', the test is uninformative.
- For any transferable method claim, evaluate an **independently implemented second scheduling engine or a distinct model class**, with fixed unretuned prediction rule, and compare with existing V&V practice. A positive in a single 8.5.7 stock scheduler is version-specific evidence, not evidence of general transfer.
- Real deployment/IoT performance claims require independent trace or physical references. Synthetic CPU-only one-VM timing can only support simulation-model constructs.

## E. Practical sequencing / publication stop rule

**Current recommendation: NO AUTOMATIC EXECUTION.** First write a one-page independent model specification + a 2-control prediction table. If there is no genuinely nontrivial model distinction, do **not** perform BH1 runs; treat the manuscript as a bounded version-pinned CloudSimPlus model-comparison case study and assess an appropriate publication venue/article type without inventing a new research contribution.

Only if source-only feasibility and distinctiveness gates PASS should the team:
(i) freeze a specific held-out test protocol; (ii) obtain author sign-off on scope/resources; (iii) execute native Java once with all predeclared controls; (iv) audit raw logs and negative outcomes; (v) update paper only after evidence warrants it.

**Current SIMPAT full original-research disposition: HOLD.** Permanent Git source mirror exists, but no independent DOI archive and no author-approved final submission package. Do not alter existing A1/A2/A3 outputs or the earlier strict30k Java/Python parity FAIL, Stage65 safety FAIL. Program B remains RESERVED/NOT STARTED.
