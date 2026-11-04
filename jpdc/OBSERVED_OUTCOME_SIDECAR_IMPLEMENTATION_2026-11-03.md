# JPDC observed-outcome instrumentation — implementation checkpoint (2026-11-03)

## Purpose
Prepare the first *true observed outcome* MISSION trace on generated E45 for independent future trace-replay, correcting the earlier conflation of `pred[j]` (prediction) and measured latency.

## Source-level verified semantics
The frozen E42 SHA is `34256ca7bff46f911cf20e8b94278fbd09175746`. In the deployment CloudSim finish callback, `actualLatency=m.actualNetworkMs + cl.getStartWaitTime()*1000.0 + serviceMs`; `dvr=actualLatency>m.task.deadlineMs()`; `far=m.certified && dvr`. The new observational log is inserted immediately after the existing MissionRec addition in **generated E45 only**. There is one exact matching insertion anchor in frozen E42. The logger records actual network, wait, service and total observed latency separately from predicted latency, deadline, eta, certificate, family coverage and miss/false-cert booleans. It prints only S3 CASPER_FULL and CASPER_HEALTH_STATIC mission completions.

## Committed implementation
- `jpdc/instrument_observed_outcome_generated_e45.py`, commit `9f3d761604c8fbef4f68589c0df3fa1389bcc464`. Fail-closed exact anchor; observational print only; does not modify policy or latency calculations.
- `jpdc/audit_observed_outcome_sidecar.py`, commits `38373b8dbaf107773a7554cca906ff2ab79a1960`, `4f3e43bbe34e5e764ef6c4866e55b26cc1cf0b33`. Validates sidecar field cardinality, 21-node bounds, seed/policy/scenario identity, unique tasks, physical network + wait + service total, miss/false-cert logic, mission/post/late counts, FAR/AIR/FWC/DVR, eta and p99 against the official results CSV. Requires 250 late mission tasks.
- **Protocol registered before workflow:** `jpdc/OBSERVED_OUTCOME_SIDECAR_PROTOCOL_2026-11-03.md` commit `f44e5994a7995810226ccff21c81e91d47f87a4a`.
- `.github/workflows/jpdc-observed-outcome-sidecar-smoke-once.yml` commit `3957e22aab6b32474d46f0b3397fcde533bfe270`. Runs S3 seed40 HIGH fixed mask [9,12,14,15,17,18], 80k calibration / 30k tasks twice: uninstrumented and instrumented generated E45. Requires exact parity of 8 policies' official scientific CSV columns except wall-clock mapper time, then full task-level sidecar reconciliation; uploads logs/CSVs even on failure.
- Static source validation done: correct E42 blob, one instrumentation insertion anchor, correct observed outcome formula and fields, validator and paired noninterference workflow present.

## CURRENT EVIDENCE STATUS
**The Actions run has NOT been independently observed completed in this checkpoint.** Creating a workflow on a push-triggered path is NOT a successful scientific execution. There are NO verified new measured sidecar outcomes or noninterference results as of this report. Do not claim this step established true experimental pass/fail yet.

## Interpretation / next action
Find the workflow run triggered by `3957e22`, inspect jobs/conclusions, retrieve sidecar artifact and validate observed outcomes. On any failure, diagnose and correct only generated-E45 instrumentation/validator/workflow. E42/E4.6 frozen. Prior disjoint S2/S3 holdout p=.0625 (not significant) and exploratory mask×eta seed-level sign p=.125 remain unchanged. Next external trace-replay must be built from actual observed outcomes, not `pred[j]`, and will require independent assumptions beyond recomputing the same simulator's summary.
