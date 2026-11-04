# JPDC generated-E45 observed-outcome sidecar validation protocol
Date: 2026-11-03. Registered prior to the experimental workflow.

## Question
Can we record actual mission outcomes (not the prediction pred[j]) on the generated E45 path without changing its science? This is an INSTRUMENTATION VALIDATION, not a new adaptive-eta efficacy test.

## Frozen and controlled design
- Branch jpdc-seed0-repro-20261024, immutable E42 original Git blob 34256ca7bff46f911cf20e8b94278fbd09175746; E4.6 must not change.
- One previously studied seed index 40, S3_HIDDEN_NETWORK_50LOSS, HIGH fixed six-node mask [9,12,14,15,17,18]; 80000 calibration samples, 30000 deployment tasks.
- First execute an uninstrumented generated E45 HIGH run, then regenerate from the same frozen E42 and apply the identical mask plus the observational-only sidecar.
- Compare all eight policies' official scientific CSV columns exactly; ignore mean_mapper_us (instrumentation can increase logging overhead). All other rows/metrics must be equal. Verify frozen E42 SHA before both conditions.
- For CASPER_FULL and CASPER_HEALTH_STATIC, sidecar logs only MISSION completion events, with task index, chosen node, effective dispatch eta, predicted latency, **realized** network latency, observed CloudSim wait + service latency, actual total latency, deadline, certificate, family coverage, actual deadline miss, false certificate.
- Sidecar should emit one row per mission task/policy. Reconstruct reported mission/post/last250 rates (FAR, AIR, FWC, DVR, eta, p99) from events. Assert every metric agrees with official CSV. Fail on duplicates, invalid numbers, malformed flags, physical component discrepancies.
- A successful validation establishes observational trace integrity and noninterference in ONE seed/scenario, not independent implementation/generalization. No hypothesis testing or performance claims. Later trace-replay must use held-out trace assumptions and actual events, not pred[j] as an actual outcome.

## Falsification / failure conditions
Any modified scientific CSV value, missing task, duplicate task, invalid decomposition of observed latency, incorrect certification boolean, official metric mismatch, inconsistent seed or scenario, or generation/frozen-source error is a failed run. Preserve logs even on failure; do not infer from an incomplete artifact.

## Registered output
Workflow .github/workflows/jpdc-observed-outcome-sidecar-smoke-once.yml, generated-E45-only patch jpdc/instrument_observed_outcome_generated_e45.py, strict validator jpdc/audit_observed_outcome_sidecar.py. Final status and artifact IDs must be checked after run; workflow creation alone is not execution.
