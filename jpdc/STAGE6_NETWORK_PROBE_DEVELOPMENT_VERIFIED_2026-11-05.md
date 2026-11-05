# JPDC Stage6: NORMAL-only network observation exploration — real development evidence (2026-11-05)

## Verdict: probe mechanism works; no execution benefit established

The original independent native Python `NEW_NETWORK_RESIDUAL` node network-delay penalty (last32 positive network excesses, minimum8 per node, nearest-rank90) can stop sampling damaged nodes after it avoids them. Stage6 added **one fixed-rate real physical probing opportunity every 100th NORMAL arrival** (no hidden fault state, no future outcomes, no synthetic zero-cost probes), prioritizing nodes with fewer previously delivered end-to-end feedback observations. The source-independent physical E2E event timing established in Stage5 remains unchanged. This is a **development ablation**, not a significance test, novel bandit theorem, successful deadline-optimization claim or external validation.

**BEFORE the first Stage6 evaluation**, preregistration `jpdc/STAGE6_NETWORK_PROBE_DEVELOPMENT_PREREG_2026-11-05.md` was committed `3a918826a62b9570ae74cc196010e5c02d005943`. Only prechosen previously unused **development-only seed82**, 80k independently generated physical calibration for original FULL, S2 compute-loss and S3 network-loss, **4 policies × 2 scenarios × 12000 tasks = eight physical runs / 96000 task-policy observations**. Policy arms: PRED_GREEDY, original harmonized CASPER_FULL, original untouched NEW_NETWORK_RESIDUAL, and NEW_NETWORK_RESIDUAL_PROBE. Original E42 SHA frozen `34256ca7bff46f911cf20e8b94278fbd09175746`; E4.6 untouched. No outcome-based tuning of window32/min8/q90/cadence100.

## Implemented new probe policy

`jpdc/normal_network_probe_stage6.py` commit `5af50156b683c35653247756615a2eec385984ab`: on every100th NORMAL arrival, eligible node j must have **nominal predicted latency <= current NORMAL deadline**. Choose by (1) fewest previous E2E task feedbacks on node, (2) oldest last E2E feedback ordinal (-1 for never observed), (3) lowest nominal current predicted latency, (4) lowest ID. All other tasks use unchanged original new network risk selector. No affected-node mask or future network outcome is available to selector. Exactly one selected NORMAL task executes on actual 21-node strict FIFO physical CPU, with original stochastic service/network, and new network delay is observed only at E2E time. The measured task is real production-like NORMAL traffic, so any queue interference and deadline costs are real within the native model; its network probe sample is not a guarantee for MISSION workload.

`jpdc/independent_network_probe_stage6.py` commit `697e5d20450fe11053050ee03a90d97914557b25`: separate fork of Stage5 fully harmonized E2E feedback physical event engine, four policy modes, counters for per-node completed-feedback counts, probe opportunity/attempt/change, positive probe network samples, probe NORMAL missed deadlines, actual probe task latency, extra *nominal predicted* latency compared with the **same-state hypothetical** unprobed new-risk choice. The hypothetical difference is a decision-time diagnostic only: rerouting task would alter downstream queue trajectories, so NOT a valid realized causal comparison. Existing Stage5 simulator, original CP E17, native Stage3 calibration, original E42/E4.6 untouched.

`jpdc/test_network_probe_stage6.py` commit `f1daef8f3abb59cf7bcede23b53e24fd2c2a8a54`: deterministic synthetic information-starvation rescue, exactly 99 nonprobe + 100th probe, MISSION never probed, zero-eligible skip, feedback age requirement, malformed state reject. Original `jpdc/test_network_residual_risk_policy.py` also passed. Fixed real eight-arm development driver `jpdc/run_network_probe_stage6.py` commit `75fa1c99e75b7bc9e2cfbbb3f80e54525be0d1d1` strongly validates **old exact original Stage5 physical/mission/health/eta/node dispatch/risk outputs for THREE old policies across both S2/S3 (six control cells)**. CI `.github/workflows/jpdc-network-probe-stage6.yml` commit `7174580609d41af0c99684cb8f8f3f605674c747` freezes original E42 SHA, runs units, full 8-arm seed82 matrix twice and asserts byte-identical complete JSON.

## Actual REAL GitHub Actions CI

