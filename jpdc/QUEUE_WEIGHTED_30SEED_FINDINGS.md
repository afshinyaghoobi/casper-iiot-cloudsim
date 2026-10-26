# JPDC Queue-aware challenger: completed 30-seed paired experiment

## Provenance and status
- Experiment: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/40280807901 — 30/30 successful.
- Statistics: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/40280910310 — successful, 1350 rows, 30 seeds, 20 paired comparisons.
- The exploratory challenger QUEUE_AWARE_WEIGHTED_COMPLETION minimizes nominal network + nominal service + 2 x estimated backlog. Weight 2 was set before its three-seed pilot; this work is not reproduction of a published state-of-the-art method.
- Frozen E4.6 remains unchanged.

## Verified thirty-seed mean late deadline violation rate (fractions)
|Scenario|CASPER_FULL|PRED_GREEDY|QUEUE_AWARE_WEIGHTED_COMPLETION|Queue minus CASPER|Holm-adjusted p (vs CASPER)|
|---|---:|---:|---:|---:|---:|
|S0 stationary|0.006933|0.006933|0.007067|+0.000133|1.0000000|
|S1 lambda x2|0.020800|0.020400|0.016933|-0.003867|0.0678241|
|S2 hidden compute 40% loss|0.016533|0.031733|0.026533|+0.010000|0.0075197|
|S3 hidden network 50% loss|0.034400|0.034267|0.034933|+0.000533|1.0000000|
|S4 compound|0.048800|0.096400|0.090267|+0.041467|0.0003216|

All percentages represent proportions; a positive queue-minus-CASPER late DVR favors CASPER. Significance determined using paired t tests and Holm within the ten late-DVR comparisons (5 scenarios x 2 references). There are another ten comparisons for P99 latency in their separate Holm family; download machine-readable results for precise P99 data and confidence intervals, rather than inferring from DVR.

## Interpretation
CASPER shows lower late DVR than the queue-weighted challenger on S2 and S4, with Holm-adjusted p<0.05. This provides stronger within-generator evidence for benefit under these synthetic disruption scenarios. S1's lower average DVR for queue weighting is not statistically significant after correction. S0 and S3 are statistically unresolved. Against PRED_GREEDY, all five queue-policy late-DVR differences have adjusted p>=0.05 (minimum approximately 0.0678), so this experiment does not validate superiority of the queue policy over greedy.

## Limits, validity, and publication guardrails
- The queue comparator is an exploratory homegrown policy, not state of the art. Evidence supports only performance relative to this specified comparator, not all published schedulers.
- The challenger was chosen for scaling after reviewing a favorable three-seed pilot; 30-seed results overlap with those pilot seeds. The full study is therefore exploratory/model-development evidence, not a statistically independent confirmation of the pilot. Reserve new independent seeds or workload traces for confirmatory claims.
- All methods use the same synthetic generator and broad simulator conditions; this is not out-of-distribution external validation.
- Deadline violation and conformal family-wise coverage are different constructs. A lower DVR does not establish reliable 99% coverage, and the hidden-network S3 scenario continues to pose a serious coverage concern.
- No claim on computational overhead is justified without a controlled timing measurement.
- Test reproducibility artifacts, comparator implementation correctness, and stressor semantics before journal submission.

## Next experiment recommendation
Add holdout scientific seeds disjoint from 0..29, with strict pre-declared comparisons CASPER vs queue-weighted challenger on S2 and S4, plus explicit S3 coverage assessment. This would reduce pilot-informed selection bias, though it would still use the same synthetic generator. Then seek a literature-faithful strong scheduler and independently generated workloads.
