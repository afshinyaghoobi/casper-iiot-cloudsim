# JPDC independent queue replay: HIGH criticality correction and executed regression (2026-11-03)

## New source-level defect found and fixed
An inspection of frozen `src/main/java/org/casperiiot/e42/E42Campaign.java` (Git blob `34256ca7bff46f911cf20e8b94278fbd09175746`) established that task criticality has exactly **three** categories: `NORMAL`, `HIGH`, `MISSION`. Previously committed `jpdc/replay_s3_queues_independent.py` only accepted `NORMAL` and `MISSION`. The genuine all-task generated-E45 logger would therefore emit `HIGH` events that the independent replay rejected with `unexpected criticality`. This bug could make a valid CloudSim trace fail before any mechanical comparison.

The fix **does not filter** HIGH tasks, since they occupy the same VM queues and can delay subsequent MISSION tasks. Updated `jpdc/replay_s3_queues_independent.py` to accept all three categories, commit `3463c934aa188ec2823a7c2784e057e5a4114cf8`.

## New stronger falsification fixture
`jpdc/test_replay_s3_queues_independent.py` now contains a HIGH task arriving at 3ms on node0, following NORMAL work arriving at 0ms (10ms service) and MISSION work arriving at 2ms (5ms service). The HIGH task must wait **12ms**, work for 4ms and release the node at 19ms, causing a subsequent MISSION task arriving at 10ms to wait **9ms**. This directly tests the previously missing queue-coupling mechanism. New fixture commit `6ddfb479fa40b2ae8105f985b2604bc01aed5584` after adding initial HIGH coverage at `b2807dfafb64a005d99b8c2fa62b4a8a7c804637`.

Local test was actually rerun in the container against a functionally equivalent reconstructed script, including the HIGH queue competition. Result:

```
PASS deterministic FCFS queue replay: two policies, four tasks each
PASS mismatch detected when observed queue wait is perturbed
JPDC_INDEPENDENT_QUEUE_SYNTHETIC_CONTRACT_PASS
```

The test additionally rejected omitted NORMAL work and altered shared arrival metadata. It checks the predicted wait and latency against expected synthetic values without using observed waits for the replay calculation. This is **unit-level evidence only** and is not evidence of CloudSim/second-simulator agreement.

## CI safeguard
Added a lightweight fast unit test workflow `.github/workflows/jpdc-independent-queue-unit-tests.yml` commit `a40362e58334a8c9ac87f5c48b0175914f9224a1`, triggered by replay source/test changes or workflow_dispatch. The actual GitHub Actions conclusion has not yet been fetched; the verified outcome is the local test above.

## Next and limitations
Obtain/check real CloudSim workflow `.github/workflows/jpdc-s3-independent-queue-replay-once.yml` result, and inspect full output including HIGH task events and actual queue wait. If the cloud-to-Python FCFS fidelity gate fails, report the failure without changing preregistered MAE/max thresholds. Source E42 and E4.6 remain immutable. Registered independent S2/S3 holdout p=.0625 and exploratory factorial sign p=.125 remain nonsignificant. No new CASPER scheduler performance experiment was run.
