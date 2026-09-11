# E4.3 Trace-Only Root-Cause Report

## Conclusion

The 30-seed trace campaign isolates an implementation/event-ordering failure in the intended online feedback loop. Health alarms and E1.7 detector triggers do occur in completion callbacks, but no later VM-mapper decision observes an active alarm mask or active E1.7 state.

This diagnosis does **not** authorize threshold tuning, architecture redesign, or reinterpretation of the failed E4.2 publication gate.

## Decisive evidence

Across all **584,326** trace rows:

- nonzero `alarm_mask_at_dispatch`: **0 rows**
- `e17_alarm_ever=true` at dispatch: **0 rows**
- `e17_transition_age>=0` at dispatch: **0 rows**
- `eta_at_dispatch != 1`: **0 rows**
- `health_changed_dispatch=true`: **0 rows**
- `eta_changed_certification=true`: **0 rows**

At the same time, completion-side triggers were real:

- S2 / CASPER_FULL: **67 health alarms**
- S4 / CASPER_FULL: **74 health alarms**
- S3 / CASPER_FULL: **0 health alarms**, consistent with the frozen detector observing service time rather than hidden network latency
- E1.7 triggered in **20/30 S2 seeds**, **20/30 S3 seeds**, and **22/30 S4 seeds**

Therefore the detector mechanisms are not simply absent. Their state changes are not reaching subsequent dispatch/certification decisions in the traced execution.

## Health detector findings

The compute health detector is capable of detecting hidden compute loss. Every recorded first health alarm in S2 and S4 was on a truly affected node.

Median first-alarm delay after the hidden change was approximately:

- S2: **531 ms**
- S4: **220 ms**

Yet even after those alarms occur, no dispatch row contains a nonzero alarm mask. This is incompatible with the intended online semantics where later tasks should exclude alarmed nodes.

Affected nodes are also highly relevant to Mission decisions, so lack of effect cannot be explained by zero exposure:

- S2: affected node appears in the Mission candidate family in **59.95%** of rows; selected Mission node is affected in **24.49%**
- S3: **62.42%** candidate-family exposure; **31.60%** selected-node exposure
- S4: **55.40%** candidate-family exposure; **22.94%** selected-node exposure

## E1.7 findings

The E1.7 detector itself triggers in many runs, generally after the hidden change. Median trigger offsets were about:

- S2: **582 tasks** after change
- S3: **513 tasks** after change
- S4: **690 tasks** after change

However, every dispatch still uses `eta=1.0`; no dispatch observes `e17_alarm_ever=true`, and the eta counterfactual changes **zero** certification decisions.

Thus the aggregate E4.2 observation that adaptive policies are outcome-equivalent to static ranked CP is explained by event-state propagation, not by evidence that the chosen eta limits or detector thresholds are intrinsically ineffective.

## Mechanistic interpretation

The frozen E4.2 implementation updates health and E1.7 inside Cloudlet finish listeners, while VM selection is performed by the broker VM mapper. The trace shows completion-side state changes, but mapper-side snapshots remain at their initial state for every dispatch. The strongest diagnosis is therefore that the current CloudSim submission/mapping execution does not interleave outcome-driven state updates with later dispatch decisions in the way the scientific online policy assumes.

CloudSim Plus supports delayed/dynamic Cloudlet creation and runtime policies, so a future implementation-parity correction should explicitly schedule arrivals/dispatches as simulation events rather than relying on a pre-submitted list if online feedback is required. This should be treated as a new implementation-parity stage, not E4.2 retuning.

## Required next stage

Create a new stage (recommended: **E4.4 Online-Dispatch Parity**) with a prelocked protocol requiring:

1. identical scientific seeds, workload, thresholds, policies, and hidden-change scenarios;
2. only event-scheduling/submission semantics may change;
3. dispatch must occur at task arrival during simulation time;
4. completion callbacks must update health/E1.7 before later arrivals are mapped;
5. a small deterministic parity harness must prove causal ordering before any 30-seed rerun;
6. E4.2 remains frozen and retained as failed publication-scale evidence;
7. no scientific tuning between parity correction and any subsequent campaign.
