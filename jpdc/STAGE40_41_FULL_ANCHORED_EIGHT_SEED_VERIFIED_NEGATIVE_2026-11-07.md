# Stage40–41 scientific source evidence — CASPER_FULL-anchored feedback HOLDOUt scientifically NEGATIVE (2026-11-07)

## User goal / changed research stance
Target JPDC practical incremental applied cloud–edge IIoT deadline scheduling with fair experiments, inspired by six 2026 accepted FGCS/JPDC full PDFs the user supplied, bibliographic metadata in `jpdc/references_2026_six_uploaded.bib` and English `jpdc/RELATED_WORK_MANUSCRIPT_DRAFT_SCHEDULING_FIRST_2026-11-07.md`. No novel mathematical theorem requirement, BUT scientific evidence / practical advantage necessary. No claim the published AUHS/DFAQ-LB software has been faithfully reproduced.

## Stage40 methods locked BEFORE development outcomes
Prereg `jpdc/STAGE40_FULL_ANCHORED_MISSION_E2E_PREREG_2026-11-07.md` commit `3ef75e282989c395e154958ec2242dc386023294`. Original E42 Git blob `34256ca7bff46f911cf20e8b94278fbd09175746` and E4.6 untouched. New `jpdc/casper_full_anchored_reranker_stage40.py` and `jpdc/independent_physical_full_anchored_stage40.py` source clone.
- FIRST choose original CASPER_FULL route with original ranked-CP family, E17 adaptive memory, health screening and original NORMAL/HIGH health probes. For MISSION only, potential switch restricted to SAME original eligible top3 family, original candidate rank screening, nominal predicted route <= original full chosen+2ms, delivered E2E residual q90 last32 min8 per node and freshness<=5000ms at BOTH source and alternative, estimated corrected-score gain>=1ms, never hidden oracle/future outcome. Additional variant `NEW_FULL_ANCHORED_CPU_E2E` uses CPU-finish positive residual q75 last32 min4 source+target, freshness<=5000ms. Strict fallbacks to original FULL if no CP-screening or fresh evidence, no claimed hard deadline/conformal certificate.
- Adversarial causality/no-future tests and original source parity passed [Stage40 42405082241](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42405082241) SUCCESS, two new DEVELOPMENT seeds93–94, 2×2×5×12k=240000 dependent job-policy source records, not independent validation. Both Stage40 variants maintained original FULL MISSION POST miss counts on S2; Stage40 E2E S3 seed93 had6 vs FULL7, seed94 both15; fragile apparent improvement n2. Development-only report `jpdc/STAGE40_FULL_ANCHORED_DEV_VERIFIED_2026-11-07.md` commit `f3c57ed7a98e1edf9e2ec0aecf0c0f3b6008e803`.

## Stage41 pre-outcome strict independent holdout
Prereg `jpdc/STAGE41_EIGHT_SEED_FULL_ANCHORED_HOLDOUT_PREREG_2026-11-07.md` git `9ea6d7d4ef18e725ce1f0c173f7fdc056e3a7c1c` BEFORE source outcomes. Exactly 8 new independent source seeds **701–708**, original 80k calibration each, S2 compute40%-loss / S3 network50%-loss and 5 fixed policies (GREEDY, CASPER_FULL, frozen Stage38 mission-only combined, Stage40 E2E-only and Stage40 CPU+E2E); 8×2×5×12000=**960000 DEPENDENT task-policy observations**, science n**8 source seeds**, all 8 in aggregate (no exclusions, no optional stopping or altered thresholds). Original Stage6 JSON parity and frozen Stage38 parity for all source seeds, causal CPU-finish/E2E accounting=12000 per arm, original E42 hash unchanged. Runner `jpdc/run_stage41_full_anchored_holdout.py`, aggregate `jpdc/audit_stage41_full_anchored_holdout.py`, CI `.github/workflows/jpdc-stage41-eight-seed-full-anchored.yml`.

**Actual FULL GitHub Actions [42405407050](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42405407050) SUCCESS** all 8 source jobs and complete science aggregate `JPDC_STAGE41_COMPLETE_EIGHT_SEED_FULL_ANCHORED_PAIRED_AUDIT_PASS`.

