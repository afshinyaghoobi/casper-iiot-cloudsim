# CASPER JPDC — Native SpaceShared scheduler admission bypass confirmed (2026-11-04)

## Direct result and scientific qualification

An additional **predeclared mechanism forensic** (not a new efficacy/holdout test) instrumented the protected `CloudletSchedulerAbstract.cloudletSubmitInternal(CloudletExecution,double)` on generated E45, by a passive subclass of `CloudletSchedulerSpaceShared`. The public `cloudletSubmit` method is `final` in CloudSim Plus 8.5.7; an initial probe run failed compilation before the hook was moved to the protected API. The unmodified 8-policy control and instrumented generated-E45 simulations were then compared under the same S3 HIGH mask, seed40, 80k calibration /30k deployment. **All scientific CSV columns matched exactly (excluding wall-clock `mean_mapper_us`).**

Predeclared protocol: `jpdc/S3_SCHEDULER_SUBMISSION_FORENSIC_PROTOCOL_2026-11-04.md`, commit `04e5621eda291b835fbcffe323bfce0707abba80`.
Original generated-only probe `jpdc/instrument_scheduler_submit_generated_e45.py`, later fixed to protected hook at commit `52f9ede4d70e121d27645283d4f5a30eb728637b`.
Reproducible strict diagnostic `jpdc/audit_scheduler_submit_forensic.py`, commit `b37fafbc5880be0ba4931798cdfce48fbdf636df`.
**Real successful GitHub Actions run 41777312914**, code commit `6a668a58e90872e5aadf600fc5734a1963d9762b`, raw artifact **13297158892**. The run printed both `JPDC_SCHEDULER_SUBMISSION_SCIENTIFIC_PARITY_PASS` and `JPDC_SCHEDULER_SUBMISSION_FORENSIC_AUDIT_PASS`.

## Exact queue states, node 14, both CASPER policies

| Event | Simulation time (ms) | Running cloudlet IDs | Waiting cloudlet IDs |
|---|---:|---|---|
| **BEFORE 10900 submit** | 91360.8116306425 | [10898] | [] |
| **AFTER 10900 submit** | 91360.8116306425 | [10898] | [10900] |
| **BEFORE 10901 submit** | 91363.59245000247 | [] | [10900] |
| **AFTER 10901 submit** | 91363.59245000247 | [10901] | [10900] |

Exactly the same four snapshots occurred in BOTH `CASPER_FULL` and `CASPER_HEALTH_STATIC`. In this trace, `10900` was submitted earlier to the SpaceShared scheduler and queued behind running `10898`; when `10901` was submitted, the execution list had become empty but `10900` was still waiting; `10901` was admitted directly into execution ahead of `10900`.

Thus the earlier discovered 10900/10901 inversion **is now directly observed at SpaceShared scheduler admission**, not merely inferred from a latency calculation, workload timestamps, mapper timestamps, datacenter-arrival timestamps or Cloudlet native start timestamps. This is a **waiting-queue bypass by a newly submitted Cloudlet when a PE is free but an older Cloudlet remains in the waiting list** in this concrete CloudSim Plus 8.5.7 execution. It does **not** identify why the older task remained waiting after 10898 completed (possibly scheduling/update-event mechanics); that separate upstream scheduler timing mechanism has not been proven.

## Original preregistration and outcome must remain unchanged

The original independent Python strict chronological-FCFS mechanical test **FAILED** in run 41773297282: maximum absolute wait error **9.12140093294972 ms**, against the **pre-registered 5 ms limit**. This new queue snapshot explains why the strict chronological-FCFS abstraction is not fully equivalent to this CloudSim execution; it does **not** magically pass the old test or justify silently excluding two task outliers. Prior observed mean absolute wait error 0.001719783725738875ms, two >1ms discrepancies among 30000 tasks per policy, and 90 postshock mission deadline misses in both original and independent replay remain valid *descriptive* outputs.

This diagnosis is **not a new independent CASPER scheduler implementation** and is not proof of performance superiority or wider simulator portability. The two policies show the same bypass. Holdout p=.0625 and four-seed exploratory sign p=.125 are still nonsignificant. E42/E4.6 unchanged: frozen E42 Git blob `34256ca7bff46f911cf20e8b94278fbd09175746`.

## Scientific next action
1. Preserve the original strict FCFS fidelity FAIL as the primary reported result.
2. If useful, add an explicitly separate follow-up *mechanism* micro-reproduction of the waiting-queue bypass under CloudSimPlus 8.5.7, and/or observe the scheduler's completion/update event at the point where 10898 frees CPU but 10900 stays waiting. Do not claim all SpaceShared scheduling is non-FCFS or a general bug without broader tests.
3. A second independent CASPER scheduling implementation remains a separate pending research step; queue mechanic forensics alone cannot substitute for it.

Run: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41777312914
Artifact: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41777312914/artifacts/13297158892
