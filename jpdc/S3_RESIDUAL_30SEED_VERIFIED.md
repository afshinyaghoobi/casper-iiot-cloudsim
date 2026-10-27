# S3 residual decomposition — validated 30 seed findings

Experiment: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/40414189982 (30/30 successful).
Aggregation: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/40414300205 (successful).
Script: jpdc/analyze_s3_residual30.py. Frozen E4.6 is unchanged.

Across 90,123 candidate evaluations in post-shock S3 Top-3 CASPER_FULL families, 4,803 candidates violated their upper bound, 4,752 of which were on network-affected nodes (98.94% of *candidate* violations). These counts differ from 4,294 failed *families* previously audited: one family can contain multiple violations.

Summed over the 4,803 failing candidates:
- Actual minus nominal **network increase**: 108,429.389 ms.
- Signed queue residual: +554.334 ms; absolute queue residual: 697.270 ms.
- Signed service residual: +1,703.441 ms; absolute service residual: 3,776.874 ms.
- Total positive excess over upper conformal bound: 30,257.371 ms.
- Sum eta values at failing candidate evaluation: 11,243.458, which gives conditional mean eta 2.341, **not** an overall time-course estimate.

The hidden network increase is far larger than the signed or absolute queue/service residuals on this selected set, giving strong mechanistic evidence that S3 coverage failures primarily coincide with unmodeled network degradation. These are NOT a causal additive decomposition of bound exceedance, and conditioning on failing candidates induces selection bias. The 99% nominal family-wise coverage target remains unmet in S3; this analysis identifies a limitation and does not fix it.

Next analysis should measure network and queue errors on *all* post-shock candidates, not only misses, and eta over event-time windows to distinguish drift adaptation and selection effects. Published-baseline and out-of-generator validation are still needed for journal-level generalization.
