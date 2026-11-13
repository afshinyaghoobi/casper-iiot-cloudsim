# Stage59 pre-outcome specification — ambiguity-set deadline-aware minimax-regret decision contract (2026-11-13)

## Why a formal decision contract, not another heuristic sweep
- Original n=10 independent native Python CASPER_FULL-vs-PRED_GREEDY holdout (GitHub run41920321822) showed **no primary statistically significant benefit** (paired sign p=1.000); stage52 queue-pressure S2 no-harm gate failed and Stage58 least-inflight DEV n=2 was adverse. Stop inventing threshold versions and burning holdouts.
- Existing Stage22 `RobustDominanceController` only switches when a candidate's assumed *upper cost* is below greedy's *lower cost*. It did not establish physically valid bounds, and is different from the present finite-ambiguity-set *decision-risk* objective.
- Stage59 is **pure mathematical and software contract validation ONLY**. It does **not** design/validate a realistic ambiguity set, estimate its coverage, implement a causal model of shock probabilities, run a new physical source simulation, change original CASPER E42/E4.6 or claim algorithmic novelty or superiority.

## Frozen precise algorithm
Input: 21 nominal end-to-end predicted costs `nominal[j]>0`, a nonempty finite rectangular set of **hypothetical** cost vectors `worlds[w][j]>0`, and a positive task relative deadline `deadline_ms`. The input matrices are generated hypothetically here, **not** extracted from the unobservable true fault set, future service, future arrivals or true per-node counterfactual latencies. Real deployment would need a separate time-causal calibrated ambiguity-set builder with source-specific validation. At decision time all 21 possible candidates share the same legal node/VM eligibility set (all nodes), no migration/preemption.

For each node j:
`M_j = max_w 1{cost[w,j] > deadline_ms}` (worst-case integer missed-deadline indicator, 0/1);
`R_j = max_w(cost[w,j] - min_k cost[w,k])` (worst-case latency regret w.r.t. **world-specific** best node, an idealized comparator used only inside the *hypothetical* matrix).
Select lexicographically **(M_j, R_j, nominal[j], j)** minimum. This guarantees an ambiguity-robustly deadline-feasible choice *if and only if* some eligible j satisfies all provided hypothetical world deadlines; this is only a model-conditional guarantee and **no claim of actual deadline coverage**. Minimizes worst-case regret only **among** minimum worst-case miss choices; do not misstate as unconstrained minimax regret.

In nominal mode with just one world of `worlds[0]=nominal`, the selector must be identical to PRED_GREEDY. Other scenarios may choose differently. Inputs reject NaN/Infinity, nonpositive costs, malformed dimensions, boolean numbers, invalid deadlines, no worlds. Deterministic index-based ties.

## Prior-example proofs and falsifiability
1. **Indistinguishable-world no-free-lunch:** two nodes and two physically possible worlds `A=(10,12)`, `B=(40,12)`, all same observable information at issue time. Nominal greedy selects node0; with deadline20, robust choice node1. If world A is true, greedy has latency10 vs robust12 (+2ms); if B true, robust12 vs greedy40 (-28ms). No causal deterministic policy at this observation can have the optimal per-world latency in both worlds: choices cannot depend on the hidden world. For randomized selection with probability p of node0, expected regrets are `2(1-p)` in A and `28p` in B; minimizing max gives `p=1/15`, worst expected regret `28/15 ≈ 1.8667ms`, not 0. These simple minimax-regret calculations hold only for this two-world toy matrix, not a physical CASPER distribution.
2. **Model-conditional feasibility:** For finite world-cost matrix, a candidate has M_j=0 exactly when its costs are ≤deadline in **every provided world**. Lex-min selection chooses such a candidate if any exists. Does not show real-world true state belongs to set.
3. **Decision complexity:** O(W·N) for calculating world-min costs, then worst-case indicators/regrets per node, with W explicit finite worlds and N=21; storage O(W·N) input. This is a small deterministic observation-to-decision component, **not** a new proven uncertainty predictor.

## Strict engineering gates before any future DEV
- Unit checks toy counterexample, nominal-only greedy equivalence, deterministic ties, missing/invalid inputs, verified regret and deadline feasibility, no future-world oracle.
- Exhaustive enumeration of **two-node two-world positive integer costs 1..8, deadline 1..8**, embedding those two candidates into a 21-node matrix with all other nodes strictly dominated (high fixed costs), must agree with a separately implemented brute-force objective; record total enumerated combinations (8^5=32768). No stochastic simulation or significance.
- CI checks immutable E42 SHA `34256ca7bff46f911cf20e8b94278fbd09175746`, frozen original E4.6 unchanged, source commit and twice byte-identical JSON/test logs. If code or check fails, preserve the failed job and correct implementation rather than moving the mathematical acceptance gate.
- **STOP after unit validation**. Before any real-world or large scientific DEV run, preregister how the ambiguity worlds are built from legal CPU-finish and E2E-delivered feedback, how calibration/coverage are audited out of sample, and why model scenarios are non-oracle. Do not call this paper novelty or efficacy before that study.
