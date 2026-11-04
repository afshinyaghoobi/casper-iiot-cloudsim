# CASPER JPDC — native CloudSim start time forensic protocol (2026-11-04)

Purpose: resolve whether the task 10900/10901 inversion reported in 41774034113 is also present in the **native Cloudlet.getStartTime()** records, as distinct from the previously *derived* start = planned workload arrival + getStartWaitTime().

This protocol is recorded before the new run; the original FCFS mechanical fidelity experiment 41773297282 remains **FAILED** (max wait error 9.12140093294972ms > preregistered 5ms). No retrospective threshold changes.

## Source-backed API contract
`org.cloudsimplus:cloudsimplus:8.5.7` exposes `Cloudlet.getStartTime()` and `Cloudlet.getStartWaitTime()`. It does not expose `getExecStartTime()`. Existing generated-E45-only forensic logger already records arrival source clock, mapper clock, finish callback clock, and derived start. The new observation *adds* a native start field, without altering the task pipeline or any scheduling decisions.

## Prespecified execution
Seed index 40, S3_HIDDEN_NETWORK_50LOSS, HIGH fixed affected mask [9,12,14,15,17,18], 80000 calibration, 30000 deployment tasks. Compare all eight policies' official CSV outputs between uninstrumented control and generated E45 with BOTH previous forensic stage logger and added native Cloudlet.getStartTime logger; ignore only non-scientific mapper wall-clock microseconds. Original frozen E42 blob must remain `34256ca7bff46f911cf20e8b94278fbd09175746`; E4.6 frozen unchanged.

Native start and derived start are **different source variables**, not interchangeable by assumption. Record both without asserting equality. Extract task IDs 10898..10902 for CASPER_FULL and CASPER_HEALTH_STATIC. Require source arrival/mapper/finish identity and exactly eight deployment+one calibration arrivals (source-specific existing behavior). Determine native start chronological order and compare with derived order, including absolute native-versus-derived deviations. Do not automatically assign a causal explanation to any mismatch.

This is **exploratory mechanism forensics on a previously identified pair**, not independent validation of CASPER scheduling, and does not constitute new independent seed-level evidence. An actual CI result and saved raw evidence are required before any observational claim. Registered holdout p=.0625 and exploratory four-seed sign p=.125 remain nonsignificant.
