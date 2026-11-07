# JPDC Stage42–43 — causal regime-gated MISSION scheduling: source-valid but limited network recall, 2026-11-07

## Frozen science provenance
User's requested realistic JPDC contribution targets *practical incremental engineering scheduling* with real MISSION deadline metrics and direct ablations, **not** a wholly new conformal theorem. Six supplied accepted FGCS/JPDC 2026 articles are in `jpdc/references_2026_six_uploaded.bib` and the ready-to-integrate English Related Work draft. No published DFAQ-LB/AUHS algorithm is falsely claimed reproduced.

Stage42 method preregistered **before development outcomes** `jpdc/STAGE42_CAUSAL_REGIME_GATED_SCHEDULING_PREREG_2026-11-07.md` commit `75a32068538ec202ec63c0d0f2e541b8179c5f30`. New `jpdc/causal_regime_selector_stage42.py`, `jpdc/independent_physical_regime_gated_stage42.py`, causal tests and dev runner. Separate actual/nominal CPU ratio observations ONLY AT CPU FINISH and actual/nominal network ratio observations ONLY AFTER E2E DELIVERY. Badness actual/nominal >=1.5; first256 reports per evidence stream lock baseline fraction, last64 recent fraction, signal if recent >=.35 and >=baseline+.20; select NETWORK iff network signal and no CPU signal; otherwise FULL. No oracle affected-node mask, true scenario or index10000 shock timing read by policy. Original FULL route for NORMAL/HIGH and for MISSION when FULL; on NETWORK only MISSION uses frozen Stage38 CPU+E2E or E2E-only within +2ms nominal PRED_GREEDY candidate budget, no certified deadline/conformal claim. Original FGCS E42 Git blob SHA `34256ca7bff46f911cf20e8b94278fbd09175746`, E4.6 frozen.

Stage42 initial CI [42408647939](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42408647939) failed overstrict **unit fixture** that asserted no network signal from previously already delivered observations. Fixture corrected to assert CPU-finish alone cannot change network classification, **without changing policy, thresholds or science source**. [Stage42 successful CI 42408742874](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42408742874) PASS development seeds95 and96 original source parity and repeated bit-identical. On S2, FULL and both new methods POST MISSION misses seed95 7/83, seed96 1/92; NETWORK mode zero. On S3 FULL 5/83,0/92 and both new 4/83,0/92; NETWORK mode dispatch counts1962 and1352 from12k. Development n2 only, not independent effect.

Stage43 genuine source HOLDOUT prereg `jpdc/STAGE43_EIGHT_SEED_CAUSAL_REGIME_HOLDOUT_PREREG_2026-11-07.md` commit `8831f06b48e34ebab6e39dcc7047957c50dad7db` BEFORE any cohort outcomes, exact algorithm unchanged. New science seeds **801–808**, source Stage3 80k physical calibration each, scenarios S2 CPU40%-loss and S3 NETWORK50%-loss, 5 policy arms GREEDY/FULL/old Stage38 MISSION-only/Stage42 E2E gated/Stage42 combined gated, each12k: **960000 DEPENDENT task-policy records, scientific n=8 independent source seeds**. Original PRED_GREEDY/CASPER_FULL full Stage6 JSON parity and old Stage38 full policy JSON parity, original E42 and E4.6 frozen. Strict native Python FCFS only. Runner `jpdc/run_stage43_regime_independent.py`, complete-cohort `jpdc/audit_stage43_eight_seed_regime.py`, workflow `.github/workflows/jpdc-stage43-eight-seed-regime.yml`.

**Real GitHub Actions [42409065033](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42409065033) SUCCESS 8/8 source science jobs plus all-or-nothing complete aggregate**: `JPDC_STAGE43_COMPLETE_EIGHT_SEED_CAUSAL_REGIME_PAIRED_AUDIT_PASS`. No dropped seed, no retuning, no optional stopping.

## Independent Stage43 source MISSION POST-shock counts (all eight)
Per-seed post MISSION denominators for source seeds801…808 = **[96,77,92,102,99,96,92,96]**, total **750 dependent MISSION tasks per policy/scenario**.

