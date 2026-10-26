# S3 counterfactual candidate residual decomposition — three-seed pilot

Workflow: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/40412923871
All 3/3 jobs passed. Instrumented variant: jpdc/s3_residual_decomp_patch.py, no changes to CASPER selection or immutable E4.6.

For each *missing candidate bound* among all post-shock mission Top-3 families, passive counters record: hidden actual network increment relative to nominal, signed true-minus-predicted queue backlog, signed actual-minus-nominal service, eta at dispatch, and actual latency above its conformal upper bound.

|Seed|Candidate bound misses|Affected-node candidate misses|Network increment sum (ms)|Queue residual sum (ms)|Service residual sum (ms)|Eta sum|Upper-bound exceedance sum (ms)|
|---|---:|---:|---:|---:|---:|---:|---:|
|4202202600|310|310|4799.976903|0.622522|63.202680|885.390401|524.887162|
|4202202601|23|23|368.878842|33.929048|10.025976|56.146475|79.139424|
|4202202602|383|382|10254.820332|0.647413|96.296301|483.843154|3452.845283|
|Total|716|715|15423.676078|35.1990|169.524958|1425.380029|4056.871769|

The candidate-level mismatch count (716) is not a number of failing families (700 in prior three-seed family audit), because a single family can have multiple failing members.

**Interpretation:** Almost all failing candidates (715/716) belong to affected network nodes. The aggregate hidden network increment on failing candidates is much greater than net signed queue and service residuals, consistent with network degradation being the dominant model discrepancy in these pilot samples. This is **not** a causal variance decomposition, nor an additive attribution of final bound exceedance: the upper bound includes adaptive eta, calibrated quantiles, and sigma. Signed queue/service residuals can cancel. The eta average on failing candidates alone is selection-biased and does not describe the full adaptation time series. This pilot is not 30-seed evidence and does not show 99% coverage.

Next: full thirty-seed instrumentation, plus absolute queue/service residual summaries and eta by time window for stronger mechanistic analysis.
