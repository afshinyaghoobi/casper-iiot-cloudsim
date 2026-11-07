# JPDC Stage41 fixed independent source HOLDOUT protocol — CASPER_FULL anchored MISSION E2E (2026-11-07)

The Stage40 source code/thresholds are frozen *before any holdout outcomes* and MUST NOT be modified during independent evaluation. Development seeds93,94 were inspected and are **not** independent validation. Stage39 seeds601–608 were also already examined and MUST NOT be re-used as new validation. Original E42 blob SHA `34256ca7bff46f911cf20e8b94278fbd09175746` and E4.6 untouched.

### New fixed independent cohort
Eight source seeds **701,702,703,704,705,706,707,708**, distinct from reported prior experimental seeds and frozen in advance. Each seed: original Stage3 80k native physical calibration, original S2_HIDDEN_COMPUTE_40LOSS and S3_HIDDEN_NETWORK_50LOSS, 12k tasks each. EXACT policies:
1. PRED_GREEDY
2. CASPER_FULL
3. NEW_MISSION_ONLY_CPU_E2E_FEEDBACK (Stage38)
4. NEW_FULL_ANCHORED_E2E (Stage40)
5. NEW_FULL_ANCHORED_CPU_E2E (Stage40)
8×2×5×12000 = **960,000 DEPENDENT task-policy records**, independent science n=8 SOURCE SEEDS. Include all seeds even if adverse; no optional stopping, editing code/thresholds, or interpreting tasks as independent scientific observations.

Use exact Stage6 JSON parity for every original PRED_GREEDY/CASPER_FULL arm. For old Stage38 combined MISSION-only exact JSON parity with frozen Stage38 run. Stage40 source e17 adaptive and health/CP structure must remain. In FULL-anchored arms, CPU service errors only after CPU FINISH, network errors only after E2E delivery; MISSION-only family/health and 2ms nominal switch budget and qrank candidate screening, >1ms gain, >=8 fresh E2E reports<=5s, optional >=4 fresh CPU finishes<=5s; no peek at future fault masks or task outcome. Exact count conservation: 12k CPU and 12k E2E reports, all source physical tasks completed. Include per-seed original CP-screened counts, reroute counts, fallback reasons, mission deadline misses, actual E2E mean and queue wait.

### Primary source-seed-level paired scientific end points
POST shock MISSION missed-deadline COUNT and denominator, per seed/scenario/method. Compare Stage40 E2E and Stage40 CPU+E2E to CASPER_FULL primarily, and to Stage38 and PRED_GREEDY secondarily. Negative paired count means improvement. Report every seed, paired mean and range, better/worse/ties, and two-sided exact sign p on non-ties. Also report pooled task counts **descriptive only**, never as statistical independent n. Predeclare retention gates for *Stage40 E2E* first, CPU+E2E second:
- S2 mean candidate minus CASPER_FULL <=0 and <=2/8 source seeds worse (CPU-shock preservation);
- S3 mean candidate minus CASPER_FULL **<0** and <=2/8 source seeds worse (network benefit);
- exact two-sided sign p<.05 required for a statistical direction claim in each scenario. The engineering gates are not a claim of mathematical deadline safety.
If no/low switch count leads to FULL-equivalent outcomes, document it as a failed practical contribution, not "robust safety" or a success of learning.

### Scope and methodological limitations
Strict Python FCFS simulator only. Original Java CloudSimPlus8.5.7 SpaceShared queue semantics registered fidelity FAIL max wait difference9.1214009ms >5ms; no external trace validation. Six uploaded FGCS/JPDC 2026 papers in bibliography, methods not faithfully reproduced. Even a successful holdout is not automatically JPDC novel or submission ready until strong comparable baselines and simulator sensitivity are addressed.
