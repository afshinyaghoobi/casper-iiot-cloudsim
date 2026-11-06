# JPDC Stage26–26b — causal WAIT score calibration UNIT and archived prequential replay VERIFIED (2026-11-06)

## Actual evidence, strict scope
- Prospective standalone method protocol `jpdc/STAGE26_CAUSAL_WAIT_CALIBRATION_PREREG_2026-11-06.md`, committed **before** Stage26 unit outcomes (commit `fb6536fdd49d19fcec399b63c065d4f4ecd9d802`). Code `jpdc/causal_wait_calibration_stage26.py` and `jpdc/test_causal_wait_calibration_stage26.py`. [Stage26 unit CI 42268358913](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42268358913) **SUCCESS**, exact duplicate log, Stage24/22/15 regressions pass. Frozen original E42 Git blob `34256ca7bff46f911cf20e8b94278fbd09175746` unchanged.
- Frozen original Stage25 [42254782412](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42254782412): one DEVELOPMENT seed89, independent native Python FCFS, S2/S3 x PRED_GREEDY/CASPER_FULL, 4 x12000 **dependent task-policy records**; original frozen Stage6 exact parity. WAIT-only residual label created at **CPU finish** after dispatch backlog prediction, no network contamination.
- Additional archive-only evaluation protocol `jpdc/STAGE26B_ARCHIVED_WAIT_PREQUENTIAL_PREREG_2026-11-06.md`, commit `33578a9b0c2ea89c60f17f1def6e74ddc6c52073` before replay outcomes (data seed89 already examined). [Stage26b real CI 42268581195](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42268581195) **SUCCESS** `JPDC_STAGE26B_ARCHIVED_CAUSAL_WAIT_REPLAY_PASS` and `JPDC_STAGE26B_IMMUTABLE_PREQUENTIAL_REPRODUCIBLE_PASS`. Reads only original Stage25 saved artifact; no new simulation/seed, repeated output byte identical.

## Exact Stage26 method as actually tested
- A task's immutable predicted `VirtualQueue` wait and telemetry age are recorded at dispatch, with NO actual waiting label known at that moment.
- Signed WAIT residual enters a context window only after **CPU finish**, in delivery order; no rewinding current decision time, no pending-task score leakage. Strict acceptance of finite clocks, class, node, unique task ID and measured `actual_wait = service_start - arrival`. A late-arriving CPU label can update the model at its delivery time but never retroactively change an issued interval.
- Three telemetry-age bands [0,10), [10,25), [25,+inf) ms x task class NORMAL/HIGH/MISSION. Frozen source context `native_python_strict_fcfs_vq_telemetry50ms`, bounded last-200 CPU-delivered signed labels per stratum; require at least 40 before issuing a central empirical `floor(.05*(n-1))` lower and `ceil(.95*(n-1))` upper order-statistic interval. **Always `certified=False`, `descriptive_only=True`**, even when 40 samples exist. No CPU residual integrated; this is WAIT-only, not the full Stage24 nonnetwork additive q.

## Immutable Stage26b four-arm prequential replay results
| Scenario | Policy | Total decisions | Issued intervals | Abstentions due sparse context | Empirical future signed WAIT inclusion rate among issued |
|---|---|---:|---:|---:|---:|
|S2 compute|PRED_GREEDY|12000|11638|362|91.295755%|
|S2 compute|CASPER_FULL|12000|11638|362|91.321533%|
|S3 network|PRED_GREEDY|12000|11638|362|91.347311%|
|S3 network|CASPER_FULL|12000|11638|362|91.416051%|

The target nominal central interval is 90%, but these are **post-hoc on previously examined same seed89**, not untouched validation or statistical coverage guarantees. Data are dependent, nonexchangeable queues; task-level count is NOT scientific n=48k. The policy/scenario arms share source workload and selection-dependent queues. Issue-time outputs are chronologically causal, but method choices (band edges, window, min count) were not independently validated prospectively on untouched science seeds.

### Crucial local undercoverage / variability
In S2 PRED_GREEDY MISSION context telemetry age10–25ms: **105 of 124** eligible labels inside empirical interval, inclusion **84.6774%**. S2 CASPER_FULL in same stratum 105/124, 84.6774%. Similar 84.6774% in S3 MISSION 10–25ms. S2 HIGH 10–25ms: PRED_GREEDY 382/426 =89.6714% (CASPER_FULL 379/426 =88.9671%). Normal 0–10ms overcovers (~94%). Worst recorded missed interval value for S2 PRED_GREEDY NORMAL 25+ms is 15.801ms and CASPER_FULL 15.905ms. These show actual context heterogeneity and tail risk, so **aggregate nominal 91% does not establish per-MISSION safety**. Overall comparisons have no p-values.

## What has NOT been done
- No proof of exchangeability, sequential or conditional conformal validity, and no calibrated probability of coverage out-of-distribution. Central historical signed quantiles are not hard deterministic error envelopes.
- No CPU service-time prediction error term; Stage24's **full** nonnetwork q residual still lacks data and validation. No calibrated network interval guarantees either.
- No Stage24/Stage26 physical policy integration or improvement claim. Blindly feeding Stage26 output into Stage24 as a hard certificate would be incorrect.
- No independent external-trace/CloudSimPlus equivalence; Python strict FCFS vs Java CloudSimPlus v8.5.7 SpaceShared original max-wait fidelity gate remains **FAIL**, 9.12140093294972ms >5ms. Stage18–21 source inspection explained mechanism, not passing parity.
- No scientifically established novel JPDC algorithm or acceptance likelihood. Stage16 Stage15 S3 vs FULL n8 p=.375 (not significant), S2 harm; Stage17 probing n2 null miss differences; Stage23 network-only robust seed88 S3 16 vs FULL33 but S2 14 vs FULL9 (one development seed, not independent).

## Next defensible work
1. Create **separate CPU-service-only signed prediction residual** at dispatch and CPU finish in native source, avoiding waiting/network double-counting, with source Stage6 exact parity.
2. Explicitly freeze new untouched validation cohort, inspect prior code for seed usage, use blocked chronological train/calibration/holdout by independent source seeds; monitor MISSION context coverage and worst-case near deadline.
3. Validate actual joint total nonnetwork q and e intervals under nonstationarity and model queue differences; establish principled uncertainty/risk definition and stronger published baselines before changing scheduling policy or claiming a JPDC-level contribution.
