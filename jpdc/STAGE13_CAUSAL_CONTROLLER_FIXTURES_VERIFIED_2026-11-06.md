# JPDC Stage13 — causal controller unit gate VERIFIED, 2026-11-06

## Verified executable evidence
GitHub Actions [42184251939](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42184251939), job 127780718457: COMPLETE SUCCESS. Official job logs explicitly contain `JPDC_STAGE13_CAUSAL_CONTROLLER_FIXTURES_PASS`, `JPDC_STAGE10_NORMALIZED_NETWORK_EPOCH_AND_SHOCK_FIXTURES_PASS`, `JPDC_STAGE6_PROBE_POLICY_UNIT_PASS`. E42 source blob remains unchanged. These are unit fixtures only, **not a physical full scheduling run**, **not empirical policy gains**, and **not JPDC-ready proof**.

## What passed
- UNKNOWN at no history and stale fallback never interpreted as certified low risk.
- E2E causality and age-aware state; bounded recent network feedback is usable only after delivery.
- Long-gap 0-to-1 normalized shock remains mathematically indistinguishable under frozen synthetic L, so no false guaranteed-detection claim.
- Post-alarm new epoch remains unverified until two new delivered samples.
- Older-generated late report quarantined, not allowed to overwrite newer history.
- Maximum one probing attempt per 100 NORMAL arrivals, never probe MISSION, deterministic rotating selection across equally unknown nodes.
- Empty deadline-eligible probe set safely skips.
- Retroactive observations rejected.
- Old Stage10 and Stage6 fixtures remain passing.

## Explicit limitations and technical debt before policy validation
- Standalone `FreshnessAwareController` is NOT yet inserted into the actual strict-FCFS physical event-loop. No performance comparison.
- Development-only constants `DRIFT=.0001/ms`, `EPS=0`, `MAX_FRESHNESS_MS=10000`, `MAX_PROBE_EXTRA_MS=2`, `PROBE_CADENCE=100` require independently justified or sensitivity-tested choices. 10000ms is algebraic insight from source-specific 0→1 shock under frozen L, not externally calibrated.
- `verified` is an **assumption-conditioned fresh-interval flag**, not a predictive guarantee or validated confidence certificate. A stale fallback decision is deliberately marked unverified.
- Synthetic controller computes task-specific network upper excess but currently does not carry over E42 conformal certificates/CP states. Do NOT call this a validated extension of CASPER_FULL or imply conformal guarantee.
- A NORMAL probing action reroutes a real task and may incur deadline/energy/latency opportunity costs; these have not been measured yet.
- The frozen Stage12 source simulator uses CPU finish as measurement-generation time, with E2E arrival as feedback-delivery time. It is stylized and cannot be called real transport congestion data.

## Next (Stage14): isolated source-generated physical integration
1. Predeclare development seed(s), scenario matrix, exact baselines and output schema. Never reuse seed83 as an untouched confirmatory holdout.
2. Clone or parameterize the frozen Stage11 Python strict-FCFS physical engine, leaving original files unchanged. Route only new policy arms via the standalone Stage13 controller. Before each arrival use controller.select(now,pred,task-specific nominal-net,deadline,class). On every completed E2E report call controller.deliver_e2e(...); no pre-E2E data exposure.
3. Assert task and CPU/E2E conservation, probe <=1% NORMAL, deadline-eligible probe, no MISSION probing, finite decision values, strict FCFS, E42 source unchanged; compare all old policy arms against Stage6 exact outputs.
4. Collect mission deadline misses, latency distribution, probe overhead, stale/UNKNOWN decisions, true alarm times (offline), budgets, per-node feedback counts and false alarms. Do not claim improvements without independent paired multi-seed validation and uncertainty reporting.
5. Only after Stage14 developmental integration passes design confirmatory heldout paired experiments, sensitivity and cross-simulator fidelity work.
