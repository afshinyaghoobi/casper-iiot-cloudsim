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
