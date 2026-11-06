# JPDC Stage13 — prospective algorithm-design specification, before new efficacy runs (2026-11-06)

## Scientific objective
Construct and falsifiably evaluate a genuinely distinct **information-freshness-aware active observation + deadline-risk scheduling** mechanism. Stage12's 5 missed alarms under dev seed83 are fully accounted for by the *assumed* L drift bound and long time separation, not by absent prehistory. The new method must not purport to infer a hidden change from inherently uninformative delayed measurements. No tuning or successful outcome selected from seed83.

## Definitions
At real scheduler time t, a node j's causally delivered E2E network observations have generated times m <= delivered times d <= t. Normalized excess `z=max(0,actual_network_ms/nominal_network_ms -1)`. Under an **explicit, unvalidated assumption** `|z(t)-z(m)| <= L_j (t-m)+epsilon_j`, interval for current network excess from an accepted observation is `[max(0,z-epsilon-L(t-m)), z+epsilon+L(t-m)]`. Unseen nodes must remain UNKNOWN (not zero risk). Disjoint intervals are an observed-epoch contradiction; changes learned only after delivery. The original Stage10 observer, its L and epsilon, and the prior shadow engine must remain baseline fixtures.

## Separate candidate decision components (not yet claims)
A. Staleness state: age of latest **delivered accepted** node observation (not task index), uncertainty interval width, and completeness after an alarm. Any prospective action uses only this available state.
B. Probe budget: at most 1% of NORMAL task routing opportunities, *no MISSION probe traffic*. Predeclare a per-probe deadline slack constraint and measure opportunity cost against original policy. Candidate probes target high expected value of fresh information under long-age gaps, while honoring independent no-observation and feedback latency. If no feasible probe, abstain; no oracle node selection.
C. MISSION routing: choose among baseline admissible nodes using a decomposed nominal predicted time + task-specific network-excess penalty + explicit unknown/staleness handling. Do not claim statistical guarantees from synthetic L intervals. If all nodes unknown or unsafe, use a fixed, documented fallback and record a separate unverified decision flag. Existing CASPER conformal state must not be reinterpreted as valid for new policy without new calibration.
D. Change response: after an observed incompatible change, mark node interval UNKNOWN/UNVERIFIED until sufficient *new delivered* measurements; never retroactively change previous dispatch decisions.

## Development tests required before running scheduling comparisons
1. No future E2E outcomes / source truth / affected-node masks enter controller.
2. An old-generated late-delivered report cannot contaminate fresh model.
3. Construct counterexamples to naive 'more probes guarantees detection': long measurement gap under large L can remain unidentifiable.
4. In no-history and all-stale environments, action follows documented fallback and labels uncertainty.
5. Probing never exceeds 1% NORMAL opportunities, never routes MISSION as probe, never creates fictitious free observations.
6. Record within-node age/coverage, detectability gap and probe cost.
7. Compare against CASPER_FULL, PRED_GREEDY, the original Stage6 residual policy and 1% NORMAL probing policy, and relevant published methods chosen after independent literature review.

## Pre-registration gate
Before any new scientific **confirmatory** scheduling experiment, freeze: novel decision rule; all hyperparameters and fallback semantics; scenarios incl compute-only negative control and network shock; paired evaluation seeds independent of seed83; budgets and workload; primary deadline-miss measure and secondary tail latency, mean latency, probing cost, detection/coverage; statistical plan and stop criteria. Do not run a large seed search or cherry-pick. If routing improvement is absent or not robust, report that truth and reconsider paper story/venue. Stage13 implementation and evaluation are NOT performed or validated by the existence of this design specification.

## Independent simulation caveats
All Python FCFS/Java SpaceShared mismatches remain. No new physical trace, CloudSim queue parity, or YAFS claim without corresponding real runs.
