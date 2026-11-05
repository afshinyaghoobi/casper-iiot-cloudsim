# JPDC Stage11 — full original-native physical E2E network epoch shadow VERIFIED, 2026-11-05

## Status upfront

For the FIRST time in this new follow-on, the Stage10 **normalized network slowdown and E2E-delivered change-epoch observer** ran on FULL source-generated, independent native **strict-FCFS 21-node queues** instead of only constructed algebraic fixtures. It was deliberately **shadow-only**. Thus it detected network state changes from completed physical observations but did **not** determine routing choices, health E17 scores, network probing, certificate status or any deadline outcome. The result demonstrates instrumentation/observation fidelity **not deadline performance benefit or validated new JPDC scheduler**.

The original first-paper CASPER E42 source remains git blob `34256ca7bff46f911cf20e8b94278fbd09175746`, E4.6 unchanged, and all Stage6 original policies untouched. No YAFS, external trace or CloudSimPlus physical queue parity is claimed.

## Before-data preregistration and frozen matrix

Original protocol `jpdc/STAGE11_PHYSICAL_NETWORK_EPOCH_SHADOW_PREREG_2026-11-05.md`, commit `1ef1348b7119e4ece09e1a3ebef10b98cf47dffc`, pre-registered previously unused **development seed index83** (now observed, never eligible for a confirmatory holdout), 80k independently generated native physical calibration for the original FULL policy, exactly two scenarios S2 hidden compute40loss and S3 hidden network50loss, exactly four original routing policies `PRED_GREEDY`, `CASPER_FULL`, `NEW_NETWORK_RESIDUAL` and `NEW_NETWORK_RESIDUAL_PROBE`, and exactly 12000 task-policy physical outcomes per cell = **8 runs, 96000 task-policy observations, ONE independent scientific seed**. Fixed observer params `L_normalized=.0001 per ms`, `epsilon_normalized=0`. These parameters are synthetic conditional diagnostic values, NOT learned/validated from the source's real-world dynamics. Do not tune after seed83 outcome.

A standalone copy of the existing Stage6 strict-FCFS physical engine added **only** observer calls after actual E2E delivery: `jpdc/independent_physical_network_epoch_shadow_stage11.py`, commit `300e588eb07646d397154831ba213d49e44aea0e`. Actual net duration is known internally to physical engine at dispatch but never enters observer until independent E2E event `CPU_finish+actual_network_duration`; observer measurement-generation timestamp is CPU finish in this stylized postCPU model. Observer receives **node, actual completed network duration, nominal task-node network duration, CPU finish timestamp, E2E delivery timestamp**—NOT `affected_nodes` or task-index shock marker. Source truth labels are used **only after action** for offline scoring. Exact original simulator end-to-end feedback/E17 and original 1% NORMAL probe policies continue unchanged.

Run driver `jpdc/run_physical_network_epoch_shadow_stage11.py`, commit `0f859004461a592db4a4e0848139c650715336c5`, executes each policy/scenario in both new shadow engine and frozen original Stage6 engine, asserts **all old output JSON fields exactly equal** (not tolerance), and checks task/feedback conservation and offline affected-node diagnostics. Entire eight-arm experiment repeated from source and original JSON `cmp` byte identical under workflow `.github/workflows/jpdc-stage11-physical-epoch-shadow.yml`, commit `1781d1eee958a7cf05145a3b0d828b08ea694535`.

### REAL original full physical CI outcome

**GitHub Actions `42093920896` COMPLETED SUCCESS**, job `127478869996`, original source artifact **`13446096806`**. Eight markers `JPDC_STAGE11_SOURCE_POLICY_EXACT_REGRESSION_PASS` for S2/S3 × all four policies; `JPDC_STAGE11_NATIVE_SHADOW_E2E_DIAGNOSTIC_PASS`, `JPDC_STAGE11_FULL_PHYSICAL_SHADOW_BYTE_REPRODUCIBLE_PASS`, `JPDC_STAGE11_ORIGINAL_SHADOW_ARTIFACT_EVIDENCE_AUDIT_PASS`. Original E42 Git blob checked unchanged and Stage10/6 unit tests passed.

To avoid overstating a first-observation detection gap, a separate **artifact-only** GitHub audit `.github/workflows/jpdc-stage11-archived-observation-audit.yml`, commit `637225b089274ae4e58d17f4f6c456dd413a7b8d`, downloaded original immutable completed Stage11 artifact WITHOUT rerunning any simulations and checked all eight source truth and delivered-alarm timestamps. **Real GitHub Actions `42094262596` SUCCESS**, job `127480076232`, verified marker `JPDC_STAGE11_IMMUTABLE_SHADOW_OBSERVABILITY_AUDIT_PASS`.

## Frozen original source-development results: seed83

### S3 hidden network degradation (the primary observation target)

| Policy | Postshock damaged-node dispatches | Distinct damaged nodes receiving E2E feedback /6 | Distinct damaged nodes generating an alarm /6 | All-MISSION misses | Alarm delay from first damaged-node arrival |
|---|---:|---:|---:|---:|---:|
| PRED_GREEDY | 333 | 1 | 1 | 4 | **76.8413 ms** |
| CASPER_FULL | 335 | 6 | 1 | 4 | **73.5232 ms** |
| NEW_NETWORK_RESIDUAL | **8** | 1 | 1 | 2 | **76.8413 ms** |
| NEW_NETWORK_RESIDUAL_PROBE | **16** | 6 | 1 | 2 | **73.5232 ms** |

