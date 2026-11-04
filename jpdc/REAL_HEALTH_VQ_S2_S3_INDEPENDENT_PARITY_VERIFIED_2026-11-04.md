# JPDC — Real CloudSim health and VQ independent replay: S3 and S2 verified (2026-11-04)

## Real execution and scientific scope

Two distinct preregistered generated-E45-only observational experiments compare the original unmodified CloudSim science with an **independently written Python state engine** (`jpdc/independent_casper_state.py` classes `NodeHealth` and `VirtualQueue`). Input streams consist of the actual completion service times and original predicted service, original physical `trueNextFree` telemetry snapshots, and calibration-derived per-node health thresholds. The Python program independently maintains all node health windows/alarms and predicted queue next-free states in *chronological* original simulator event order. It does **not** independently derive service/queue physical outcomes or telemetry and does **not** simulate an entire CASPER system in YAFS.

Both workflows test E42 original git blob `34256ca7bff46f911cf20e8b94278fbd09175746` and leave E4.6 unchanged, scientific seed index40 (seed `4202202640`), 80k calibration and 30k deployment, all eight original policies, paired uninstrumented vs generated-E45-only observational sidecar; science CSV parity passed excluding non-scientific mapper timing.

| Characteristic | S3 network loss | S2 compute loss |
|---|---:|---:|
| Original event-study protocol | `jpdc/REAL_HEALTH_VQ_EVENT_REPLAY_PROTOCOL_2026-11-04.md` | `jpdc/S2_REAL_HEALTH_POSITIVE_EVENT_PREREG_2026-11-04.md` |
| Real GitHub Actions run | **41873772600 SUCCESS** | **41874289007 SUCCESS** |
| Original artifact ID | **13346515623** | **13345786902** |
| 21-node pre-dispatch alarm mask checks | 30,000 tasks | 30,000 tasks |
| Independent full task dispatches | 30,000 | 30,000 |
| Actual task completion / health updates | 30,000 | 30,000 |
| Physical telemetry resets processed | 4,269 | 4,269 |
| Real health alarm transitions | **0** | **6** |
| Alarmed nodes at end | **0** | **6** |
| First alarm triggering task ID | None | **10131** |
| Maximum 21-node virtual backlog error | **0.0 ms** | **0.0 ms** |
| Maximum selected-node next-free error | **0.0 ms** | **0.0 ms** |
| All eight scientific CSV metrics match logger-free control | **PASS** | **PASS** |
| Independent per-event health and VQ audit | **PASS** | **PASS** |

### First: S3 network-only real event stream
- Preregistered `jpdc/REAL_HEALTH_VQ_EVENT_REPLAY_PROTOCOL_2026-11-04.md`, commit `7ca51287745b4d3fba7e94c7bc2d34db818a5455`.
- Original generated-E45-only logger `jpdc/instrument_real_health_vq_generated_e45.py`, initial commit `20825126013de6b75c4f96637cc3f83ae354cb7a`.
- New independent real event queue/health replay `jpdc/replay_real_health_vq_events.py`, initial commit `23937e75a1007e6e601bdd8ff4146e788192c732`.
- Workflow `.github/workflows/jpdc-real-health-vq-replay-once.yml`, commit `c95a427e72c1d8d48f01820292b148b9cb2eba3c`.
- **Run 41873772600 SUCCESS**, job 126727580133, original artifact **13346515623**, `JPDC_REAL_HEALTH_VQ_SCIENTIFIC_NONINTERFERENCE_PASS` and `JPDC_REAL_HEALTH_VQ_INDEPENDENT_REPLAY_PASS`. Health alarms zero in this network-only shock. This run verifies actual no-alarm health path and all 21-node virtual queue transitions.

### Second: S2 degraded-compute real positive alarm coverage
- Preregistered *before simulation* `jpdc/S2_REAL_HEALTH_POSITIVE_EVENT_PREREG_2026-11-04.md` commit `d19247ea857a6d76ebfedc0d9781d99cd5fda5cb`.
- Extended the exact same generated-E45-only logger with a selected scenario guard `--scenario S2_HIDDEN_COMPUTE_40LOSS` while preserving default S3 behavior; commit `a08251ec94fc51670a1fea5fb1925dcf7d0a360a`. Extended independent replay to record first genuine health-alarm triggering task while retaining all existing strict checks, commit `1303eb14bbbdb52892378c8efc01c770912d6946`.
- Original scientific S2 compute loss scenario and original affected-node selector; **no S3 damaged-mask customization applied to S2**, no threshold/deadline/calibration/eta modification. Workflow `.github/workflows/jpdc-s2-real-health-positive-replay.yml`, commit `26c5494d2caa980af29d860f08d849da000f2623`.
- **Real GitHub Actions run 41874289007 SUCCESS**, job 126729372061, original raw artifact **13345786902**. `JPDC_S2_REAL_HEALTH_SCIENTIFIC_NONINTERFERENCE_PASS`, `JPDC_REAL_HEALTH_VQ_INDEPENDENT_REPLAY_PASS` and explicit `JPDC_S2_REAL_POSITIVE_HEALTH_ALARM_COVERAGE_OBSERVED`.
- Actual task completion events caused **6 different nodes to latch true**; first alarm was on task **10131**. All 30,000 completed service/nominal ratios and 30,000 dispatch-time 21-node alarm masks were independently reconstructed and matched without exceptions, plus all 4,269 telemetry resets and every selected-node queue next-free. No hidden filtering or altered acceptance bound.

## What this establishes (and does not)
**Established:** independently written Python has the same health detector and queue *state transition semantics* as Java on original chronological real event streams, including both no-alarm S3 and positive-alarm S2 conditions. The previously validated E17 adaptive memory independently matched real seed40 dispatch history: workflow 41848215650, all 30k `eta` values, 1545 feedback scores, one detector alarm.

**Not established:** independently generated calibration/score, independent task arrivals/workloads/predictions/physical processing in another engine, causal policy efficacy, nominal conformal coverage, external generalization, or a new statistically significant comparison. Original registered ten-seed S2/S3 holdout exact sign p=.0625 and exploratory four-seed factorial p=.125 nonsignificant. Original strict independent Python chronological-FCFS physical queue transfer **FAILED**, max error 9.1214ms vs original accepted 5ms (run41773297282); later observed CloudSim SpaceShared task bypass explains the mismatch but does not change original FAIL. In original 4-seed 41..44 S3 HIGH screen rank2 activated 14 times, 14/14 selected task completions on time in a *post-selection* follow-up, no tested rank1 counterfactual; rank3 unobserved.

## Scientific next steps
1. Independently reconstruct **workload arrivals, task attributes, node properties, network and prediction inputs**, rather than repeatedly verifying components conditional on Java output streams.
2. Execute a second discrete-event runtime (possibly YAFS) with a complete new Python implementation and a preregistered out-of-sample scientific evaluation, explicitly separating different physical queue semantics.
3. Write JPDC Results/Limitations around evidence gates. Avoid changing frozen source, claiming full independent second simulator or searching seeds to force rank3 activation.

## Links
- S3 actual replay https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41873772600
- S2 positive-health replay https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41874289007
- S2 artifact https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41874289007/artifacts/13345786902
