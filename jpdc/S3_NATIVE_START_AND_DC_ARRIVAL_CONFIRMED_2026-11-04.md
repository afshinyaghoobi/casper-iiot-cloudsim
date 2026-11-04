# JPDC S3 Queue Forensics — CloudSim native start and datacenter arrival, 2026-11-04

## Executive finding
With the **original preregistered queue replay FAIL preserved**, we independently verified two deeper stages on a frozen scientific simulator: (1) the native CloudSimPlus 8.5.7 `Cloudlet.getStartTime()` confirms the same unexpected 10900/10901 service-order inversion previously inferred from arrival+wait, and (2) the native `Cloudlet.getDcArrivalTime()` shows that the Cloudlets **arrived at the Datacenter in the original workload order**. Thus the inversion is not an artifact of using an inferred execution start, nor a late Datacenter arrival. It is localized *after datacenter arrival* to VM/cloudlet scheduling/event handling. We have **not** proven the precise internal mechanism (scheduler choice, event tie-break/quantization, pending request delivery, etc.).

## Immutable original performance gate
Original CloudSim ↔ independent Python FCFS run 41773297282: **FAIL**, max wait absolute error **9.12140093294972ms** vs preregistered acceptance <=5ms. Both policy traces had wait MAE **0.001719783725738875ms** and postshock mission deadline misses **90 actual vs90 replay**, but cannot call experiment fully passed. Original disjoint S2/S3 holdout p=.0625, exploratory mask×eta four-seed sign p=.125, both nonsignificant.

## New original source-backed observations
1. Native start experiment registered in `jpdc/S3_NATIVE_START_FORENSIC_PROTOCOL_2026-11-04.md` commit `5d9c58bb64027eb031833c7d7c32afb81840aa40`. Instrumentation `jpdc/instrument_native_start_generated_e45.py` commit `cf77a02e67b8e0d3dbc9aa53dff3cfe87d6404e0` and audit `jpdc/audit_native_start_forensic.py` commit `f45964a996219c0e056a70aecff28f9c3dcde624`. Real GitHub Actions workflow `.github/workflows/jpdc-s3-native-start-forensic-once.yml`, commit `e3f025334f7ba86d626dbc45918dfdfecc795f4f`; **Run 41775078177 SUCCESS**, original artifact **13296542533**. Original scientific control-vs-logger parity PASSED. Both CASPER_FULL and CASPER_HEALTH_STATIC show mapper order [10898,10899,10900,10901,10902]; native-start and derived-start orders [10898,10899,10901,10900,10902]. Native/derived start numeric differences for the two target tasks <=1.46e-11ms.

2. Datacenter-arrival question registered BEFORE second experiment in `jpdc/S3_DATACENTER_ARRIVAL_FORENSIC_PROTOCOL_2026-11-04.md` commit `0651bcbf5e1180724a72e17e230c4aece9d00794`. Generated-only logger `jpdc/instrument_dc_arrival_generated_e45.py`, commit `ffe4fbac82f9b4e29731f7054de2db151f5b9ba3`; auditor `jpdc/audit_dc_arrival_forensic.py`, commit `a35285100e9b7e56c45da00a1d88e9566fd58bb7`. Workflow `.github/workflows/jpdc-s3-dc-arrival-forensic-once.yml`, commit `ba266b7cf421ab75cbd461f19c924e60680d9d58`. **Run 41775318037 SUCCESS**, original artifact **13296393568**, both scientific control-vs-logger parity and stage audit PASS.

### Source-derived timing; seed index40, S3 HIGH, node14, both policies identical

| Clock (milliseconds) | task10900 | task10901 |
|---|---:|---:|
| Frozen workload arrival | 91360.8116306425 | 91363.59245000247 |
| CloudSim mapper invoked | 91360.8116306425 | 91363.59245000247 |
| **Cloudlet.getDcArrivalTime()** | **91360.8116306425** | **91363.59245000247** |
| **Cloudlet.getStartTime()** | **91372.713733334** | **91363.59245000247** |
| Cloudlet.getStartWaitTime(), ms | 11.902102691508 | 0 |
| Actual native start - DcArrival - Wait, ms | approximately -8.25e-12 | 0 |

All five source-selected tasks 10898–10902 have correct datacenter arrival order. Both policies have inverted native start order for exactly this pair in the five-task window. The native Cloudlet start and the previously derived start are not independent scientific replications: they are two API reads from the same CloudSim run semantics, but they clarify interpretation and rule out a mislabeled derived start.

The source code instantiates one VM with `CloudletSchedulerSpaceShared` per node. CloudSimPlus 8.5.7 Javadoc documents this as one Cloudlet per VM and a waiting list. This observation alone does not establish the precise order by which the Datacenter/VM internal cloudlet queue accepted or started task10900 versus task10901. A source-level investigation of event ordering or a tiny two-task CloudSim test is the *next falsifiable experiment*.

## Integrity and applicability
- Every new run used frozen E42 blob SHA `34256ca7bff46f911cf20e8b94278fbd09175746`; E4.6 unchanged.
- New experiments used generated E45 only and succeeded with exact eight-policy scientific parity apart from wall-clock mapper time.
- This is **mechanistic forensic** work on *one pre-identified pair* and seed 40; it does not validate CASPER scheduling improvement in a second independent simulator or add new confirmation of the research hypothesis.
- Continue to report original FCFS queue fidelity as **FAILED**; do not posthoc relax 5ms threshold or ignore task10900/10901.

## Original GitHub run links
- Native Cloudlet start success: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41775078177
- Datacenter-arrival success: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41775318037
- Original queue fidelity failure: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41773297282
