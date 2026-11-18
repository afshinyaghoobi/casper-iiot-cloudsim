# SIMPAT v2.2 — exact deadline-disagreement certificate and static 288-job audit

**Title unchanged:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation

**Status:** Posthoc *direct read and independent arithmetic* from the existing Git-tracked archived CSV, performed 2026-11-18. **No new Java simulations; no new observations; no prospective prediction, new theorem, general-method validation or external IoT truth.** This note does not change the manuscript. It extends `SIMPAT_V22_CONSTRUCT_VALIDITY_AND_NONTAUTOLOGY_GATE_2026-11-18.md`.

## Actual inspected input

`jpdc/evidence/simpat_v857_original_2026-11-18/a2_derived_original_288_job_margins.csv`, previously derived by `jpdc/audit_simpat_a2_per_job_completion_margins.py` from the original archived 8.5.7 native A2 log. It contains 288 actual rows in 24 deterministic cases and fields including `submit_ms`, `native_finish_ms`, `fifo_finish_ms`, `disagree25`, `disagree50`, native/fifo waits and nominal/native-reported execution durations. This continuation inspected the CSV directly through the GitHub connector and recomputed the threshold-crossing identity with a separate JavaScript calculation. Earlier repository CI checks and SHA manifest pertain to the underlying archive; this report does not claim an independent Java reproduction.

## A precise *retrospective identity*, NOT a prospective semantic-compatibility classifier

For each job j and synthetic threshold \(d>0\), let \(a_j\) be the recorded native submit time, \(C_j^{N}\) the observed native completion callback and \(C_j^{F}\) the completion produced by the stated analytical FIFO recurrence. Define relative finish latencies \(L_j^N=C_j^N-a_j\) and \(L_j^F=C_j^F-a_j\), and classification \(I(L>d)\). The exact **classification-disagreement certificate** is

\[
D_j(d)=\mathbf{1}\{[L_j^N>d]\oplus[L_j^F>d]\}.
\]

With strict positive lateness and no tolerance, this is equivalently **one completion is later than threshold d and the other is not**: \(\min(L_j^N,L_j^F)\le d < \max(L_j^N,L_j^F)\), except that the precise endpoint inclusion depends on which completion is the later one. More precisely, with \(u=\min(L^N,L^F)\), \(v=\max(L^N,L^F)\), it is \(u\le d < v\). The current original Python auditor instead uses \(L>d+10^{-8}\), so the exact compatible audit is \(u\le d+10^{-8}<v\) at stored numeric precision.

**Important:** This is an algebraic equivalence, already implicit in the original per-job auditor; it is **not new scientific theory, not a statement of simulator validity, and not an out-of-sample prediction**. It uses postcompletion native outcomes. It is a useful transparent audit certificate for why deadline-disagreement counts cannot be inferred from a case-level maximum waiting difference alone.

## Direct archived-row audit results

Independent recomputation from the downloaded GitHub file: 288 rows in 24 distinct cases; native-vs-FIFO threshold disagreements **86 at submit+25 ms and 107 at submit+50 ms**. The independent strict > threshold recomputation with epsilon 1e-8 exactly matched the CSV `disagree25` and `disagree50` labels: **zero mismatches in 288 rows at either threshold**. There are **two rows at the +25ms threshold boundary** at the audit precision and zero at +50ms; therefore endpoint/tolerance conventions must be documented rather than silently modified.

Additional CSV consistency: 250/288 native-reported execution durations differed from requested service by >1e-6ms; the maximum absolute native/FIFO waiting-time gap among the 288 rows is 246ms. Splitting by VM PE, with 144 tasks in each capacity group: 1PE has **27** (+25ms) and **49** (+50ms) classification disagreements; 2PE has **59** (+25ms) and **58** (+50ms). These are paired synthetic models, *not* measured real deadlines or independent samples.

Concrete **fixed-input counterexample**: BURSTY_S0_1US_P1 max absolute waiting gap **157.018ms**, +25ms disagreements **1 of 12**; BURSTY_S0_1US_P2 max absolute waiting gap **25.005ms**, +25ms disagreements **5 of 12**. Thus smaller maximum wait-model discrepancy does not imply smaller deadline *classification* discrepancy when case configuration and capacity change. This is a bounded descriptive result, not proof that adding PEs harms real-world deadline outcomes.

## Structural semantic-compatibility test — formal decision design, present evidence status

To compare native and FIFO quantities as **measurements of the same construct**, a proposed diagnostic must predefine:
1. **Observation mapping**: same job identities, actual submit order, time units, and a predeclared match between the native wait time-origin and reference arrival origin.
2. **Resource mapping**: matched PE/task demand, capacity and resource allocation restrictions; a one-VM two-PE native scheduler is not automatically two independent FIFO servers at all event phases.
3. **Service definition**: requested CPU work, native-reported *postcompletion* execution duration and physically measured service must NOT be conflated. If native execution differs from requested service, mark this comparison as confounded, not simply invalid or corrected with hindsight.
4. **Event-phase observability**: if FIFO order and native queue admission are to be treated as the same behavioural construct, a documented queue policy and observed phase order must justify that identification. Snapshot-only A2 logs do not isolate every callback branch; known A1 traces do not transfer automatically to all A2 jobs.
5. **Endpoint/threshold mapping**: completion callback vs analytical completion must be separately defined; a declared synthetic deadline is not an actual IoT SLA.

For each dimension return `SUPPORTED` (with evidence), `CONTRADICTED` (specific counterexample) or `NOT_IDENTIFIED` (missing independent evidence), **not** a single threshold-calibrated success score. A3 supports equal clock origins on exactly 288 original jobs *at recorded precision*. Native-vs-requested service equivalence is contradicted in 250/288. Native-FIFO event-phase equivalence is not established across full A2. Physical IoT deadline fidelity is not identified. Hence overall same-construct equivalence cannot be certified from these data.

This rubric deliberately avoids using the observed +25/+50ms disagreements as *inputs* to declare comparability; otherwise it would merely classify disagreement after seeing the label. The rubric is a proposed documentary framework from established model V&V principles, **not a new validated scientific instrument**. To claim a transferable method, independently predeclare pass/fail decision rules, evaluate known compatible and incompatible controls with blinded held-out outcomes and a different model, compare with established V&V practice, and retain negative outcomes. The current 288-job table alone cannot do that.

## Research/publication disposition

**NO-GO for claiming a new generally validated method, novel simulator bug, causal explanation or real-world IoT deadline reliability.** A narrow, precise discussion about *which construct is being measured* and a documented retrospective per-job threshold certificate can strengthen the honest version-specific case study, but the broader SIMPAT full-article novelty gate remains **HOLD**.

Preserve the user-locked title, frozen A1/A2/A3 native results, all earlier negative 5ms input-only hypothesis (1/4 versus 1/4), failed historical 30k Java/Python parity and Stage65 safety, unverified FGCS status, author/AI disclosure gates, and separate reserved Program B. No DOI, journal submission or author approval is claimed.
