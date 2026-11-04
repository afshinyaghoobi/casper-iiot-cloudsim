# CASPER JPDC — independent queue mismatch forensic: source-verified stages (2026-11-04)

## Verified evidence and provenance

Original independent queue run **41773297282** (commit `2f72013e96724d62999112de445c557124d29cfc`) completed **FAILURE** under the original preregistered maximum wait error bound: **9.12140093294972 ms**, upper threshold **5 ms**, despite mean wait MAE **0.001719783725738875 ms** and perfect agreement in **90** postshock mission deadline misses for each of the two CASPER policies. This original outcome remains **FAILED**. Real original artifact: `13296215627`.

An event-stage forensic logger was added to *generated E45 only* (no frozen E42 or E4.6 modifications), targeting tasks 10898–10902. Protocol was registered in `jpdc/S3_NODE14_EVENT_ORDER_FORENSIC_PROTOCOL_2026-11-04.md` before the experimental run. The first two forensic attempts failed because the installed CloudSimPlus version did not expose `Cloudlet.getExecStartTime()`; this was removed. The repaired real CloudSim forensic run **41774034113**, commit `c10b5aa0447e2b36932aeb13d9d405350eb88e1c`, completed Java builds and both scientific executions and **PASSED** exact 8-policy scientific CSV noninterference, but the initial audit incorrectly expected 8 arrival-source events per task. The original artifact is `13296057807`.

Analysis of this artifact established **9 E45ArrivalSource event records per selected task**: **one calibration phase + eight deployment-policy phases**. The audit was corrected to distinguish the calibration arrival timestamp from deployment timestamps and require the eight matching deployment arrivals to have source event clock equal to their frozen planned arrival timestamp, then cross-check mapper and finish records.

### Successfully repeated exact committed auditor in GitHub Actions

The artifact-only workflow `.github/workflows/jpdc-node14-forensic-artifact-audit.yml` on commit **`c3b54fd89edd56c4ffa84cf3d2982702771f8bbc`**, Actions run **41774360581**, job `126391125803`, completed **SUCCESS**. It downloaded the exact original forensic artifact `13296057807`, executed `jpdc/audit_node14_event_order_forensic.py` without rerunning CloudSim, printed `JPDC_FORENSIC_STAGE_AUDIT_PASS`, and uploaded audit artifact **`13296312446`**.

## Confirmed chronological findings

Seed 4202202640, S3 HIGH damaged-node mask [9,12,14,15,17,18], node14, both `CASPER_FULL` and `CASPER_HEALTH_STATIC`:

| Event clock / time (ms) | task 10900 | task 10901 |
|---|---:|---:|
| Source planned arrival | 91360.8116306425 | 91363.59245000247 |
| E45ArrivalSource event clock | 91360.8116306425 | 91363.59245000247 |
| E45 mapper invocation clock | 91360.8116306425 | 91363.59245000247 |
| **Derived start**: planned arrival + CloudSim recorded wait | 91372.71373333402 | 91363.59245000247 |
| CloudSim recorded wait (ms) | 11.902102691508 | 0 |

The derived start above is NOT an independent Cloudlet native start event: the installed CloudSimPlus `Cloudlet` interface lacks the requested getter. The forensic record uses observed wait for diagnosis **only**, not for rerunning independent FCFS predictions.

Within each policy the complete five-task ordering is:
- Planned arrival and mapper clock: `10898,10899,10900,10901,10902`;
- Derived service-start order: `10898,10899,10901,10900,10902`.

Thus the task-order inversion arises **after** the source arrival and mapper invocation, not from timestamps delivered late to the mapper. It could result from CloudSim broker-to-VM event delivery and/or cloudlet scheduler enqueue behavior, but that specific mechanism has **not yet been traced independently or proven**. Both policies have identical event timing, ruling out policy-specific selection differences as the direct explanation in this pair. One inversion is visible per policy, matching the earlier independent replay discrepancy.

## Scientific interpretation and next step

- The *forensic audit* passed in real GitHub CI, and observational logging was noninterfering on the recorded scientific summary fields.
- The *original independent FCFS fidelity experiment* still **FAILED** the registered maximum wait criterion (9.1214 > 5 ms); a better root-cause hypothesis cannot change that decision.
- This is a comparison of fixed policy routes and queue mechanics, **not** independent implementation or external proof of the CASPER scheduler's efficacy. No inference from 30000 tasks as independent seed-level replications.
- For causal mechanism confirmation, instrument generated-only broker submit/VM queue enqueue ordering or create a tiny standalone CloudSim event schedule reproduction around two task arrivals. No posthoc change to the registered fidelity threshold; preserve E42/E4.6.
- Disjoint preregistered S2/S3 holdout `p=.0625`, and 4-seed exploratory factorial sign `p=.125`, remain non-significant.

## Links

- Original failed fidelity: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41773297282
- Real forensic CloudSim run: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41774034113
- **Successful artifact audit**: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41774360581
- Original forensic raw artifact ID: 13296057807
- Verified auditor output artifact ID: 13296312446
