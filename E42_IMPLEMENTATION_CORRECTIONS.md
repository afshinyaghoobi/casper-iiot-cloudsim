# E4.2 Implementation Corrections Before Publication Results

The E4.2 scientific protocol was locked before any publication-scale result was opened. Two preflight-only implementation corrections were made before the 30-seed campaign.

1. **CloudSim Plus 8.5.7 API compatibility and metric provenance.** Deprecated/removed Cloudlet methods were replaced by the current API (`getFinishTime()-getStartTime()` for executed service duration and `getStartWaitTime()` for queue wait). Mission records are summarized in task-arrival order, the reported E1.7 eta is the value used at dispatch rather than the post-outcome value, and a health alarm counts as a true positive only for an actually compute-degraded node. No scientific CASPER parameter changed.

2. **CloudSim event resolution.** The default CloudSim minimum event interval is too coarse for the locked 40–120 ms Mission deadline regime and short edge/fog service times. Both calibration and deployment therefore construct `CloudSimPlus(0.0001)`, i.e. a 0.1 ms numerical event resolution. This is a simulator precision setting, not a scheduler, conformal, detector, probing, workload, or shift parameter. It was selected before publication results to make the numerical resolution comfortably smaller than the locked 2 ms CloudSim service-parity tolerance and the 50 ms telemetry period.

The failed preflight runs are retained in GitHub Actions for provenance. They are not publication results and were not used to choose CASPER thresholds, windows, risk levels, probing rates, or any other scientific parameter. After preflight passes, no result-driven retuning is permitted.
