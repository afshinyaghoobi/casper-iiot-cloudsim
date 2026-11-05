# JPDC Stage7: identification boundary under selected-only delayed node feedback
**2026-11-05 | Mathematical diagnostic, NOT a new claim to bandit-theory originality**

## Prespecified mathematical claim

In original Stage6, NEW_NETWORK_RESIDUAL chooses only observed-task E2E node-local network residuals, while NEW_NETWORK_RESIDUAL_PROBE can spend one actual NORMAL job every100 NORMAL arrivals to observe a relatively underobserved eligible node. The pilot was executed (seed82) BEFORE this analysis: probing increased nodes with any E2E feedback S3 13/21→21/21, yet increased total MISSION missed deadlines 5→6, with only one positive new probe sample. This document does **not** retroactively convert that exploratory result into a confirmatory theorem.

We isolate the **information limitation**, not a proof of regret for CASPER's endogenous 21-node queueing system.

### Proposition 1 — two observationally indistinguishable worlds

Consider one pre-dispatch choice between two eligible nodes `a` and `b`, and a state of common observed history H. Node `a` has known task E2E latency **10 ms** in both deterministic worlds. Node `b`, which has **no E2E feedback delivered** during the relevant observation window, has actual latency **6 ms in W_good** and **14 ms in W_bad**. All pre-dispatch task attributes, nominal predictions, previously delivered event timestamps, risk-window state, available feedback counts, and health observations are identical across the worlds. Hidden latent outcome at b is the only distinguishing variable.

For **any** (possibly randomized) nonclairvoyant policy, its probability p of selecting b conditional on this common H is the same in both worlds. Optimal latency is 6 in W_good (select b) and 10 in W_bad (select a). Regret (ms) is therefore:
- `E[regret | W_good,H] = 4(1-p)`
- `E[regret | W_bad,H] = 4p`
Thus `max(E[regret|W_good,H],E[regret|W_bad,H]) >= 2 ms`. For deterministic p∈{0,1} the worst-world regret is **4 ms**.

**Proof:** identical observed histories imply identical conditional action distributions. Substituting the two actual action latencies into the expected one-step regret gives the expressions; their maximum is at least their arithmetic average 2. This is an elementary bandit **indistinguishability** observation, not a claim of a new lower bound in the literature. It is strictly about *one isolated dispatch with exogenous fixed latencies* and no queue interference.

**Scope:** Does NOT prove a 2ms unavoidable regret on the actual 21-node Stage6 source model, nor any missed-deadline or conformal-coverage lower bound. It only proves impossibility of world-uniform best-node selection without distinguishing information under this constructed model.

### Corollary 1 — no chance to learn from feedback unavailable before decision
If a task probes b but its task-specific E2E observation arrives at time later than the next routing decision, the two histories are still indistinguishable **at that decision**, even though b was previously dispatched. Only completed and delivered feedback can distinguish the two worlds. Counting dispatched probes as if they were already observed creates look-ahead leakage.

### Proposition 2 — the deterministic 1%-NORMAL probe budget is a *coverage upper bound*, not a statistical guarantee
With exactly `M` NORMAL arrivals, at most `floor(M/100)` Stage6 NORMAL probe opportunities exist. The number of **new distinct previously unobserved nodes whose feedback could be collected exclusively because of probing** is at most `min(21, floor(M/100))`, and the number of successfully **delivered** such feedbacks by a fixed decision horizon can be smaller (even zero) if E2E completion is delayed beyond it. This combinatorial bound neither guarantees unbiased observation, nor represents total node coverage: a policy may observe additional nodes through ordinary dispatch.

**Proof:** each eligible probe opportunity selects at most one node for one physical task; it can add at most one first-time node observation, and observations cannot precede their physical E2E completion. No independence or positivity assumption is made.

### Why Stage6 did not establish improved resource decisions

- The number of different nodes observed is a **breadth** metric and can reach 21/21 even when the number of informative positive network-excess samples remains one.
- The probe target uses counts and staleness, not a randomized sampling mechanism with known propensity. Therefore conventional inverse-propensity correction is not defined without an added randomized policy and positivity assumptions.
- NORMAL probes sample a different task class; without assumptions linking NORMAL to MISSION network delays, statistical identification of MISSION-specific counterfactual delay is not established.
- More coverage can be expensive: actual probed NORMAL task E2E latency was about120.7ms and the same-state **nominal predicted** latency penalty about+71.3ms; no realized causal increment is identifiable from two diverging queue trajectories.
- Actual mission misses worsened from 5 to6 in the one observed S3 development seed. This does not establish a harmful population effect either.

### Literature boundary
This identification argument is a common feature of censored/bandit/delayed feedback, not a new JPDC theorem:
- Zierahn et al., *A Unified Analysis of Nonstochastic Delayed Feedback for Combinatorial Semi-Bandits, Linear Bandits, and MDPs*, JMLR 26 (2025): https://jmlr.org/papers/v26/24-0496.html
- Masoudian, Zimmert, Seldin, *A Best-of-both-worlds Algorithm for Bandits with Delayed Feedback with Robustness to Excessive Delays*, NeurIPS 2024: https://papers.nips.cc/paper_files/paper/2024/hash/ff54269c8c51ae379822f5f655b0f9a7-Abstract-Conference.html
- Bar-On and Mansour, *Non-stochastic Bandits With Evolving Observations*, ALT 2025: https://proceedings.mlr.press/v272/bar-on25a.html

This is targeted prior-work context, NOT a comprehensive novelty clearance and not a claim those bandit models equal this work's native strict FCFS queue/IIoT classes.

## Falsification fixture (not scientific outcome sampling)
Implement exactly the two-world arithmetic for p∈{0,.25,.5,.75,1}, check shared observables until a physically delivered end-to-end observation, verify randomized minimax bound 2ms and deterministic worst-case4ms. Test the 1% count upper bound and delayed feedback blindness with a purely synthetic clock. This requires NO new work seeds, no threshold tuning, and NO additional statistical inference. The original E42 and E4.6 stay frozen.

## Next credible algorithmic question
To move beyond this known identification barrier, a JPDC follow-on would need to specify (1) a **physically available and measurable** feedback process (including transfer/queue delays), (2) the target benefit (deadline misses with explicit exploration cost), (3) an observability/positivity or drift assumption under which learning is theoretically identifiable, (4) a new feasible decision procedure and mathematically meaningful bound (not a retrofitted empirical win), and (5) independent workload/network validation. With Stage6 1%-NORMAL probes, there is currently no demonstrated improved deadline completion, no regret proof, no independent industrial topology, and no YAFS.
