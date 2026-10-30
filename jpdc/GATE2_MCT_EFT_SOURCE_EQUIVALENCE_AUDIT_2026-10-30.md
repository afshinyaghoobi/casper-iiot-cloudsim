# Gate 2 source-level MCT/EFT equivalence audit — 2026-10-30

## Evidence from unchanged simulator code
Frozen E4.2 source blob: `34256ca7bff46f911cf20e8b94278fbd09175746`. E45 generation retains this dispatch score and queue-estimator behavior unless explicitly patched.

- `E42Campaign.predictedLatency`: `nominalNetworkMs(t,node) + vq.predictedBacklogMs(node,now) + nominalServiceMs(t,node)`.
- `PRED_GREEDY`: `argMin(pred,eligible)`; for this policy `eligible` includes every node.
- `VirtualQueueEstimator.predictedBacklogMs`: `max(0, nextFreeMs[node]-now)`. `onDispatch` tracks *nominal CPU service only*: `nextFree=max(nextFree,now)+service`.
- The CloudSim cloudlet runs CPU only; network latency is incorporated algebraically in reported end-to-end latency, not as pre-service VM arrival latency. Thus `PRED_GREEDY` is precisely the existing **online estimated completion/response-time minimum** under this model. An "online MCT" policy using these same terms, eligibility and tie breaks is an exact alias, NOT an independent comparator.

## Why the standalone Online EFT reference is not a drop-in baseline
Current independent Python reference scores `max(arrival + network_transfer, free_at) + service`. Its assumption is **network transfer before CPU service** and possible overlap of network time with earlier queue work. Existing E45 mapping scores `arrival + network_transfer + max(0,free_at-arrival) + service`, adding network time **after** CPU queuing and service for the measurement. The second form is consistent with the current model's explicit algebraic network term, the first introduces a different timing model.

Deterministic two-node counterexample at `arrival=0` (times in ms):
- Node A: `free_at=100`, `network=20`, `service=10`. Existing model predicts response `20+100+10=130`; standalone EFT predicts finish `max(20,100)+10=110`.
- Node B: `free_at=0`, `network=40`, `service=80`. Existing score `40+0+80=120`; standalone EFT `max(40,0)+80=120`.
- Therefore current `PRED_GREEDY` selects **B** while standalone `choose_eft` selects **A**, solely because of timing semantics.

This establishes non-equivalence and prevents falsely claiming a literature-style EFT policy as an equal-information, equal-system-model competitor. It does not imply either semantics is universally preferable.

## Baseline decisions
1. **Reject duplicate baseline:** do not implement online MCT by copying `argMin(pred,eligible)`; report existing `PRED_GREEDY` as response-time greedy/MCT-like.
2. **Do not insert EFT reference into the frozen E45 CPU/network accounting unchanged.** An experiment with transfer-before-computation needs its own fully specified model variant, shared consistently by *all* policies, and a separate model-validity study.
3. Select a substantively distinct online decision rule from published literature whose information and execution model match this simulator, or explicitly label a transparent exploratory control. Paper-faithful comparator selection remains open pending full text.
4. CloudSim performance claims require actual workflow artifacts, parity checks and paired independent seeds. No new CloudSim results are asserted here.
5. E4.6 unchanged.

Source code: `src/main/java/org/casperiiot/e42/E42Campaign.java`, `src/main/java/org/casperiiot/e41/core/VirtualQueueEstimator.java`, `jpdc/online_eft_reference.py`.
