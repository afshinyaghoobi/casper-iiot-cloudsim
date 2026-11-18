# A3 measurement-construct source audit — frozen before reading v8.5.7 definitions

**Date:** 2026-11-17 America/Chicago. **Status: source audit protocol, NOT experiment, NOT executed yet.**
User goal: complete a small defensible independent JPDC evaluation manuscript; do not add exploratory full simulations. This is a *critical model-definition check* before publication claims.

## Scientific concern
A2 measures native `Cloudlet.getStartWaitTime()` and `getTotalExecutionTime()` (seconds converted to milliseconds) and compares it against a FIFO recurrence initialized from observed `CloudletSchedulerSpaceShared.cloudletSubmitInternal` callback times. These different variables MAY use different time origin (broker submit, datacenter arrival, processing activation) and different execution-duration accumulation semantics. A large numerical difference is **not** necessarily a queue-order violation, and cannot be ascribed to an implementation bug or event granularity alone.

## Immutable source, inspection and reproducibility
Use exact publisher Maven source JAR **org.cloudsimplus:cloudsimplus:8.5.7:jar:sources**, previously verified SHA256 `8d3efcacfc661b2f1e018e279761fc4ae1e5584a770b2022d20930568688966c`. Java/CloudSim source version pinned, no remote HEAD/main replacements. Inspect source of:
- org/cloudsimplus/cloudlets/CloudletAbstract.java (getStartWaitTime; relevant datacenter/broker arrival/start time);
- org/cloudsimplus/cloudlets/CloudletExecution.java (state/arrival and actual processing time, if applicable);
- org/cloudsimplus/core/ExecDelayableAbstract.java (getTotalExecutionTime);
- org/cloudsimplus/schedulers/cloudlet/CloudletSchedulerAbstract.java (cloudletSubmitInternal; move waiting→exec or updateProcessing where visible).
Capture method snippets with source line numbers as context, classify how close documented return definitions are to our FIFO reference. If method is inherited/delegated or source not clear, explicitly mark unresolved.

## Safety limits
This is a source-only inspection, NOT evidence a branch executed in 24-case A2 and NOT native replay. Do not change frozen experiment or old negative gates (30k Java/Python parity FAIL, Stage65 safety FAIL). Do not infer internal causality from exact text grep. Produce a concise method-origin table and link to exact source-code file/JAR SHA and CI run.

## Decision rules
- If timestamps/metrics differ in origin/meaning, **revise claims in manuscript to emphasize measurement-construct mismatch** rather than waiting-order effect; report numerical differences descriptively, without blaming simulator.
- If a metric is ambiguous, mark it unknown instead of guessing. Use a new focused validation only if absolutely necessary to sustain scientific claim.
- Data remain 24 deterministic synthetic cases, not deployed IIoT.
