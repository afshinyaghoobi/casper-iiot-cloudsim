# S3 native Cloudlet datacenter-arrival forensic — protocol (2026-11-04)

## Source and prior truth
The original independently replayed FCFS mechanical test **FAILED** its preregistered max wait error: 9.12140093294972ms > 5ms (GitHub 41773297282). Real native start run 41775078177 independently verified that the native CloudSim getStartTime() ordering inverts task10900/10901 on node14 even though source arrivals and mapper event times are increasing; experiment 41775078177 PASSED its separate observational scientific parity and forensic gates.

## Fresh question, registered before measurement
Is native **Cloudlet.getDcArrivalTime()** for 10900 later than that of 10901, despite workload-source arrival and mapper times appearing in ascending task order? CloudSimPlus 8.5.7 documents getDcArrivalTime, getStartTime, getStartWaitTime separately. Additional datacenter-arrival timestamp is recorded at completion via public API, without changing broker, queue discipline, scheduling, or generated workload.

## Prespecified protocol and interpretation
- Same frozen scientific source `34256ca7bff46f911cf20e8b94278fbd09175746`, S3 HIGH mask [9,12,14,15,17,18], seed40, 80k calibration/30k tasks.
- Generate temporary E45 from E42; compare 8-policy scientific CSVs from uninstrumented control and triple-stage forensic instrumentation, excluding only mapper wall-clock timing.
- Record native Cloudlet start, Cloudlet datacenter arrival, workload arrival, mapper clock, observed wait for IDs 10898..10902, both policies.
- Audit exact per-stage identity and time cardinalities. Report: order by workload arrival, mapper clock, datacenter arrival and native start; numerical difference between native start minus datacenter arrival and getStartWaitTime; no automatic assumption they match.
- If datacenter arrival order differs from mapper, identify where the inversion first becomes visible. If not, mark deeper VM scheduler/event mechanism unresolved. Do not use recorded wait to predict wait; this study is diagnostic only. No posthoc exceptions or threshold changes.
- E42/E4.6 are immutable; original independent holdout p=.0625 and exploratory 4-seed factorial p=.125 nonsignificant; no independent scheduler implementation claimed.
