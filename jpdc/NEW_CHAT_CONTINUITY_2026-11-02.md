# JPDC CASPER — VERIFIED NEW-CHAT HANDOFF (2026-11-02)

## START HERE
Repository: https://github.com/afshinyaghoobi/casper-iiot-cloudsim
Branch: `jpdc-seed0-repro-20261024`. Original frozen E42 source blob SHA `34256ca7bff46f911cf20e8b94278fbd09175746`; NEVER modify E42 or E4.6. Use generated E45 only for intervention.
Scientific journal target JPDC. User prefers a technically real new step each turn, verified provenance, no repeated requests for files. Do not fabricate code runs or data. If prior chat is unavailable, start with this file and relevant GitHub workflow output.

## Workflows and verified completed real executions
1. 30-seed S3 baseline: `40517282086` (8 policies, 30 seeds, 30k tasks/seed), 250 late mission tasks per seed.
2. Task-level seed29 actual CloudSim trace, run `41504014147` successful, artifact `13170236795`. 66/30,000 differing node choices FULL vs STATIC; 7 mission outcome disagreements, all with different node choices; 6 differing chosen nodes in last 250 mission tasks; one late mission outcome difference, Task 28313.
3. Candidate bound audit for Task 28313, run `41505713127` successful: exact common rank candidates 12,15,20; static eta=1 chooses node12, adaptive eta=3 chooses node15. Deadline=50.669 ms; node12 static bound=37.362ms, FULL bound=51.818ms; FULL node15 bound=50.319ms; observed FULL latency=50.937ms (miss), STATIC latency=29.781ms (success). eta crossing threshold approximately 2.8411 for node12.
4. S3 seed29 eta intervention, run `41508071810` successful: original CASPER_FULL late DVR .124, eta=1 late DVR .120; clamp exactly reproduces HEALTH_STATIC science. Other-policy invariance verified.
5. S3 three-seed eta intervention, run `41510962554` successful seeds 0,7,18.
6. S3 six additional seeds, run `41511810120` successful seeds 1,5,9,13,21,27. S3 ten seeds 0,1,5,7,9,13,18,21,27,29: in 2,500 late mission task opportunities per arm, adaptive FULL false certs 21 vs clamp 80; abstentions 233 vs 46; deadline violations 113 vs 112. Seed-level paired exact signs with Holm across late_far, late_air, late_dvr: adjusted p=.03125, .0234375, 1.0 respectively. Do not treat tasks as independent.
7. S2 compute 40%-loss seed 0,7,18 intervention, run `41516881350` success.
8. S2 six-seed intervention, run `41517917953` success, seeds 1,5,9,13,21,27.
9. S2 seed29 completion, run `41520884581` success. Ten perfectly matched seed indices with S3; no false certificates in either arm for S2 across these seeds.
10. CI trace contract, run `41502534232` success. Task-level analyzer `jpdc/analyze_seed29_task_trace.py`; `jpdc/test_seed29_trace_contract.py`.
Provenance branch commits: candidate diagnosis `961561f`, seed29 intervention `d57824b`, S3 six extension `eb5f733`, S2 six extension `24353df`, S2 seed29 `d41ddbf`.

## Current best statistical result: cross-scenario interaction
Paired seed set: 0,1,5,7,9,13,18,21,27,29. Define effect per seed = CASPER_FULL adaptive metric minus CASPER_FULL eta=1 metric; interaction = S3 effect minus S2 effect.
S3 vs S2 mean difference:
- late_far -2.36 percentage points; exact paired two-sided sign p=.015625; 3-metric Holm p=.046875; 95% exploratory paired bootstrap percentile interval [-3.92,-1.04] pp.
- late_air +6.8 pp; sign p=.0390625; Holm p=.078125.
- late_dvr +.04 pp; p=1 and Holm p=1.
**IMPORTANT NEW FINDING** Nov 2 robustness audit: leave-one-seed-out Holm-adjusted late_far interaction loses p<.05 for 7 out of 10 exclusions (p=.09375), though direction of effect stays negative for every exclusion (mean between -1.78 and -2.62 pp). It remains significant for exclusions 5,7,9. Thus describe cross-scenario interaction as fragile/borderline exploratory; do NOT claim robust confirmation. Also design / repeated exploratory testing should be disclosed. Inference unit=seed. Zero observed FAR in S2 does not prove zero underlying risk.

