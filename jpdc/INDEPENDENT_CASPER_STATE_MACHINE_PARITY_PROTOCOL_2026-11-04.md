# JPDC independent CASPER state-machine portability contract — 2026-11-04

## Scope and source
This is a **new independent cross-language portability test of the state-machine components**, not a second CloudSim performance experiment. Frozen science: E42 Git blob `34256ca7bff46f911cf20e8b94278fbd09175746`, E4.6 unchanged. Original Java classes in `src/main/java/org/casperiiot/e41/core`: `E17DualMemory.java` SHA `62008de14532927aa3f4c3b7efa19d0c7448dbe5`, `NodeHealthDetector.java` SHA `e21460e6c9184205bc1a555d7d15405b10c8a403`, `VirtualQueueEstimator.java` SHA `9a66ed8b0b7a2b46ab86e8ff19b76b3bfc3169d2`, and `FrozenConfig.java` SHA `5513f13c66fdb42cc9db9d431035f21e03270d60`.

The Python standard-library implementations cannot import Java code, numerical outputs, or frozen Java objects. A separately compiled, read-only Java harness shall exercise the actual original classes, using deterministic synthetic inputs defined below; Python independently regenerates the same inputs and checks every output.

## Frozen deterministic test coverage

**E1.7 adaptive dual memory:** 300 original calibration reference scores `0.50+((i*37)%101)/100`, 600 outcome scores: for i<150, `0.65+((i*17)%23)/100`; for 150<=i<330, `2.50+((i*29)%31)/100`; otherwise `0.80+((i*13)%19)/100`. At t=0..600, record eta *before* outcome and alarm flag, transition age, reference Q95; compare with Python. This exercises slow/fast Q95, detector alarm, finite transition hold, clipped eta, and shifting score distribution.

**Node health:** two independently stateful detectors with original default 8-observation window and 5 exceedances; thresholds 1.10 and 1.40; for t=0..179, ratio generated as `0.80+((t*11+node*7)%17)/10` (nominal predicted service 10ms). Require equality of alarm states at each observation, including permanent alarm latch.

**Virtual queue:** three independent nodes and deterministic predicted service durations, variable dispatch selection and 50ms telemetry resets. 180 steps: `now=2.5*t`, reset from synthetic true-next-free array when `t%20==0` (`now+5*(node+1)`); before each dispatch, record backlog at every node, then dispatch to `node=(t*7)%3`, predicted service `2+(t%11)*0.25`, and record all predicted next-free values. At every step compare Python against original Java outputs. This is a mathematical estimator test, NOT simulation of actual CloudSim queue behavior.

## Pass/fail
Every Java record must be present exactly once with expected stage/order, numeric finite, tolerance 1e-10 for eta/reference/queue values, exact booleans and transition age. Any disagreement, changed threshold/fixture or source blob drift FAILS; report, do not silently fix output by copying Java state. Synthetic inputs and test do not provide independent CASPER efficacy results, task deadline improvement or YAFS generalization. Original primary disjoint holdout p=.0625 nonsignificant, exploratory factorial p=.125 nonsignificant, original external strict FCFS mechanical gate FAILED 9.1214ms>5ms. Do not reinterpret.

## Next technical step
After success, port task-arrival/workload generation, predictedLatency and calibration independently and compare against original source under a separately registered protocol. Only then combine with a second discrete-event engine to form a complete independent scheduler performance assessment.
