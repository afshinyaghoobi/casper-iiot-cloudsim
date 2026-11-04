# JPDC real-event E1.7 dual-memory independent replay protocol (2026-11-04)

This is a **component-level cross-language replay using the original CloudSim event stream**, not a second simulator or a new policy-efficacy holdout. Registered BEFORE running the new simulation. Frozen E42 blob 34256ca7bff46f911cf20e8b94278fbd09175746 and frozen E4.6 unchanged. No scientific behavior modifications.

## Fixed scientific run
S3_HIDDEN_NETWORK_50LOSS, seed index 40, original six HIGH affected-node mask [9,12,14,15,17,18], 80k calibration / 30k deployment tasks, eight original policies. Pair uninstrumented control vs generated-E45 observational logger for each policy and require exact scientific CSV parity excluding `mean_mapper_us`.

For CASPER_FULL only, emit the *actual calibration reference scores* once, in original array order, immediately after constructing E17. Emit an event for EVERY deployment task when `etaBeforeOutcome()` has been called but **before** its task's outcome is observed. Emit a score event immediately **after** the original Java E17 has observed each completed MISSION task's score, recording that score and Java post-observation detector state. These records are in true event order as generated during CloudSim simulation, not task-index order.

## Independent Python falsification
Python `DualMemory` from `jpdc/independent_casper_state.py` receives the one-time calibration reference input (not E17 memory internals) and replays each chronological event. For every dispatch, recompute eta from its own history, compare Java observed eta, alarm flag and transition age. For every observed mission outcome, feed the independently maintained E17 engine the logged *actual score*, then compare detector state and transition age. Scores themselves are native Java-computed outcome residuals; this does NOT independently validate their underlying predicted latency or service/queue realizations.

Require exactly 30,000 distinct dispatches, nonempty contiguous calibration references of at least 200 scores, unique MISSION outcome task IDs, complete/valid state booleans, deterministic event ordering, finite/physical scores, Java/Python eta within 1e-10, exact alarm and transition age. Require all 8 official policies' summary results unchanged by logging. If these gates fail, report failure without changing threshold or dropping events.

## Scope
A pass establishes E1.7 **feedback-state transition parity conditional on Java-sourced calibration reference and actual score stream** for one real scientific seed. It cannot establish independent stochastic workload, prediction, queue or CASPER full-system validation, causal improvement in deadlines, or statistics. Original registered 10-seed holdout p=.0625 and exploratory factorial p=.125 remain nonsignificant; original strict independent FCFS queue transfer gate remains FAILED (max wait 9.1214ms >5ms). Do not conflate them.