## Metrics semantics
- late_fwc = counterfactual family-wide bound coverage for all top-3 candidate nodes, NOT certificate correctness.
- late_air = fraction late mission tasks that abstained (did not issue certificate).
- late_far = fraction ALL late mission tasks incorrectly certified (not conditional among issued certs). Conditional error among issued certs = FAR/(1-AIR).
- late_dvr = deadline violation rate among ALL late mission tasks.
- Certifier and candidate decision depend on eta; for NORMAL tasks probes may override chosen node, but mission-only FAR/AIR not directly affected by NORMAL-only probe override.
- No statistically significant FULL vs advanced scheduler deadline improvement shown in 30-seed S3.

## Generated local artifact paths (may not persist in a new chat)
`/mnt/data/jpdc_s2_s3_ten_seed_interaction_2026_11_02.zip` and CSV `/mnt/data/jpdc_s2_s3_ten_seed_interaction_2026_11_02/matched_10_seed_effects.csv`.
`/mnt/data/jpdc_s3_eta_10seed_replication_2026_11_02.zip`.
`/mnt/data/jpdc_s2_eta_9seed_verified_2026_11_02.zip`.
`/mnt/data/jpdc_seed29_real_trace_findings_2026_11_02.zip`.
If local paths are missing, recover from listed GitHub Actions artifacts; file paths do not automatically transfer between chats.

## Next most valuable technical step
Expand *matched* S2/S3 intervention seeds by e.g. 10 more currently unused indices in 0..29; run matched pairs with strict scientific parity and assess interaction with confidence interval and leave-one-seed-out sensitivity, explicitly mark expanded testing as exploratory or define held-out confirmation. To avoid unbounded repeated exploratory testing, ideally pre-register and run a disjoint 30..59 holdout with S2/S3 pair. Ensure same seed in both scenarios, and avoid mixing fixed 10 with new seeds for an unqualified confirmatory p-value. Use GitHub Actions jobs with generated E45 and frozen blob guard; do not edit E42/E4.6.

## New November 2 research step — PRE-REGISTERED DISJOINT HOLDOUT STARTED
- Pre-registered BEFORE launch: `jpdc/PREREG_S2_S3_DISJOINT_HOLDOUT_2026-11-02.md`, commit `2520adb`.
- New workflow `.github/workflows/jpdc-s2-s3-holdout-10seed-once.yml` commit `8254c58`.
- Real GitHub Actions run: **41524202008**, 10 parallel jobs, seed indices 30..39, each runs S2 and S3 *before and after* eta-clamp, 4 simulations/seed, total 40 simulations. At last inspection all 10 jobs were `in_progress`; NO results have been verified; do not claim any outcomes until checking the run, downloading artifacts and validating `paired_summary.json` and pass checks.
- Workflow verifies frozen E42 SHA, non-intervened policy parity across before/after, and exact clamp CASPER_FULL=CASPER_HEALTH_STATIC science. Each job uploads `jpdc-holdout-seed-<seed>` with two before CSV, two after CSV and `paired_summary.json`.
- Primary preregistered test: paired seed-level interaction S3-minus-S2 for `late_far` (adaptive FULL minus eta=1), exact TWO-SIDED sign test excluding ties, unadjusted alpha=.05 because one prespecified primary test. Secondary `late_air` and `late_dvr` exploratory. No pooling with original 10 seed exploratory study for confirmatory p.
- On next user "ادامه", FIRST inspect run 41524202008, download all success artifacts, check all parity gates, compute holdout results and scientific caveats, then update this continuity file again.

