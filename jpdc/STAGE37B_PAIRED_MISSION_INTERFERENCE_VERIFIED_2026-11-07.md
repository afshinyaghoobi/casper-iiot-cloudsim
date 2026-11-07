# JPDC Scheduling-First: Stage37b task-matched causal-feedback forensic VERIFIED (2026-11-07)

## True independent source provenance
[CI 42356617921](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42356617921) **SUCCESS**; full task outcome audit seed91, already known developmental science n=1, unchanged physical/stochastic workload, all 10 original-policy/scenario arms, all four frozen Stage6 baseline JSON outputs exact parity, CPU+wait+network decomposition, exact per-task MISSION outcome conservation, repeat artifact byte-identical. Passive source `mission_audit_hook` added to isolated Stage37 source clone only: routing never uses hook. Original E42/E4.6 untouched.

Stage37 pilot overall [42356350140](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42356350140) had S2 post MISSION (N89) misses GREEDY6, CASPER_FULL4, CPU_ONLY8, E2E_ONLY6, COMBINED8; S3 GREEDY2, FULL2, CPU_ONLY1, E2E_ONLY2, COMBINED2. This triggered an explicitly retrospective, NOT prospectively confirmatory, protocol `jpdc/STAGE37B_MATCHED_MISSION_FORENSIC_PROTOCOL_2026-11-07.md` (commit `2ec0bdbd63601bfd5a5054d144f36df66768f256`), before reading task-level labels. No post-outcome rule retuning.

## Per-task matched outcomes (all differences reflect overall policy intervention and shared-resource interference)
| S2 policy | POST MISSION miss/89 | POST mission selected nodes differing from GREEDY trace | New POST mission misses vs GREEDY | Eliminated POST mission misses vs GREEDY | New misses vs FULL | Eliminated misses vs FULL |
|---|---:|---:|---:|---:|---:|---:|
|PRED_GREEDY|6|0|0|0|5|3|
|CASPER_FULL|4|47|3|5|0|0|
|CPU-only feedback|8|32|6|4|5|1|
|E2E-only feedback|6|0|0|0|5|3|
|Combined|8|32|6|4|5|1|

The naive CPU feedback produces 4 *saved* misses and 6 *new* misses vs GREEDY, net+2; vs FULL only1 saved but5 new, net+4. These are actual paired **task IDs** compared between complete policy runs; task-level outcomes are NOT independent replicates. 32 selected-node differences for post MISSION vs baseline occur even though CPU policy chose a non-greedy node on only **5** post MISSION decisions in its own instantaneous state, because earlier NORMAL/HIGH rerouting changes queue states (interference). Thus local nominal 2ms budget does not constrain the global causal effect of all dispatched jobs. This distinction is a mechanism hypothesis, NOT a proven causal decomposition into direct and spillover effects.

| S3 policy | POST MISSION miss/89 | POST mission different node from GREEDY trace | New misses vs GREEDY | Eliminated misses vs GREEDY |
|---|---:|---:|---:|---:|
|PRED_GREEDY|2|0|0|0|
|CASPER_FULL|2|1|0|0|
|CPU-only feedback|1|10|0|1|
|E2E-only feedback|2|35|2|2|
|Combined|2|37|2|2|

S3 E2E-only and combined change WHICH tasks fail, with equal total misses, an important robustness warning. CPU-only saves just ONE MISSION miss on ONE development seed. Do not claim statistical superiority or call the baseline errors IID.

## Immediate engineering hypothesis to predeclare separately
A straightforward **MISSION-only** CPU-E2E feedback scheduler would keep NORMAL/HIGH source decisions at original GREEDY and apply feedback routing only to MISSION arrivals, testing whether reducing cross-class rerouting curbs S2 collateral miss harm. Other possible approaches include background load budget or class-aware FCFS queue reservation; none proved safe or original. Hypothesis drawn *after observing seed91 forensic*, hence any new version requires new DEV source seed(s) first and separate later frozen HOLDOUT seeds. Preserve the fully adverse S2 numbers, not tuning on seed91 then calling it a confirmation.

No peer-reviewed novelty claim; Stage36 elementary TV lemma and no-free-lunch are known and not original. An eventual JPDC contribution should demonstrate credible actual deadline gains across paired independent workload seeds and additional engine/queue model; registered original Python FCFS vs Java SpaceShared parity remains FAILED 9.1214ms>5ms. This is not JPDC submission-ready yet.
