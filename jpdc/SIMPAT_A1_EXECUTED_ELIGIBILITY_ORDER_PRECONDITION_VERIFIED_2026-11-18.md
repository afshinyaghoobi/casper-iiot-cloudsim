# SIMPAT A1 — verified executed event-order precondition for older WAIT / younger EXEC

**Date:** 2026-11-18. **Author-locked exact title:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation. **Target:** *Simulation Modelling Practice and Theory* (Elsevier).

## Actual new verification and provenance
The latest source-only analysis re-reads the **original six-case genuine native Java 8.5.7 experimental trace** from [real earlier passive promotion run44359114031](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44359114031), not a new Java simulation. It combines original observed `updateProcessing` BEFORE/AFTER records, native internal `moveNextCloudletsFromWaitingToExecList` before/after snapshots, `canExecuteCloudletInternal` boolean returns (new and older job IDs), and the later direct submit BEFORE/AFTER list states.

- [Committed stand-alone event-sequence auditor](audit_simpat_a1_event_sequence_precondition.py).
- [Actual independent GitHub Actions run44365200058 **SUCCESS**](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44365200058): downloads archived source-run outputs, checks original A1 control is byte-identical after filtering new promotion-only lines, audits exact observations from all six cases, requires two specific matches and four negative controls, and preserves old negative gates.
- This is a **RETROSPECTIVE event-sequence reconstruction** in conditions already known to exhibit younger EXEC/older WAIT, not a new causal experiment or a holdout. The new code was authored after original experiments; the sequence was source-audited independently of the original before/after promotion parser.

## Directly observed chain (not source-only assumptions)

| Source-observed event | ORIGINAL_5MS | LATE10_5MS |
|---|---:|---:|
| Native `updateProcessing` and deferred promotion call: job0 EXEC, job1 WAIT | 1013.099623 ms | 1013.099623 ms |
| At above promotion method call, job1 eligibility returned | **false** | **false** |
| Promotion returned without moving job1; end of same `updateProcessing` EXEC empty, job1 still WAIT | **yes** | **yes** |
| Later native job2 submission: EXEC empty, job1 WAIT | 1013.0997406 ms | 1023.0997406 ms |
| Job2 eligibility at its own native submit method returned | **true** | **true** |
| Job2 added directly to EXEC, while job1 remains in WAIT | **yes** | **yes** |
| Native clock interval from update end to new submit | **0.0001176 ms** | **10.0001176 ms** |
| Older job1 finally joins EXEC from WAIT on later promotion call | 1037.2200236 ms | 1058.099623 ms |

The other four original A1 conditions (EARLY4_1US; EARLY4_5MS; ORIGINAL_1US; LATE10_1US) **do not satisfy this complete ordered event pattern** under the audited trace; this does *not* prove they can never exhibit it in another workload.

**Source-rooted interpretation:** At an observed update call, the older waiting job is checked while job0 is still listed as executing and is not promoted. After the update returns, the EXEC list is empty while the older job remains WAIT. The next direct job2 submission checks eligibility and is admitted. This demonstrates a *timing/phase-sensitive eligibility state*: a waiting-job promotion attempt and a new direct submission can see different availability states, and the earlier waiting job is not necessarily rechecked between those events in the observed fixture.

### Crucial inferential restraint
- The verified observation is **ordering of *executed* method callbacks and *recorded* list states**. It strongly narrows the mechanism beyond merely showing a FIFO-model difference or two separate code paths.
- It does **not** prove how VM free-PE capacity is internally updated in every substep, which documented behavior the library promises, a Java bug, a universal FIFO-policy violation, a physical CPU start, or causal responsibility for A2's 24-case numerical discrepancy. A direct eligibility-method call return value is *not* a guarantee the same job would be admitted if invoked at an altered time.
- This is **not** an independent causal test: timing context, scheduler update cadence and previous service consumption are jointly changing between the observed update and the next submit. The A1 six fixed cases are not random independently sampled workloads, and the two positive cases were known before this retrospective audit.
- The analytical FIFO comparator is defined deliberately differently; the observed state sequence shows an actionable **precondition to inspect** when applying the FIFO approximation, but does not establish a universal model incompatibility theorem.

## Scientific editorial decision
**SIMPAT novelty gate remains HOLD**. There is now a genuinely observable, narrowly specified native event sequence which is **more mechanistic and falsifiable** than the old raw wait-gap/threshold comparison. However, novelty compared with existing 8.5.7 scheduler documentation and prior simulators, independent generality and any physical IoT/IIoT validation remain unproven.

**Most defensible next test, if pursued:** a prospectively frozen *negative-control transition* at the same source-defined eligibility and free-capacity check, with duplicate byte-identical original control and a known WAIT→EXEC positive control. A true *causal* claim would need an isolated scheduler-event timing manipulation with competing mechanisms prespecified; merely toggling minimum event gap changes multiple other simulator dynamics and is not isolated. Do not introduce new algorithm, increase grids or claim causality without such controls.

Original native A2/A3 outputs and synthetic deadline metrics unchanged. Original 30k strict Java/Python fidelity gate **FAIL**; Stage65 safety **FAIL**; Program B separately RESERVED/NOT STARTED. Author sign-off, manuscript overlap, Elsevier AI disclosure and permanent archive remain pending.
