# JPDC Stage14 — full native physical causal prototype VERIFIED with negative total MISSION result (2026-11-06)

## Original immutable evidence
Preregistered original seed index84 DEVELOPMENT, S2/S3 x 4 arms x12,000 source-generated strict-FCFS tasks: GitHub Actions [42184744223](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42184744223) SUCCESS, artifact 13487340799; exact byte-identical second run; six baseline per-scenario output-parity passes vs original Stage6; E42 source unchanged. Earlier Stage14 run [42184642040](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42184642040) failed at a **software variable collision** before full matrix; corrected without changing frozen seed or scientific protocol. This failure remains part of the record.

Independent archived-artifact-only pre/post audit [42184993467](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42184993467) SUCCESS, `JPDC_STAGE14_FROZEN_PREPOST_MISS_ACCOUNTING_PASS`, reads frozen original JSON, no simulation reruns or changed parameters.

## Frozen descriptive observations — ONE seed, dependent task-policy records
Each arm 620 MISSION jobs, comprising 511 pre and 109 post (source shock segmentation by task index); report both, no p-values.

| Scenario | Policy | pre misses /511 | post misses /109 | TOTAL misses /620 | mean end-to-end ms | mean wait ms |
|---|---|---:|---:|---:|---:|---:|
| S2 compute | PRED_GREEDY | 2 | 5 | 7 | 55.251 | 1.703 |
| S2 compute | CASPER_FULL | 2 | 6 | 8 | 55.662 | 1.833 |
| S2 compute | RESIDUAL_PROBE | 2 | 5 | 7 | 55.800 | 1.673 |
| S2 compute | NEW_FRESHNESS_ACTIVE | **14** | **3** | **17** | 58.206 | **4.119** |
| S3 network | PRED_GREEDY | 2 | 3 | 5 | 58.601 | 1.676 |
| S3 network | CASPER_FULL | 2 | 3 | 5 | 59.130 | 1.646 |
| S3 network | RESIDUAL_PROBE | 2 | 2 | 4 | 56.528 | 1.776 |
| S3 network | NEW_FRESHNESS_ACTIVE | **14** | **1** | **15** | 58.906 | **4.216** |

The pre-shock misses rise +12 vs CASPER_FULL in each scenario and post-shock misses decrease by 3 (S2) /2 (S3), producing +9/+10 worse TOTAL misses, respectively. The postshock improvement is small descriptive one-seed observation and the *primary overall task outcome is worse*. In S3 relative to CASPER_FULL mean latency is -0.225ms despite worse total misses; tail/deadline impacts dominate. In S2 mean latency +2.544ms, worse. Do NOT present new policy as superior.

Stage13 active probe: 95 NORMAL probe attempts per scenario, 33/42 actually changed candidate, 0 NORMAL probe deadline misses; nominal route changes vs greedy 1744 S2 /3348 S3. Active observed 0 unverified MISSION decisions in these arms, but this is **not** proof of true calibration or safe confidence. S3 affected-node dispatches: new 32 vs CASPER_FULL 1012 and RESIDUAL_PROBE 26; note physical exposure depends on policy and cannot be used as a randomized detection sample.

## Best-supported diagnosis
The active policy is **overreactive on normal pre-shock workload**: 14 vs 2 pre MISSION misses, and mean physical queue waits 4.12–4.22ms vs 1.65–1.83ms, coincident with thousands of routing changes. This is consistent with congestion caused by freshness-driven node selection, but node-level causal attribution is NOT established by aggregate data; a frozen per-node queue/dispatch trace or separate ablation is needed. Probing by itself is unlikely to account for all 12 extra pre misses given only 95 NORMAL attempts and 0 probed NORMAL misses, but routing effects and coupled queues need proper tests.

## Decision gate
Stage14 passed engineering integration, reproducibility, task conservation and frozen baseline parity, **FAILED improvement criterion**. Freeze original numbers, do not post-hoc change seed84 or present selective postshock advantage. Next Stage15 should pre-register congestion-safe freshness routing, queue-aware fallback, targeted shadow/ablation and separate DEVELOPMENT seed(s), *before* test outcomes; no confirmatory seeds contaminated by tuning. Stage14 original prototype remains for comparisons. Algorithm not JPDC-ready. Cross-engine Python FCFS / CloudSimPlus Java queue equivalence is still unestablished.
