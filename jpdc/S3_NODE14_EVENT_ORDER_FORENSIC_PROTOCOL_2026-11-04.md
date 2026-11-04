# S3 node-14 event-order forensic protocol — 2026-11-04

## Status and original outcome
Real Actions run 41773297282 did NOT pass the originally registered queue replay max-error gate: 9.12140093295 ms observed, maximum permitted 5 ms. All eight-policy science parity and actual mission outcome reconciliation passed. The original FAIL is immutable; the diagnostic below must not reclassify it.

## Predefined observation
Use original fixed seed index 40, S3_HIDDEN_NETWORK_50LOSS, fixed HIGH six-node mask [9,12,14,15,17,18], 80000 calibration samples, 30000 deployment tasks, and unchanged CASPER_FULL / CASPER_HEALTH_STATIC policy behavior. Exactly the event neighborhood task IDs 10898 through 10902 (inclusive) is selected BEFORE this diagnostic run. Inspect:
1. E45ArrivalSource event time at submitTask.accept(task).
2. E45Campaign mapper invocation time (sim.clock) and chosen node for each selected task.
3. Actual CloudSim cloudlet execution start, end callback clock, recorded wait/service, arrival, cloudlet ID at finish.
4. Whether these three time series preserve task arrival-index order. Report any inversion with all timestamps and no untested causal explanation.
5. Exact scientific CSV parity compared with an uninstrumented same-seed control for ALL eight policies excluding the timing-only mapper_us field. The instrumentation must not alter science, queue dynamics, or observed outcome metrics.

## Implementation and falsification
Patches instrument ONLY the generated temporary E45Campaign.java and E45ArrivalSource.java after the frozen generator; no frozen E42/E4.6 edits. All Java changes are additional observational print statements only. Unique source anchors fail closed. Use two runs (control versus forensic) in the same workflow; original E42 SHA must equal 34256ca7bff46f911cf20e8b94278fbd09175746. Capture complete logs, official CSVs and provenance even on failure.

A failed compile, source anchor mismatch, missing/duplicate per-stage event, mismatch between instrumented/control scientific metrics, or observed edge inversion that is not fully explained by the three event-order stages MUST be reported, not silently fixed. Do NOT change the previously registered 1-ms mean / 5-ms maximum wait-error queue thresholds based on this outcome.

## Research scope
This is an exploratory forensic investigation of a known failure, **not an independent holdout**, not proof of a CASPER scheduling effect, and not evidence of second-simulator validation. Scientific holdout p=.0625 and exploratory factorial p=.125 remain nonsignificant.
