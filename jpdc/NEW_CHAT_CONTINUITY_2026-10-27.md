# CASPER → JPDC new-chat continuity checkpoint (2026-10-27)

## Repository and scientific boundaries
- Repository: https://github.com/afshinyaghoobi/casper-iiot-cloudsim
- Development branch: jpdc-seed0-repro-20261024
- Immutable reference tag: v1.0.0-casper-iiot-e46
- Original frozen 30 seeds are indices 0..29, scientific seeds 4202202600..4202202629. Disjoint validation used indices 30..59.
- Never edit original E4.6 or claim it was re-evaluated after modifications.
- Work on generated experimental E45 isolated patch workflows in the development branch.
- Preferred journal under investigation: Journal of Parallel and Distributed Computing (JPDC), not an accepted submission.

## Confirmed recent experiment actions
- Queue-weighted challenger 30 seeds: 40280807901; paired statistics: 40280910310. CASPER less late DVR in S2/S4, Holm p 0.0075197 / 0.0003216.
- Disjoint seed holdout 30..59: 40281748580; paired statistics 40281798985. Repeated S2/S4 lower DVR in CASPER than queue-weighted heuristic (Holm p 0.0407792 / 0.0007245). Still same synthetic generator, not external validation.
- S3 affected-node family attribution 30 seeds 40350526730, aggregation 40350683076: 4251 of 4294 failing families involved an affected candidate; 43 did not. Entire postshock aggregate, not late FWC.
- S3 residual candidate pilot: 40412923871.
- S3 candidate residual 30 seeds: 40414189982; aggregation 40414300205 succeeded. Candidate misses 4803, affected candidate misses 4752; aggregate network increment 108429.389154045 ms, absolute queue residual 697.269728119 ms, absolute service residual 3776.874380878 ms. These are conditional-on-miss signed/absolute sums, not causal partition of exceedances.
- Newer ALL-candidate (not just failed candidates) S3 eta temporal experiment 40517282086 and statistical aggregation 40517387076 both succeeded. Three windows reported with all candidate count 30273, 30108, 29742; candidate miss rates 0.0615399861, 0.0537066560, 0.0444825499. Mean eta 2.3051200, 2.4181395, 2.4297433; mean network increment ~5.125, 5.143, 5.111 ms; mean absolute queue error 0.177, 0.174, 0.174 ms, mean absolute service error 0.784, 0.774, 0.779 ms. These are aggregate candidate-level windows; ascertain time definitions from actual code before publication claims.
- Last reviewed GitHub Actions runs all completed successfully. Verify current HEAD, artifacts, and integrity in new chat.

## Next scientifically valuable immediate action
1. Inspect 40517387076 artifact JSON/CSV, source workflow and analysis scripts; document exact temporal window semantics, correct denominators, and sampling.
2. Check whether S3 candidate-level calibration failure decreases with eta in time windows, distinguish correlation from causal improvement.
3. Validate audit instrumentation does not change frozen-policy outputs by matching CASPER_FULL S3 late_fwc, late_dvr on same original seeds.
4. Plan a *separate* cross-generator workload or literature-faithful strong scheduling baseline; evidence from synthetic generator and homemade heuristic comparators does not establish broad SOTA superiority.
5. Avoid claiming nominal 99 percent conformal coverage under hidden network shocks. S3 still undercovers.

## Data/report files previously confirmed on branch
- jpdc/S3_RESIDUAL_DECOMP_PILOT.md
- jpdc/S3_COVERAGE_ATTRIBUTION_30SEED_VERIFIED.md
- jpdc/QUEUE_HOLDOUT_30SEED_VERIFIED.md
- jpdc/s3_residual_decomp_patch.py
- Investigate additional new files produced around run 40517387076.

Do not simply propose steps: inspect connected GitHub artifacts, implement one reproducible scientific action, record results with attribution and limitations.
