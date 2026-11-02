# JPDC interpretation audit: FWC vs certification (2026-11-02)

## Verified implementation
Source: `src/main/java/org/casperiiot/e42/E42Campaign.java`, frozen blob `34256ca7bff46f911cf20e8b94278fbd09175746`.

For CP policies, `family = topK(pred, eligible, 3)`. For every candidate k in this family, the code computes
`upper[p] = pred[k] + eta * q * sigma` and
`actualAudit[p] = counterfactualActualLatencyMs(..., k, ...)`.
`familyCovered` is set false if **any** candidate has `actualAudit[p] > upper[p]`.
This counterfactual family-wide coverage is recorded as `MissionRec.fwc` and aggregated as `late_fwc`.

Separately, `certified` means that at least one candidate satisfies `upper[p] <= deadline`.
`late_air` counts `!certified`; `late_far` counts `certified && actualLatency > deadline`.
The deadline violation uses the **observed completion latency of the selected task**, not the
counterfactual family audit used by FWC.

## Scientific implications
1. Do **not** label `late_fwc` as the fraction of correctly certified jobs, or a conditional
   accuracy/precision of certificates. It is *family-wide upper-bound coverage*.
2. An elevated `late_fwc` can coexist with a larger `late_air` and nearly unchanged
   `late_dvr`; they refer to different events.
3. `late_far / (1 - late_air)` estimates conditional deadline misses among certified
   mission tasks (if any certified). It does not imply matched-certificate causal improvement.
4. The `familyCovered` field in the seed29 dispatch trace records this counterfactual
   family-wide audit already computed by the simulator.
5. For the eventual manuscript include explicit event definitions and denominators. Do not
   infer calibration of selected-node certificates from `late_fwc` alone.

## Evidence status
Source-code interpretation only; no new CloudSim run. Seed29 task-level experimental trace
still not verified. Frozen E4.6/E42 source remains unchanged.