## COMPLETED PRE-REGISTERED DISJOINT HOLDOUT — verified 2026-11-02
- GitHub Actions run `41524202008`, commit `8254c58`; all ten jobs seed indices 30..39 SUCCESS, all ten artifacts `jpdc-holdout-seed-30` .. `-39` uploaded with paired_summary.json. Frozen E42 guard and non-intervened policy/clamp parity passed on each job. Pre-registration `jpdc/PREREG_S2_S3_DISJOINT_HOLDOUT_2026-11-02.md` committed BEFORE run (`2520adb`).
- Primary estimand = [S3 adaptive FULL - S3 eta=1] minus [S2 adaptive FULL - S2 eta=1] for late_far, paired on seed, predeclared two-sided exact sign test. Result: mean interaction **-1.32 percentage points**, 5 negative, 0 positive, 5 tied seed differences, exact p=**0.0625**. **The predeclared two-sided confirmatory test FAILED alpha=.05** despite matching predicted direction. DO NOT claim confirmation or combine the exploratory earlier ten seeds with holdout to manufacture a significant confirmatory p.
- S3 late false certificates 7 FULL adaptive vs 40 eta-clamped, among 2500 late mission task opportunities per arm; S2 0 vs 0. S3 late abstentions 176 vs 47, S2 93 vs 78. S3 late deadline violations 65 vs 63, S2 20 vs 20.
- Secondary exploratory interaction late_air +4.56 pp, exact sign p=.0703125; late_dvr +.08 pp, p=1. Bootstrap paired percentile 95% for FAR interaction [-2.60,-.32] pp, exploratory and not to override the registered primary test.
- Locally created artifact `/mnt/data/jpdc_holdout_30_39_2026_11_02.zip` and CSV `/mnt/data/jpdc_holdout_30_39_2026_11_02/holdout_matched_effects.csv`; recover from GitHub Actions artifacts if unavailable in new chat.
- Next: explicitly report replication in direction but no formal confirmation. Investigate low-power/ties without post hoc claiming significance; consider manuscript-ready statistical transparency and independent-simulator/generalization rather than repeatedly searching for significant p.

## New exploratory calibration sensitivity pilot (2026-11-02)
- New generator-only E45 patch `jpdc/patch_full_q_sensitivity.py` commit `df0c392`: scales conformal q multiplier inside `upper[p]` for CASPER_FULL only, x0.9 or x1.1. Not altering calibration data, E42 or E4.6. Important nuance: tests *scaling decision bounds* not fitting/recalibrating from alternative calibration sets.
- Workflow `.github/workflows/jpdc-q-sensitivity-pilot-once.yml` commit `f498aab`, GitHub Actions run `41534252067`, S3 seed18, 3 sequential executions (baseline, x0.9, x1.1) with 30k tasks; guarded invariant on seven other policies. At last inspection run IN_PROGRESS and no artifact; results NOT YET KNOWN. Do not claim executed successfully until verified.
- Next turn: inspect run status and artifact `jpdc-s3-q-seed18-pilot`. Analyze q sensitivity `late_far`, `late_air`, `late_dvr`, `late_fwc` without overgeneralizing one seed.

## VERIFIED S3 seed18 q-bound sensitivity pilot — completed
- GitHub Actions run `41534252067` completed SUCCESS; artifact `13183775928` `jpdc-s3-q-seed18-pilot`, three actual CloudSim executions and seven other policies' scientific outputs identical by workflow gate.
- Generated E45 patch `jpdc/patch_full_q_sensitivity.py` scales decision-time q term for CASPER_FULL x0.9 or x1.1. DOES NOT refit conformal calibration; E42/E4.6 unchanged.
- Baseline S3 seed18: late_far=.020, late_air=.176, late_fwc=.772, late_dvr=.128, late P99=83.202342ms.
- q x0.9: late_far=.028, late_air=.156, late_fwc=.592, late_dvr=.128, P99=83.202342ms.
- q x1.1: late_far=.016, late_air=.192, late_fwc=.780, late_dvr=.128, P99=83.202342ms.
- In final 250 mission tasks, false certificates are 7,5,4 (x0.9,baseline,x1.1); abstentions 39,44,48. Do not claim significance from one seed.
- Next useful technical step: replicate q perturbations on a few independent S3 seed indices with unchanged policy parity, then quantify whether the trend is consistent without significance chasing.

