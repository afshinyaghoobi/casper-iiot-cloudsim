# JPDC Stage12 — immutable node-specific temporal identifiability audit VERIFIED (2026-11-06)

## Status and non-claims
**Real GitHub Actions success:** original Stage12 trace run [42180091694](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42180091694), artifact 13484148975, exact legacy Stage6 parity and byte-identical repeat, and separate **immutable-artifact-only** archived margin audit [42183045593](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42183045593), success marker `JPDC_STAGE12_IMMUTABLE_NODE_MARGIN_AUDIT_PASS`. No Stage12 physics rerun was used to generate this second audit. This is source-generated **seed83 developmental evidence**, two predefined S3 policies, not independent inference or confirmed scheduler gain.

## Actual mechanism
The frozen Stage10 contradictory-epoch test triggers on a delivered nonquarantined same-node pair only if

`abs(z_new-z_old) > L * abs(t_measured_new-t_measured_old) + 2*epsilon + 1e-10`.

Frozen assumptions: `L=.0001 per ms`, `epsilon=0`. In S3, affected node network multiplier is 2, so its normalized slowdown `z=max(0, actual/nominal - 1)` changes from 0 to 1 (within source physics). **A pre/post shock pair can detect a unit change only when measurement-generation separation is <10,000ms**, under this assumption; at >=10,000ms, a complete 0→1 jump is formally compatible with the assumed smooth drift. This is an observability / assumption issue, not proof of no shock and not a statistical detector property. Feedback is revealed at E2E delivery, but the bound uses CPU-finish *measurement-generation* time. It never uses hidden shock onset to make decisions.

## Six damaged nodes: frozen pre/post trace; amounts in ms

| S3 affected node | Prior pre-shock reports | FULL post reports | FULL minimum measurement generation gap | FULL maximum incompatibility margin | PROBE post reports | PROBE minimum gap | PROBE maximum margin | Alarm FULL/PROBE |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 0 | 6 | 1 | 13380.448 | -0.338045 | 2 | 12444.902 | -0.244490 | 0 / 0 |
| 3 | 6 | 1 | 13355.284 | -0.335528 | 2 | 12273.789 | -0.227379 | 0 / 0 |
| 5 | 7 | 1 | 13518.620 | -0.351862 | 1 | 12356.495 | -0.235649 | 0 / 0 |
| 6 | 6 | 1 | 13255.225 | -0.325523 | 2 | 12394.400 | -0.239440 | 0 / 0 |
| 9 | 6 | 1 | 13183.969 | -0.318397 | 1 | 12148.431 | -0.214843 | 0 / 0 |
| 17 | 1614 | 330 | 24.964 | +0.997504 | 8 | 24.964 | +0.997504 | 1 / 1 |

The tabulated `minimum gap` is computed over accepted postshock observations having prior accepted pre-shock information available at that delivery instant. The maximum incompatibility margin is the actual reconstructed delivered-state rule margin in that subset: `|delta z| - L*|delta t|`; it is **not** a statistical score or learned posterior. Node17 has 13 postshock quarantined E2E reports under FULL, none for PROBE. No postshock reports were quarantined for nodes 0,3,5,6,9 in either policy. All five no-alarm nodes had prior pre-shock accepted observations and at least one genuinely comparable postshock observation at decision/feedback delivery time. Thus **missing pre-shock history or postshock quarantine are not the causal explanation in this frozen episode**. The frozen specified drift envelope explains the five no alarms: even the most favorable accepted generation-time separation exceeds 12 seconds > the 10-second identifiability limit.

## Causal limitations
The evidence establishes a *conditional algebraic explanation* of the detector outcome, not causal generalization over seeds/faults, not a diagnosis of true fault onset, not a validated choice of L, not real network telemetry and not proof that increasing probing will always help. The exploratory source's shock is task-index based, not a network wall-clock event. Reusing seed83 for sensitivity selection is development, never untouched confirmatory evidence. Probe itself affects routing and observation opportunities, but the detector remains shadow-only. Source-generated S3 multiplies full network duration; native Python strict-FCFS does not establish Java CloudSimPlus equivalence.

## Next research design: distinct contribution required
Stage13 must distinguish **information freshness, costly active observation, interval-width uncertainty, and change-aware scheduling** rather than presenting the old Stage10 simple drift contradiction as a new publishable algorithm. Candidate approach: causal age-aware exploration-budgeted scheduling; observation events arrive strictly after E2E completion; node risk is unknown when no fresh compatible evidence; targeted probing must consume explicit NORMAL-task and performance budget; MISSION decisions include conservative fallback. Pre-register development vs untouched holdout cohorts, metrics and comparison set before running any positive performance experiment. A fixed synthetic L may be investigated only as sensitivity on DEVELOPMENT data, not retrospectively advertised as externally calibrated. Keep original CASPER / FGCS E42 unchanged.

## Sources
- [Original Stage12 evidence](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42180091694)
- [Archived-only margin evidence](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42183045593)
