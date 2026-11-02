# Certificate attribution and probe routing audit (2026-11-02)

Frozen source blob: `34256ca7bff46f911cf20e8b94278fbd09175746`.
Scope: source-level audit, not a new CloudSim experiment.

## Observed execution ordering

1. For CP policies, `family=topK(pred,eligible,3)`, then upper prediction
   bounds are built and the first candidate with `upper[p]<=deadline`
   is assigned `safe`.
2. `certified = safe>=0` and `j = family[safe>=0?safe:0]` are assigned.
3. **Only** if `policy.health && t.crit()==Crit.NORMAL`, the sparse
   probe may override `j` with `target`, provided `target>=0` and
   `baseEligible.test(target)`.
4. `DispatchMeta(...,j,...,certified,familyCovered,probe)` holds the
   final selected node and previously calculated certificate.
5. At task completion, `MissionRec` records only tasks where
   `m.task.crit()==Crit.MISSION`.

## Interpretation

- For `Crit.MISSION` tasks, the NORMAL-only probe override is not
  taken; this particular certificate/node mismatch mechanism does **not**
  directly affect reported mission-only `late_far` or `late_air`.
- For `Crit.NORMAL` tasks, a probe may override the previously certified
  candidate; a certificate should **not** be assumed to describe the final
  probe target. These normal-task certificates do not directly populate
  mission-only FAR/AIR.
- NORMAL probe routing can indirectly change queue conditions and future
  MISSION outcomes; source inspection alone cannot quantify that effect.
- Counterfactual `familyCovered` is separate from the chosen-node
  deadline certificate (see `FWC_CERTIFICATION_SEMANTICS_AUDIT_2026-11-02.md`).

## Manuscript-safe language

"Mission-task certificate outcomes were recorded for final dispatches;
the sparse-probe override is restricted to normal-priority tasks.
Effects of normal-priority probing on subsequent mission-task queue
states cannot be excluded without task-level intervention."

No E4.6/E42 modification. Follow up: inspect real seed29 trace
and compare mission-task node/certificate decisions across policies.
