# JPDC Results — eta adaptation: exploration and disjoint confirmation

Date: 2026-11-02. Evidence is from CloudSim simulation; no deployment or external-simulator validation. Research branch `jpdc-seed0-repro-20261024`; E42 scientific blob `34256ca7bff46f911cf20e8b94278fbd09175746` unchanged.

## Design, estimand and units
For each seed and scenario (S2 hidden compute -40%, S3 hidden network -50%), compare `CASPER_FULL` adaptive dispatch eta with an intervention that clamps only effective dispatch-time eta to 1 in the generated E45 implementation. Other policy outputs are required to remain scientifically identical; clamped FULL equals HEALTH_STATIC scientifically. Outcome rates are computed over the final 250 mission tasks per seed and arm. Statistical independent unit is **seed**; do not treat pooled mission tasks as independent replications.

- `late_far`: incorrect certificates / ALL final mission tasks (not conditioned on issue).
- `late_air`: absent certificates / ALL final mission tasks.
- `late_dvr`: deadline misses / ALL final mission tasks.
- `late_fwc`: counterfactual upper-bound coverage for every candidate in the family, not certificate accuracy.

Per-seed intervention effect = adaptive metric minus eta-clamped metric. Scenario interaction = S3 effect minus S2 effect.

## Cohort A: exploratory, matched S2/S3 10 seeds
Indices `0,1,5,7,9,13,18,21,27,29`.
- S3 adaptive/clamped: false certificates 21/80; abstentions 233/46; deadline misses 113/112, each arm n=2500 late mission tasks.
- S2 adaptive/clamped: false certificates 0/0. (Full matching CSV and exact row counts: see prior S2 artifacts.)
- Interaction for FAR: -2.36 percentage points, exact two-sided paired sign p=.015625, Holm-adjusted across three exploratory metrics p=.046875. Bootstrap seed-paired 95% exploratory CI [-3.92,-1.04] pp.
- Leave-one-out correction sensitivity: excluding any of seven seeds yields Holm p=.09375. Therefore exploratory significance is not stable to removal of one nonzero seed.

## Cohort B: **separately preregistered** disjoint holdout
Pre-analysis plan committed `2520adb` to `jpdc/PREREG_S2_S3_DISJOINT_HOLDOUT_2026-11-02.md` BEFORE launch. Seed indices `30..39` disjoint from Cohort A. Successful GitHub Actions run `41524202008`, workflow commit `8254c58`, all ten parallel jobs passed all scientific parity and source guards. Ten uploaded artifacts `jpdc-holdout-seed-30` through `jpdc-holdout-seed-39`. 40 CloudSim runs across 10 seeds × 2 scenarios × 2 intervention states.
- S3 adaptive/clamped: incorrect certificates 7/40, abstentions 176/47, deadline misses 65/63 (n=2500 tasks per arm).
- S2 adaptive/clamped: incorrect certificates 0/0, abstentions 93/78, deadline misses 20/20 (n=2500 tasks per arm).
- **Prespecified primary** FAR interaction: -1.32 percentage points (S3 minus S2), 5 negative, 0 positive, 5 tied seed interactions. Exact **two-sided** sign test p=.0625. **Does not reject null at preregistered alpha=.05**. Do not call holdout 'statistically confirmed'. Exploratory paired bootstrap percentile CI [-2.60,-0.32] pp does not override the prespecified primary test.
- Secondary exploratory interactions: AIR +4.56 pp, two-sided exact sign p=.0703125; DVR +0.08 pp, p=1.
- Directional reproduction is scientifically informative; inferential confirmation failed.

## Publication-safe passage (draft)

> To distinguish the effect of adaptive uncertainty scaling from other scheduling mechanisms, we compared CASPER_FULL against an intervention that fixed dispatch-time eta to one, using identical random seeds and simulator settings. The exploratory, ten-seed paired analysis suggested fewer false deadline certifications under S3 network degradation, albeit at the cost of more abstentions and without evidence of a deadline-violation improvement. We then preregistered a disjoint ten-seed (indices 30–39) S2-versus-S3 interaction analysis before execution. In this holdout, S3 false certifications decreased from 40 with fixed eta to 7 with adaptive eta across 2,500 late mission tasks per arm, whereas neither condition produced a false certification in S2. The mean paired interaction was −1.32 percentage points, but the prespecified two-sided exact sign test was not significant (five negative differences, five ties, p = .0625). Thus, although the direction replicated, we do not claim confirmatory evidence for a scenario-dependent effect. Mission deadline-violation differences were negligible. These findings concern the simulation model; generalization requires additional validation.

## Inference boundaries and next step
1. Explicitly distinguish pooled task counts (descriptive) from per-seed inference; 10 seed pairs is small, many ties.
2. Do not retrospectively switch to a one-sided test, reclassify outcomes, or pool exploratory and holdout seeds to create a purported confirmatory result.
3. Additional exploratory or genuinely new pre-registered external validation is allowable, but avoid indefinite p-value hunting.
4. Report coverage versus correctness and mapper overhead; adaptation can reduce wrong certificates while increasing abstention and compute costs.
5. For stronger JPDC contribution, prioritize validation on a second simulation model/realistic trace, sensitivity to calibration and distribution shift, or technically deeper scheduling improvement, without mutating frozen E4.6/E42.

## Provenance
- `jpdc/NEW_CHAT_CONTINUITY_2026-11-02.md`: complete handoff and run provenance.
- `.github/workflows/jpdc-s2-s3-holdout-10seed-once.yml`: exact holdout execution.
- `jpdc/PREREG_S2_S3_DISJOINT_HOLDOUT_2026-11-02.md`: prespecified analysis.
- GitHub Actions run `41524202008`: actual artifacts. Artifact paths within runs: `holdout/before_S2_HIDDEN_COMPUTE_40LOSS.csv`, `holdout/after_S2_HIDDEN_COMPUTE_40LOSS.csv`, corresponding S3 files, `holdout/paired_summary.json`.
