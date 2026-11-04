# JPDC native eight-policy parity expansion — development protocol, 2026-11-04

Registered BEFORE the first 8-policy test. Frozen E42 git blob 34256ca7bff46f911cf20e8b94278fbd09175746 and E4.6 are untouched. Existing 3-policy native Stage4 41908306200 SUCCESS. This is a **known development-seed** mechanistic extension, NOT a confirmatory holdout or YAFS equivalence.

## Fixed eight policies and semantics
Implement all exact frozen E42 policy flags:
- CLOUD_ONLY: no CP, no ranked, no adaptation, no health, eligible nodes 18..20.
- EDGE_FIRST: no CP, no ranked, no adaptation, no health, eligible nodes 0..11.
- PRED_GREEDY: no CP/rank/adaptation/health, all nodes.
- GLOBAL_CP: CP=true, ranked=false, adaptive=false, health=false, qGlobal for all top3.
- RANKED_CP_STATIC: CP=true, ranked=true, adaptive=false, health=false, qRank[p].
- CASPER_ADAPT_NO_HEALTH: CP=true, ranked=true, adaptive=true, health=false.
- CASPER_HEALTH_STATIC: CP=true, ranked=true, adaptive=false, health=true.
- CASPER_FULL: CP=true, ranked=true, adaptive=true, health=true.

Original first-feasible upper-bound logic, selected-rank fallback, health alarm exclusions and no-healthy fallback; original NORMAL sparse probe eligibility only for health-enabled policies. Only adaptive modes observe MISSION actual completion scores and compute eta>1. Family-wise counterfactual diagnostic upper bounds must use global q for GLOBAL_CP (previous code always used qRank). CP-disabled policies must report noncertified and no CP family statistics; leave out misleading zeroes by using null for not applicable if needed.

## Fixed diagnostic tests and matrix
First pure decision tests of all 8 policies: cloud/edge eligible candidate sets, zero CP on three no-CP baselines, globally calibrated non-ranked CP upper bounds distinct from qRank, both adaptive policies recognized, health masks ignored by no-health policies, rank2/rank3 synthetic feasibility, all alarmed fallback for health policies, invalid states rejected.
Then run known development seed index **50** with previously verified native independent 80k calibration and original S2_HIDDEN_COMPUTE_40LOSS and S3_HIDDEN_NETWORK_50LOSS scenario, **12000 deployment tasks/policy**, all eight policies => **16 policy-runs / 192000 task-policy outcomes**. Check full task and mission conservation, optional policy flags, 21 node routing counts, no health updates for non-health policies, E17 only for two adaptive policies, strict FIFO, self-contained native physics, all rank and certification counts; require full matrix JSON byte-identically reproduced.

Crucially, the original already successful three-policy Stage4 development results for seed50/S2 and seed50/S3 must remain identical after adding the other policies, not silently mutate. The original 10-seed holdout p=.0625 nonsignificant, exploratory factorial p=.125 nonsignificant and separate strict Java-vs-Python physical FCFS parity 41773297282 FAIL max9.1214ms>preregistered5ms remain unchanged. No seed-level significance claim from this development matrix. Later separately preregister untouched holdout seeds and primary metrics **after** passing all eight-policy mechanics.
