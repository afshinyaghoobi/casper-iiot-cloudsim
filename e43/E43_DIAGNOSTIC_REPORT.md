# E4.3 Post-hoc Diagnostic Report

This analysis reads the frozen E4.2 publication artifact only. No E4.2 parameter, threshold, workload, seed, policy, health rule, probe budget, CloudSim runtime setting, or publication gate was changed.

## Frozen source

- E4.2 scientific SHA: `ee1600b808a9747bc0373489e8ce531bd6bfb5e0`
- Publication run: `34559237514`
- Artifact: `e42-publication-results` (`10183790808`)
- Artifact SHA-256: `ad625e3581121b53ce5c93a7f2b71643fed924f32b64dd45967e1aee51680204`
- Rows: 1,200
- Seeds: 30

## Primary diagnosis

The most important aggregate finding is exact behavioral equivalence. Across every frozen seed and scenario, the reported FWC, AIR, FAR, DVR, and P99 latency outcome metrics for `CASPER_ADAPT_NO_HEALTH`, `CASPER_HEALTH_STATIC`, and `CASPER_FULL` are identical to `RANKED_CP_STATIC` within numerical equality.

This means that, in E4.2, enabling the adaptive layer and/or health layer did not change the reported run-level outcomes relative to the static ranked conformal policy.

A second strong finding is that `late_eta` is exactly `1.0` in every E4.2 run for both adaptive policies. Therefore the E1.7 adaptive conformal multiplier did not alter the late-window envelope in any reported seed/scenario.

## CASPER_FULL late-FWC evidence

| Scenario | Mean late FWC | Seeds with late FWC >= 0.99 |
|---|---:|---:|
| S0_STATIONARY | 0.99147 | 18 / 30 |
| S1_LAMBDA_X2 | 0.98947 | 14 / 30 |
| S2_HIDDEN_COMPUTE_40LOSS | 0.54387 | 0 / 30 |
| S3_HIDDEN_NETWORK_50LOSS | 0.43893 | 1 / 30 |
| S4_COMPOUND | 0.45520 | 0 / 30 |

The hidden-degradation failures are therefore not isolated seed outliers. They are systematic in S2, S3, and S4.

## Compute-health evidence

For `CASPER_FULL`:

| Scenario | Mean compute alarm coverage | corr(alarm coverage, late FWC) | corr(alarm coverage, late DVR) |
|---|---:|---:|---:|
| S2_HIDDEN_COMPUTE_40LOSS | 0.37222 | -0.57277 | 0.28294 |
| S4_COMPOUND | 0.41111 | -0.72880 | 0.63967 |

The correlations are descriptive only and are not causal. They do show that seeds with more final degraded-node alarms did not exhibit improved late FWC in this campaign. This is consistent with the health layer being too late, targeting nodes that are not decision-critical, or otherwise failing to alter the selected candidate family in time.

## Source-code observations

The frozen E4.2 source constructs an `alarmMask` and excludes alarmed nodes from the eligible set for health-enabled policies. Sparse Normal-task probes can target alarmed or stale nodes, and `NodeHealthDetector.observe(...)` is updated only on Cloudlet completion. The E1.7 adaptive memory is updated from completed Mission outcomes and `etaBeforeOutcome()` is queried at dispatch.

These mechanisms exist in the code, but the aggregate outcomes show that they did not change the final reported behavior. Since the aggregate artifact does not contain event-level node selections, alarm timestamps, probe targets, candidate-family membership, or E1.7 detector transitions, aggregate analysis alone cannot identify the exact event-level mechanism.

## E4.3 conclusion

E4.2 remains closed and frozen as a valid publication-scale FAIL. No result-driven retuning is permitted.

The next permitted step is **E4.3 trace-only instrumentation**. That experiment must preserve the E4.2 scientific decision rules and record, at minimum:

- selected node and candidate family for Mission tasks,
- affected/degraded membership of candidate and selected nodes,
- alarm state at dispatch,
- first alarm time/task per node,
- sparse-probe target and outcome,
- E1.7 detector transition/alarm state and eta at dispatch,
- whether health exclusion actually changed the selected family/node relative to the no-health counterfactual,
- whether adaptation changed any certification decision relative to eta = 1.

Only after those traces establish a causal mechanism should a new architecture experiment be designed. Any such architecture change must be a new predeclared stage and must not be relabeled as E4.2.