**Run `42033188272` COMPLETED SUCCESS**, job `127264519809`, original artifact **`13417540579`**. Confirmed success markers `JPDC_STAGE6_PROBE_POLICY_UNIT_PASS`, `JPDC_STAGE6_UNCHANGED_OLD_POLICY_REGRESSION_PASS` (six S2/S3×3 control cells), `JPDC_STAGE6_NETWORK_PROBING_FIXED_MATRIX_PASS`, `JPDC_STAGE6_ORIGINAL_PROBE_FULL_MATRIX_BYTE_REPRODUCIBLE_PASS`, `JPDC_STAGE6_ORIGINAL_PROBE_EVIDENCE_AUDIT_PASS`.

### All eight original recorded physical outcomes: seed82 at 12000 tasks

| Scenario | Policy | ALL MISSION missed deadlines | Postshock MISSION miss rate | Postshock dispatches to damaged nodes | Positive network-excess E2E observations | Risk-only reroutes (probe overridden separately) | Actual new NORMAL probe attempts / changed selections | Positive network-excess probe feedback | Direct NORMAL probe misses |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| S2 compute | PRED_GREEDY | 2 | 2.35294% | 822 | 0 | 0 | 0 | 0 | 0 |
| S2 compute | CASPER_FULL | 1 | 1.17647% | 21 | 0 | 0 | 0 | 0 | 0 |
| S2 compute | NEW_NETWORK_RESIDUAL | 2 | 2.35294% | 822 | 0 | 0 | 0 | 0 | 0 |
| S2 compute | NEW_NETWORK_RESIDUAL_PROBE | 2 | 2.35294% | 821 | 0 | 0 | **96 / 96** | 0 | 0 |
| S3 network | PRED_GREEDY | 2 | 2.35294% | 1085 | 1085 | 0 | 0 | 0 | 0 |
| S3 network | CASPER_FULL | 2 | 2.35294% | 1077 | 1077 | 0 | 0 | 0 | 0 |
| S3 network | NEW_NETWORK_RESIDUAL | **5** | 5.88235% | 27 | 27 | **1657** | 0 | 0 | 0 |
| S3 network | NEW_NETWORK_RESIDUAL_PROBE | **6** | **7.05882%** | **28** | **28** | **1644** | **96 / 96** | **1** | **0** |

In both S2 and S3, 96 original-normal probe opportunities were eligible and selected a different node. Both fulfilled the <=floor(NORMAL/100) gate, with no actual directly probed NORMAL task deadline miss. In S3, **only one** such probe delivered a positive network-excess measurement; the total completed positive network-excess observations increased by only 1 (from27 to28), and damaged-node exposure increased by one dispatch. This does **not** demonstrate a substantial or sustained cure for feedback starvation. The network-risk-only re-routing counter fell 1657→1644 due to downstream trajectory state changes; the 96 probe overrides are separately counted and must not be added as though they were comparable same-state causal effects.

**Important negative finding:** S3 all-MISSION deadline misses increased from5 with no-probe new policy to6 under probing. PRED_GREEDY and CASPER_FULL each missed2 in that scenario. In S2 NEW and NEW+PROBE both missed2, FULL missed1. With only one development seed, these differences have **no statistical interpretation**, and the probe's zero direct NORMAL misses do NOT mean probes are harmless to future MISSION workload (queue interference is possible). Seed82 is exposed and never available for future confirmatory holdouts.

## Mechanism risks observed/remaining
1. E2E feedback starvation can be self-reinforcing: routing away from a node reduces evidence for renewed health; 1% normal traffic probing can increase observations but the actual positive damage feedback was only ONE on this original scenario.
2. Generic exploration/probing under online scheduling is not a novel idea on its own. Related work includes Wang et al., *Bandit Learning for Online Scheduling with Immediate Decision*, UAI 2026, https://proceedings.mlr.press/v337/wang26g.html , and online edge offloading with bandit feedback (IEEE TMC 2024, https://doi.org/10.1109/TMC.2023.3275851). More detailed novel contribution and assumptions analysis required.
3. Probe target prioritizes underobserved nodes, **not a physical damaged-node oracle**; measured negative excess is useful for representation, but is not proof of unbiased mission network behavior. The current original source generator assumes network multiplier uniform within one affected node and scenario, which is not industrial congestion.
4. In this native model aggregate network time is realized after CPU completion for feedback timing. No independent upload/downlink queues, shared network links, topology routing or YAFS.
5. Missing statistical independence: there are eight task-policy runs but only seed82 single scientific unit, and task records are dependent. No p-value or superiority claim.
6. Original native n10 FULL-vs-GREEDY p=1.000, original Java n10 p=.0625, original Java 4-seed factorial p=.125 all nonsignificant; old original native-vs-CloudSim queue-transfer gate **FAILED** max wait9.1214ms>5ms and is not retroactively fixed by this new native study.

