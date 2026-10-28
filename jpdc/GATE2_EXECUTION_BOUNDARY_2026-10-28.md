# CASPER Gate 2 — local execution boundary and validated fixture (2026-10-28)

## What ran in the current environment
- Executed the current `verify_risk_greedy_pilot_parity.py` logic against local **synthetic** fixtures at `/mnt/data/casper_gate2/before.csv` and `after.csv`.
- Received `RISK_GREEDY_PARITY_PASS (40, 45)`. This checks 8 old policies × 5 scenarios, plus one new policy × 5 scenarios. The fixtures are NOT results from CloudSim and provide no performance evidence.

## Why full CloudSim was not run locally
- `java` is installed, but `mvn` is not available.
- The active runtime cannot resolve `github.com` to clone the repository; the connected GitHub tool can read and commit source files, but it has no workflow-dispatch or push-run-list action.
- GitHub Actions pilot is configured as `workflow_dispatch` and on selected branch pushes. No successful run was verified.

## Precise next execution action
On the GitHub workflow page:
`https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/workflows/jpdc-risk-greedy-pilot.yml`
select **Run workflow**, choose `jpdc-seed0-repro-20261024`, and run. The workflow will generate E45 in isolation, run unmodified seed0 (40 rows), patch risk greedy, run patched seed0 (45 rows), compare all original scientific columns and preserve diagnostics when failures occur.

## Evidence boundary
Do not interpret fixture `late_dvr` and latency columns as simulator output. Do not assert 5-scenario success or any risk-greedy improvement without downloading and verifying the real pilot artifact. E4.6 tag is unchanged.
