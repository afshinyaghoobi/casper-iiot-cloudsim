# JPDC independent real health-detector positive-path S2 test, preregistered 2026-11-04

## Why a distinct S2 test
Prior successful S3 HIGH network-shock event replay `41873772600` verified all health masks, queue backlogs and telemetry transitions exactly but produced **zero observed health alarm transitions** in its network-only degradation. A real positive-path check needs a *different, explicitly prespecified* scenario, not a tuned synthetic increase to alarm sensitivity.

## Fixed setup
Original E42 `34256ca7bff46f911cf20e8b94278fbd09175746`, E4.6 frozen. Original E45 S2_HIDDEN_COMPUTE_40LOSS, seed index40 (scientific seed 4202202640), original untouched affected-node selector, 80k calibration and 30k deployment tasks. Do NOT modify the original workload, 8-policy set, task deadlines, node health thresholds, probe allocation, task routing, detector window/exceedance criteria, or calibration. Use the already verified generated-E45-only event logger, with just a scenario guard switched to S2 for CASPER_FULL, and independent Python replay of original per-node actual completion ratios, full 21-node dispatch alarm masks and queue state. Pair an uninstrumented control and the instrumented run.

## Prespecified pass/fail
Exactly 21 original health thresholds, 30k unique pre/post dispatches, 30k native completion service-ratio outcomes, every real telemetry reset, all 21-node backlog vectors and alarm masks independently reconstructed. Java-Python absolute virtual backlog/selected next-free difference <=1e-8 ms and exact all health alarms and zero missing/duplicate events. All 8 policy science CSV fields equal to uninstrumented control except wall-clock mapper time. Independent result is FAIL if any mismatch, **even if observed health alarms remain zero**. Separately REPORT observed number of alarm transitions, alarmed nodes, and first alarm task index. If no alarm actually occurs, do not label positive-path covered; report limitation.

## Scientific boundary
This is independent state-transition logic conditioned on Java-sourced actual completed service times, per-node calibration thresholds and telemetry snapshots, **not** an independent external physical simulator nor proof of actual deadline improvements. No changed primary 10-seed S2/S3 holdout (p=.0625 nonsignificant), exploratory factorial p=.125 nonsignificant, or original strict Python FCFS fidelity test (FAILED 9.1214ms >5ms).
