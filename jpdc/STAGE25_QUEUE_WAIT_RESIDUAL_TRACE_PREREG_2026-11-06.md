# JPDC Stage25 — preregister read-only queue prediction error observation (2026-11-06)

## Goal and restriction
Capture **signed WAIT-only prediction error** in the native strict-FCFS Python engine without changing dispatch, queue, CPU service or E2E behavior, to assess whether Stage24 could later obtain valid queue-error bounds. Previous performance seed88 network-only S3 was promising but S2 poor; DO NOT use Stage25 to choose policy thresholds or treat data as a clean efficacy holdout. Stage24 externally supplied error intervals are NOT empirically calibrated.

## Frozen fixed exploratory design
Scientific seed **89** is a DEVELOPMENT trace seed only, no earlier reported use in prior Stage12–24 summary, never eligible for untouched confirmation. 80,000 task calibration for seed89. Scenario S2_HIDDEN_COMPUTE_40LOSS, S3_HIDDEN_NETWORK_50LOSS. Policy arms PRED_GREEDY and CASPER_FULL ONLY. Each: 12,000 tasks, all task classes, exact source workload, node physics and algorithm. 4*12,000=48,000 *dependent task-policy* queue error observations, scientific n=1 seed; task-level quantiles are descriptive, not independent statistical confidence.

## Exactly defined observable
At arrival/dispatch of task i to node j at time a_i:
- immutable value `b_ij = vq.predicted_backlog(j,a_i)` **before** `vq.on_dispatch`, along with node/class/task index and arrival time. The virtual queue may have just reset from a periodic physical-queue telemetry event; that source is already part of frozen policy.
- actual service start time `s_i` is obtained when strict-FCFS `start()` is invoked; no policy is allowed to see `s_i` until later.
- at **CPU finish** `f_i` emit event via a passive hook with `actual_wait = s_i-a_i`, `signed_q_wait_error = actual_wait-b_ij`. This is a *WAIT component* residual, **not yet the full non-network q term** in Stage24, and contains NO network residual; physical CPU service error remains separately unmodeled.
- timestamp `delivered_cpu_finish_ms=f_i` marks first observable CPU wait label. It is NOT E2E delivery and MUST NOT be fed into the E2E-only network observer. State a context label `native_python_strict_fcfs_vq_telemetry50ms`; this context does not transfer to CloudSimPlus Java.
- record optional `time_since_last_telemetry_ms` measured since actual dispatch-received telemetry, for offline error stratification.

## Hard engineering gates
Identical full original policy JSON output for PRED_GREEDY and CASPER_FULL versus frozen independent Stage6; verify 12k trace entries per arm, unique monotonically increasing task indices when sorted (finish emission may be out-of-order), exact causal `arrival<=start<=cpu_finish`; `actual_wait=max(0,start-arrival)`; signed residual exact; finite nonnegative predicted backlog; no trace side effect on source policy results; E42 frozen original blob SHA `34256ca7bff46f911cf20e8b94278fbd09175746`. Run full matrix twice and compare files **byte identical**. Do not discard negative residuals or hide errors.

## Descriptive report, no data leakage
Output per-arm wait-only signed error min/max, mean, median, q90/q95/q99 ABSOLUTE error, rate of |error|>2ms (selected as a descriptive threshold, not Stage24 valid bound), count by class and how stale the last periodic telemetry was. No parameter selection, fake coverage claims, p-values, independent validation, or production deployment. Before Stage24 interval learning, pre-register a separate strict chronological calibration/validation split, independent sources, block-aware coverage, non-stationarity and queue model context consistency. Original Stage16/Stage23 performance outcomes and Python/CloudSimPlus mismatch remain unchanged.
