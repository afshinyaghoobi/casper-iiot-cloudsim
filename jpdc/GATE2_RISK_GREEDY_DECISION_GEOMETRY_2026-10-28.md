# Gate 2: risk-greedy decision geometry, executed 2026-10-28

## Source model
The current Java `fixedSigma(pred,mult) = (3 + 0.10 * pred) * mult`. Node multipliers in `makeNodes` are 1.10 (12 edge), 1.00 (6 intermediate) and 0.90 (6 cloud). The experimental score is `pred + fixedSigma(pred,mult)` with lambda 1.0; legacy `PRED_GREEDY` ranks by `pred`.

## Formal identity within a tier
For fixed multiplier s, risk score `(1+0.1s)*pred + 3s` is strictly increasing in `pred` since `s>0`. Thus pairwise rankings **cannot reverse within the same tier**, independent of predicted latency distribution.

## Executed synthetic exhaustive enumeration
`python3 jpdc/test_risk_greedy_decision_geometry.py` returned:
```
SAME_TIER_INVERSION 0 / 30000
CROSS_TIER_INVERSION 268 / 60000
FIRST_CONSTRUCTIVE_INVERSION (1.1, 1.0, 81, 82, 93.21000000000001, 93.2)
RISK_GREEDY_DECISION_GEOMETRY_PASS
```
All ordered pairs of multiplier tiers and predicted latencies in {1,...,100} were enumerated. Only *strict ranking reversals* were counted; tie changes were excluded. The cross-tier 268 / 60000 = 0.4467% is a property of **this arbitrary regular synthetic grid**, not a measured workload frequency, a probability of improvement or a CloudSim statistic.

## Research decision
The risk-penalty comparator currently offers a narrow form of differentiation from `PRED_GREEDY`: its main effect is reweighting between node tiers. It is therefore more defensible as a **tier preference / uncertainty-weight sensitivity control** than as evidence of a genuinely independent robust scheduler.

Next valid empirical step: obtain actual completed pilot artifact, measure how often assignments disagree between policies on matched arrivals and whether group-specific late DVR and latency trade-offs improve. Aggregate CSV alone can show performance differences, but not assignment-disagreement rates; that requires passive decision logging or a controlled instrumented rerun. Do not relabel this synthetic finding as an observed assignment rate.

Frozen E4.6 unchanged. No SOTA, nominal coverage, generalization or statistical superiority claim.