## Latest q-bound sensitivity replication
- Workflow `.github/workflows/jpdc-q-sensitivity-3seed-once.yml`, commit `8137680`; GitHub Actions run `41541558291` launched on S3 seed indices 0,7,29 (three sequential scales baseline, q*0.9, q*1.1 in each job), plus earlier confirmed seed18 in run `41534252067`.
- At last inspection, all three jobs were in_progress with no completed artifacts. **No experimental outcomes may be claimed until all jobs and parity assertions succeed.**
- Next turn: check run 41541558291, obtain artifacts, compare FAR/AIR/DVR/FWC against each other and prior seed18, preserve limits of four-seed exploratory pilot. Frozen E42/E4.6 unchanged.

## VERIFIED four-seed S3 conformal q sensitivity (2026-11-02)
- GitHub Actions run `41541558291` completed SUCCESS (seed indices 0,7,29), artifacts 13186582133, 13186292396, 13185952527. Prior seed18 run `41534252067` SUCCESS artifact 13183775928. All original policies excluding FULL match across three scale runs per seed.
- Effective generated-E45 decision conformal bound scale q × {0.9,1.0,1.1} for FULL; NOT retrained calibration. 250 late mission tasks/seed, 1000/scale.
- Pooled late_far incorrect certificates: 23,17,13 at ×0.9,baseline,×1.1 respectively; late_air abstentions 75,93,106; late_fwc family upper-bound coverage 662,757,826 (out of 1000); late_dvr misses 70,71,70. Changes are descriptive counts on paired workloads, not independent task inferences.
- Four-seed paired sign (×1.1 minus ×0.9) for late_far 0 positive/3 negative/1 tie, two-sided p=.25; late_air 3 positive/0 negative/1 tie p=.25; late_fwc 3 positive/0 negative/1 tie p=.25; late_dvr 4 ties, p=1. NO statistical significance claim; low n.
- Seed29 late_dvr baseline .124, ×0.9=.120 and ×1.1=.120; changed decision bounds can affect deadline outcomes; other seeds' DVR unchanged. P99 unchanged all four.
- Local reproducibility archive `/mnt/data/jpdc_q_sensitivity_4seed_2026_11_02.zip`; recover via GitHub Actions artifacts if new session cannot access.
- Recommended next move: independent calibration quality/alternative simulator rather than repeatedly tuning p-values on S3.

## Verified 2026-11-03 S3 pre/post phase multi-seed trace expansion
- GitHub Actions **41652750267**, all three jobs SUCCESS for seeds 0,7,18; artifacts seed0 13237917384, seed7 13238761161, seed18 13238521488. Frozen E42/E4.6 unchanged.
- New `jpdc/audit_phase_mission_trace.py` validates 60k dispatch + 60k outcome trace rows per seed and reconciles official post/late aggregate CSV; workflow `.github/workflows/jpdc-s3-phase-trace-3seed-once.yml`.
- Detailed write-up `jpdc/S3_PHASE_REPLICATION_3SEED_2026-11-03.md`, commit `ea42d54`.
- Across 3020 postshock mission tasks **per policy**, FULL vs STATIC: FWC 2439 vs 1033, false certificates 21 vs 115, abstentions 216 vs 54, deadline misses 163 vs 163. Before shock n=1529/policy, FULL vs STATIC FWC 1516 vs 1512, false certificates both zero, deadline misses both 11. Late 750/policy: FWC 622 vs 266; FAR 5 vs 30; AIR 59 vs 12; DVR both 40.
- Per seed post FAR difference FULL-STATIC: seed0 -13, seed7 0, seed18 -81. Two-sided exact seed-paired sign p=.5 (only 2 nonzero seeds); **do not claim statistical significance** from 3-seed trace. Seed7 a meaningful identical-output case.
- Local zip `/mnt/data/jpdc_phase_s3_multi_seed_2026_11_03.zip` may not transfer; GitHub Actions artifacts are durable. Original E42/E4.6 unchanged. Do not mix task counts as independent inferential n.

