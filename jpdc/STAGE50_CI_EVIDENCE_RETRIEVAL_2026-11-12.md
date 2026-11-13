# Stage50 CI evidence retrieval / operator handoff (2026-11-12)

**Status: No observed GitHub Actions run success or failure.** The connected GitHub API's commit-workflow-runs reader reports only PR-triggered runs, which is NOT an exhaustive read of the branch's push-triggered workflows. Empty results must not be interpreted as a workflow that never ran. The available connector cannot list workflow runs by YAML name or dispatch a new one. Do not claim PASS based on commits or code inspection.

## Browser route (requires GitHub session authorized to view this repository)
Open: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/workflows/jpdc-stage50-native-queue-transitions.yml
Select branch `jpdc-seed0-repro-20261024`; open the newest relevant run. Record the numeric run ID, exact run conclusion, attempt number, commit SHA and failed job/step if any. If no run exists, select **Run workflow**, choose the same branch, and dispatch. Upload the artifact `jpdc-stage50-native-transitions-all-clocks` if the workflow produces it. On failure retain all native/stdout logs and failure tracebacks; do not suppress failed checks.

## Optional CLI route (on a machine with gh authenticated)
```bash
gh run list -R afshinyaghoobi/casper-iiot-cloudsim --workflow jpdc-stage50-native-queue-transitions.yml --branch jpdc-seed0-repro-20261024 --limit 5
gh workflow run jpdc-stage50-native-queue-transitions.yml -R afshinyaghoobi/casper-iiot-cloudsim --ref jpdc-seed0-repro-20261024
# Use the ACTUAL numeric run ID from list, not a guessed value:
gh run view RUN_ID -R afshinyaghoobi/casper-iiot-cloudsim --json status,conclusion,headSha,attempt,jobs
gh run view RUN_ID -R afshinyaghoobi/casper-iiot-cloudsim --log-failed
gh run download RUN_ID -R afshinyaghoobi/casper-iiot-cloudsim -n jpdc-stage50-native-transitions-all-clocks -D stage50-evidence
```
If the artifact has expired or the run has not produced one, record this limitation. Never substitute synthetic contract fixtures for real CloudSim event traces.

## Mandatory evidence review after retrieval
Inspect `native.log`, `native_repeat.log`, `audit.json`, `audit_repeat.json`, `audit.log`, `source_commit.txt` and job steps. Confirm all 3 clock scenarios and 3 cloudlets each; source E42 hash freeze check, native/JSON byte equality and no failed tests. If successful, compare first observed EXEC-list placement, native wait, and ideal strict-FCFS wait; do not equate EXEC-list appearance with actual CPU start or assert the failed original 30k Java–Python parity is repaired. If failed, diagnose from raw native logs and record the failure before changing code. No Stage50 result may be called verified without the real artifact and run conclusion.
