# JPDC independent physical event engine Stage 1 — verified 2026-11-04

## Execution status
Stage 1 was registered before execution in jpdc/INDEPENDENT_DISCRETE_EVENT_ENGINE_STAGE1_PREREG_2026-11-04.md. Frozen original E42 Git blob 34256ca7bff46f911cf20e8b94278fbd09175746 unchanged. This is a **new, executable, independent Python physical simulator**, not a validated full CASPER second-simulator implementation.

Final actual CI GitHub Actions run **41895984369 SUCCESS**, job 126805486872, commit bb92d23c869371bed902cb6f4db01383ea052d07, artifact 13354274606. Prior initial CI 41895799063 SUCCESS, but the final version additionally required explicit parallel execution and exact byte-identical replay of all 12 runs.

Python-only scientific inputs: independently generated native Java-compatible RNG workloads and 21 node specifications. Physical engine jpdc/independent_physical_event_engine.py uses a true priority event heap for arrivals/completions, 21 independent nonpreemptive single-server FCFS queues, exact completion-before-arrival event tie handling, immediate promotion of oldest waiting jobs, network delay outside CPU queue, and original 50ms virtual-queue telemetry updated from **independently simulated** queue state. No imported CloudSim physical trace.

Preregistered matrix: two new scientific seed indices 50,51; scenarios S0_STATIONARY, S1_LAMBDA_X2; each three baseline policies CLOUD_ONLY, EDGE_FIRST, PRED_GREEDY; 12,000 source tasks per run; **12 runs, 144,000 task-policy evaluations**. No adaptive CASPER/health/certification policy was simulated in this stage. The clean-room service and transport are *nominal deterministic*, with NO original service noise, hidden performance loss or YAFS equivalence yet.

### Real numerical results, descriptive within independent nominal engine

| Seed | Scenario | Policy | Mean latency ms | Mean wait ms | MISSION deadline misses |
|---|---|---|---:|---:|---:|
| 50 | S0 | CLOUD_ONLY | 72.825677 | 2.042122 | 190 |
| 50 | S0 | EDGE_FIRST | 154.073589 | 34.596357 | 338 |
| 50 | S0 | PRED_GREEDY | 58.514040 | 4.573533 | 14 |
| 50 | S1 | CLOUD_ONLY | 73.491211 | 2.339271 | 193 |
| 50 | S1 | EDGE_FIRST | 679.657347 | 559.380577 | 387 |
| 50 | S1 | PRED_GREEDY | 59.364377 | 4.683774 | 17 |
| 51 | S0 | CLOUD_ONLY | 67.210990 | 5.731573 | 99 |
| 51 | S0 | EDGE_FIRST | 246.776172 | 115.169984 | 497 |
| 51 | S0 | PRED_GREEDY | 53.356252 | 1.385169 | 3 |
| 51 | S1 | CLOUD_ONLY | 69.324964 | 6.841658 | 127 |
| 51 | S1 | EDGE_FIRST | 900.892616 | 768.977146 | 515 |
| 51 | S1 | PRED_GREEDY | 54.104571 | 1.745428 | 5 |

### Falsification tests passed
All native GitHub logs explicitly show older waiting job promoted at completion, completion-before-arrival tie handling, physically parallel execution on two different nodes, three baseline candidate sets, complete event conservation, rejection of malformed source workload, frozen matrix completeness, and **byte-identical JSON reports from a full second execution of all 12 runs**.

### Scientific limitations
The original CloudSimPlus SpaceShared queue admission sometimes bypasses older waiting tasks, unlike this new STRICT FCFS engine. Original prespecified Java-vs-Python queue fidelity test 41773297282 **FAILED** max error 9.1214009ms > original 5ms limit; this new success does NOT change that classification. The original S2/S3 holdout p=.0625 and exploratory factorial p=.125 remain nonsignificant, and rank2 outcome observations remain descriptive without causal rank1 counterfactual. No CASPER efficacy, generalizable superiority, CloudSim queue parity or YAFS evaluation should be inferred from these nominal baseline-only tests.

Next: independently reproduce original serviceNoise/mix64 and compute/network degradation, integrate physical outcomes into independently generated calibration scores, then assemble ranked certification/E17/health/queue feedback into this engine and freeze previously unseen seed-level comparative holdout tests.

GitHub run: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41895984369
Raw artifact: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41895984369/artifacts/13354274606