For every S3 policy, **exactly one observed incompatible-change alarm** occurred, associated with an actually damaged postshock delivered observation; **zero false alarms** according to the frozen synthetic truth. For each policy, the first observed affected-node feedback E2E delivery timestamp was exactly the first alarm timestamp, so *alarm delay relative to first affected feedback was 0 ms*. This does **NOT** mean no real detection latency: first affected task was dispatched **73.5–76.8 ms before that feedback**. Crucially, the source defines fault onset by **task index10000**, not an independently measured physical instant; first affected dispatch-to-alarm gap is NOT causal fault-onset detection delay for the entire network.

**Why FULL and PROBE see 6 of 6 but alarm only 1:** node coverage counts mean there was at least one postshock E2E result, but an inconsistency alarm requires a comparable prior within-node earlier feedback and a violation of the stated normalized drift bound. More feedback breadth alone does not create a contradictory pre/post pair on each node; late-delivered earlier-generated reports are quarantined and some nodes have sparse history. This is a mechanism hypothesis consistent with the outputs, **not a separately proven causal attribution** to any single specific missed pre-shock observation; full per-node historical pre/post evidence must be audited before assigning exact cause.

S3 older-generated late-delivered feedback quarantines: PRED_GREEDY173, FULL175, NEW171, PROBE174; these are all-stage counts across 12000 reports, not solely damaged-node or postshock reports. The loss of older reports may reduce detector informativeness. Do not silently call this method a statistically consistent arbitrary-delay change-point estimator.

### S2 hidden compute degradation (negative control)

| Policy | Affected compute-degraded postshock dispatches | Distinct affected compute nodes observed /6 | Network alarms | All-MISSION misses |
|---|---:|---:|---:|---:|
| PRED_GREEDY | 1102 | 4 | **0** | 7 |
| CASPER_FULL | 26 | 6 | **0** | 7 |
| NEW_NETWORK_RESIDUAL | 1102 | 4 | **0** | 7 |
| NEW_NETWORK_RESIDUAL_PROBE | 1096 | 6 | **0** | 6 |

S2 source changes CPU service only, not network multiplier, therefore **zero normalized network alarms was expected**. The observed negative-control result passed. The one-miss difference in the PROBE row (7→6) is descriptive seed83 and from old physical probe routing, not this new shadow detector.

## Interpretation and remaining issues

1. **No routing efficacy caused by the new detector:** Shadow-only code leaves every old physical outcome and dispatch count byte-exact. S3 NEW risk's 2 vs GREEDY/FULL's 4 misses is merely a single previously uninspected development seed, not statistically valid evidence of population superiority, and it cannot be attributed to the observational detector.
2. **Observability vs identification:** At least one postshock affected E2E report for each of six nodes is **not enough** for a node-specific smoothness violation alarm; consistent pairwise pre/post histories are required. Exactly 1/6 alarms despite 6/6 coverage is the strongest Stage11 diagnostic, motivating per-node pre-vs-post comparisons before new control algorithms.
3. **Algorithm feedback cannot predate information:** No affected-node result can be detected at the hidden source shock task index or at arrival. Earliest observed alarm at the first affected E2E report for this seed and these policies, with positive 73.5–76.8ms first exposure-to-feedback gap.
4. **Source-model pathology/realism:** The S3 `network_multiplier=2` multiplies **both RTT and data transfer** of affected path, and network measurement generation was assigned at physical CPU finish with entire network delay after CPU; no modeled upload/downlink shared link or protocol congestion. Real network observations and true physical traffic traces required for external validity.
5. **Nonrandom source fault placement, dependent samples:** Six affected nodes per source scenario, one dev seed83, one source-generator distribution; 96000 task-policy records are not independent replications. No p-value.
6. **No detection guarantee:** L=.0001 and epsilon=0 arbitrary conditional settings; observed alarm is a contradiction to local model given delivered history, not proof physical fault time, duration or best corrective action. The current detector quarantines delayed older measurements, possibly throwing away useful evidence.
7. **Historical negatives unchanged:** original native ten-seed FULL-vs-GREEDY two-sided sign p=1.000 NONsig, Java disjoint p=.0625 NONsig, four-seed eta×mask p=.125 NONsig; original Java CloudSimPlus vs native Python strict-FCFS wait fidelity test FAILED max9.1214ms>5ms. Original FGCS first paper already owns CP rank/ETA/health/probes/S3 network blind spot. No second publishable algorithm yet.

## Highest-value next work
Perform an original **archived-artifact-only per-node episode audit** of why five affected nodes (in FULL/PROBE) had no contradictory delivered history; in present Stage11 artifact only counts and alerts are available, not individual per-node pre/post history. To answer it accurately, predeclare new **diagnostic trace capture** for a separate development cohort or enhance a read-only trace of original seed83 *without changing the scientific policy outcomes* and clearly label as exploratory. Then design a genuinely distinct observable change-aware routing rule and task-specific risk costs, benchmark external related literature, and only then run independent full scheduling comparisons with held-out seeds. No seed hunting.

## Reproduction
- Stage11 protocol https://github.com/afshinyaghoobi/casper-iiot-cloudsim/blob/jpdc-seed0-repro-20261024/jpdc/STAGE11_PHYSICAL_NETWORK_EPOCH_SHADOW_PREREG_2026-11-05.md
- Original policy engine with shadow https://github.com/afshinyaghoobi/casper-iiot-cloudsim/blob/jpdc-seed0-repro-20261024/jpdc/independent_physical_network_epoch_shadow_stage11.py
- Original CI https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42093920896
- Original artifact https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42093920896/artifacts/13446096806
- Immutable time audit https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42094262596
