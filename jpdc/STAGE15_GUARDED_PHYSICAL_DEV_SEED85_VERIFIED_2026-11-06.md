# JPDC Stage15 — preregistered guarded physical DEVELOPMENT seed85 VERIFIED (2026-11-06)

## Evidence
GitHub Actions [42185326575](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42185326575) SUCCESS; original artifact 13487116919. Prespecified S2/S3 x 5 arms x12,000 deployment tasks =120,000 dependent task-policy records, ONE developmental seed85. Complete matrix ran twice byte-identically. All six original Stage6 baseline comparisons passed exact equality, both unguarded policy comparisons matched the frozen Stage14 algorithm exactly, and guarded E2E/budget/FCFS assertions passed. Original E42 source hash unchanged. Seed85 is never a fresh confirmatory holdout.

## Complete actual descriptive outcomes

| Scenario | Policy | pre MISSION misses | post misses | TOTAL misses | mean latency ms | mean wait ms |
|---|---|---:|---:|---:|---:|---:|
| S2 compute | PRED_GREEDY | 5 | 17 | 22 | 51.688 | 4.249 |
| S2 compute | CASPER_FULL | 6 | 14 | **20** | 52.184 | 3.855 |
| S2 compute | RESIDUAL_PROBE | 6 | 16 | 22 | 52.385 | 4.176 |
| S2 compute | FRESHNESS_ACTIVE (Stage14) | 8 | 20 | 28 | 53.183 | 5.676 |
| S2 compute | FRESHNESS_GUARDED (Stage15) | 5 | 17 | **22** | 51.957 | 4.503 |
| S3 network | PRED_GREEDY | 5 | 2 | 7 | 51.177 | 3.520 |
| S3 network | CASPER_FULL | 6 | 2 | **8** | 51.791 | 3.450 |
| S3 network | RESIDUAL_PROBE | 6 | 6 | 12 | 52.160 | 4.238 |
| S3 network | FRESHNESS_ACTIVE (Stage14) | 8 | 2 | 10 | 52.209 | 5.270 |
| S3 network | FRESHNESS_GUARDED (Stage15) | 5 | 0 | **5** | 51.179 | 3.689 |

The 2ms nominal-detour guard substantially improves the developmental unguarded policy in both scenarios (S2 28→22, S3 10→5 total MISSION misses). Against CASPER_FULL it remains *worse in S2* (22 vs20) but *better in S3* (5 vs8); against PRED_GREEDY it ties S2 (22) and improves S3 (5 vs7). Not statistically validated, and S3 post miss count zero occurs among relatively few post-MISSION jobs in ONE scientific seed. No causal interpretation of specific node behavior from aggregate outcome alone. Record pre/post, not cherry-picked postshock.

Guarded policy performed 95 NORMAL probing attempts in both scenarios. No measured probe-cost or deadline guarantee outside source conditions. Confirmatory multi-seed, sensitivity and alternative queue engines absent. Stage15 mechanism is a CONGESTION-GUARDED nonconformal prototype, not an extended conformal certificate or FGCS CASPER replacement. The original fixed source generator and Python FCFS vs Java queue mismatch remain external validity threats.

## Decision
Stage15 is a credible early positive **development result under S3 only**, with an important S2 weakness. Keep both results; do not retune the 2ms threshold on seed85. Before any confirmatory study: add independent frozen-code unit tests for the MISSION nominal detour invariant, E2E causal state, and NORMAL probe eligibility, then predeclare disjoint evaluation seeds and scenario sensitivity; consider parallel separate cross-engine validation. Baseline policy set requires literature audit before JPDC manuscript claims.
