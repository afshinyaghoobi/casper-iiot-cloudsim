# JPDC Gate 2 — additive vs overlap EFT semantic audit (2026-10-28)

## Verified source behavior
Read the frozen E4.2 Java campaign source `src/main/java/org/casperiiot/e42/E42Campaign.java` on research branch. Its `predictedLatency` combines `nominalNetworkMs + vq.predictedBacklogMs + nominalServiceMs` (near source line 535). For nonconformal policies including `PRED_GREEDY`, the dispatch branch chooses `argMin(pred,eligible)` (near line 330). The E4.5 generator `tools/e45_generate.py` preserves this scientific scoring logic while changing arrival scheduling. The prior exploratory `QUEUE_AWARE_WEIGHTED_COMPLETION` specifically adds another weight of the backlog term, so it is not equivalent to `PRED_GREEDY`.

## Distinction from earlier reference
The initial Python `online_eft_reference.py` uses `max(arrival+network, free_at)+service`; in relative-time terms this is `max(network, backlog)+service`. This **can rank nodes differently** from the additive `network+backlog+service` predictor. The earlier reference is a separate alternative overlapping-transfer semantics, not a faithful port of the simulator's `PRED_GREEDY`, and must not be presented as a fair, literature-faithful head-to-head baseline until assumptions are matched.

## Executed unit evidence
Run `python3 jpdc/test_eft_semantic_gap.py`. Four deterministic synthetic fixtures passed locally on 2026-10-28; the ranking reversal fixture uses:
- Node 0 network 8, backlog 0, service 1: additive score 9, overlap score 9.
- Node 1 network 3, backlog 6, service 1: additive score 10, overlap score 7.

Additive chooses node 0, overlap chooses node 1. Units are arbitrary consistent synthetic time units, not simulator measurements. This is a semantic counterexample, **not** a CASPER performance experiment.

## Scientific decision
- Use the already-existing `PRED_GREEDY` as the simulator-faithful additive predicted completion reference, not a new baseline under a different name.
- Retain overlapping EFT only as a separately labeled modeling sensitivity experiment if comparable network transfer/queue overlap can be justified in the simulator implementation.
- A truly stronger publication baseline must be selected based on task semantics, information availability, complexity and source-paper algorithm description. If the workload is independent tasks, do not label an online heuristic HEFT (an offline DAG method).
- No new SOTA, statistical superiority, cross-generator transfer, coverage or novelty claims result from this unit test. E4.6 remains immutable.

## Next gate
Audit whether the task model has precedence/DAG constraints; inspect the scheduler's queue estimator and dispatch clock to establish valid comparator state, then specify an actual independent competitor rather than duplicating `PRED_GREEDY`.
