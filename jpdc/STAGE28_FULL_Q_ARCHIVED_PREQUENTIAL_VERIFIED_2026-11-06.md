# JPDC Stage28 — full nonnetwork q causal prequential development replay VERIFIED, 2026-11-06

## Provenance and reproducibility
- Stage28 protocol **committed before results**: `jpdc/STAGE28_FULL_Q_CAUSAL_PREQUENTIAL_PREREG_2026-11-06.md`, commit `c1e628ce1932811442c9e5943ed11d79fd190bc6`. No new hidden seed selection or retrospective threshold tuning.
- Causal full `q=(actual WAIT - predicted WAIT)+(actual CPU - predicted CPU)` controller `jpdc/causal_nonnetwork_calibration_stage28.py`. At dispatch knows only predicted backlog, nominal CPU, class, telemetry age; actual values enter only after causal CPU finish. No E2E network residual mixed into q. Missing/under-40-sample contexts abstain; rolling last200 delivered labels per 9 groups (3 class × 3 telemetry-age bands); central empirical 5th–95th order-statistics. **Always descriptive_only=True, certified=False**. No Stage24 physical scheduling intervention or claimed deterministic bounds.
- Unit file `jpdc/test_causal_nonnetwork_calibration_stage28.py` exercises no future labels, under-40 abstention, negative signed CPU residual, completing tasks out-of-dispatch order, context independence, last200 rolling, immutable prior issued intervals, invalid clock/id/node and adversarial source regime shift counterexample. Prior Stage26 and Stage24 regressions PASS.
- Archived Stage27 `jpdc/replay_stage28_archived_full_q.py` reads **original source artifact only** from [Stage27 native run 42269844289](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42269844289), which had original Stage6 exact policy JSON parity and 48k CPU-finish-labeled task-policy traces with full CPU+WAIT algebra.
- [Stage28 GitHub Actions 42277500263](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42277500263) **SUCCESS**: Stage28 unit and Stage26/24 regression checks pass, all four archived source arms replayed in causal clock order, all 48k recorded q error identities exactly matched, archived prequential JSON and logs repeat byte identically, marker `JPDC_STAGE28_FULL_Q_PREQUENTIAL_BYTE_REPRODUCIBLE_PASS`. Original E42 source frozen blob `34256ca7bff46f911cf20e8b94278fbd09175746` unchanged. No new source physics run; original E4.6 unchanged.

## Complete archived DEVELOPMENT seed90 primary descriptive results

| Scenario | Frozen policy | Original tasks | Issued intervals | Sparse abstentions | Empirical inclusion among issued | Postshock inclusion (tasks10000–11999) |
|---|---|---:|---:|---:|---:|---:|
|S2 hidden CPU 40%-loss|PRED_GREEDY|12000|11638|362|**88.6578%**|**1679/2000 = 83.9500%**|
|S2 hidden CPU 40%-loss|CASPER_FULL|12000|11638|362|**89.4655%**|1777/2000 = 88.8500%|
|S3 hidden network 50%-loss|PRED_GREEDY|12000|11638|362|**89.7491%**|1806/2000 = 90.3000%|
|S3 hidden network 50%-loss|CASPER_FULL|12000|11638|362|**89.7147%**|1806/2000 = 90.3000%|

All PRE-shock tasks 0–9999: 362 abstained, 9638 eligible. PRE total inclusion S2/S3 GREEDY8639/9638=89.6348%, FULL8635/9638=89.5933%. S2 postshock Greedy had **239 high-end misses, 82 low-end misses**, worst interval exceedance +42.9877ms. S2 FULL had **110 high,113 low** with worst exceeding interval by **146.8922ms**, reflecting rare extreme CPU-only residual; no deletion. S3 postshock each 1806/2000 inclusion and manageable but nonzero violations.

### Undercoverage by task class / shift severity (postshock)
- S2 PRED_GREEDY **HIGH 212/315 = 67.3016%**, MISSION **86/101 = 85.1485%**, NORMAL1381/1584=87.1843%; significant-looking differences are *descriptive, no hypothesis test*. The strongest issue is hidden CPU fault and changing queue prediction errors under PRED_GREEDY.
- S2 CASPER_FULL HIGH266/315=84.4444%, MISSION93/101=92.0792%, NORMAL1418/1584=89.5202%; still HIGH undercovers and rare huge NORMAL outliers.
- S3 PRED_GREEDY HIGH284/315=90.1587%, MISSION92/101=91.0891%, NORMAL1430/1584=90.2778%.
- S3 CASPER_FULL HIGH282/315=89.5238%, MISSION90/101=89.1089%, NORMAL1434/1584=90.5303%.
- Important: this is **one seed** already seen in Stage27; 48k dependent task-policy labels ≠ 48k independent scientific replicates. Exact task classes and policy exposure are model-generated, not representative of real factory traces.

## Interpretation and major limits
1. Under a sudden unobserved compute-fault regime, a signed empirical 90% central interval calibrated on previous completed jobs does **not** achieve its nominal aim, particularly HIGH and MISSION for S2 GREEDY. An interval marked available is not a safety certificate, even though predictions were generated chronologically with no future labels.
2. Stage26b WAIT-only archived seed89 had ~91.3% aggregate inclusion, but Stage28 **FULL q** includes a large CPU uncertainty component and loses inclusion under S2. Do NOT compare percentages as a scientifically paired causal experiment because methods/used seeds differ.
3. No `certified=True`, no conformal conditional coverage or finite-sample exchangeability proof, no fixed hard deadline guarantee, no valid Stage24 external queue bounds, no new policy performance or journal novelty. Source class, age bins, min40, window200, central90% are **development design choices** and not validated as transferable.
4. Strict Python-FCFS vs Java CloudSimPlus 8.5.7 SpaceShared original queue fidelity remains **FAILED** max wait 9.1214ms > predeclared 5ms. Stage18–21 source audits explained implementation mechanisms, not independent policy parity.
5. Prior empirical Stage16 older Stage15 multi-seed S3 exact sign p=.375 (not significant) and S2 harm; Stage17 probe ablation n2 no miss-count improvements; Stage23 Stage22 network-only seed88 S3 16 vs CASPER_FULL33 but S2 14 vs FULL9, ONE development seed. None override these negative results.

## Science-first go/no-go
- Stage28 = successful **causal engineering/diagnosis**, failed conditional calibration adequacy during S2 shift, and not an approved input for deterministic robust domination.
- Next **pre-register prospectively independent source seed cohort** (exclude all prior used seed83–90 and 301–308), fixed per-seed S2/S3 metrics, high/mission coverage minima, block-aware confidence and source/regime-shift performance. Never adjust parameter definitions after observing Stage28 just to claim nominal rate.
- A practical *new* algorithm must handle detection and abstention/recovery when CPU errors shift, quantify false alarm and coverage delay and integrate network E2E uncertainty under explicitly defined assumptions. Need published robust/delayed-feedback and deadline scheduling baselines, alternate workload/queue physical engine/real trace validation. Until then JPDC is **not ready for submission**.
