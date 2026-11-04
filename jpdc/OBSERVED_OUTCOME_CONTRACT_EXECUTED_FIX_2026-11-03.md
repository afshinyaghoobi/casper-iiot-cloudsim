# Observed-outcome contract: executed local test and fixed stale expectation (2026-11-03)

## Scientific scope
This step is **code quality and data integrity**, not an additional scheduling experiment. E42 frozen source blob remains `34256ca7bff46f911cf20e8b94278fbd09175746`; E4.6 unchanged. No new inferential results.

## Real execution and discovered failure
Fetched the source text of the current sidecar validator and test through the GitHub connector, reconstructed their functional contents in a local Python environment, compiled both using `python -m py_compile`, and actually ran the regression with the unchanged previous test expectation.

The initial test **FAILED**, after accepting 1,000 valid synthetic mission outcome rows, on the injected missing-record case. The validator correctly rejected the missing task with `cross-policy mission task ID mismatch`; the test incorrectly expected the older `mission count mismatch` message, which had become unreachable first because the more stringent cross-policy set comparison now runs earlier.

## Minimal correction and re-execution
Corrected exactly that test expectation in repository `jpdc/test_observed_outcome_sidecar_contract.py`, commit **`fef7aebb1256d6e30b0c755f8f7e0b4625407b34`**; no modification to the validator's scientific or audit semantics. Recompiled and reran the locally reconstructed updated source; it completed successfully:

```
PASS CASPER_FULL: missions=500 post=250 late=250, official metrics match
PASS CASPER_HEALTH_STATIC: missions=500 post=250 late=250, official metrics match
JPDC_OBSERVED_OUTCOME_RECONCILIATION_PASS
PASS valid 1000 mission-outcome events and eight official policies
JPDC_OBSERVED_OUTCOME_CONTRACT_TEST_PASS
```

All **nine** deliberately malformed cases were rejected: duplicate event, observed latency sum mismatch, incorrect false certificate flag, missing record, wrong seed, malformed boolean, substituted task ID, altered deadline, and corrupted official CSV rate. This is a full positive-and-negative run on a **locally reconstructed source file**, not byte-for-byte execution of a Git checkout. A local ZIP at `/mnt/data/jpdc_sidecar_contract_verified_2026_11_03.zip` contains reconstructed source, a successful log, and a README distinguishing their origin.

## Provenance limits and next experiment
GitHub connector does not list arbitrary push-triggered workflow runs (its commit-run lookup is PR-only), so the GitHub CI conclusion for the corrected test and the **actual instrumented-versus-uninstrumented CloudSim sidecar experiment** have not yet been directly observed. No sidecar result or noninterference parity claim is made.

Next priority: obtain the workflow's Actions run ID/status and artifact; verify eight-policy noninterference and event-to-official metrics on real CloudSim outputs; only then define an independent trace-replay exercise. Holdout p=.0625 and exploratory factorial p=.125 remain nonsignificant and unchanged. Avoid counting synthetic tasks as independent experimental replications.
