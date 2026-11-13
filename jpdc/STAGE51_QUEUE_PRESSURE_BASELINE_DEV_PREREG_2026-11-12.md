# Stage51 prospective DEV: transparent queue-pressure + delivered-feedback online comparator (2026-11-12)

## Purpose and scientific status
Stage50 native three-cloudlet queue transition tracing **passed** in [run43362375409](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43362375409), but independent original 30k Python strict FCFS vs Java SpaceShared waiting parity still **FAILED** 9.1214009 ms > prereg 5 ms. The original 30k bypass was already observed previously in run41777312914: do not pretend Stage50 solved general queue fidelity or repeat the same trace merely to increase stage number. High-value next work: a transparent online contemporary **comparator**, NOT an improvement to original CASPER.

Inspired conceptually by queue/feedback responsiveness in Wu et al. (2026) DFAQ-LB (FGCS 182, 108460), this is **NOT the authors' method reproduced**, and must be called **QUEUE_PRESSURE_05** (queue-only ablation) / **QUEUE_PRESSURE_E2E_05** (queue + delayed node network-excess feedback), not DFAQ-LB. No original author source code claims, ant-colony method, threshold learning, or accuracy transfer.

## Immutable design, prior to Stage51 outcomes
Same independent 21-node Python strict FIFO physical simulation and *exact same* E42-style source workload, Stage3 S0 calibration (80,000 tasks) and S2 hidden CPU40%-loss / S3 hidden network50%-loss scenarios. Every task irrevocably assigned on arrival. For task at issue time `now`, observe all 21 `pred[j]` nominal arrival-time predicted latency and `vq.predicted_backlog(j, now)` causal virtual backlog, along with `risk_state.penalties()` containing only node-specific E2E-delivered excess prior to `now`. No true affected set, realized service/net, arrival-future task or event oracle enters decision.

Define fixed queue pressure `b_j = min(20.0, 0.5 * max(0.0, virtual_backlog_ms[j]))`. For QUEUE_PRESSURE_05, score `pred[j] + b_j`. For QUEUE_PRESSURE_E2E_05, score `pred[j] + b_j + min(20.0, max(0.0, delayed_e2e_network_penalty_ms[j]))`. Choose minimum score with deterministic lowest index tie. No tuning by seed, task criticality or scenario. No claim of calibrated risk bound, deadline guarantee or novelty by itself. Both retain original source simulation event physics; no CPU service prediction oracle.

Controls `PRED_GREEDY`, `CASPER_FULL` must remain exact frozen Stage6 original source JSON (modulo previously verified observational `shadow_network_epoch` key if present); baseline against original NodeLocal optional but not primary. Source code original E42/E4.6, Stage6, Stage44 and Stage50 unchanged; only isolated Stage51 simulator clone, pure selector, source runner/tests/workflow.

## DEV protocol before result
Fixed new development source seeds **101 and 102** only (distinct from prior DEV91–100, holdouts601–608/701–708/801–808/901–908/1001–1008). Two scenarios S2 and S3, 4 policies `PRED_GREEDY`, `CASPER_FULL`, `QUEUE_PRESSURE_05`, `QUEUE_PRESSURE_E2E_05`; 12,000 deployments each and independent S0 80k calibration each. Total **192,000 dependent policy-task observations**, science DEV n=2 source seeds, **not inferential significance**. The report must disclose every per-seed per-scenario postshock MISSION deadline miss integer count/denominator, all-MISSION misses, latency, wait, switches vs greedy, no negative result suppressed.

Before full DEV, test selector deterministically with synthetic examples: no-backlog mode equals PRED_GREEDY, large queue redirects, delayed E2E residual redirects, no future scenario info accepted, tie-break by ID, finite nonnegative input validation. Require exact original source parity for PRED_GREEDY and CASPER_FULL at each seed/scenario. Repeat all source outputs byte-identically. If any gate fails, stop, report real failure and fix errors before further claims; never report half-success as science.

## Development decision rules
- Operational success: all source runs, baseline unit tests, original policy parity, exact output repeat and task conservation PASS.
- Scientific outcome: report directional S2 and S3 postshock MISSION miss differences vs both PRED_GREEDY and CASPER_FULL, including harm. **No baseline superiority claim based on n2 development** even when favorable; no independent holdout until explicit new prereg and policy freeze.
- If QUEUE_PRESSURE versions rarely differ from PRED_GREEDY, report that as negative independent comparator value and do not rename near-alias as a strong baseline.
- Engine scope is **strict FCFS Python only**, not Java SpaceShared parity and not real IIoT validation.
