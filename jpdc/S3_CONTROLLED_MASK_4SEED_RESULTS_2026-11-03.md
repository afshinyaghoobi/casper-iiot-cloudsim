# Controlled S3 network-mask placement: successful four-seed intervention

Date: 2026-11-03. Protocol fixed **before execution** at `jpdc/S3_CONTROLLED_MASK_EXPERIMENT_PROTOCOL_2026-11-03.md` (commit `1e50189`, clarification commit `7fbb579`). Experiment: GitHub Actions **run 41719553340**, all **4/4 jobs success**. Seeds **40,41,42,43** disjoint from preceding indices 0–39; 12 real CloudSim runs, each 30,000 tasks, 80,000 calibration, S3_HIDDEN_NETWORK_50LOSS.

## Reproducibility and scientific invariants
- Original frozen E42 blob `34256ca7bff46f911cf20e8b94278fbd09175746`; E4.6 unchanged.
- Existing generated E45 `jpdc/instrument_s3_network_exposure_generated_e45.py` writes mission placement, actual/nominal network delay, and affected mask.
- New `jpdc/patch_s3_mask_generated_e45.py` (commit `10060a0`) overrides **only S3 six-node affected mask**, identically for all eight policies within each run; no other E42/E4.6 changes.
- `jpdc/controlled_mask_exposure_audit.py` (commit `76cc75c`) preselects masks using baseline **pre-shock** FULL MISSION node counts, 6 smallest vs 6 largest count nodes (disjoint, deterministic tie rule); independently validates scientific-seed identity, 21-node/6-affected mask, 2x affected-node network multiplier after task 10000 and 1x before, official results cardinality, 250 late mission tasks, and **identical pre-shock node placement counts across all three conditions**. All checks passed in four seed jobs.
- Seed artifacts: 40 `13272215535`, 41 `13271273184`, 42 `13270784276`, 43 `13272485400`. Each artifact includes original baseline, LOW and HIGH official CSV, network traces, masks, selected pre-shock counts and `paired_results.json`.

## Main intervention checks (seed-level means; each arm 4 x 250 = 1000 late mission tasks)
| Outcome | LOW affected-node placement | HIGH affected-node placement | HIGH minus LOW |
|---|---:|---:|---:|
| Pre-shock mission-node overlap with future mask | 0% | 99.854% | +99.854 pp |
| Actual post-shock mission task exposure | 0.051% | 99.656% | +99.605 pp |
| Mean added postshock network delay (ms) | 0.0032 | 12.8762 | +12.8731 |
| FULL late_eta | 1.0840 | 3.0000 | +1.9160 |
| FULL late_far (all late mission tasks) | 0/1000 = 0% | 3/1000 = 0.3% | +0.3 pp |
| FULL late_air | 14/1000 = 1.4% | 125/1000 = 12.5% | +11.1 pp |
| FULL late_dvr | 1/1000 = 0.1% | 45/1000 = 4.5% | +4.4 pp |
| FULL late_fwc (counterfactual family bound coverage) | 992/1000 = 99.2% | 835/1000 = 83.5% | -15.7 pp |

For actual outcomes, HIGH minus LOW `late_eta`, `late_air`, `late_dvr` are positive in all four seeds, `late_fwc` negative in all four seeds, exact two-sided sign-test p=.125 each (EXPLORATORY, low-powered). FAR higher in only two seeds, two ties (p=.5). HIGH versus LOW `post_exposure` achieved 4/4, but the sign test on the deliberately engineered manipulation is not an independent confirmation of scientific benefit.

## Mask and outcome detail
- Seed40: LOW late eta 1.051, HIGH 3; late_dvr 0 vs 0.064, late_air 0.032 vs 0.224.
- Seed41: LOW late eta 1.104, HIGH 3; late_dvr 0.004 vs 0.044, late_air 0.008 vs 0.124.
- Seed42: LOW late eta 1.106, HIGH 3; late_dvr 0 vs 0.028, late_air 0 vs 0.052.
- Seed43: LOW late eta 1.074, HIGH 3; late_dvr 0 vs 0.044, late_air 0.016 vs 0.100.

## Interpretation — carefully delimited
This is a **controlled physical exposure contrast** establishing that different placements of six equally damaged nodes can generate dramatically different actual stress and corresponding E17 responses with all other settings and seed held fixed. It is not an intervention on eta itself: higher exposure naturally increases deadline misses. It does **not** show that adaptive eta reduces missed deadlines or infer general population risk under random masks. HIGH/LOW are intentionally selected extremes; no assumption of random mask assignment to natural workloads is warranted. Post-shock exposure is policy-dependent and should not be adjusted for as an ordinary exogenous confounder. Do not use these four seeds to retroactively alter inference for the prior preregistered holdout (`p=.0625`).

## Recommended next scientific step
Evaluate the *same* LOW and HIGH S3 mask states under both adaptive FULL and eta-clamped FULL with strict cross-policy invariant checks. This can separate effects of induced stress from effects of eta adaptation within the controlled-exposure experiment without altering frozen code. Any resulting inference is exploratory; propose independent validation in other simulator/traces.

Reproducible local result package `/mnt/data/jpdc_s3_controlled_mask_4seed_2026_11_03.zip` (local session only). Long-term source is GitHub Actions run 41719553340 and the repo analysis tools.
