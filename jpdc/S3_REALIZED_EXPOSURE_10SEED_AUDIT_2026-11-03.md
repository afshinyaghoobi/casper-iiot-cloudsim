# S3 real-network exposure, baseline overlap and adaptive eta: complete ten-seed exploratory audit

Date: 2026-11-03. This is a *descriptive mechanism audit*, not a new confirmatory significance test. Cohort fixed **before** executing remaining traces in `jpdc/EXPOSURE_AUDIT_10SEED_PROTOCOL_2026-11-03.md` (commit `86212067`).

## Grounded execution
- Already verified seeds 7 and 18: workflow `41685852046`, success artifacts seed7 `13255386941`, seed18 `13253124265`.
- Remaining eight predetermined indices 0,1,5,9,13,21,27,29: run `41697794315`, **8/8 completed success**; artifacts accessible from that run.
- Source scientific control: frozen E42 Git blob `34256ca7bff46f911cf20e8b94278fbd09175746`, E4.6 unchanged; only generated E45 logging via `jpdc/instrument_s3_network_exposure_generated_e45.py`. 80,000 calibration, 30,000 deployment tasks, S3 50% network retention, six affected nodes among the actual **21 nodes**.
- Per-seed FULL trace mask and individual MISSION network exposures reconciled against official `results.csv` count. No filtering of seeds based on results.

## Seed-level results
`pre_overlap` = proportion of MISSION assignments *before* task 10000 on the six nodes that will later be degraded; `post_exposure` = proportion *after* task 10000 actually assigned degraded nodes. Both use real traces; post-exposure is policy dependent.

| Seed index | Pre overlap % | Post exposure % | Mean network shock increment (ms; post MISSION) | FULL late eta | FULL late FAR |
|---|---:|---:|---:|---:|---:|
| 0 | 35.3 | 38.8 | 5.974 | 3.000 | 0.000 |
| 1 | 35.1 | 31.4 | 4.672 | 3.000 | 0.000 |
| 5 | 0.0 | 0.3 | 0.016 | 1.080 | 0.000 |
| 7 | 0.0 | 0.0 | 0.000 | 1.000 | 0.000 |
| 9 | 52.1 | 50.0 | 5.513 | 3.000 | 0.008 |
| 13 | 30.4 | 33.6 | 5.948 | 3.000 | 0.008 |
| 18 | 94.2 | 94.0 | 14.665 | 3.000 | 0.020 |
| 21 | 85.9 | 81.6 | 9.719 | 3.000 | 0.000 |
| 27 | 9.1 | 11.3 | 2.068 | 3.000 | 0.000 |
| 29 | 61.5 | 62.7 | 13.140 | 3.000 | 0.048 |

## Descriptive correlations across ten seed-level units
- Pre overlap vs post exposure: Pearson **r=0.9970**, Spearman **rho=0.9848**.
- Pre overlap vs FULL late eta: Pearson **r=0.6394**, Spearman rho=0.6941.
- Post exposure vs FULL late eta: Pearson **r=0.6566**, Spearman rho=0.7006.
- Post exposure vs FULL post FAR: Pearson r=0.4631, Spearman rho=0.4815; vs FULL late FAR: r=0.4857, rho=0.6169.

All are descriptive correlations without confirmatory p-values. Eta saturates at three for 8/10 seeds, so linear correlation is not a calibrated dose-response estimate. Seed27 has 11.3% post mission exposure but eta=3; nonzero exposure need not imply proportional eta. Seeds5 and7 show near-zero/zero exposure and late eta near one.

## Interpretation and experimental design implication
The *placement–failure-mask overlap* is a major hidden driver of effective S3 scenario intensity. The same nominal loss rate and number of damaged nodes can produce nearly no realized stress in one seed and near-universal task exposure in another. Crucially, the pre-shock overlap is measured before the shock and strongly predicts the post-shock exposure in this experimental cohort, which offers a useful, predeclared stratification variable for *future separate* validation.

This is **not** evidence of causal effects of pre-shock overlap; seed influences both mask and workloads, while post-shock exposure is affected by policy routing. Conditioning on measured post-shock exposure in causal treatment comparisons could create selection/collider bias. Do **not** discard low-exposure seeds after viewing data, retrospectively reweight the prior confirmatory holdout, or claim this resolves previously failed confirmatory p=.0625. A next genuinely independent exposure-controlled experiment should preassign mask overlap based on baseline routing on distinct seeds and verify mask provenance *before* perturbation.

## Reproducibility
GitHub run `41697794315` contains raw `mask.csv`, `mission_network.csv`, official `results.csv`, and logs for all eight new seeds. Earlier run `41685852046` contains the other two. Locally generated audit `/mnt/data/jpdc_exposure_tenseed_analysis.py` calculates all counts and checks frozen scenario multipliers; `/mnt/data/jpdc_s3_exposure_10seed_2026_11_03/` contains CSV and JSON results. These local paths may not persist across chats; GitHub Actions artifacts are the durable source.
