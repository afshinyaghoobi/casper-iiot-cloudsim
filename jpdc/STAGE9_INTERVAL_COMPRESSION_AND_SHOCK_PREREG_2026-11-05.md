# JPDC Stage9 — exact constant-size interval envelope and abrupt-shift falsification
**Pretest registration, 2026-11-05. No new scientific seeds, no performance inference.**

## Mathematical objective
The Stage8 observed-feedback Lipschitz interval at time t is:
`LOW(t)=max(0,max_i(y_i-eps-L(t-m_i)))`, `HIGH(t)=min_i(y_i+eps+L(t-m_i))`, for DELIVERED reports with generation timestamps m_i <= delivery d_i <= t.

Algebraically this equals:
`LOW(t)=max(0, A-Lt)` with **A=max_i(y_i-eps+L m_i)**;
`HIGH(t)=B+Lt` with **B=min_i(y_i+eps-L m_i)**.

Thus for a *fixed externally justified drift L and measurement error eps*, the numeric interval **after ingestion** can be evaluated from just **two accumulated extremal scalars per node**, in O(1) per query. A 21-node selection is O(21), and the interval summary requires O(21) state. Keep per-node observation count and latest *measurement generation* timestamp for diagnostics; old report data not needed for *envelope evaluation*.

### Important distinction: interval evaluation vs consistency of ALL delivered reports
Stage8 checks every new report against every earlier report with the pairwise requirement `abs(y_new-y_old) <= L abs(m_new-m_old) +2eps`. Under arbitrary delayed out-of-order measurement arrivals, two A/B extrema at the current decision time are **NOT sufficient** to certify every pairwise historical constraint. The O(1)-state Stage9 summary MUST NOT claim it can validate the original full historical model unconditionally. Instead:
- An **audited reference mode** delegates deliveries to original Stage8 full-ledger model, which rejects historical contradictions and preserves out-of-order generation reports.
- A separate **summary-only mode** accepts reports for O(1) interval evaluation but explicitly identifies its status as **UNAUDITED**; it is NOT allowed to emit a valid-model or certified-latency claim without an independent consistency audit. It should reject any aggregate interval with LOW>HIGH at query time but that alone cannot establish historical consistency.
- We also test a *chronological measurement-time mode*: if generation timestamp m is nondecreasing across deliveries on that node, the incremental A/B extrema suffice to check new pairwise compatibility in O(1) under the same drift/noise assumptions; such ordering is **NOT automatically valid for real E2E delayed delivery**, so this is a restricted contract only.
- All observations use E2E delivery timestamps and no use of undelivered/future measurements. Global delivery must be nondecreasing, while generation times across reports can arrive out of order in audited/unaudited modes.

## Shock falsification contract
Under a deterministic synthetic node-level risk jump (e.g. r=0 at t=0 and r=20 at t=10), L=.1ms/ms, eps=0, the assumed Lipschitz bound permits only 1ms change, so a **proper audited model must reject the second observed report**. The algorithm may not respond by secretly tuning L upward on the inspected shock to claim original coverage. A summary-only version can be described as an interval arithmetic state, but not as a verified dynamic model.

Test a separate **task-size counterexample**: identical latent node condition but task-specific transfer excess differs with task size; a single node-only latent excess and epsilon=0 can be inconsistent. This shows dependence on task size needs a physical model or explicit error budget; merely including node ID is not sufficient.

## Fixed executable gate
Create a new pure module with:
1. Audited exact summary: full original Stage8 ledger for all historical consistency, plus stored O(1) A/B state for exact-time interval evaluation, retaining unbounded ledger **for audit**. This runs O(1) envelope query but **not** O(1) total memory; do not mislabel.
2. Compact chronological-only summary: O(1) per node memory/updates and mathematically exact pairwise check **if** measurement generation timestamps nondecrease on each node. Reject any out-of-order generation per node and distinguish restriction from Stage8 unrestricted audit. Need explicitly prove sufficient extrema conditions.
3. Compact unaudited out-of-order summary: O(1) per node memory and exact algebra for *any ingested reports*, but never assert that the underlying drift/noise assumptions are validated.
4. Synthetic exact path parity against original Stage8 over monotonic and out-of-order generation streams, edge cases L=0 and eps=0, multi-node, no feedback, delayed delivery, invalid inputs, 20ms abrupt jump and task-dependent excess counterexamples. Test a deliberate case where summary-only **cannot certify historical consistency** even if current LOW<=HIGH, to prevent incorrect claims.
5. Complexity tests do not benchmark runtime without controlled environment. No task-policy simulations, seeds, empirical p-values or out-of-sample performance statements.

Current prior research statuses remain fixed: original native n10 p=1.000, Java n10 p=.0625, exploratory n4 p=.125, all nonsignificant; original CloudSimPlus vs strict-FCFS physical parity gate FAILED 9.1214ms >5ms. Original frozen E42 blob SHA 34256ca7bff46f911cf20e8b94278fbd09175746 and E4.6 unchanged. This standard algebraic compression is not claimed new literature-wide novelty; Stage9 is primarily scientific quality assurance before integration into physical scheduling.
