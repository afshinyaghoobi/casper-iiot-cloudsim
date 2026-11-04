# JPDC independent CASPER state-port verification — executed 2026-11-04

## Two separately verified independent cross-language results

### A. Independent Python state machines compared against frozen Java classes
- Preregistered `jpdc/INDEPENDENT_CASPER_STATE_MACHINE_PARITY_PROTOCOL_2026-11-04.md` commit `ed219cac9fb21fc40a046eae62a5362bbf0971fc`.
- New independent standard-library `jpdc/independent_casper_state.py` (E17 slow/fast dual memory, node health detector, virtual queue estimator), commit `3c71eb696fee01fc408febe18967dcc748266421`.
- Read-only compiled original Java reference `jpdc/java_tests/CASPERStateReferenceHarness.java`, commit `5779e1d276d46bc888174feed98f5760cd9fd1ff`; Python strict comparator `jpdc/test_independent_casper_state_parity.py`, final commit `0a3b74625b2b895264225771351f0c5421322b4a`.
- First Actions run `41847634853` failed only *after* all three comparisons passed due to import path error in a negative test. Repaired CI `PYTHONPATH=jpdc`, commit `3dffda1bd82eaebfadf4440c8f3a7639c404675b`.
- **Real CI run 41847775502 SUCCESS**, artifact **13331748231**. Exact original Java vs independent Python parity: **601 E17 state observations** including eta, detector alarm and transition age; **360 node-health observations**, two thresholds and permanent alarm; **180 virtual-queue steps** including telemetry resets and pre/post predicted dispatch updates. Deliberately corrupted Java snapshot was rejected, `JPDC_INDEPENDENT_STATE_CORRUPTION_REJECTED_PASS`.
- All inputs in this first contract are deterministic synthetic fixtures. This passes cross-language state-function semantics, NOT CloudSim/YAFS policy performance.

### B. Independent E17 feedback state on REAL CloudSim event stream
- Preregistered **before simulation** `jpdc/E17_REAL_EVENT_INDEPENDENT_REPLAY_PROTOCOL_2026-11-04.md` commit `3e5897b152f3e62abd677b8f34df566826913fe1`.
- Generated E45-only observational logger `jpdc/instrument_e17_real_event_generated_e45.py` commit `5ea3d6484954107be1e69620db849b78de7fcae3`, and independent Python event-order replay `jpdc/replay_e17_real_cloudsim_events.py` commit `489cefaceed882b791b521e4fe02f5002a410579`.
- Real E45 S3_HIDDEN_NETWORK_50LOSS, scientific seed **4202202640** (seed index40), HIGH affected-node mask [9,12,14,15,17,18], 80k calibration and 30k deployment tasks. Both uninstrumented control and event-logged generated-E45 ran successfully.
- **Real GitHub Actions run 41848215650 SUCCESS**, source commit `55de7ac9a61bbdb5448e2bc2a8d3dcd9cb5a7b8e`, artifact **13333005342**. `JPDC_E17_REAL_EVENT_SCIENTIFIC_NONINTERFERENCE_PASS`: all eight policies' original scientific CSV fields exactly match control (except wall-clock `mean_mapper_us`).
- The Java source yielded **3501 original raw calibration reference scores** and a full chronological stream of **30000 dispatch events** and **1545 MISSION outcome feedback-score events** for CASPER_FULL. Python created a *fresh independent E17 object* from raw calibration scores, independently processed every outcome score at its actual CloudSim event position, and matched Java's independently emitted **eta, alarm and transition age at all 30000 dispatches** and **alarm/transition age at all 1545 MISSION outcomes**, with no discrepancy.
- Observed adaptive behavior: **29825 dispatch events with eta>1**, **one detector alarm transition**, detector alarm latched at end, `transitionAge=1022` at last outcome.
- `JPDC_E17_REAL_EVENT_INDEPENDENT_REPLAY_PASS`. This validates **E17 state transitions conditional on exogenous original Java calibration scores and completed-task residual scores**, not independent derivation of those scores, network/VM queue physics, entire workload, prediction vector or CASPER efficacy.

## Frozen science and unmodified historical conclusions
- E42 blob SHA `34256ca7bff46f911cf20e8b94278fbd09175746`; original E4.6 unchanged.
- Registered S2/S3 10-seed holdout two-sided sign p=.0625 **nonsignificant**; exploratory four-seed factorial sign p=.125 **nonsignificant**.
- Strict independent Python FCFS queue replay run `41773297282` remains **FAIL** on registered max wait 9.12140093294972ms >5ms, despite later observed CloudSim SpaceShared queue-bypass cause.
- Previous four-seed [41..44] S3 HIGH screen found real rank2 choices 14 across both policies, rank3 none. In separately labeled post-selection exploratory check, all 14 chosen rank2 tasks met actual deadlines, but **no rank1 counterfactual was evaluated**. None of that changed here.

## Research implications
The independent second-policy implementation now has three additional separately written Python state components (E17, health detector and virtual queue estimator) whose logic matches original Java on fixed test streams; E17 also matches a *real* chronological original CloudSim feedback stream. These are stronger verification than copying Java's eta as a precomputed input, but **a full independent simulator is still NOT validated**. Next defensible steps: replay actual per-node health observed-score streams and virtual queue telemetry/dispatch on scientific input streams; independently generate workloads and predictions; integrate those independently with a discrete-event engine and run predefined holdout scenarios before asserting external performance generalization.

## Provenance links
- Synthetic state parity success: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41847775502
- Actual E17 feedback replay success: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41848215650
