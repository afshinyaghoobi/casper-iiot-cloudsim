# JPDC S3 native VM scheduler submission forensic — registered before measurement, 2026-11-04

Prior independent Python FCFS mechanical fidelity gate **FAILED** in run 41773297282 (max observed wait error 9.12140093294972ms > prespecified 5ms); this result will remain FAILED regardless of any new diagnosis. Real native Cloudlet start and native Datacenter arrival runs 41775078177 and 41775318037 both succeeded and showed task 10900 before 10901 at mapper/DC arrival but *after* 10901 at native service start.

## Question
Do the Cloudlets reach `CloudletSchedulerSpaceShared.cloudletSubmit` on node14 in original task order (10900 then 10901) or reversed order? What are the VM scheduler's actual running and waiting Cloudlet ID lists **before and after** submissions? These events are more proximate to VM scheduling than native Datacenter arrival fields.

## Controlled design and objective
- Frozen E42 Git blob 34256ca7bff46f911cf20e8b94278fbd09175746, frozen E4.6 untouched. Generated E45 only, fixed S3 HIGH six-node mask [9,12,14,15,17,18], scientific seed index 40, 80000 calibration / 30000 deployment tasks.
- Compare an uninstrumented run with a targeted generated-E45-only observational subclass of SpaceShared. The subclass delegates to `super.cloudletSubmit` without altering method parameters, return, task priority, queues, or dispatch; logs BEFORE/AFTER scheduler acceptance, simulation clock, Cloudlet ID, VM ID, running/waiting IDs, and file transfer delay for Cloudlets 10898–10902.
- Scientific parity gate: exactly eight policies' CSV columns identical, except non-scientific wall-clock mapper timing.
- The logger must not infer task index from arbitrary Cloudlet ID without verifying correspondence; the workload's Cloudlets are created sequentially. Capture native start and original mapper for 10898–10902 in the same run, and compare scheduler submitted Cloudlet IDs to the original task index.
- If compilation fails because API does not permit this override, or the subclass has behavioral effects, report failure without changing frozen science.
- Do not claim `getDcArrivalTime()` proves the internal scheduler enqueue order; separate recorded native fields are distinct from real event callbacks.

## Falsifiability
- If submit order is 10901 before 10900: inversion exists at scheduler submission/event arrival; investigate broker/DC event dispatch. If 10900 is submitted first but starts later while queued: investigate queue admission and selection. If list snapshots cannot disambiguate, label unresolved and propose a smaller independent reproduction. No threshold changes.
- This is exploratory engineering diagnosis of a known outlier; it is NOT validation of CASPER in a second scheduling simulator, NOT an independent holdout, and NOT new seed-level efficacy evidence.
