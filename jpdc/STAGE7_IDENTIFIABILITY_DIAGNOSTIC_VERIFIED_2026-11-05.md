# JPDC Stage7 delayed-feedback identifiability diagnostic — VERIFIED 2026-11-05

## Outcome and precise boundary

Established an **elementary, source-independent and mathematically exact two-world indistinguishability example** for selected-only, completion-delayed task-network observations. A single decision maker with identical observable history cannot uniformly identify which of two eligible nodes has lower actual latency when the unselected node's latent network condition differs in two plausible worlds. The argument is **well known in bandit theory** and must NOT be described as a newly invented theoretical lower bound or a proven lower bound on the actual 21-node CASPER system. It does explain why Stage6's 21/21 physical E2E-feedback node coverage does **not imply** stable identification of current network health or improved deadline outcomes.

The main document `jpdc/STAGE7_DELAYED_FEEDBACK_IDENTIFIABILITY_PROPOSITION_2026-11-05.md` was committed **`c5a9e18b820ca302d8d9b7a00ddabf8780af56e7`**. First original Stage7 test implementation `jpdc/test_stage7_identifiability_counterexamples.py` was committed **`e5ad662cdbfcc649014eb2e8277c3b7f62c5cb58`**. CI `.github/workflows/jpdc-stage7-feedback-identifiability-gate.yml` committed **`6cb4c36c77e2c6207e8af6b62abc1d1d1310957b`**.

## Mathematically verified counterexample

- Two eligible task-node choices `a` and `b`. Both physically possible worlds have the same delivered task/health/queue observation history up to this decision and observed latency on a of 10ms.
- In W_good unobserved b has actual E2E latency **6ms**, so optimum b. In W_bad unobserved b has actual E2E latency **14ms**, so optimum a. Every policy conditional on identical observed history assigns the **same probability p** to choosing b in both worlds.
- Expected regret relative to **one-step exogenous fixed latency oracle**: `4(1-p)` ms in W_good, `4p` ms in W_bad. Hence `max{4(1-p),4p} >=2ms`. A fair coin p=.5 minimizes worst-case regret to **2ms**; every deterministic choice has worst-world regret **4ms**.
- Prior dispatch to b with E2E result still pending doesn't resolve the two worlds. The synthetic delivered-feedback clock test confirms histories equal at t<100ms and different only once the task's network outcome arrives at t=100ms. No current-task outcome, hidden physical mask or future latency enters state.
- With M NORMAL arrivals and a fixed probe cadence every 100, max probe *opportunities* `floor(M/100)`. Each can create at most one first-time node observed exclusively through probing, giving upper bound `min(21, floor(M/100))` first-time nodes in this 21-node setting. This is only an **upper bound**: if feedback is too delayed, actual delivered first-time node information before a chosen horizon may be zero, and ordinary dispatch may independently cover nodes.

**This is not a theorem about the native CloudSim network model:** exogenous two-node latencies, one isolated action, no resource queues, no stochastic task-dependent network distribution, and no repeated learning/counterfactual policy interference. It does not assert 2ms lower-bound regret for 21-node FIFO systems, anything about missed-deadline statistics or conformal validity.

## Real CI execution

**GitHub Actions run `42041296367` COMPLETED SUCCESS**, job `127292486870`, original audit artifact **`13421515268`**. Frozen original E42 Git blob `34256ca7bff46f911cf20e8b94278fbd09175746` checked; E4.6 unchanged. CI ran isolated synthetic mathematical fixtures, existing Stage6 bounded probe unit tests and Stage5 original network risk policy unit tests with markers:

- `PASS two-world common-history randomized minimax 2ms and deterministic worst-world 4ms`.
- `PASS delayed feedback indistinguishable until actual completed E2E delivery`.
- `PASS 1-in-100 NORMAL budget only upper bounds first-new-node feedback coverage`.
- `PASS before E2E report, dispatched exploratory task does not identify latent network state`.
- `JPDC_STAGE7_IDENTIFIABILITY_FINITE_COUNTEREXAMPLE_PASS`.
- `JPDC_STAGE7_IDENTIFIABILITY_AND_EXISTING_POLICY_GATES_PASS`.

No new source physical simulation, new seed, calibration, p-value or retrospective tuning was run. Original Stage6 seed82 results remain intact: S3 NEW no probe =5 MISSION missed deadlines; NEW+PROBE =6, 96 physical NORMAL probes, 1 positive probe network feedback, observed node breadth 13/21→21/21 but no demonstrated efficacy. Previous original native n10 sign p=1.000 nonsignificant, Java disjoint n10 sign p=.0625 nonsignificant, original n4 factorial p=.125 nonsignificant, original CloudSimPlus vs native strict-FCFS queue parity test FAILED max9.1214ms>prespecified5ms.

## Related prior work and novelty disclaimer

The mathematical indistinguishability is **not new** and overlaps the underlying information constraints of delayed/censored bandit feedback; it is used only as a rigorous diagnostic for this project's observed failure:

- Zierahn et al., JMLR 26 (2025), https://jmlr.org/papers/v26/24-0496.html (delayed feedback for multiple bandit/MDP classes).
- Masoudian, Zimmert & Seldin, NeurIPS 2024, https://papers.nips.cc/paper_files/paper/2024/hash/ff54269c8c51ae379822f5f655b0f9a7-Abstract-Conference.html (role of missing observations at decision time and delay).
- Bar-On & Mansour, ALT 2025, https://proceedings.mlr.press/v272/bar-on25a.html (feedback evolves/corrupts over time).

These model settings and guarantees are **not** proven to transfer to the native IIoT strict-FCFS queue; there is no novel regret guarantee or an original JPDC theorem.

## Research implications

The *next* genuinely novel research object is NOT simply "add probes". To support credible independent JPDC contribution, it would need an original and physically grounded **observation contract and joint control** with mathematically explicit assumptions (bounded feedback age, stochastic stationarity or quantified temporal drift, coverage/positivity under selected-only feedback, transport costs and network contention), explicit task-criticality-specific target and constrained exploration cost, plus a falsifiable result beyond known bandit theory and the original FGCS Algorithm1. Independent source network/workload traces or YAFS and a new disjoint preregistered holdout would be required for strong external claims. The Stage6 fixed1% probe was shown to add breadth but also same-state predicted cost and one MORE MISSION miss on original S3 dev seed82. Do not retune those data and claim significance.

### Reproduction
- Source proposition and proof: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/blob/jpdc-seed0-repro-20261024/jpdc/STAGE7_DELAYED_FEEDBACK_IDENTIFIABILITY_PROPOSITION_2026-11-05.md
- Finite deterministic fixtures: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/blob/jpdc-seed0-repro-20261024/jpdc/test_stage7_identifiability_counterexamples.py
- Real original success: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42041296367
- Original QA artifact: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42041296367/artifacts/13421515268
