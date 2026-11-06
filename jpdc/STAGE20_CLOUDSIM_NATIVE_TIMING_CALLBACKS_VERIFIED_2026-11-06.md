# JPDC Stage20 — native CloudSimPlus 8.5.7 execution timing / scheduler callbacks VERIFIED (2026-11-06)

## Provenance and immutable outcome
Pre-results protocol `jpdc/STAGE20_NATIVE_TIMING_ACCOUNTING_PREREG_2026-11-06.md`, commit `996b4827592762ea53ba6f6a72db28b45c48a8e8`. Stage20 implements separate Java `org.casperiiot.jpdc.Stage20TimingAudit` with passive `CloudletSchedulerSpaceShared.updateProcessing(currentTime,MipsShare)` BEFORE/AFTER event-list snapshots, `cloudletSubmitInternal` pre/post snapshots and `Cloudlet.addOnFinishListener` clock records. Original Stage19, original E42 frozen source blob 34256ca7bff46f911cf20e8b94278fbd09175746, original E4.6, and original library/dependency remained unchanged.

[Real successful Stage20 CI 42234742284](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42234742284): Java compile PASS, full scientific submit-snapshot and finish-wait/service outcome identity **against original saved Stage19 artifact 42232972792** PASS, complete Stage20 trace byte-identical on two runs PASS, machine-readable audit `JPDC_STAGE20_ORIGINAL_NATIVE_TIMING_PARITY_PASS` and `JPDC_STAGE20_NATIVE_TIMING_BYTE_IDENTICAL_PASS`.

## Audited real numbers, not intended values
Two frozen microfixture cases:
- `NEAR_ORIGINAL_EVENT_GAP`: intended first MI/MIPS service 8.099623ms, first native `getTotalExecutionTime()` **18.100623ms**, difference **10.001ms**, first native `getStartWaitTime()` 0, finish callback simulation time **1018.101623ms**, third cloudlet VM submit **1008.1007406ms**.
- `LATE_AFTER_COMPLETION_CONTROL`: same intended first service 8.099623ms, native execution **18.100623ms**, difference 10.001ms, finish callback **1018.101623ms**, third submit **1010.001ms**.
- Both have **16** update-before/after events, eight distinct update clocks: `0.0`, `1008.100623`, `1018.101623`, `1028.102623`, `1038.103623`, `1048.104623`, `1058.105623`, `1068.106623` ms.
- During both third submissions the first cloudlet is still in execution and the second is waiting. Thus **the necessary free-PE/older-waiting bypass state is absent** in the original Stage19 case; no valid test of queue-bypass possibility occurred.

## Interpretation and limits
The exact 10.001ms surplus of *reported total execution time* relative to service demand and 10.001ms inter-update spacing strongly suggest CloudSimPlus event-processing time discretization / update scheduling is crucial to original microfixture timing. This is a descriptive empirical relationship, **not yet proven causal source-level formula**. No measurement proves CPU length, VM start time, or network modeled improperly; further library internal code inspection and one predeclared timing-boundary variation may isolate source cause. Don't attribute the whole difference to a general library bug, 10ms default, or a specific scheduling interval without tracing that path.

This Stage20 static + native event study **does not** establish a general SpaceShared inversion, doesn't reproduce original task10900/10901, cannot make strict FCFS replay pass, and is not independent JPDC algorithm validation. Original preregistered independent Python-FCFS versus Java SpaceShared max wait discrepancy remains **FAIL 9.12140093294972ms >5ms** (real run 41773297282). Original E45 generated 30k-task direct bypass remains observed (real 41777312914). Stage16 guarded S3 eight-seed sign p=.375 and S2 adverse directional result unchanged. Stage17 active probing ablation two dev seeds showed no MISSION miss-count differences; no general proof of zero effect.

## Next scientifically distinct work
- Stage21: inspect CloudSimPlus 8.5.7 exact library sources for VM/datacenter cloudlet update timing, including why update `1008.100623ms` precedes actual completion `1018.101623ms` and why next updates are spaced exactly 10.001ms. Pre-register before new experiment; do not tune arrival times based on observed result or retroactively call Stage19 a bypass.
- Parallel paper priorities: seek independent scheduling novelty rather than accumulated forensic-stage count; cross-domain validator/model semantics and rigorously relevant strong baselines remain submission blockers.
