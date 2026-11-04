# JPDC 2026-11-04: verified VM SpaceShared queue bypass and repaired manuscript CI gate

## 1. New native scheduler mechanism observation — real Actions PASS

- Registered targeted experiment before running: `jpdc/S3_SCHEDULER_SUBMISSION_FORENSIC_PROTOCOL_2026-11-04.md`, commit `04e5621eda291b835fbcffe323bfce0707abba80`.
- Diagnostic only, generated-E45-only passive subclass of SpaceShared: `jpdc/instrument_scheduler_submit_generated_e45.py`, latest fix `52f9ede4d70e121d27645283d4f5a30eb728637b`. CloudSimPlus 8.5.7 `cloudletSubmit` is final; protected `cloudletSubmitInternal(CloudletExecution,double)` was the validated supported hook.
- Original frozen E42 blob `34256ca7bff46f911cf20e8b94278fbd09175746` and E4.6 unchanged.
- Actual workflow `.github/workflows/jpdc-s3-scheduler-submission-forensic-once.yml`, source commit `6a668a58e90872e5aadf600fc5734a1963d9762b`: **run 41777312914 SUCCESS**, artifact **13297158892**. Frozen 8-policy scientific CSV parity PASS, strict scheduler snapshot auditor PASS.

### Original CloudSim real queue snapshots, node14

Both CASPER_FULL and CASPER_HEALTH_STATIC showed exact same transitions:

| S3 scientific event | time (ms) | executing | waiting |
|---|---:|---|---|
| before 10900 submitted | 91360.8116306425 | [10898] | [] |
| after 10900 submitted | 91360.8116306425 | [10898] | [10900] |
| before 10901 submitted | 91363.59245000247 | [] | [10900] |
| after 10901 submitted | 91363.59245000247 | [10901] | [10900] |

Source code for native scheduler probe logs BEFORE/AFTER and calls `super.cloudletSubmitInternal`, preserving the inherited scheduler logic. These records directly demonstrate **a newly submitted Cloudlet overtaking an already-waiting Cloudlet** at one concrete VM event. The source/mapper/native Datacenter-arrival timestamps of 10900 precede those of 10901; native start timestamps are reversed, so the simulator's actual handling of already-waiting tasks, NOT policy routing, explains the disagreement with strict chronological-FCFS independent replay in this pair.

**Limit:** The detailed reason why the old queued task 10900 was not promoted to the execution list before 10901 admission remains unverified (possible VM processing update/event order behavior). This is not evidence that all SpaceShared scheduling is unfair or non-FCFS across all workloads.

**Original registered fidelity remains FAILED.** Run 41773297282 had maximum wait error 9.12140093294972 ms vs predefined <=5ms. No exclusions or retroactive threshold changes. It had low MAE 0.001719783725738875 ms, and 90 postshock mission misses each in CloudSim/Python; not an independent CASPER scheduling efficacy replication.

Additional original detailed report: `jpdc/S3_VM_SCHEDULER_QUEUE_BYPASS_CONFIRMED_2026-11-04.md` commit `1a0e9994c792cf43b62ec9cb65c81c07a55d913a`.
Source trace ZIP: artifact `13297158892`, https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41777312914.

## 2. Long-standing JPDC manuscript arithmetic CI failure — fixed without scientific data changes

Multiple previous executions of `.github/workflows/jpdc-manuscript-numeric-audit.yml` failed because `jpdc/audit_integrated_manuscript_numbers.py` used a broad text-prefix match for the row `False certifications`, unintentionally matching the distinct, valid secondary metric `False certifications among issued certificates`. The table contained both legitimate rows. This was a **test parser false positive**, NOT an incorrect number in the manuscript.

Fixed the audit script to select exact first-column metric labels while still requiring exactly one row and all previous numerator, denominator and cross-document checks: commit `57e730187b6b611d00a08b966c14468028002704`. NO scientific CSV or paper values changed. **Real CI workflow run 41777654256 SUCCESS**, markers `PASS holdout count and denominator` for all metrics and `PASS: manuscript aggregate transcription and arithmetic audit complete`. Report explicitly flags a harmless display-rounding issue: source high-low mean delta 12.8731ms derived from unrounded data versus rounded displayed figures 12.8730ms; do not claim extra precision without raw artifact.

This is numerical *transcription* validation, not a replay of raw experiments.

## Research boundary and next steps

- E42/E4.6 frozen, no new CASPER policy code change or independent second-simulator scheduling confirmation.
- Disjoint confirmatory S2/S3 holdout exact sign p=.0625 and exploratory four-seed factorial p=.125 both nonsignificant; no p-hacking.
- Next: isolate when CloudSimPlus 8.5.7 scheduler moves waiting tasks into execution when a prior task finishes, via a separate diagnostic microtest or updateProcessing trace, not a posthoc workaround or altered main fidelity gate. Then return to independent policy-level validation for JPDC.

## Real executions

- VM queue forensic PASS: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41777312914
- Manuscript arithmetic audit PASS: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41777654256
- Original strict independent FCFS failure: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41773297282