| Seed | S2 FULL | S2 old ungated Stage38 | S2 new gated BOTH | S3 FULL | S3 old ungated Stage38 | S3 gated BOTH | S3 NETWORK-mode dispatches/12000 |
|---:|---:|---:|---:|---:|---:|---:|---:|
|801|6|4|6|9|7|7|1950|
|802|1|2|1|2|1|1|1948|
|803|1|2|1|1|0|1|902|
|804|4|4|4|2|2|2|0|
|805|2|5|2|1|1|1|850|
|806|5|2|5|0|0|0|0|
|807|2|0|2|3|1|3|248|
|808|1|0|1|4|3|4|8|
|**Pooled descriptive counts (NOT scientific iid n)**|**22**|**19**|**22**|**22**|**15**|**19**|**5906**|

Both gated ablations E2E-only and combined had IDENTICAL MISSION deadline miss counts in both scenarios. In S2 both exactly match original FULL in every source seed (22 vs22, all eight ties, sign test undefined). This establishes no source S2 harm in THIS synthetic cohort, but does **not** prove safety or superior outcomes relative to GREEDY (PRED_GREEDY S2 18 vs FULL22).
S3 both gated methods vs FULL POST MISSION counts **19 vs22**; paired seed improvements2, worse0, ties6, mean candidate-minus-FULL **−0.375** mission misses per seed; two-sided exact sign **p=.5**, NOT statistically significant. PRED_GREEDY S3 also22 and older ungated Stage38 MISSION-only15, descriptively better than gated19 but potentially S2 harm in other used independent cohorts. **No strong independent S3 advantage demonstrated.**

## Independent preregistered detector gate (important negative)
S2 whole-source NETWORK mode dispatch count zero in all8 seeds: fixed S2 false-mode <=1% each seed **PASS8/8**. S3 prereg >=5% network regime dispatch rate in >=6/8 seeds **FAILED**; only 4/8 passed threshold (8011950, 8021948, 803902, 805850). Other source seeds: 8040, 8060, 807248, 8088. Thus network detection/exposure is **incomplete/late/absent** in half the S3 cohort despite true physical scenario. These scenario ground truth labels are used OFFLINE in evaluation only, never dispatch. Gated method's observed S3 gain is hindered by under-detection. No oracle "fix" and no posthoc threshold tuning on seeds801–808 allowed.

Predeclared Stage43 combined and E2E gates:
- S2 no average MISSION harm vs FULL **PASS** (equal)
- S2 at most2 harmed source seeds **PASS** (0)
- S3 strictly lower mean MISSION miss than FULL **PASS** (−.375/seed)
- S3 at most2 harmed source seeds **PASS** (0)
- S2 max1% NETWORK mode EVERY source seed **PASS**
- S3 >=5% NETWORK mode at least6/8 source seeds **FAIL** (4/8)
- S2 two-sided sign p<.05 **FAIL/not applicable** (all ties)
- S3 two-sided sign p<.05 **FAIL** (.5)
Hence **DO NOT promote this version to final JPDC scheduler**. The detector protects FULL fallback in S2, but misses network-mode opportunities in 4/8 S3, and gains are small. This is engineering negative/mixed independent evidence, not CI failure. Preserve all outcomes without cherry-picking.

## Next research go/no-go
A relevant **structural** next question is whether source E2E ratio anomaly should be assessed by per-node or class-adjusted evidence, rather than global first256/last64 window, to reduce false negatives without creating S2 false positives. Any changed threshold/detector validated on Stage43 seeds801–808 is development/exploration only and requires NEW, untouched scientific source cohort for confirmation. A system-level MISSION deadline scheduling contribution needs direct competitive baselines (may adapt queue-control idea of 2026 DFAQ-LB with explicit honesty), actual runtime/decision overhead, alternative queue physics / real trace, and broad independent source uncertainty. Original Python FCFS vs Java CloudSimPlus SpaceShared queue parity preregistered FAIL wait max9.1214ms>5ms remains unresolved. Do NOT call a mixed system contribution submission-ready.
