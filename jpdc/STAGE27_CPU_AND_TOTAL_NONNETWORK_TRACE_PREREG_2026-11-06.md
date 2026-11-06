# JPDC Stage27 — preregister causal CPU-service prediction residual and combined non-network error trace (2026-11-06)

## Background and frozen scientific boundaries
Stage25 WAIT-only residual observed at CPU finish, one development seed89. Stage26 archival causal central WAIT intervals achieve ~91.3% pooled empirical inclusion on same already-examined source seed, but MISSION age10–25ms fell to 84.68%. No independent coverage claim. Stage24 full nonnetwork q residual `q = actual nonnetwork duration - dispatch-predicted nonnetwork duration` is still missing CPU service error. Source Stage23 seed88 network-only policy S3 positive single-seed and S2 negative. Original Java SpaceShared vs native Python FCFS fidelity FAIL 9.1214ms>5ms. The original E42 Git blob `34256ca7bff46f911cf20e8b94278fbd09175746` and E4.6 must remain untouched.

## Frozen observational pilot, before new results
Exactly one new DEVELOPMENT scientific seed index **90** (not a fresh holdout for scientific efficacy) with native Stage3 calibration 80000 source tasks. Two scenarios S2_HIDDEN_COMPUTE_40LOSS and S3_HIDDEN_NETWORK_50LOSS, each with frozen PRED_GREEDY and CASPER_FULL, 12000 deployment tasks/arm, 48000 dependent *task-policy* observations (scientific n=1 seed). No Stage24 scheduling policy / no new active probes. Full original Stage6 output JSON must exactly equal the cloned engine (besides preexisting observer-only shadow field). Run full source matrix twice byte-identical.

## Immutable causal decomposition, recorded per CPU-finished task
At dispatch, after the selected node j is known but before queue update, record:
- `predicted_wait_ms = vq.predicted_backlog(j,now)` (can use last 50ms physical telemetry as frozen Stage6 already does);
- `predicted_cpu_ms = task.work/node.cap*12` (same `nominal` used in original physical source, *not* fitted to hidden physical CPU or future service noise);
- `predicted_nonnetwork_ms = predicted_wait_ms + predicted_cpu_ms`;
- source task class, source task index, chosen node, arrival/dispatch time, last actual telemetry timestamp and model context.
At actual **CPU finish**, record elapsed `actual_wait_ms = start-arrival`, `actual_cpu_ms = cpu_finish-start`, and two signed independently computed errors `q_wait = actual_wait-predicted_wait`, `q_cpu = actual_cpu-predicted_cpu`. Aggregate `q_total = q_wait+q_cpu = (cpu_finish-arrival) - predicted_nonnetwork_ms` at label delivery. No network realization is part of these errors. CPU finish is never an E2E network feedback event; no CPU service label is supplied to routing at dispatch.

No source truth `affected_nodes`, service shock onset, future task outcome or actual CPU is allowed as an input to the policy. Offline ground-truth exposure may be grouped descriptively, never used to choose intervention. The CPU finish trace may include task completion times earlier than the event-loop final time but must preserve exact per-task causal arrival<=start<=finish and unique index 0..11999.

## Prespecified engineering gates and diagnostics
For each arm assert 12000 task labels, zero duplicate IDs, valid signed arithmetic and finite values, exactly 12000 CPU+E2E events, exact Stage6 policy JSON parity, E42 blob unchanged, exact rerun of original trace and summary. Original policy and physical formula unchanged. Report separately pre-task-index10000 and post-task-index10000 signed CPU error mean/min/max and p95/p99 absolute values; same for full q_total and wait residual. Report S2 vs S3 and both policies irrespective of sign; do not claim stable conditional coverage. Reject any source that tries to equate `predicted_cpu` to actual CPU or include network delay in q_total.

## Next research gate
Only after gathering an independent source seed set with frozen protocol and describing failure modes should the full `q_total` be put through chronological prequential calibration/validation. An empirical 90% central interval is probabilistic/descriptive, not a sure hard bound. Absolute safety and JPDC novelty do not follow from this experiment.
