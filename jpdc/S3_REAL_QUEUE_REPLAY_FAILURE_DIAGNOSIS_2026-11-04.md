# JPDC S3 CloudSim→Python queue fidelity: observed real run and FAIL diagnosis — 2026-11-04

## Real evidence and provenance
Received the user's actual GitHub Actions run link **41767491200** (original SHA `c46ad3821e838df4898de8e6b7bc6996b6a0e5c8`). Job `126369215800` completed **failure** because the original queue replay rejected valid criticality `HIGH`. The *real* run nevertheless passed frozen source integrity, Java compile and simulation, scientific noninterference with versus without instrumentation, and independent task-outcome reconciliation for both policies. Original artifact `13292194678`.

Confirmed latest branch code had already fixed `HIGH` acceptance (commit `3463c934aa188ec2823a7c2784e057e5a4114cf8`). Added an explicit three-criticality gate to the preregistered workflow (without weakening any numerical acceptance thresholds), commit **`2f72013e96724d62999112de445c557124d29cfc`**, which triggered *new* workflow **41773297282**, job `126387741678`. This run completed **failure** in the original prespecified MAX-error gate, after complete scientific simulation and task trace validation. Original artifact **`13296215627`**, SHA256 of GitHub archive `25a49a511627fe31526d55bcb4fbef0047775660db0fb5dc10a93e06cab86b3b`; downloaded and inspected the actual instrumented log and eight-policy CSV.

## Preregistered independent queue acceptance results, seed40 HIGH
| Gate | CASPER_FULL | CASPER_HEALTH_STATIC | Registered target | Result |
|---|---:|---:|---:|---|
| Python/CloudSim observed WAIT MAE (ms) | 0.00171978372574 | 0.00171978372574 | <=1 | PASS |
| Maximum absolute WAIT error (ms) | 9.12140093295 | 9.12140093295 | <=5 | **FAIL** |
| Postshock MISSION actual deadline misses | 90 | 90 | identical to replay | PASS |
| Postshock MISSION replayed deadline misses | 90 | 90 | identical to actual | PASS |
| Task count | 30000 | 30000 | exactly 30000 | PASS |
| Tasks with absolute wait error >1 ms | 2 | 2 | descriptive | 2 |

Also **PASS**: all 8 policies' scientific CSV columns identical for instrumented and uninstrumented run except `mean_mapper_us`; source E42 frozen SHA `34256ca7bff46f911cf20e8b94278fbd09175746`; observed actual MISSION outcome vs official CSV (1545 mission tasks total, 1031 post-shock, 250 late) for both policies. No E42/E4.6 changes.

## Original task-level root-cause diagnosis
Parsed every `JPDC_QUEUE_REPLAY` record in the original archived `instrumented.log`. Compared task-arrival order with **observed start order** (arrival + CloudSim recorded wait) within each of 21 nodes. Exactly ONE order inversion was identified in **each** policy across 30,000 tasks: node 14 tasks **10900 and 10901** swapped service start order. All other tasks retained their per-node arrival rank.

- Task 10898: arrival 91355.4927097819 ms, service 8.099622619170 ms, actual finish 91363.59233240107 ms.
- Task **10900** (NORMAL): arrival **91360.8116306425 ms**, realized service **4.730689013229 ms**, CloudSim wait **11.902102691508 ms**; observed start **91372.7137333340 ms**. Independent FCFS wait (from arrival order) **2.780701758558 ms**; abs error **9.12140093295 ms**.
- Task **10901** (NORMAL): arrival **91363.59245000247 ms**, service **9.120283331541 ms**, CloudSim wait **0**; actual start **91363.59245000247 ms** and finish **91372.71273333402 ms**. Independent FCFS replay wait **4.730571411827 ms**.
- Task 10902: arrival 91364.69534818656, CloudSim wait 12.750074160678, consistent with execution after 10900. The apparent inversion is about the two preceding tasks.
- These results and the error pattern are IDENTICAL for CASPER_FULL and CASPER_HEALTH_STATIC, so this is not a difference in CASPER selection decisions. Underlying Java/CloudSim event scheduling or VM submission-order details are a **hypothesis**, not yet independently proved as the cause.

This result strongly indicates that simple strict per-node arrival-order FCFS is an imperfect approximation to the observed CloudSim scheduling semantics at one event boundary. It does NOT justify fitting a posthoc exception or pretending the prespecified max 5ms criterion was passed. An alternative observed-start-order replay would be circular if using observed queue waits to predict them.

## Scientific interpretation
- **The registered mechanical fidelity test FAILED** at the max error gate despite exceptionally low average wait error and exactly matching postshock deadline miss counts. Do not rename the result as overall PASS.
- This tests *queue mechanics conditional on original CASPER-chosen nodes and realized service times*, **NOT a second independent CASPER scheduler implementation**.
- Task count 30k is not independent replication; here n=1 seed and two policy traces sharing nearly identical routes/outputs.
- Registered S2/S3 10-seed holdout p=.0625 and exploratory four-seed factorial p=.125 unchanged, nonsignificant.
- Actionable next independent research: inspect CloudSim event order and scheduler queue behavior on the pair, possibly add a *separate, prespecified* dispatch/submission/event-order logger to generated E45; do NOT alter frozen E42/E4.6 and do NOT retroactively relax original thresholds.

## Reproduction
- GitHub workflow `.github/workflows/jpdc-s3-independent-queue-replay-once.yml`, newly triggered from commit `2f72013e96724d62999112de445c557124d29cfc`.
- Real run `https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41773297282`, artifact `13296215627`.
- Diagnostic-only script `jpdc/diagnose_queue_start_order_inversions.py`, commit `fd336d1d7911f5cde2ec2846ba1ebe95a262dfe9`. This script uses observed wait solely to diagnose actual observed order, not to derive the independent replay wait predictions.