## Next rigorous technical check
Use an **archived artifact-only** reporting gate (no new scientific rerun) to quantify old-vs-probe *per-node completed feedback coverage* and two real probe cost counters (`network_probe_actual_latency_sum_ms` and `network_probe_predicted_nominal_extra_ms`) with correct units and explicit noncausal interpretation. Then decide if the core problem requires a different estimator/controller or external network model rather than more samples of the same fixed 1% probe. Any altered probe cadence/priority MUST be a separately preregistered new method with distinct development/confirmatory data, never a silent retune of these fixed results.

## Links
- Original real CI: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42033188272
- Original raw artifact: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42033188272/artifacts/13417540579
- First original protocol: `jpdc/STAGE6_NETWORK_PROBE_DEVELOPMENT_PREREG_2026-11-05.md`.

## Additional immutable artifact-only cost and feedback coverage diagnostic (no new experiment)

To validate aggregate reported costs rather than extrapolating from the 96 probe counts, a **separate read-only CI workflow** `.github/workflows/jpdc-stage6-archived-probe-cost-audit.yml` was created **after** the original pilot and downloaded the immutable original GitHub Actions Stage6 result `42033188272` artifact `13417540579` without rerunning or changing scientific data. **REAL audit run `42033570758` SUCCESS**, job `127265825807`, with marker `JPDC_STAGE6_IMMUTABLE_ORIGINAL_PROBE_COST_AUDIT_PASS`. Audit CI commit `0cb0f0241e34c42be0136c39588997a96c9a4a5a`.

Original stored measurements:
| Scenario | Original no-probe number of nodes with any E2E feedback | Probe number of nodes with any E2E feedback | Mean actual observed E2E latency of 96 directly probed NORMAL tasks | Mean *nominal predicted* latency difference between probe choice and risk policy's same-state unprobed choice | Probe positive network-excess E2E feedback |
|---|---:|---:|---:|---:|---:|
| S2 compute | 9 of 21 | **21 of 21** | **120.7805 ms** | **+71.5076 ms** | 0 |
| S3 network | 13 of 21 | **21 of 21** | **120.7403 ms** | **+71.2624 ms** | 1 |

This confirms a REAL increase in **observation breadth**; it does not prove a meaningful improvement in recognizing hidden damage (only one positive probe feedback during S3), or in deadline outcomes (all-MISSION misses worsened from5 to6 with probes in S3). Crucially, the +71 ms values are **predicted nominal timing differentials at the same original probe-decision state**, *not actually measured causal latency penalties*: different dispatch choices modify all later node queues. Mean observed E2E latency ~120.7ms is the realized latency of the probed tasks, NOT the increment relative to hypothetical unprobed physical completion. Probe budget 96/96 attempted and rerouted, 0 directly probed NORMAL deadline misses, but later MISSION effects cannot be assumed safe.

### Related-work novelty boundary, preliminary
Online scheduling with censored/delayed feedback and exploration/exploitation is an established research topic, not a broad novel principle from this project alone. Direct preliminary related context:
- Wang et al. (2026), *Bandit Learning for Online Scheduling with Immediate Decision*, Proceedings of UAI / PMLR 337, https://proceedings.mlr.press/v337/wang26g.html : bandit/UCB learning with censored feedback, different identical-machine preemption/abandonment model.
- Xiong Wang et al. (2024), *Online Learning Aided Decentralized Multi-User Task Offloading for Mobile Edge Computing*, IEEE TMC 23(4), DOI 10.1109/TMC.2023.3275851, https://doi.org/10.1109/TMC.2023.3275851 : decentralized bandit offloading with/without processed-task neighbor feedback and network-delay-aware rewards.
Neither directly establishes equivalence to this native strict-FCFS, MISSION/NORMAL, node-local quantile model. They establish that adding bandit-style exploration/probing **cannot alone be called newly invented without a full prior-art analysis**. Avoid claiming a novel regret bound for this simple fixed-rate probe (none was derived).

Archive: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42033570758
