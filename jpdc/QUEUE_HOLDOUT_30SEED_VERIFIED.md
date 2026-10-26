# Independent seed holdout: queue-weighted comparator vs CASPER

## Reproducibility
Experiment GitHub Actions run 40281748580: 30 of 30 successes, scientific seed indices 30..59 (scientific seeds 4202202630..4202202659), five scenarios, nine policies, 1350 records.
Paired statistical analysis run 40281798985: success, 20 paired comparisons with two separate Holm families (10 late DVR; 10 p99 latency).

The prior 30-seed model-development analysis used indices 0..29. There is no overlap in random seeds, although both runs use the same synthetic simulator and workload-generator family.

## Independent holdout late deadline violation rate
|Scenario|CASPER_FULL|PRED_GREEDY|QUEUE_AWARE_WEIGHTED_COMPLETION|Queue minus CASPER|Holm adjusted p versus CASPER|
|---|---:|---:|---:|---:|---:|
|S0 stationary|0.008400|0.008533|0.008400|0.000000|1.0|
|S1 double arrivals|0.022800|0.023333|0.021867|-0.000933|1.0|
|S2 hidden compute 40% loss|0.016267|0.028133|0.025867|+0.009600|0.0407792|
|S3 hidden network 50% loss|0.029067|0.028800|0.030667|+0.001600|1.0|
|S4 compound|0.058933|0.105333|0.103600|+0.044667|0.0007245|

At alpha 0.05 after Holm adjustment, the specified CASPER_FULL advantage for late DVR on S2 and S4 replicates on fully disjoint seeds. Difference at S1 favors queue weighting numerically but is not statistically significant; S0 equal, S3 unresolved.

Relative lower violation rates for CASPER compared to queue weighting: S2 (0.025867 - 0.016267)/0.025867 = 37.1%, S4 (0.103600 - 0.058933)/0.103600 = 43.1%. These are ratios of aggregated means, not seed-level inferential effect measures.

## Honest evidentiary scope
- The challenger is a documented exploratory queue-aware online scheduling heuristic, not a reproduced peer-reviewed state-of-the-art scheduler.
- This is a seed holdout independent of the model-selection sample, but **not independent external workload validation**. It cannot establish performance on real IIoT traces or alternate simulators.
- Empirical conformal family-wise coverage and deadline violation are different outcomes; the present analysis does not demonstrate nominal 99% coverage under S3.
- The full results file also provides p99 latency comparisons and confidence intervals; these must be consulted for quantitative latency claims.
- Original frozen E4.6 and the tag v1.0.0-casper-iiot-e46 remain unchanged.

## Publication-safe sentence
In a holdout experiment involving 30 previously unused simulator seeds, CASPER yielded lower late deadline violation rates than an explicitly specified queue-weighted online heuristic under hidden compute degradation (S2) and compound disruptions (S4). The differences persisted after Holm correction, but neither out-of-generator generalization nor robustness of nominal coverage under hidden network faults is established.
