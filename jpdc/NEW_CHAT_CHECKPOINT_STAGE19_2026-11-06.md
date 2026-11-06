# JPDC continuation checkpoint after Stage18/Stage19, 2026-11-06

## Actual new verified runs
Stage18 original exact CloudSimPlus 8.5.7 sources [42232194179](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42232194179), pass, archived-only code-path check [42232445025](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42232445025), pass. Original Maven source archive SHA256 8d3efcacfc661b2f1e018e279761fc4ae1e5584a770b2022d20930568688966c. Abstract cloudletSubmitInternal lines247–258 admits incoming cloudlet when canExecuteCloudlet; SpaceShared canExecuteCloudletInternal lines95–98 checks free PEs. Queued jobs promoted separately by Abstract updateProcessing lines477–494 calling moveNextCloudletsFromWaitingToExecList lines910–923. These split paths are consistent with actual earlier node14 10900/10901 waiting-list bypass; precise event-level chronology remains unresolved. Full Stage18 report `STAGE18_CLOUDSIM_857_SOURCE_PATH_VERIFIED_2026-11-06.md`.

Stage19 genuine independent Java microfixture with original CloudSimPlus simulator [42232972792](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42232972792) pass engineering/twin byte reproducibility; archive-only validity audit [42233244383](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42233244383) pass. Neither preregistered near-gap nor late control reproduced waiting-list bypass, because first cloudlet remained RUNNING when third submitted. Intended first physical service8.099623ms; native reported total execution18.100623ms. Thus no free-PE+older-waiter interval and this is NOT a legitimate negative falsification of Stage18 mechanism. Full `STAGE19_NATIVE_CLOUDSIM_MICRO_NO_BYPASS_PRECONDITION_VERIFIED_2026-11-06.md`.

## Never misstate original scientific results
- Original E42 blob SHA34256ca7bff46f911cf20e8b94278fbd09175746 and E4.6 unchanged.
- Original Python chronological strict-FCFS vs Java SpaceShared independent queue max absolute wait error9.12140093294972ms exceeds 5ms registered limit: **FAIL**, run41773297282. This is unresolved cross-runtime physics mismatch.
- Actual original generated-E45 30k-task native queue bypass directly observed run41777312914, no assumption needed to claim the specific observation.
- Stage16 eight-seed S3 guarded minus FULL mean -1 MISSION miss/seed, predeclared sign p=.375; no statistically reliable superiority. S2 tends harm. Stage17 probing ablation two development seeds86/87: zero change MISSION misses, no proof of all-scenario null effect. Neither CASPER Stage15/17 algorithm is validated novelty or new JPDC acceptance claim.

## Next precise work
Before setting next microfixture arrival times, instrument CloudSimPlus native task finish callback and VM queue processing update timing to explain target8.099623 vs reported18.100623ms. Preregister exact tests; distinguish service demand vs Cloudlet reported execution accounting. Do not brute-force timings or select reproductions. Then establish independent simulator model domain; in parallel develop theoretically distinct hard-deadline queue-aware scheduling objective with competitive published baselines. Retain negative and non-significant findings.

## Strategic request
User wants JPDC journal-first, no CCGrid paper splitting, no rush; scientific quality and full continuity matter most.