## 2026-11-03 — VERIFIED S3 eta activation/decision divergence diagnostic
- Verified source: GitHub Actions run `41652750267` all 3 jobs success, task-level artifacts seed0 `13237917384`, seed7 `13238761161`, seed18 `13238521488`. New reproducible audit `/mnt/data/jpdc_s3_eta_activation_audit_2026_11_03.zip` (session-local); GitHub permanent results report `jpdc/S3_ETA_ACTIVATION_MECHANISM_2026-11-03.md`, commit `d729aae`.
- S3 postshock mission eta FULL mean seed0 2.9513 (max3; 992/1019 missions eta>=2), seed7 1.0363 (max1.2996; 0/980 eta>=2), seed18 2.9886 (max3; 1014/1021 eta>=2).
- **Last 250 mission tasks:** eta constant3 for seed0 and seed18, constant1 for seed7. Seed7 was *not globally inactive*: postshock eta>1 on 5,669 of 20,000 all tasks but never >=2. Thus previous claim that seed7 has no relevant change is now mechanically explained.
- Postshock mission certificate disagreements FULL vs HEALTH_STATIC: 31 (seed0), 0 (seed7), 131 (seed18). All three seeds have ZERO differing task routing nodes across ALL 30,000 tasks and ZERO postshock mission outcome disagreements. This does not generalize; seed29 had 66 differing routes.
- The mechanism is different eta trajectories and certification thresholds, **not** measured different routing in these three seeds. Correlation not proof of mechanism causing eta trajectory differences; new trace instrumentation of eta feedback updates would be appropriate.
- E42 source frozen, E4.6 unchanged. Do not replace main manuscript Result with an overgeneralized three-seed claim.

## 2026-11-03 verified E17 detector mechanics: WHY seed7 differs from seed18
- Final **SUCCESS** Actions run `41658004816`, feedback trace artifacts seed7 `13241260387`, seed18 `13239324890`; original 2 Actions runs had validator-only failures because the logger legitimately emitted both CASPER_FULL and CASPER_ADAPT_NO_HEALTH, corrected workflow commit `0baa782`. Generated-E45-only instrument `jpdc/instrument_eta_feedback_generated_e45.py`, SHA `6345efd`. No science change E42/E4.6. Validated event replay analysis `jpdc/audit_e17_feedback_detector.py`, SHA `987ebc9`. Durable report `jpdc/S3_E17_FEEDBACK_DETECTOR_REPLAY_2026-11-03.md`, commit `f5213af`.
- E17 detector threshold frozen config: 12/50 mission score exceedances over per-seed referenceQ95; slow memory 200, fast 50; clip eta 1..3; fast transition hold 200. Strict replay of alarm_before/after and age_before/after PASSED for every observation for both adaptive policies.
- Seed7 CASPER_FULL postshock score exceed 40/980=4.08%, max rolling50 6, alarm NEVER, final eta=1. Seed18 postshock exceed 965/1021=94.52%, max rolling50 50, alarm FIRST at task10165, final eta=3. CASPER_ADAPT_NO_HEALTH independently reproduces same alarm divergence (seed7 40/980; seed18 961/1021). Critical caveat: slow quantile can independently adjust eta, even absent alarm; also alarm remains latched but fast-memory only active for first 200 outcome updates.
- This **establishes why the threshold detector fired or not** from actual feedback, NOT what caused contrasting realized normalized network scores. Next productive diagnostic: look at seed-specific affected-node sets, actual realized network delays, and normalization inputs, without changing E42/E4.6. The E17 result is descriptive state-machine verification, not statistical proof of improved deadline outcomes.
- Session-local reproducibility bundle `/mnt/data/jpdc_e17_feedback_mechanism_2026_11_03.zip`, if missing recover Actions artifacts above.
