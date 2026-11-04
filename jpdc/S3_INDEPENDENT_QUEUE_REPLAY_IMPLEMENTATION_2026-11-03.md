# JPDC S3 independent FCFS queue replay: implementation checkpoint (2026-11-03)

## What was actually implemented
To move beyond repeated arithmetic audits, a **separately written, Python-stdlib FCFS single-server per-node queue simulator** was developed. It independently calculates queue waits from externally recorded `arrival_ms`, policy-selected node, and observed service demand for *all* tasks. It does not read observed queue waits when predicting queue waits and does not import CloudSim or CASPER scheduling implementation.

Frozen E42 source SHA: `34256ca7bff46f911cf20e8b94278fbd09175746`; original E4.6 untouched. Source-level static check found exactly one correct instrumentation anchor in the deployment completion listener.

New generated-E45-only logger `jpdc/instrument_queue_replay_generated_e45.py`, commit `edd27b0154bd0cead460b089d78850717101d121`. Records one `JPDC_QUEUE_REPLAY` row for EVERY NORMAL and MISSION task for CASPER_FULL and CASPER_HEALTH_STATIC: arrival, chosen node, realized service, actual wait, realized network, total CloudSim-derived latency, deadline. Normal tasks MUST be present because they compete with mission tasks for the same VM. Source confirms 21 separate one-VM nodes using `CloudletSchedulerSpaceShared`.

New independent executable `jpdc/replay_s3_queues_independent.py`, commit `b654e1845555566b5a9fec0dad3cfcc274d85944`. For each node and policy, order ALL tasks by (arrival, task index), compute `start=max(arrival,node_free)`; then `wait=start-arrival` and `node_free=start+realized_service`; replay latency is network+replayed_wait+service. Compares full trace, error MAE/max, and postshock mission deadline misses with observed CloudSim-derived values. Rejects incomplete task populations, corrupted physical decompositions, and mismatched shared input metadata.

New synthetic regression `jpdc/test_replay_s3_queues_independent.py`, latest commit `61b87848f33f981346ee287c12a2f00bc26b79f6`. A *local functionally equivalent reconstruction* of simulator/test was **really compiled and executed** successfully:
```
PASS deterministic FCFS queue replay: two policies, four tasks each
PASS mismatch detected when observed queue wait is perturbed
JPDC_INDEPENDENT_QUEUE_SYNTHETIC_CONTRACT_PASS
```
Synthetic tests demonstrate two 4-task queues exactly replay, rejection if one NORMAL task is omitted or if a shared task arrival differs, and detection of deliberate wait-time error. The local reconstruction is not a byte-identical Git checkout; the exact committed GitHub file has not been run through independently observed CI yet.

## Preregistered real CloudSim cross-language mechanical check
Before creating the execution workflow, registered `jpdc/S3_INDEPENDENT_QUEUE_REPLAY_PREREG_2026-11-03.md`, commit `4920c3763ea82fb37ddd40795fc891cbe7b2b3cb`. New workflow `.github/workflows/jpdc-s3-independent-queue-replay-once.yml`, commit `c46ad3821e838df4898de8e6b7bc6996b6a0e5c8`:
- S3 seed index 40, HIGH 6-node mask [9,12,14,15,17,18], 80k calibration and 30k deployment tasks, paired control versus generated-E45 dual-instrumented run.
- Eight-policy scientific CSV exact parity (ignore only wall-clock mapper microseconds).
- Validate true observed MISSION outcomes using existing `jpdc/audit_observed_outcome_sidecar.py`.
- Run the independent Python queue emulator on **all-task** trace and record replayed wait and latency diagnostics.
- Prespecified acceptance criteria for each policy: wait MAE <=1ms; max absolute wait error <=5ms; EXACT equality of postshock MISSION miss counts. If unmet, report a failed mechanical transfer, not an improved or successful simulator.

**ACTUAL WORKFLOW OUTCOME NOT VERIFIED:** creation of a push-triggered GitHub Actions workflow does not establish run success. It may fail due to simplifying assumptions (same-arrival ordering, host/VM scheduling semantics, simulation time step). No real CloudSim dual-instrumentation artifact or queue result is yet available to this checkpoint.

## Scientific claim boundary
The Python emulator is independent **queue mechanics**, conditional on frozen CASPER-chosen node assignments and realized service demands. Even if all gates pass it does **not** independently implement a scheduling policy, independently generate workload/physical outcomes, or validate generalization to YAFS/other simulators. Do NOT claim second-simulator validation of CASPER from a successful mechanical replay. Task-level results are not independent seeds.

The original registered holdout p=.0625 and exploratory four-seed factorial sign p=.125 remain nonsignificant. Do not tune a threshold after observing outcomes or inflate claims.
