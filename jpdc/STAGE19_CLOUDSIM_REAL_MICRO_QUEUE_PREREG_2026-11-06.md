# JPDC Stage19 — tiny genuine CloudSimPlus 8.5.7 VM scheduler experiment prereg, 2026-11-06

## Falsifiable hypothesis
Stage18 source audit found direct admission when an incoming Cloudlet has free PEs, with older queued tasks promoted during `updateProcessing`. Prior actual E45 S3 node14 10900/10901 inversion occurred with ~0.0001176ms between physical completion of 10898 and 10901 arrival. Test whether a 3-job single-VM original CloudSimPlus **event-driven** micro workload can reproduce bypass without CASPER policy code. This would strengthen mechanism understanding but not prove original event chronology.

## Before execution frozen fixtures
Single VM one PE, SpaceShared CloudletScheduler, CPU-only tasks 3 jobs (IDs 0,1,2) submitted on broker at known delays. Job 0 service target 8.099623ms; Job 1 service 4.730689ms, arrives 5.318920ms after Job0; Job 2 service 9.120283ms, arrives 8.0997406ms after Job0. These offsets approximate the previously observed node14 timing without claiming byte-identical original CloudSim service times. Default minimum simulation event interval 1e-6 seconds as E42. A *predeclared negative control* increases Job2's arrival delay after Job0 to 10.0ms (should usually allow queue advancement first); if no inversion in either fixture report negative, do not tune to force outcome.

## Setup and measured result
Compile original CloudSimPlus 8.5.7 dependency using same Maven project, write **new `org.casperiiot.jpdc.Stage19QueueMicro` standalone class**, no modification to E42, E4.6, E45 or CloudSim source. A passive subclass of SpaceShared logs scheduler submission BEFORE/AFTER: simulator clock, job ID, running/waiting cloudlet IDs. The actual processing outcome logs total execution and start wait for each job; determine observed start order using actual Cloudlet start-wait. Track if Job1 is waiting while Job2 enters execute. Run the two deterministic fixtures twice and compare machine-readable event logs byte-identically; if a run fails compile/API constraints, preserve failure, correct only engineering faults.

## Interpretation boundary
A successful 3-job bypass shows it is possible even without CASPER routing; a failure means this simple fixture is insufficient. Neither outcome verifies original upstream event cause or original strict-FCFS replay max-wait acceptance; it remains FAIL 9.1214009ms>5ms. No JPDC performance claim. All prior seed-level n remain unchanged.
