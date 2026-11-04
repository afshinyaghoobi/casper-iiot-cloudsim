# JPDC NEW network-residual risk routing: first native physical development pilot VERIFIED (2026-11-04)

## Status upfront — new decision operation executed, no deadline improvement established

A distinct **nonconformal, source-observable, per-node network-risk penalty** was designed from scratch and **tested before any new confirmatory trial**. It is not a renamed CASPER/E17 controller, a novel conformal method, or a validated superior system. The complete first FGCS submission PDF already contains the CP top-3 first-feasible algorithm, selected-score eta memory and service-only health detection. The present experimental addition is a **direct observed network-specific risk penalty in the dispatch objective**, not a new CP guarantee.

Before running the pilot, the fixed full protocol `jpdc/NEW_NETWORK_RESIDUAL_POLICY_PILOT_PREREG_2026-11-04.md` was committed at `2e01c61af8059bf04680c9233833d14661c5f165`: development seed index **80**, S2 hidden 40% compute degradation and S3 hidden 50% network degradation, 12k tasks/policy, three policies **PRED_GREEDY**, original **CASPER_FULL**, and NEW_NETWORK_RESIDUAL, for **six native physical scenario-policy runs and 72,000 task-policy observations**. Seed80 is now **exposed development**, never future untouched holdout. New experimental results were not used to tune the 32-sample window, eight-sample warm-up or 90th-percentile risk quantile. Original E42 frozen Git blob `34256ca7bff46f911cf20e8b94278fbd09175746`, E4.6 unchanged.

## New decision rule (actual executable)
For a node j, original nominal task-specific network duration `n_ij = RTT_j + 8000 (input_i + output_i) / bandwidth_j`. Only at the future event time `physical_CPU_finish + measured_full_network_ms`, record observed nonnegative network excess `e_ij = max(0, observed_full_network_ms - n_ij)` in the node's deque (bounded to **32** past observations). Pre-dispatch risk `r_j = nearest_rank_quantile_0.90(last32 e_j)` if at least **8** completed and reported network observations exist, else **0**. The NEW policy dispatches to the lowest-index stable minimizer of

`predicted_original_nominal_latency_ij + r_j`, over all 21 nodes.

This is a **causal-timed, node-level network feedback mechanism**, distinct from original E17 selected MISSION nonconformity inflation and distinct from original CPU-service-only health alarm. It applies to any task criticality, without a conformal certificate. It has no access to which nodes are secretly damaged, the actual next-free physical CPU time, true future service or network events, postshock task outcome labels, or an oracle. A literal 21-node × window32 naive nearest-rank quantile implementation needs O(21×32log32) per arriving task and O(21×32) retained memory; not currently a formal optimality or tail-coverage guarantee.

**Temporal subtlety:** The source-style native CPU physical server is released at CPU finish; additional network measurement is placed on the future feedback heap at CPU_finish + actual end-to-end network time. This aggregate-network-feedback ordering is a conservative **synthetic approximation**, not packet-level modeling of upload/transmission/downlink; it does prevent the new policy from using network results at the earlier CPU-finish event. Original CASPER_FULL comparator's E17 still inherits prior Stage4 CPU-finish feedback semantics; therefore controller feedback timelines are not identical, and these pilot arms must not be claimed to satisfy matched feedback budget or matched real transport dynamics. More accurate event decomposition will be needed for strong causal comparisons.

## Real code and CI provenance

- `jpdc/network_residual_risk_policy.py` commit `2fdef2bfd6eb5cfc88a283460d2843ec1d295e1c`: new strict per-node observation state, 32-slot FIFO, 8 minimum observed samples, 90th percentile, positive-excess clipping, pure stable argmin selection.
- `jpdc/independent_network_risk_physical_pilot.py` commit `75eca6fad58a7d5498cc4d13e2c34bf453552626`: separately executing independent physical event engine, 3-policy physical pilot and feedback **only at timestamp CPU_finish + network duration**; original Stage4 engine is not edited. Original physically simulated service noise, source scenarios, 21 strictly FCFS nodes and calibrations retained.
- `jpdc/test_network_residual_risk_policy.py` commit `91fc7543789f32b6ae7d02c3364fda048062b06b`: adversarial synthetic no-feedback->greedy, 7 observations no risk, 8 positive observations trigger genuine reroute, 32-slot clipping, nearest-rank .90, malformed/out-of-order feedback rejection.
- `jpdc/run_new_network_risk_pilot.py` commit `134201fef63ceba3e6ace175a365d3e043d308bc`: original original-model 80k native calibration at seed80, new policy and two original policies S2/S3×12k, complete seed/task conservation, detailed non-oracular risk counters; crucial **baseline comparator regression** compares original Stage4 simulator's PRED_GREEDY and CASPER_FULL against the new feedback-event simulator on two scenarios for original all-mission miss counts, postshock miss rate, all 21 node dispatch counts, physical latency/wait and health/eta states.
- CI `.github/workflows/jpdc-new-network-risk-mechanism-pilot.yml` commit `bd8adf2b00816126f636886b0574a4b96050f107`.

