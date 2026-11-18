# VERIFIED CI — Native CloudSimPlus v8.5.7 dynamic eligibility callback audit

**Date:** 2026-11-17 local / CI UTC 2026-11-18.
**Status:** ACTUAL NEW JAVA EXECUTION SUCCESS; A1 PARTIAL (eligibility observed; explicit waiting-promotion method callback not yet instrumented).
**Original run:** https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44214864810
**Source commit:** 79b0df4300690e94a675537d9f1a739de4947859
**Job:** 134502046272; **Artifact ID:** 14387108203
**Artifact ZIP SHA256 reported in GitHub Actions logs:** 75fa8603e8dc1690129866f0d0560f6c189adcaf90ef995e5ac5d5e7ad476b9a

## New actual code and experiment
New isolated Java NativeV857EligibilityCallbackTrace extends CloudletSchedulerSpaceShared and overrides canExecuteCloudletInternal, calling super exactly once and passively logging returned eligibility, native clock and WAIT/EXEC snapshot; also logs original submit/update path. Original unmodified NativeArrivalOffsetCounterfactual runs in same CI job for control. Maven CloudSimPlus 8.5.7 and Java17. Independent new parser audit_native_v857_dynamic_eligibility.py does not import old primary parser.

## Evidence from actual completed GitHub job logs and checks
- 6 actual native simulator scenarios with 18/18 Cloudlets FINISHED.
- 54 genuine dynamic eligibility-method callback observations; not merely static source scan.
- Original same-snapshot direct-submit bypass configurations ORIGINAL_5MS and LATE10_5MS reproduced; four others without detected bypass.
- New native trace byte identical on repeat; audit JSON byte identical on repeat.
- After filtering ONLY eligibility log rows and normalizing prefixes, new trace was byte-for-byte identical to an independently rerun original Java harness. This controls for observation perturbation in measured trace.
- Independent new eligibility audit and original baseline wait/queue parser both PASSED.
- Original FGCS E42 and rejected Stage64 Git blobs validated unchanged during CI.
- Original 30k Java/Python max waiting mismatch 9.12140093294972 ms > 5ms remains FAIL; original Stage65 independent policy safety remains FAIL.

## Interpretation and limits
New native Java instrumentation on SAME six fixed synthetic cases, not a new workload holdout or a scheduler-efficacy trial. A method-level eligibility callback is dynamically shown to execute, but a separate waiting-list promotion callback was NOT directly instrumented; 54 callbacks do not prove why the older job remains WAIT. EXEC membership is not hardware CPU start and this experiment does not establish a CloudSim library bug. Do not promote original CASPER or Stage65 results as successful.

## Provenance limitation
Connected GitHub Actions job, steps, stdout and artifact identity plus ZIP SHA reported by GitHub upload were inspected. The original ZIP was not independently downloaded, extracted and locally rehashed during this continuation, so no claim of independent ZIP rehash is made.

## Next
A1 PARTIAL: eligibility complete, waiting-promotion method dynamic trace still unresolved. A2 24-case bounded prospective synthetic generalization protocol frozen in JPDC_A2_BOUNDED_GENERALIZATION_PREREG_2026-11-17.md; A2 Java runs not yet executed. Highest priority now A2 native study / independent audit / manuscript. B next-paper research remains RESERVED.
