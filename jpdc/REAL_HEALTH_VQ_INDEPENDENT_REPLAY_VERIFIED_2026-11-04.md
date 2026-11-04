# JPDC — independently verified health and virtual queue state on real CloudSim events (2026-11-04)

## Verified experiment
This study was registered *before* its new CloudSim execution: `jpdc/REAL_HEALTH_VQ_EVENT_REPLAY_PROTOCOL_2026-11-04.md` commit `7ca51287745b4d3fba7e94c7bc2d34db818a5455`. It verifies independently implemented health detector and virtual queue state machine semantics against all task events from an original science run; it is **not** independent workload generation, physical VM simulation, YAFS, or demonstration of CASPER efficacy.

Generated-E45-only read-only logger `jpdc/instrument_real_health_vq_generated_e45.py` commit `20825126013de6b75c4f96637cc3f83ae354cb7a`; Python independent replay `jpdc/replay_real_health_vq_events.py` commit `23937e75a1007e6e601bdd8ff4146e788192c732`; actual workflow `.github/workflows/jpdc-real-health-vq-replay-once.yml` commit `c95a427e72c1d8d48f01820292b148b9cb2eba3c`.

**Real GitHub Actions run 41873772600 COMPLETED SUCCESS**, job `126727580133`, original artifact **13346515623** (2,744,360 bytes). No inferred or simulated success. The exact original-source E42 hash was checked: `34256ca7bff46f911cf20e8b94278fbd09175746`; E4.6 unchanged.

Control vs generated-only logged original E45 used fixed scientific seed `4202202640` (seed index40), S3_HIDDEN_NETWORK_50LOSS, HIGH six-node affected mask [9,12,14,15,17,18], 80k calibration, 30k deployment tasks, all eight policies. Logged scientific summaries matched uninstrumented controls exactly except non-scientific wall-clock mapper time; marker `JPDC_REAL_HEALTH_VQ_SCIENTIFIC_NONINTERFERENCE_PASS`.

## Original event replay output
All events for the **CASPER_FULL** policy:
- **21** original per-node calibration health thresholds; Python constructs new independent `NodeHealth` instances without copying Java detector history.
- **30,000** unique task dispatches and independently verified `VirtualQueueEstimator` backlog across all 21 nodes, in true source event order.
- **30,000** unique completed tasks, whose original realized service duration and predicted nominal service are fed into independent Python node-specific health detector history.
- **4,269** true telemetry reset events; original physical `trueNextFree` snapshots are exogenous inputs to the Python queue and *not* independently derived physics.
- Maximum difference in all pre-dispatch 21-node backlog checks = **0.0 milliseconds**.
- Maximum difference in selected-node post-dispatch next-free = **0.0 milliseconds**.
- Health detector state matched Java on every completed task and all 21-node pre-dispatch alarm masks; exact alarm discrepancy **0**.
- **Zero** health alarm transitions and zero alarmed nodes by end for this S3 **network-only** shock. Thus this run only covers the actual no-alarm path of health detection. Earlier synthetic Java-vs-Python test `41847775502` covers positive alarm latch but does not replace empirical degraded-compute positive alarm testing.
- Marker `JPDC_REAL_HEALTH_VQ_INDEPENDENT_REPLAY_PASS`.

A single complete observational run on seed40 establishes conditional event-state portability, NOT independent evidence of performance improvement. Strict historical FCFS mechanical fidelity test `41773297282` remains FAILED (9.1214ms max wait error > registered 5ms threshold); that was the physical queue semantics, not the separate virtual predicted queue estimator.

## Limitations and best next actions
1. A future separately registered **S2 hidden compute degradation** scientific run would be more informative for real health alarm activation and transition coverage. Do not claim positive alarm dynamics in the S3 network-only test.
2. The Python components now successfully verify virtual backlog and health/eta state on real original event streams, but only on Java-sourced physical telemetry, realized service time, calibration inputs and residual scores. To claim a genuine external simulator, independently generate task arrivals/work/transport, implement node service and queue engine semantics and fully reproduce prediction and calibration, then run a prespecified out-of-sample comparison on second engine.
3. Previously confirmed 14 rank2 selections across original untouched seeds41..44 and 14/14 realized on-time (exploratory selected seeds) do not provide rank1 counterfactual efficacy and rank3 remains unobserved.
4. Previously registered S2/S3 10-seed primary holdout p=.0625 and exploratory factorial sign p=.125 both nonsignificant. No threshold/p-value retrofitting and E42/E4.6 remain frozen.

## Exact original links
- Successful run https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41873772600
- Artifact https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41873772600/artifacts/13346515623
- Separate E17 real event replay success https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41848215650
- Positive health alarm synthetic parity success https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41847775502
