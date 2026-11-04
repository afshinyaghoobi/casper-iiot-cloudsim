# JPDC observed-outcome validator: synthetic falsification checkpoint (2026-11-03)

## Scope
This step validates the **software contract** for the new generated-E45 observed mission-outcome logger and strict official CSV reconciliation tool, without inventing any new CloudSim results. Frozen E42 blob remains `34256ca7bff46f911cf20e8b94278fbd09175746`; E4.6 remains untouched.

## Actual locally executed validation
A local independent stdlib Python test fixture constructed 1,000 synthetic MISSION completion events (500 per policy; 250 pre / 250 post per policy) with explicit prediction, realized network + wait + service components, certification booleans, deadline misses, and an official CSV with correct rates and P99. The existing validator (reproduced locally from the committed logic) correctly accepted the valid fixture.

Seven negative cases were deliberately injected and rejected:
1. Duplicate task record.
2. Actual latency inconsistent with network + wait + service.
3. Incorrect `false_cert` boolean.
4. Missing MISSION record.
5. Incorrect scientific seed on one row.
6. Invalid certificate boolean.
7. Official CSV rate inconsistent with event-level trace.

**Result:** all seven falsification scenarios rejected, valid fixture accepted. This is a unit/contract test, not evidence of scientific performance or completed CloudSim instrumentation.

## Permanently committed regression and CI
- `jpdc/test_observed_outcome_sidecar_contract.py` commit `2cf879d9d7ed3ea2791ba601657c7e191bea871b` adds a self-contained synthetic reproduction of the positive/negative tests.
- `.github/workflows/jpdc-observed-outcome-validator-tests.yml` commit `907c8c9d4a275310a9ad153169f706fda9682b03` executes `py_compile` and the synthetic contract test after relevant changes.
- Previously registered S3 seed40 HIGH paired instrumented vs uninstrumented workflow `.github/workflows/jpdc-observed-outcome-sidecar-smoke-once.yml` remains the next **actual CloudSim gate**.

## GitHub Actions status limitation
GitHub connector `fetch_commit_workflow_runs` exposes PR-triggered runs only; it returned no associated runs for workflow creation commit `3957e22aab6b32474d46f0b3397fcde533bfe270` or a later checkpoint, which does **NOT** establish that the push-triggered workflow did not run. A public web attempt to open the Actions workflow did not resolve its status. We therefore cannot yet truthfully label the full sidecar CloudSim experiment successful or failed. The positive/negative synthetic test is the verified new result.

## Scientific next step
Retrieve the actual observed-outcome workflow run ID / job status through GitHub Actions and inspect its artifact, scientific CSV parity, and genuine task-level outcome reconciliation. If needed, correct logger/validator only. After successful source-side validation, predefine a separate trace-replay model that does not accidentally call `pred[j]` the actual latency and does not infer simulator-independent performance from a replay of the same outcomes.

Original independent holdout primary p=.0625 and four-seed exploratory factorial p=.125 remain unchanged and nonconfirmatory. No E42/E4.6 edits and no new claims of improved task completion.