**REAL GitHub Actions run 41928440771 COMPLETED SUCCESS**, job **126918912595**, artifact **13369769232**. Logs explicitly include:
- `JPDC_NEW_NETWORK_RISK_PREDISPATCH_NO_LEAKAGE_UNIT_PASS`
- `JPDC_NATIVE_EIGHT_POLICY_DECISION_UNIT_PASS`
- `JPDC_NEW_POLICY_ORIGINAL_COMPARATOR_PHYSICAL_REGRESSION_PASS` for 4 original comparator cells (S2/S3 × PRED_GREEDY/CASPER_FULL)
- `JPDC_NEW_NETWORK_RESIDUAL_PHYSICAL_PILOT_PASS`
- `JPDC_NEW_NETWORK_RISK_FULL_PILOT_BYTE_REPRODUCIBLE_PASS` (all six 12k policy runs repeated completely; rerun is NOT another independent scientific seed)
- `JPDC_NEW_NETWORK_RISK_ORIGINAL_PILOT_EVIDENCE_AUDIT_PASS`.

## Prespecified descriptive seed80 results

| Scenario | Policy | ALL MISSION misses | Postshock MISSION miss rate | Actual delayed feedback with positive network excess | Postshock damaged-node dispatches | NEW's reroutes vs its own immediate greedy choice |
|---|---|---:|---:|---:|---:|---:|
| S2 compute | PRED_GREEDY | 23 | 7.9208% | 0 | 1050 | 0 |
| S2 compute | CASPER_FULL | 22 | 6.9307% | 0 | 22 | 0 |
| S2 compute | NEW_NETWORK_RESIDUAL | 23 | 7.9208% | 0 | 1050 | **0** |
| S3 network | PRED_GREEDY | 21 | 5.9406% | 153 | 153 | 0 |
| S3 network | CASPER_FULL | 21 | 5.9406% | 158 | 158 | 0 |
| S3 network | NEW_NETWORK_RESIDUAL | **21** | **5.9406%** | **9** | **9** | **253** |

In the S3 NEW_NETWORK_RESIDUAL run, at **1,943 arrivals** at least one node's observed network-excess penalty was nonzero, and 253 of that policy's actual decisions differed from greedy computed **at the same state trajectory**. S3 postshock selected damaged nodes fell from 153 with a separate PRED_GREEDY physical run to 9 under NEW policy, a descriptive **144 fewer affected-node postshock dispatches** or **94.1% lower** (not a causal identification of deadline outcomes; policy-specific queue trajectories differ). The new policy saw only 9 positive network-excess observations because it avoided those nodes, making future self-observation and exploration under shift an important further study. Under S2 compute-only degradation, the new network-specific residual policy did **not** activate risk routing or improve deadline misses: exactly greedy's 23 total MISSION misses and 1050 damaged-node postshock dispatches. The observed selectivity is consistent with intended network-only sensitivity; this does not prove correctness outside the simulated regimes.

**No new superiority evidence**: All three policies in S3 had exactly 21 ALL-MISSION misses and the same 5.9406% postshock MISSION miss rate; the network-risk heuristic did not demonstrate the intended downstream deadline benefit at this horizon. In S2, NEW had 23 versus CASPER_FULL 22 and GREEDY 23. This is a single exposed exploratory seed and contains no statistical inference or new holdout. Do not retrofit a significance test, change the algorithm after inspecting seed80 while calling it frozen, or claim this is a new published algorithm.

## Challenges to resolve before a standalone JPDC novelty or efficacy claim

1. **Formal problem novelty:** A simple empirical network residual penalty may be common in online routing/scheduling. Need up-to-date rigorous published method comparison; first-paper FGCS difference alone does not imply scientific algorithm novelty against external literature.
2. **Observation availability:** Network excess is revealed only after post-CPU feedback in this native simulation; production telemetry may require task-level RTT and transfer measurements. Its transport model is stylized and lacks shared-link congestion/routing/protocol queues.
3. **Closed-loop feedback bias:** Avoiding damaged nodes reduces their observations. A decayed confidence term, information acquisition or sparse network probing might be necessary but is NOT part of the present frozen pilot.
4. **Separate CPU and network risk:** This network-only model cannot recognize S2 compute degradation; combined controller and compute/network ablation would be new engineering, requiring genuine methodology and independent tests.
5. **Fair comparator feedback timing:** Original E17 processes realized MISSION outcomes at native CPU finish even if the source aggregate-network latency is not completed until later. NEW risk uses delayed network observation, making feedback information timing unequal. Strong efficacy claims require harmonized completion-time definitions.
6. **Out-of-source generalization:** Simulated original source node/task distributions and shocks remain shared across independent Python/Java; this is not independent industrial traffic, YAFS, or evidence of CloudSimSpaceShared queue parity. The separately preregistered FIFO transfer FAIL remains 9.1214ms >5ms.
7. **Statistical validation:** Keep seed80 solely for development; reserve entirely new independent seeds and fault-placement/topology distributions and preregister outcome endpoints before new confirmatory deployment.

## Historical immutable science
Original FGCS first submission already included E17 and network health blind spot. Original disjoint Java follow-on 10seed S2/S3 exact sign **p=.0625** nonsignificant; original 4seed mask/eta factorial **p=.125** nonsignificant; original native strict FIFO all-eight 10seed FULL-vs-GREEDY **p=1.000** nonsignificant; original cross-engine strict FIFO physical queue fidelity **FAILED** max wait9.1214ms >5ms. No original result, source SHA, seed-level statistic or protocol has been overwritten.

## Links
- Preregistration: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/blob/jpdc-seed0-repro-20261024/jpdc/NEW_NETWORK_RESIDUAL_POLICY_PILOT_PREREG_2026-11-04.md
- Real successful pilot: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41928440771
- Original pilot artifact: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41928440771/artifacts/13369769232