## Stage41 real POST MISSION deadline misses, complete 8 source seed matrix
S2 and S3 have same per-seed MISSION denominator: seeds701..708 respectively **[97,103,102,100,101,117,103,112]**, total **835** dependent mission tasks per policy/scenario.

| Seed | S2 CASPER_FULL | S2 FULL-anchored E2E | S2 FULL-anchored CPU+E2E | S3 CASPER_FULL | S3 FULL-anchored E2E | S3 FULL-anchored CPU+E2E |
|---:|---:|---:|---:|---:|---:|---:|
|701|0|0|0|0|0|0|
|702|5|5|4|12|12|12|
|703|2|2|2|4|4|4|
|704|2|2|2|0|0|0|
|705|1|1|1|0|0|0|
|706|1|1|1|2|3|3|
|707|0|0|0|1|1|1|
|708|1|1|1|1|1|1|
|**POOLED dependent totals; NOT independent inference**|**12**|**12**|**11**|**20**|**21**|**21**|

S2 FULL-anchored E2E equals CASPER_FULL **8/8 seeds**, 0 changes in POST mission miss count, exact sign p undefined due all tied; network-only feedback does not contribute S2. S2 FULL-anchored CPU+E2E is marginally 1 lower (seed702), 1 improved source seed 0 worse 7 ties, paired mean −.125 miss/seed, exact 2-sided sign p**1.0**, NOT meaningful statistical advantage.

S3 both Stage40 FULL-anchored E2E and FULL-anchored CPU+E2E have **+1 actual POST MISSION miss vs FULL** (seed706), 0 improved seeds, 1 harmed and 7 ties, paired mean **+.125 miss/seed (WORSE)**, exact 2-sided sign p**1.0**. The predeclared S3 strict mean improvement vs CASPER_FULL gate **FAILED** for both candidates, S3 sign p<.05 gate FAIL. S2 no mean harm gate passes for both (E2E parity and CPU+E2E slight less), S2 harmed-seed<=2 passes, S3 harmed-seed<=2 passes; those alone do not rescue S3 efficacy.

S3 new Stage40 E2E had source total all-MISSION policy switches by seed [0,11,10,6,0,9,2,2] (total40 across FULL workload, NOT just postshock); Stage40 CPU+E2E [0,11,10,6,0,10,2,2] total41. No convincing benefit in actual POST deadline misses despite some route churn; preserve all adverse outcomes.

S3 pooled POST MISSION misses other policies: original PRED_GREEDY **19**, CASPER_FULL **20**, frozen previous Stage38 MISSION-only combined **16**. S2 GREEDY23, FULL12, Stage38 mission-only combined19. This demonstrates the real tradeoff: original FULL CPU S2 robustness, older feedback S3 moderate benefit, but naive FULL-anchored highly constrained rerank FAILS to combine them. These 835 dependent task counts not iid scientific samples.

## Science decision
**Do NOT PROMOTE Stage40 CASPER_FULL-anchored rerank as final JPDC scheduling contribution**, despite clean CI and baseline source parity. Original study may remain a fair negative ablation. Do not modify thresholds after viewing 701–708 then call those independent validation seeds again. A new method needs new DEV sources and later truly untouched source cohort.

Technical diagnosis (hypothesis, not proved): restrict to already CP-screened original top3, <=2ms nominal extra and evidence from >=8 fresh E2E observations in BOTH nodes causes only a handful of switches. Stage38 previously found more S3 benefit when using broader PRED_GREEDY anchor but caused S2 harm. Next promising *distinct engineering contribution* could be a **causal compute-vs-network regime selection** and mode-dependent fallback between original FULL and a network-feedback route, but need explicit observable regime diagnostics, no oracle fault scenario, no hard claims, controlled ablation and alternative queue physics. Another path: augment evidence in original FULL candidate set with network congestion avoidance without strict bilateral min8 observations, explicitly handle uncertainty/no samples, preserve S2 and test independent ablation. Need avoid trivial threshold tuning.

**Binding model validity gap:** strict Python FCFS vs Java CloudSimPlus 8.5.7 SpaceShared previously preregistered cross-queue parity FAIL max wait discrepancy9.1214ms >5ms, not remedied. No external real workload trace, no faithful reproduced 2026 competitor code. JPDC article not submission-ready even if an isolated positive source result appears.
