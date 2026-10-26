# S3 hidden-network conformal-family coverage attribution — verified 30 seeds

## Provenance
Experiment run https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/40350526730 — 30 of 30 successes.
Aggregation run https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/40350683076 — success.
Code: jpdc/s3_attribution_patch.py and jpdc/analyze_s3_attribution30.py.
Only generated exploratory E45 is instrumented; frozen E4.6 is unchanged.

## Observed aggregate counts (30 scientific seeds 4202202600 through 4202202629)
- Post-shock mission families: 30,041.
- Families with >=1 affected node among the ranked Top-3: 18,754.
- Families with >=1 conformal upper-bound failure: 4,294.
- Families whose misses included >=1 network-affected candidate: 4,251.
- Families with miss but **no** affected-candidate miss: 43.
- Ranked candidate evaluations: 90,123 (three per post-shock mission).
- Evaluations on network-affected candidates: 27,311.

Of all **failed** post-shock families, 4,251 / 4,294 = 98.9986% involved at least one bound violation at a network-affected candidate. The remaining 1.0014%, 43 families, did not. This corrects the overgeneralization that all failures arise at affected candidates: in the earlier three-seed pilot all 700 misses did, but that is not universal.

Across all post-shock mission families, 4,294 / 30,041 = 14.2931% had >=1 violation. This is a **full post-shock family miss frequency**, NOT the late-window family-wise coverage metric reported in the original E4.6 summary; avoid conflating them. Affected candidate presence itself is not sufficient for failure (18,754 families contained one, but only 4,251 exhibited an affected-candidate miss).

## Interpretation
Hidden network degradation is strongly associated with conformal family misses, and affected candidate nodes account for virtually all observed failure families in this synthetic S3 setting. It is not exclusive: 43 families missed without affected-node violations. This is instrumentation-based attribution, not a causal intervention or definitive decomposition into queue versus network error.

No 99% conformal coverage guarantee is established under S3. Next: decompose per-candidate latency residual into known nominal network, unobserved network multiplier, predicted backlog error, and service-noise contribution, including temporal adaptation eta. Avoid posthoc data-dependent tuning without fresh validation.
