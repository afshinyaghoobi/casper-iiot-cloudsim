# JPDC Stage10 normalized network shock/epoch diagnostic — verified 2026-11-05

## Status and scope
A separate synthetic-source-compatible network **feedback-state diagnostic** was implemented and verified. It is **not yet connected to Stage6's 21-node physical scheduling policy**, not an independently validated change-point detector and not a demonstrated improvement in MISSION deadlines. Its purpose is to make the original Stage8/9 notion of a single node-level absolute residual less task-size dependent, and to avoid silently assuming that a sudden observed network shock satisfies a small global Lipschitz-drift bound.

The original frozen E42 Java blob `34256ca7bff46f911cf20e8b94278fbd09175746`, E4.6 and all original independent physical evaluators are unchanged. No new scientific seed, calibration, simulator policy matrix, p-value or empirical deadline effect was produced.

## Why normalized residuals better match this precise frozen synthetic physics

The original `jpdc/independent_stochastic_physics.py` computes original nominal task-node network duration

`n_ij=RTT_j+8000(input_i+output_i)/bandwidth_j`.

The source `physical_durations` applies an affected-node scenario multiplier `g=1/bm` (S3 50% network-bandwidth setting `bm=.5` => `g=2`) to the **entire** nominal network duration, including nominal RTT:

`actual_network_duration_ij = n_ij * g_ij`.

Important: this source implementation is a **whole-network-duration multiplier**, not an independently modeled physical Ethernet/wireless bandwidth transfer phenomenon; it also scales RTT, so don't call it validated field packet network physics.

The absolute excess `actual_network-n` changes with task size even for the same g. The new observed dimensionless slowdown `z_ij=max(0,actual_network_ij/n_ij-1)` is, **for the frozen source generator only**, exactly `g-1` for any task size. Thus z=0 for multiplier1 and z=1 for multiplier2. The node-local normalized observation becomes available **only at a delivered E2E feedback timestamp**, without seeing affected-node masks, source shock index, physically future outcomes or physical next-free CPU times.

## Distinct and falsifiable epoch semantics

The new separate file `jpdc/normalized_network_shock_epochs_stage10.py` stores node-local normalized E2E feedback reports and checks them against externally assumed normalized drift bound `L_j` and error bound `epsilon_j`.

- For a new measurement generated at m and delivered at d, only when delivered can the accepted previous node-epoch reports be compared using `|z_new-z_old|<=L_j|m_new-m_old|+2eps_j`.
- If newer-generated feedback violates that bound, **observed incompatible-change alarm** is emitted at d and a new feedback epoch starts with that measurement. This detects a contradiction to assumptions, **NOT** an oracle true changepoint timestamp, not a guaranteed fault alarm or proof the new regime is stable.
- If an older-generated report is delivered after a newer-generated report on the same node, it is **quarantined** rather than used to roll back the current epoch or trigger a retrospective alarm. This sacrifices some historic information but prevents contamination; not a full delayed/out-of-order changepoint estimator.
- After the first alarm, a **single report in the new epoch leaves `unverified_after_alarm=True`**. The example uses at least 2 consistent delivered reports as a descriptive *minimum evidence* gate; this threshold is NOT a theorem ensuring stationarity or statistical confidence.
- The per-epoch normalized conditional interval propagates from measurement generation time, not delivery time, then multiplies by the **current task's nominal network duration** to express millisecond excess. No report means UNKNOWN high=infinity, not zero.
- Invalid time, duration, node or noncausal delivery inputs are rejected before state mutation.

This implementation retains per-node accepted report lists and performs pairwise checking within the current observed epoch: unbounded worst-case current-epoch report memory; not production cost-optimal. No packet-level transport, topology interference or future fault prediction.

## Real GitHub code and verification

- BEFORE experiments: `jpdc/STAGE10_NORMALIZED_NETWORK_SHOCK_EPOCH_PREREG_2026-11-05.md`, commit **`72b1d9eef0f1459f57cdb2123f6b43ca311d7655`**.
- Standalone source: `jpdc/normalized_network_shock_epochs_stage10.py`, commit **`f682c662875cc48b0173a2aab14920e79a2c4f9a`**.
- Adversarial synthetic source-physics algebra and delivery-timing tests: `jpdc/test_normalized_network_shock_epochs_stage10.py`, commit **`0f5fd3e070f41195b4e9ce78da57a7efa9c9a2b9`**, correction commit **`82cd5a127d1a84d7a8189c86192b2133d652b85c`**.
- CI workflow `.github/workflows/jpdc-stage10-normalized-shock-gate.yml`, initial commit **`279376d75ecb200881920f1994bcd8358661889a`**; successful triggering commit **`eae64c32c10297924a61bb9f04b6cdf6de6cf6f4`**.

