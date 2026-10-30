# JPDC Gate 2 — FIRST_IDLE_TIER analytical capacity sanity check (2026-10-30)

This is **not** CloudSim output. It is an expectation-level nominal CPU demand calculation directly from the unchanged E42 generator, carried to generated E45.

## Source constants
- Task class probabilities: NORMAL=0.80, HIGH=0.15, MISSION=0.05.
- Work distributions `lognormal(median, log_sigma)`: NORMAL (25, .45), HIGH (45, .50), MISSION (18, .35).
- Nominal service: `12*work/cap` ms, with `cap` in the simulator's abstract CPU-capacity units.
- Interarrival rate prechange `lambda=0.12` tasks/ms; in scenario S1_LAMBDA_X2 and S4_COMPOUND postchange `lambda=0.24` tasks/ms.
- Edge layer has 12 nodes with `cap in [2.5,6]`; middle has six nodes with cap 8–20; cloud six with cap 30–70.

## Exact expectation formula under generator distribution

`E[work] = .80*25*exp(.45²/2)+.15*45*exp(.50²/2)+.05*18*exp(.35²/2) = 30.736671... `.

Nominal CPU capacity demand in `cap` units is `lambda*12*E[work]`.

| Postchange arrival regime | lambda tasks/ms | Nominal expected CPU demand cap-units | Total edge capacity range |
| --- | ---: | ---: | ---: |
| S0 or scenarios without rate shock | 0.12 | 44.2608 | 30–72 |
| S1 and S4 after rate shock | 0.24 | 88.5216 | 30–72 |

**Conclusion:** with doubled arrival rate, expected offered nominal work is greater than the *maximum* combined capacity of the 12 edge nodes (`88.52 > 72`). A policy that never spills tasks outside the edge tier cannot be stable at steady state for this nominal workload; some middle/cloud placement or admission control is required. This is *not* a guarantee that any specific finite 30,000-task run has positive drift every interval.

## Why this matters for FIRST_IDLE_TIER

The actual adapted policy scans edge indices 0..11, then middle indices 12..17, for an idle node in the estimated virtual queue; only when **all** 18 are busy does it spill to a minimum-predicted-latency cloud node. It is not strictly edge-only. Thus the edge-tier overload bound does **not** prove FIRST_IDLE_TIER unstable. Instead, it establishes that non-edge traffic and backlog/idle detection matter essentially under the rate-doubling scenarios.

The fixed index first-fit rule can also create systematic exposure differences: low-index edge nodes receive priority whenever multiple nodes appear idle. Node capacities are independently sampled by `makeNodes(seed)` and node indices do not rank capacity. This is a testable hypothesis about dispatch concentration, not a measured finding.

## Interpretation boundaries
- Calculations use *nominal* work and capacity, not the simulator's stochastic service-noise correction, shocks, finite-sample task class realization, network costs, health effects or queue feedback.
- They do not imply a deadline violation rate, speedup, CASPER advantage or empirical significance.
- Verification should measure actual per-tier assignment counts and per-node load, using an instrumentation-only paired parity gate, **after** obtaining a real CloudSim pilot.
- Frozen E4.6 unchanged.
