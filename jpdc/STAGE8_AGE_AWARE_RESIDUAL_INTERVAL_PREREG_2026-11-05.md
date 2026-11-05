# JPDC Stage8 — auditable age-aware network residual envelope: design and unit protocol
**Registered 2026-11-05 BEFORE executing new Stage8 fixtures. This is a conditional mathematical construction, NOT an empirically validated JPDC algorithm or new bandit theorem.**

## Motivation and unchanged science
Prior Stage7 finite example established a known two-world identification barrier under selected-only delayed feedback. Original Stage6 seed82 fixed NORMAL probing broadened node observation from 13/21 to 21/21 in S3 but yielded only one positive probe residual and 6 rather than 5 ALL-MISSION misses. No seed-based tuning follows. Original E42 frozen source Git blob `34256ca7bff46f911cf20e8b94278fbd09175746`, E4.6 and previous Stage1–7 scripts unchanged. No NEW scientific seed or 21-node physical policy evaluation in Stage8, and no new confirmatory test.

## Proposed *conditional* observation contract

For each node j, there is an unknown nonnegative **node-specific time-varying network excess** function `r_j(t)`. This is an *assumption-defined abstraction*; it has not been shown to follow from the synthetic E42 original physical source or from real IIoT traffic.

Assume a known nonnegative bound `L_j` (units ms excess per ms simulation time) such that `|r_j(t)-r_j(s)| <= L_j|t-s|` for all times under study. When a completed task's network measurement was generated at physical timestamp `m_i`, its observed network excess `y_i` differs from `r_j(m_i)` by at most an externally justified nonnegative `epsilon_j` ms. The observation becomes available **only at subsequent E2E delivery timestamp `d_i >= m_i`**, and may be used only when `d_i <= decision_time`. The method may not infer `L_j` or epsilon from hidden affected-node IDs, old held-out seed60–69, or future observations. If values are unverified, the resulting envelope has no real-world guarantee.

For node j and decision t, each delivered observation yields:
`lower_ij(t)=max(0, y_i-epsilon_j-L_j(t-m_i))`;
`upper_ij(t)=y_i+epsilon_j+L_j(t-m_i)`.
Use intersection over all available observations: `LOW_j(t)=max_i lower_ij(t)`, `HIGH_j(t)=min_i upper_ij(t)`. Therefore, **conditional on assumptions**, `LOW_j(t) <= r_j(t) <= HIGH_j(t)`. These are deterministic interval bounds; no conformal coverage guarantee or calibration under nonstationarity is implied. If there is no delivered observation, set `LOW=0`, `HIGH=+inf` and mark node **unidentified**, not 0 risk. If LOW > HIGH by tolerance, reject claimed assumptions/observations instead of forcing a confidence result.

**Selection rule (separate prototype):** With nominal task-node predicted latency `p_j>0`, choose among nodes with FINITE HIGH_j the stable minimum `p_j+HIGH_j`. If all are unknown, fall back to nominal minimum but mark `identifiable=false`; never issue network-bound certificate. With finite eligible bounds, its upper-bound network-augmented score `p_{j*}+HIGH_{j*}` is bounded by the chosen score but is **not a bound on realized total end-to-end latency**, because nominal CPU/virtual-queue errors are uncontrolled. An optional bound-based *network-only* deadline screen may be computed but must not be called a valid certificate for all E2E task latency.

**One-step conditional regret:** For a *single exogenous non-interfering action*, suppose actual total candidate latency is exactly `p_j+r_j(t)`, with nominal p_j treated as exact. If every candidate has a finite interval, a conservative one-step realized regret bound for selected j* is `(p_{j*}+HIGH_{j*}) - min_k(p_k+LOW_k)` (nonnegative); this follows from selected actual<=its upper, optimum actual>=minimum lower. If any alternative has unknown HIGH but LOW=0, the inequality still holds for this selection, although lower-bound regret may be huge; the selected-node eligibility is separately marked. There is **no repeated queue-coupled dynamic regret guarantee**, because dispatch changes future CPU queues and future feedback, and nominal p_j is not exact in the existing simulator.

## Frozen mechanistic adversarial fixture matrix (no empirical performance runs)
1. One delivered measurement with m=10, d=20, t=30, y=8, epsilon=1, L=.1 gives [5,11] at t=30 (age from **measurement**, not delivery); at t<d that observation is invisible.
2. Delayed observation with m=0, d=100 cannot influence a decision at 99.999, even if the CPU already completed.
3. No observations => HIGH=inf, not zero. All-nodes-unknown => greedy only with `identified=false`; mixed known/unknown select only finite upper nodes while reporting partial observation.
4. Multiple delivered reports tighten the interval by intersection, and a deliberately contradictory pair at the same measurement time with small epsilon and L=0 fails closed.
5. A newer E2E delivery of a *older measurement* must not appear fresher than its measurement timestamp. Out-of-order deliveries can occur, subject to global delivery-time monotonicity.
6. Zero drift L=0 and noise epsilon=0 yield point-identified r_j, and a 21-node artificial world with actual residuals satisfying assumptions must lie in all returned intervals.
7. For toy single-step exogenous worlds, calculate selected score, actual regret and conservative interval regret bound and assert the latter covers actual regret; no uncontrolled queue interactions or unobserved future outcome in chooser.
8. Reject invalid measurement generation > delivery, observation timestamp > now, invalid node, negative/NaN residual, negative drift/noise, or nonmonotonic E2E feedback clock.

## Implementation and scientific limits
Implement a standalone stdlib-only `jpdc/age_aware_network_interval_stage8.py` and `jpdc/test_age_aware_network_interval_stage8.py`, separate from Stage1–6 original tested simulator. The new prototype may use all delivered reports (O(total delivered)) and must state runtime/memory or a bounded-buffer policy; do not silently introduce Stage6 window=32 which would change the mathematical intersection. A 21-node test vector is sufficient; no simulated seed tuning and no p-values. Use GitHub Actions to independently verify exact original frozen source SHA and existing Stage7/6 contract tests and log a marker. If any contradiction or failed fixture, correct source and rerun while preserving the original design assumptions.

## Explicit novelty warning
Deterministic Lipschitz uncertainty propagation, robust upper confidence envelopes, and safe/optimistic scheduling are established ideas. The present mathematical construction is a **formal diagnostic/prototype under strong assumptions**, not proof of novelty, not source-model validity and not an established improvement over FGCS CASPER. Any later JPDC claim needs a prior-art survey, realistic measurable feedback, new decision contribution beyond this standard bound, additional physical network mechanism and separate fresh development/confirmatory data. Previous original Java n10 p=.0625, factorial n4 p=.125, independent native n10 p=1.0 nonsignificant; CloudSimPlus vs independent strict FIFO transfer gate FAILED max9.1214ms>5ms. All unchanged.
