# Stage51 — causal queue-pressure and delayed-E2E comparator, fixed DEV verified (2026-11-12 CST / 2026-11-13 UTC)

## Scientific classification and provenance
**This is a completed two-source-seed DEVELOPMENT comparison, not an independent holdout or validated superiority study.** Design preregistered before source outcomes `jpdc/STAGE51_QUEUE_PRESSURE_BASELINE_DEV_PREREG_2026-11-12.md`, commit `33b8309a0d38151c90f7114f8d418b900a346383`. New methods are explicitly transparent **queue-pressure and E2E-feedback-adapted comparators** conceptually related to Wu et al. (FGCS 2026) but **NOT original author DFAQ-LB reproduction**.

First actual [Stage51 workflow run 43368527268](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43368527268) **FAILED** both jobs at `IndentationError` in isolated Stage51 source clone before any science source outputs. The syntax/placement bug was fixed in commit `888d111264955c319816fa12b383dd6ab4910429`; neither original CASPER source nor frozen Stage6/E42/E4.6 was modified.

[**Subsequent actual GitHub Actions run 43368607001**](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43368607001) **SUCCESS** both scientific seed jobs DEV101 and DEV102. Provenance: source commit `888d111264955c319816fa12b383dd6ab4910429`, artifacts `jpdc-stage51-dev-seed-101` **ID 14011636091** and `jpdc-stage51-dev-seed-102` **ID 14011023778**, both retrieved and independently inspected. Source JSON/log exact repeated byte matches for each job; Stage6 exact source PRED_GREEDY/CASPER_FULL parity verified, source E42 SHA guard verified, synthetic selector tests PASS, 80k fixed Stage3 S0 calibration per seed and 12,000 deployment tasks per seed/scenario/policy. **192,000 dependent task-policy observations; scientific development n=2**.

Both policies use 21-node issue-time virtual queue backlog `vq.predicted_backlog()`; QUEUE_PRESSURE_05 adds `min(20ms,0.5×backlog)` to nominal predicted latency. QUEUE_PRESSURE_E2E_05 adds, additionally, node E2E network-excess penalties available only after prior E2E delivery (capped20ms). Neither receives hidden shock mask, actual task service at dispatch or future outcomes. Both use independent strict FCFS Python physical simulation, **not** native Java SpaceShared parity.

## Complete observed post-shock MISSION deadline misses, no cherry-picking
| Original scientific DEV seed | POST MISSION denominator | Scenario | PRED_GREEDY | CASPER_FULL | QUEUE_PRESSURE_05 | QUEUE_PRESSURE_E2E_05 |
|---:|---:|---|---:|---:|---:|---:|
| 101 | 82 | S2 hidden CPU40% loss | 2 | 2 | 2 | 2 |
| 102 | 105 | S2 hidden CPU40% loss | 0 | 0 | 0 | 0 |
| 101 | 82 | S3 hidden network50% loss | 2 | 2 | 2 | 1 |
| 102 | 105 | S3 hidden network50% loss | 2 | 2 | 0 | 0 |
| **DEV pooled descriptive** | **187** | **S2** | **2** | **2** | **2** | **2** |
| **DEV pooled descriptive** | **187** | **S3** | **4** | **4** | **2** | **1** |

Queue pressure **actually makes decisions different from PRED_GREEDY**, rather than merely renaming it: S2 seed101 736/12k changes, seed102 486/12k; S3 seed101 queue-only738/12k vs queue+E2E1575/12k, seed102 queue-only479/12k vs queue+E2E1122/12k. E2E version shows observable changed choices. S3 seed102 its **sum of selected node E2E penalties is 0** despite changed choices; this is compatible with other nodes' positive penalties steering the choice away from penalized nodes; do not misinterpret selected-penalty zero as proof network feedback inactive.

Across two seeds, arithmetic mean of per-source *all-task* mean latency/wait, in ms:
| Scenario | Method | Mean latency (ms) | Mean wait (ms) |
|---|---|---:|---:|
| S2 | PRED_GREEDY | 48.4296 | 1.0886 |
| S2 | CASPER_FULL | 48.7883 | 1.0635 |
| S2 | QUEUE_PRESSURE_05 | 48.3852 | 0.7138 |
| S2 | QUEUE_PRESSURE_E2E_05 | 48.3852 | 0.7138 |
| S3 | PRED_GREEDY | 50.0819 | 1.0209 |
| S3 | CASPER_FULL | 50.6260 | 1.0014 |
| S3 | QUEUE_PRESSURE_05 | 49.9945 | 0.6516 |
| S3 | QUEUE_PRESSURE_E2E_05 | 48.9610 | 0.6899 |

## Gate conclusions
- Code/causality contract and actual GitHub source tests **PASS**.
- Original source exact parity, E42 immutable SHA, original E4.6 preserved, fixed 2/2 source DEV jobs complete, repeat bytes identical **PASS**.
- Descriptive S2 no mission miss harm vs both original controls **PASS for only this tiny DEV**.
- Descriptive S3 queue-only and queue+E2E fewer mission misses vs both controls **observed**, not proof or generalizable estimate.
- E2E extension adds one further mission miss reduction in this tiny cohort (from2 to1), but not a defensible causal attribution to a particular task from aggregate output; changes influence shared queues.
- **Statistical improvement NOT ESTABLISHED:** n=2 DEV seeds, not independent holdout. No p-value or confidence interval from individual tasks.
- **Physical portability NOT ESTABLISHED:** original strict Python FCFS vs original CloudSimPlus SpaceShared WAIT registered max error9.1214009ms>5ms still **FAIL**. Stage50 queue-micro did not fix it.
- No new original CASPER algorithm improvement proved; this is a comparator candidate, not claimed as JPDC ready.

## Decision / next steps
Do not tune alpha0.5, 20ms caps, or E2E inclusion using observed DEV101/102 and still call new holdout untouched. Freeze these methods and source if proceeding. Pre-register untouched independent source holdout (for example **1101–1108**, if verified not previously used), primary per-seed POST MISSION miss differences against original FULL and GREEDY, report adverse cases. Also verify simulator/queue model sensitivity and report all limitations, rather than treating this small favorable cohort as acceptance evidence. Maintain original six published 2026 bibliographic refs and clear name `queue-pressure/E2E-inspired`, not Wu DFAQ-LB reproduced.
