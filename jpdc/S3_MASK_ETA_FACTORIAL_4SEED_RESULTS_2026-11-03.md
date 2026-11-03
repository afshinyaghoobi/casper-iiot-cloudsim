# Controlled S3 mask × eta intervention: exploratory four-seed results (2026-11-03)

## Study provenance and scientific invariants
The registered analysis protocol was committed **before** the experiment: `jpdc/S3_MASK_ETA_FACTORIAL_PROTOCOL_2026-11-03.md` at `42ece48`. Fixed seed indices 40–43 and exact LOW/HIGH masks carried over from the *pre-shock-routing-based* experiment `41719553340`. GitHub Actions **41724362605**, workflow commit `2426279`, **4/4 successful jobs**, 16 full CloudSim deployments (LOW/HIGH × adaptive/clamped for each seed). Each deployment: calibration=80000, tasks=30000, S3 network 50% retained bandwidth on 6/21 nodes. The frozen original E42 source blob `34256ca7bff46f911cf20e8b94278fbd09175746` was verified. E4.6 unmodified.

The intervention `jpdc/eta_clamp_casper_full_patch.py` changes **only CASPER_FULL effective dispatch eta to 1** in generated E45 code, leaving others' science unchanged. In each of 8 mask-seed pairs, workflow asserted nonintervened-policy scientific column parity (excluding mapper clock timing) and equality of clamped FULL to HEALTH_STATIC scientific metrics. All passed.

GitHub artifacts:
- seed40 `13273915636`
- seed41 `13273755094`
- seed42 `13271869726`
- seed43 `13272339554`

## Descriptive counts (four seeds; 250 late MISSION tasks/seed/arm = 1000 per row)
| Mask | Policy state | Incorrect certificates | Abstentions | Family-wide counterfactual coverage | Deadline violations | Mean late eta |
|---|---|---:|---:|---:|---:|---:|
| LOW | FULL adaptive | 0 | 14 | 992 | 1 | 1.0840 |
| LOW | FULL eta=1 | 0 | 11 | 990 | 1 | 1.0000 |
| HIGH | FULL adaptive | 3 | 125 | 835 | 45 | 3.0000 |
| HIGH | FULL eta=1 | 33 | 11 | 3 | 44 | 1.0000 |

The high-exposure mask increases actual network stress by construction. Under HIGH, effective eta adaptation reduces incorrect certifications **33 → 3 per 1000 opportunities** (90.9% relative reduction), with **11 → 125 abstentions**, **3 → 835 family-wide covered cases**, and **44 → 45 actual deadline misses**. It is false to claim this is an improvement in on-time completion. LOW mask effects are nearly zero.

## Mask × eta effect interaction (prespecified exploratory)
For each seed and each metric, define `interaction = [adaptive - eta=1]_HIGH - [adaptive - eta=1]_LOW`. Reported seed-level signed test uses seed (not tasks) as independent unit.

| Metric | Mean interaction (percentage points) | Seed sign counts | Exact two-sided sign p |
|---|---:|---|---:|
| `late_far` (incorrect certs / all late mission tasks) | **−3.00 pp** | 4 negative, 0 positive, 0 ties | **.125** |
| `late_air` (no issued certificate / all late mission tasks) | **+11.10 pp** | 4 positive | **.125** |
| `late_fwc` (counterfactual top-3 family covered) | **+83.00 pp** | 4 positive | **.125** |
| `late_dvr` (actual deadline misses / all late mission tasks) | **+0.10 pp** | 1 positive, 3 ties | 1.0 |

`late_far` is *not* conditional error among issued certificates, while `late_fwc` is not certificate precision. Descriptive pooled counts do not constitute 1000 independent experimental replications. With n=4, even all four concordant differences give two-sided exact sign p=.125.

## Interpretation for JPDC
This controlled-factorial simulation provides additional **mechanistic** evidence that the certificate-reliability/abstention tradeoff of adaptive eta depends sharply on **realized exposure** to network failure. It does **not** establish a general scheduling performance gain: deadline misses remained virtually unchanged by eta itself. The mask selection was based on pre-shock routing on these same four seeds, so although fixed before outcome comparisons, the resulting HIGH/LOW intervention is extreme and deliberately selected, not randomized sampling of network failure masks. This experiment remains **exploratory** and does not overturn the earlier disjoint preregistered 10-seed holdout whose primary sign test was not significant (p=.0625).

## Reproduction and next step
Workflow: `.github/workflows/jpdc-s3-mask-eta-factorial-4seed-once.yml`. The four GitHub Actions artifacts contain full CSVs and logs from all 16 runs, validated `paired_summary.json`, and frozen mask assignments. Local convenience archive: `/mnt/data/jpdc_s3_mask_eta_factorial_4seed_2026_11_03.zip` with per-seed CSV and statistical analysis. Paths under /mnt/data may not persist across chat sessions, but artifact IDs and committed protocol do.

Next scientifically justified step: integrate exposure measurement and mask-controlled intervention into the JPDC Results/Discussion accurately, then consider an independent second simulator or field-inspired network trace. Do not add seeds simply to chase p<.05.
