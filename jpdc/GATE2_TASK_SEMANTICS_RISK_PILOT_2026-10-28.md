# JPDC Gate 2 — source-grounded task semantics and risk-greedy pilot (2026-10-28)

## Source audit
Read `src/main/java/org/casperiiot/e42/E42Campaign.java`, `tools/e45_generate.py`, and the prior queue-weighted comparator patch from research branch.
- `Task` is a record of task index, criticality, deadline, work, input/output size and arrival time (source lines 76–77). **No DAG predecessor or dependency fields are modeled in this simulation.** Do not advertise this as a DAG workload or claim that HEFT is a directly equivalent online baseline.
- The runtime mapper builds `predictedLatency = nominalNetwork + VirtualQueueEstimator.predictedBacklog + nominalService` using dispatch-time estimates (source near line 535).
- `PRED_GREEDY` already selects the minimum predicted latency from eligible nodes; therefore rebranding the same algorithm as EFT is duplicate-baseline inflation.
- The hidden actual shock is used to compute realized service/network and evaluation diagnostics, not as a permissible heuristic input.

## Implemented experimental candidate
`jpdc/uncertainty_penalized_greedy_patch.py` patches only a generated E45 source with a new `UNCERTAINTY_PENALIZED_GREEDY` policy, score
`predictedLatencyMs + 1.0 * fixedSigma(predictedLatencyMs,nodeSigmaMult)`.
It uses a fixed `lambda=1.0` defined before outcomes and no true affected mask, future task knowledge, oracle latencies or heldout-tuned coefficient. The fixedSigma definition is shared with CASPER, so it is **not statistically or architecturally independent** of CASPER; use as a risk-penalization **ablation/control**, NOT as a literature-faithful external baseline or evidence of novelty.

`.github/workflows/jpdc-risk-greedy-pilot.yml` generates an isolated E45 source, patches it, compiles and specifies one 30k-task, 80k-calibration seed-zero experiment across five scenarios, expecting 45 rows (9 policies x 5 scenarios). It uploads logs even if simulation fails.

## Evidence status
- Source audit completed and patch/workflow committed.
- Pilot Actions execution and success: **not verified**.
- E4.6 frozen baseline: unchanged.
- No empirical improvement, statistical significance, nominal 99% conformal coverage, external generalization or novelty claim.

## Next gate
Run/verify pilot, then confirm all original policy CSV outputs are bitwise equivalent to an unpatched generated E45 run on identical seed before scaling to 30 disjoint seeds. In parallel select a source-faithful independent-task comparator with matched task-observation and release semantics, rather than HEFT or a duplicate greedy policy.
