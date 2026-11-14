# Stage60 preregistered causal ambiguity-builder contract (2026-11-14)

**This is a software causality QA stage only.** Stage59 proved the finite-world lexicographic decision objective on hypothetical costs; it did not supply a defensible real-world world distribution or calibrated set. The current stage MUST NOT claim uncertainty coverage, physical truth, real IIoT data, deadline guarantees, publication novelty, or improved scheduling. Previous original native Python CASPER vs PRED_GREEDY holdout p=1.000 and Stage52/58 adverse results remain unchanged. E42/E4.6 untouched.

## Observable information and contract (before running tests)
Fixed topology 21 nodes. A `CausalAmbiguityBuilder` accepts only explicit observation functions:
- `cpu_complete(task_id,node,nominal_ms,actual_ms,finished_ms,delivered_ms)`: both CPU completion and its observation receipt occurred, in order, at/before selection. CPU excess `max(0,actual-nominal)`.
- `e2e_delivered(task_id,node,nominal_network_ms,actual_network_ms,cpu_finished_ms,delivered_ms)`: only E2E feedback delivered at/before decision. Network excess `max(0,actual-nominal)`; original generation/cpu finish cannot be later than delivery.
- `observe_telemetry(now_ms,virtual_backlog_ms)`: 21 nonnegative finite predicted queue backlogs from observed/estimated virtual queue; never an actual future CPU next-free oracle.
All events must have finite nonnegative clocks, nondecreasing delivery chronological order across CPU/E2E/telemetry records, valid ID/node, and unique (task, channel) records. Late CPU/E2E reports with per-node decreasing measurement timestamps are quarantined instead of overwriting newer per-node causal history. Distinguish *no feedback* from *zero observed excess*. Track count, quarantine, and telemetry timestamps. No hidden scenario label, affected mask, realized future service vector or direct physical simulator state API.

Frozen pilot parameters, no seed tuning: per-node 32 most recent valid excesses; CPU min samples=4, E2E min samples=8, freshness max-age=5000ms at selection, telemetry freshness max-age=100ms. Empirical correction magnitude per channel is max of observed excess in the recent window (a deterministic *sample maximum*, **not** a statistically certified upper bound). Require all 21 nodes to have both valid channel sample counts and fresh measurements and fresh telemetry for a **fully populated** 4-world matrix. If any node is unknown/stale, return explicit UNVERIFIED/ABSTAIN with missing-node reasons; **never turn lack of observation into zero uncertainty** and never call Stage59 `select` with missing-as-safe costs.

Given fresh nominal `predicted[j]>0`, known nominal network `nominal_network[j]>0` (input validation only), *causal* nominal queue estimator already included in predicted costs (no duplicate backlog addition); four hypothetical worlds are:
- W0 = pred
- W_CPU = pred + max(observed CPU residual)
- W_NET = pred + max(observed E2E network residual)
- W_BOTH = pred + both maxima
These are finite assumptions based on **historical delivered residual samples**, not bounds on true future, not coverage, not disjoint calibration, and they ignore unseen negative residuals. They may fail to capture shocks; nonstationary behavior makes sample maxima unsafe. Telemetry is used as a **freshness certification gate only** and the builder accepts the already computed `pred` values, not a queue oracle. The Stage59 selector may be called in unit QA only if status READY; its resulting robust-feasible flag must always be labeled model-conditional.

## Predefined tests
1. A clean cold-start with nominal values produces ABSTAIN, never a zero-penalty world.
2. Delayed network feedback delivered in the future must not influence earlier choice (e.g., before event delivery); attempt at retroactive decision after a future observation rejected.
3. Out-of-order delivery, duplicate task-channel, invalid times, NaN/Inf, wrong lengths and negative virtual backlog rejected.
4. A late generated measurement arriving after newer generated feedback must be quarantined, not rewind state.
5. Populate **every node** with four CPU completions, eight E2E deliveries and current queue telemetry, then require READY exactly four 21-vector worlds with expected deterministic maxima.
6. Freshness expiration: CPU/E2E or telemetry > threshold marks ABSTAIN; telemetry is a gate only, not injected as a duplicate cost.
7. An example changes Stage59 node relative to nominal greedy under **observable previously delivered hypothetical residuals**; this demonstrates a possible nonalias route, not superiority.
8. Run tests twice identically in GitHub Actions; preserve source hash and E42 freeze.

**No full deployment DEV or holdout** in Stage60. A future study requires independent observational calibration for uncertainty-set coverage (all candidate nodes are partially observed; unchosen node counterfactual cost may be unobservable) and empirical method/no-harm validation on fresh disjoint seeds. If most real arrivals lack 21-node fresh coverage, report abstention and do not relax requirements after seeing results.
