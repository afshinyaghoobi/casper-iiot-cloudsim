# JPDC independently implemented queue-mechanics replay: preregistered smoke protocol
Registered 2026-11-03 **before** running the new workflow. This experiment is a mechanical cross-implementation check, **NOT** independent algorithm implementation, out-of-distribution validation, or evidence of lower deadline misses.

## Frozen system
- Original E42 blob SHA `34256ca7bff46f911cf20e8b94278fbd09175746`; E4.6 never modified.
- Generate temporary E45 with `tools/e45_generate.py`. S3_HIDDEN_NETWORK_50LOSS, seed index 40, fixed HIGH affected-node mask `9,12,14,15,17,18`; 80,000 calibration samples, 30,000 deployment tasks.
- Two runs with identical science: uninstrumented control, and instrumented with BOTH `jpdc/instrument_observed_outcome_generated_e45.py` and `jpdc/instrument_queue_replay_generated_e45.py`. Reject any CSV science-column difference (except wall-clock `mean_mapper_us`).
- Archive command logs, exact git SHA, official 8-policy CSVs, outcome audit result, replay diagnostic JSON, and script versions; preserve on failure.

## New complete-queue trace
The additional all-task row `JPDC_QUEUE_REPLAY` includes **both mission and normal task** completion events for CASPER_FULL and CASPER_HEALTH_STATIC. Fields: seed, scenario, policy, task index, criticality, arrival time, selected node, observed service duration, *observed* CloudSim wait, realized network duration, CloudSim-derived observed total latency, deadline. The logger runs in the finish listener; it is observational only.

The independent standard-library Python queue simulator does not import/execute any CASPER or CloudSim scheduling classes. For each policy it takes the already chosen per-task node assignments, arrival times and realized service demands, sorts by arrival then task index, and advances a single FCFS server for each of the 21 nodes:
`start=max(arrival,node_free[node]); wait=start-arrival; node_free[node]=start+service`.
It predicts `network+wait+service` and compares to recorded CloudSim `wait` and `total`.

## Prespecified falsification and interpretation
- Fail closed if task IDs are incomplete or repeated, if the policy task populations differ in arrival/deadline/criticality, if the observed latency decomposition fails, or if metadata is inconsistent.
- **Mechanical match target:** for EACH policy, independently replayed wait-time MAE <= 1 ms, maximum absolute wait error <= 5 ms; and mission postshock count of deadline violations must be identical between replayed and observed output. If any fail, report **queue-mechanics transfer FAILED**, inspect event ordering, broker execution semantics and startup effects; do not weaken thresholds after observing outcomes.
- This is a deliberately strict initial target, not an assumption that CloudSim and Python will necessarily match. Completion order is ignored; arrivals determine replay event order.
- Even if it passes, this only validates queue and network mechanics **conditional on identical task assignments and service inputs**. It does not implement CASPER in a second simulator, test routing generalization, provide independent random seeds, or establish statistical improvement.
- If it fails, do not silently substitute observed CloudSim queue waits to obtain artificial agreement.

## Previous statistical results remain unchanged
Registered disjoint 10-seed S2/S3 holdout primary `p=.0625` (not significant); exploratory n=4 factorial sign `p=.125` (not significant). Task events are not independent seeds.

## Inputs / outputs
`jpdc/instrument_queue_replay_generated_e45.py`,
`jpdc/replay_s3_queues_independent.py`,
`jpdc/test_replay_s3_queues_independent.py`,
`.github/workflows/jpdc-s3-independent-queue-replay-once.yml`.
