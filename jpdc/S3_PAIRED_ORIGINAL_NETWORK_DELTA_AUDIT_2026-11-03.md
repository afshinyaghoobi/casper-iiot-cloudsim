# JPDC task-paired S3 original network trace audit — 2026-11-03

## Verified new descriptive result
Using the ORIGINAL physical controlled-mask GitHub Actions run `41719553340`, seed indices 40–43 (artifact IDs 13272215535, 13271273184, 13270784276, 13272485400), compared baseline vs LOW/HIGH for every matching S3 postshock CASPER_FULL mission task. This is a network trace audit, **not** a new CloudSim run.

| Comparison against the baseline's own affected-node mask | postshock mission task pairs | different routed nodes | tasks with different realized network delay | mean paired realized network delay delta |
|---|---:|---:|---:|---:|
| LOW minus baseline | 4040 | 15 | 355 | -1.196500068 ms |
| HIGH minus baseline | 4040 | 0 | 3685 | +11.676369053 ms |

The 355 changed network delays in LOW comprise 340 tasks keeping the same selected node, plus 15 tasks that changed selected node. In HIGH all 3685 changed network delays occur with identical selected node across arms. Across both arms, the pre-shock matched task-index control continues to hold for route, nominal/realized network delay, multiplier and the **predicted** value `pred[j]` (NOT observed end-to-end latency).

### Per-seed postshock network difference
| Seed | n | LOW rerouted | LOW mean delta ms | HIGH rerouted | HIGH mean delta ms |
|---|---:|---:|---:|---:|---:|
| 40 | 1031 | 0 | -0.612104383 | 0 | +11.733977282 |
| 41 | 1004 | 15 | -2.358091314 | 0 | +10.909110919 |
| 42 | 975 | 0 | -0.655613585 | 0 | +11.951621395 |
| 43 | 1030 | 0 | -1.161197798 | 0 | +12.106040947 |

## Critical design/interpretation guardrail
The experiment's **baseline has its own six-node affected shock mask**. Thus this is a *paired contrast of two distinct shock masks*, not a comparison between a shocked network and an unshocked counterfactual. That is why LOW-baseline can have a negative mean realized network delay delta, despite LOW having almost no exposure to its own selected six damaged nodes. Never interpret HIGH-baseline +11.676ms as an absolute added network penalty compared with a healthy network. For that latter interpretation one would need an explicitly unshocked matched arm, which this experiment did not supply.

The total of 4040 is descriptive task pairs, not 4040 independent statistical seeds. Neither actual end-to-end completion latency nor deadline outcome is recorded in `mission_network.csv`: last field `pred[j]` is a prediction. The observed outcome logger must be independently verified before outcome-level claims.

## Reproduction and source validation
- Original four physical artifacts: 13272215535/13271273184/13270784276/13272485400 from run 41719553340.
- New stdlib source `jpdc/audit_paired_s3_network_deltas.py`, commit `8e4f0825618c6bf27cf3e8e16e7806db29b7b614`.
- Locally executed a verbose equivalent against eight existing original Actions ZIPs, yielding the table above and fail-closed physical network checks; output saved as `/mnt/data/jpdc_next/paired_task_network_summary.json` and task-paired 12,098? rows in `/mnt/data/jpdc_next/paired_task_network_delta.csv` (the exact file row count can be checked). Do not claim the committed compact script has been separately executed under CI.
- Also reran the original 2100-assertion Actions audit from the prior archived Python code against the original eight artifacts: PASS all four seeds, 2100 assertions. The earlier locally reconstructed observed-outcome synthetic validator test also passed, but this does not establish new CI/CloudSim outcome evidence.

## Next scientific step
Acquire actual instrumented S3 CloudSim sidecar Actions job logs and artifact, validate the observed latency+certification CSV parity, and only then design and test an independent replay under predeclared assumptions. Maintain original non-significant preregistered 10-seed holdout p=.0625 and exploratory factorial p=.125. Do not change frozen E42 or E4.6.
