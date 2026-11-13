# Stage53 retrospective task-ID forensic of Stage52 adverse source seed1107 — VERIFIED (2026-11-12 CST / 2026-11-13 UTC)

## Scientific scope and execution provenance
This is **POSTHOC forensic diagnostic on an ALREADY CONSUMED holdout seed**, NOT new independent efficacy evidence (new scientific sample n=0). Registered explicitly after observing Stage52 adverse results and before new traces: `jpdc/STAGE53_RETROSPECTIVE_SOURCE_TASK_CAUSALITY_PROTOCOL_2026-11-12.md`, protocol commit `08ed1c618d5c97096e5be73092dcc6656cacada1`.

[Actual GitHub Actions run **43369672089**](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43369672089) **SUCCESS**, source commit `73294dcfe312a7a003da7f0577cd59885907d964`; artifact `jpdc-stage53-retrospective-task1107` **ID 14012300938**. Downloaded actual artifact and audited `audit.json`, `audit_repeat.json`, `audit.log`, `audit_repeat.log`, `source_commit.txt`. Complete JSON/log reruns byte-identical, JSON SHA256 `6e04640e291a295f5daa2dec57b848034e80419d3de7ab24a7a1d9374095e351`. All 4 policies×2 scenarios×12k tasks, source seed1107 80k original S0 calibration, original Stage52 seed1107 source artifact downloaded, aggregate per-policy metrics matched exactly. Full task-ID join, arrival/deadline task pairing, CPU+wait+network latency decomposition and original E42/E4.6 freeze guards **PASS**.

The original Stage51 comparator pure source, strict-FCFS Python physics and scores are untouched; passive preexisting `mission_audit_hook` only. All 96 source postshock MISSION task IDs matched across 4 policies in each scenario.

## Exact POST-shock MISSION misses by policy for seed1107
| Scenario | PRED_GREEDY | CASPER_FULL | QUEUE_PRESSURE_05 | QUEUE_PRESSURE_E2E_05 |
|---|---:|---:|---:|---:|
| S2 hidden CPU40%-loss | 6 | 1 | 5 | 5 |
| S3 hidden network50%-loss | 1 | 1 | 0 | 2 |

### S2 forensic: queue-pressure vs FULL
- QUEUE_PRESSURE_05 and QUEUE_PRESSURE_E2E_05 **exact same S2 outcomes**, with **42/96** POST MISSION tasks assigned to a different node than FULL. Delayed E2E added no marginal S2 benefit here.
- **1 saved MISSION miss**, task ID **10194** (FULL missed, queue-pressure on time).
- **5 new MISSION misses**, task IDs **[10339, 10351, 10553, 10857, 11712]** (FULL on time, queue-pressure late). Net **+4 misses**, reconciling original FULL1 vs new5.
- Illustrative matched source observations (CPU, WAIT, NET milliseconds):
  - Task10339: FULL node12, CPU18.167/wait0/network20.443, on time; queue node13 CPU23.691/wait0/network23.451, late. No queue-wait improvement to offset higher CPU and network.
  - Task10351: FULL node15 CPU27.538/wait0/network19.757 on time; queue node9 CPU46.486/wait0/network4.772 late. Lower network does not compensate larger CPU.
  - Task10857: FULL node16 CPU15.185/wait9.586/network10.686 on time; queue node13 CPU34.286/wait0/network23.437 late. Zero queue wait still missed.
  - Task10194 (SAVED): FULL node9 CPU57.811/wait0/network4.449 missed; queue node12 CPU15.750/wait0.536/network20.358 on time.
These are paired outcomes under different shared-queue and downstream-feedback histories; a node switch alone cannot be asserted as a task-level isolated causal effect.

### S3 forensic: addition of delivered E2E feedback vs QUEUE_PRESSURE_05
- QUEUE_ONLY had **0/96** misses. Adding E2E had **2/96** misses. Baseline E2E policy assigned **41/96** POST MISSION jobs to different nodes than queue-only.
- **0 saved misses, 2 NEW misses**, task IDs **[10194,10900]** vs queue-only; net +2. Relative to FULL, E2E had 0 saved and one new miss [10900], i.e. FULL1 vs E2E2; some prior full misses remain or move, and shared queues change.
- Task10194: queue-only node12 CPU15.750/wait0.536/net20.358 on time; E2E node4 CPU38.398/wait0/net7.864 late. Avoided queue/network delay did not compensate changed CPU.
- Task10900: queue-only node16 CPU18.697/wait10.682/net11.448 on time; E2E node15 CPU33.755/wait0/net20.922 late. Reduced wait was insufficient to offset increased realized CPU+network.
- This explains the observed aggregate `queue-only0` vs `queue+E2E2` in seed1107, not a universal claim about all network-feedback methods.

## Scientific conclusion
The Stage52 **S2 safety/no-harm gate failure remains**. These matched events show a plausible mechanism: a score adding queue and delayed-network penalties can route some tasks to nodes with substantially worse realized CPU and/or network times even when predicted backlog/queue wait is lower. Shared queues and future feedback make true task-level causality more complex. No new independent source seed, p-value update, parameter change, physical engine portability or original-author DFAQ-LB reproduction is demonstrated.

**Next high-value work:** avoid another numeric threshold chase. Develop an explicitly assumption-bound cross-physics validation or externally comparable baseline with mismatch documented. If a new structural candidate is proposed, preregister it before fresh DEV seeds, then run a fully disjoint holdout; Stage52 seeds1101–1108 are spent. Original CloudSimPlus SpaceShared–Python strict-FCFS 30k queue WAIT max mismatch9.1214009ms>5ms remains a separate registered FAIL.