First CI run **`42076083081` FAILED** because an assertion in the **NEW test fixture** incorrectly expected `LOW_z=0` from two observations `z0=0,z1=1` at `epsilon=.5`; their valid intersection is the single point **z=.5**, not [0,.5]. The underlying model code/scientific thresholds were unchanged. Corrected the expected exact interval and reran the same fixed protocol: **REAL GitHub Actions run `42076287709` COMPLETED SUCCESS**, job **`127417221383`**, original artifact **`13438871409`**.

Explicit verified CI output:
- `PASS initial no-shock and age-aware conditional interval`
- `PASS 2x whole-network shock triggers observation-only E2E epoch alarm (not at hidden change)`
- `PASS normalized slowdown equal for distinct task sizes; task-specific ms conversion exact`
- `PASS late delivered older-generation observation quarantined without state contamination`
- `PASS restoration is detected only after completed E2E feedback`
- `PASS change alarm NOT guaranteed under weak measurement precision`
- `PASS source-formula 21-node toy shock only detects actually observed incompatible feedback`
- `PASS unknown nodes cannot be mistaken for zero-risk certified nodes`
- `PASS invalid feedback fails closed without changing state`
- `JPDC_STAGE10_NORMALIZED_NETWORK_EPOCH_AND_SHOCK_FIXTURES_PASS`.
- Full original Stage9 interval compression and Stage8 age-aware regression tests PASS.
- `JPDC_STAGE10_NORMALIZED_SHOCK_AND_PRIOR_GATES_PASS`.

The 21-node fixture is a **synthetic constructed toy using the exact frozen network multiplier formula**, not an independent complete source-generated 21-node end-to-end deployment or YAFS.

## Research assessment and next requirements

1. The normalized latent z is exactly node-specific for the current frozen synthetic source scenario, but there is **no evidence this abstraction holds under real task-size-dependent network RTT, bandwidth saturation, congestion or transport protocols**.
2. Change alarms operate on delivered completed task observations. A hidden abrupt shift cannot be detected before its first sufficiently informative observed E2E completion; using a previous epoch's assumed finite upper bound *between* hidden change and detection would be unjustified for a global arbitrary-shift guarantee.
3. Choosing a new epoch after contradiction is an elementary change-alarm heuristic. It is not a consistent change-point estimator, novel regrettable bandit theorem or proof of optimal safe reconfiguration.
4. Two compatible post-alarm reports do not prove a new stable process; descriptive flag merely relaxes the per-epoch evidence gate.
5. Original Stage8/9 absolute millisecond-excess Lipschitz assumptions failed on sudden shock/task-size counterexamples. Stage10 addresses **specific source-model algebra and explicit observed contradictions**, not physical external validity or performance.
6. The historical source-independent native ten-seed FULL vs GREEDY sign p=1.000 nonsignificant; original Java disjoint n10 p=.0625 nonsignificant; original n4 ETA×mask p=.125 nonsignificant; original strict FIFO vs CloudSimPlus SpaceShared queue waiting-time parity FAILED max9.1214ms>5ms; E42/E4.6 frozen. Stage6 seed82 1% NORMAL probe produced 6 rather than 5 all-MISSION misses in S3. All unchanged.

**Highest-value next gate:** Define a fully observable task-level measurement-generation/CPU/upstream/downstream timing contract and compare task-size normalized network state against the actual Stage6 independent *physical source-generated events* in a separately preregistered development cohort, including true feedback delay and policy-dependent sample starvation, before asserting the new model is valid for scheduler control. A prior-art novelty review of normalized change-aware delayed-feedback routing is still essential. Do not treat the present scripted 21-node toy as independent simulator validation.

## Links
- Code: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/blob/jpdc-seed0-repro-20261024/jpdc/normalized_network_shock_epochs_stage10.py
- Preregistered contract: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/blob/jpdc-seed0-repro-20261024/jpdc/STAGE10_NORMALIZED_NETWORK_SHOCK_EPOCH_PREREG_2026-11-05.md
- Actual GitHub run: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42076287709
- Original fixture artifact: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42076287709/artifacts/13438871409
