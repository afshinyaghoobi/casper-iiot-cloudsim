# Exploratory factorial interaction: controlled network mask x adaptive eta

Date: 2026-11-03. This document precedes experiment execution. Earlier pre-shock route-derived masks and 4 seed indices are FROZEN; no mask modification or seed exclusions based on outcome.

Scientific seeds: deployment indices 40,41,42,43, generated scientific seed = 4202202600 + index.
Fixed LOW six-node mask for all 4 indices: `0,1,2,3,4,5`. Fixed HIGH masks:
- index 40: `9,12,14,15,17,18`
- index 41: `12,14,15,16,17,20`
- index 42: `12,14,15,16,17,20`
- index 43: `13,15,17,18,19,20`

These masks were selected from pre-shock CASPER_FULL node frequencies in run `41719553340`, NOT from postshock result metrics. Source selection experiment provenance `jpdc/S3_CONTROLLED_MASK_EXPERIMENT_PROTOCOL_2026-11-03.md`. New experiment must check masks exactly and compare adaptive versus eta=1 under each mask with matched seed.

Each of 4 independent seeds has 4 actual CloudSim S3 runs (LOW/HIGH × adaptive / effective dispatch-time eta=1), totaling 16 runs. Each run retains 80,000 calibration tasks, 30,000 deployment tasks, six of 21 network-damaged nodes (bandwidth retained 50%), all eight original policies. Only CASPER_FULL effective eta is clamped to 1 via `jpdc/eta_clamp_casper_full_patch.py`; all other policies should remain scientifically unchanged. Verify that clamp-FULL science output equals HEALTH_STATIC (excluding timing), both masks. E42 git blob `34256ca7bff46f911cf20e8b94278fbd09175746` and E4.6 immutable.

Estimand by seed for each metric = (FULL adaptive - FULL eta=1) at HIGH mask minus (FULL adaptive - FULL eta=1) at LOW mask. Predefined descriptive metrics `late_far`, `late_air`, `late_dvr`, `late_fwc`; eta adaptation effect on certification is primary mechanistic interest, deadline misses required safeguard. Report each seed and all counts as 250 late mission opportunities per policy/mask/seed. Two-sided exact sign test optionally exploratory only, n=4 severe low power; this is not confirmatory, is *not* independent of previous selection of masks, and cannot repair preregistered 10-seed Holdout p=.0625.

Do not exclude zero-difference seeds, change outcome denominator, or interpret counters `late_fwc` as certification accuracy. No conclusions until all four job artifacts and scientific parity assertions are confirmed.
