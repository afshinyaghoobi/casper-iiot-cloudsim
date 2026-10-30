# Gate 2 — TSSLA reproducibility and online-information incompatibility audit (2026-10-30)

## Primary source verified
Sang, Cheng, Wang, Chen (2022), "A three-stage heuristic task scheduling for optimizing the service level agreement satisfaction in device-edge-cloud cooperative computing," *PeerJ Computer Science* 8:e851, DOI: 10.7717/peerj-cs.851, https://pmc.ncbi.nlm.nih.gov/articles/PMC8802786/ .

The original published method is not simply a choice of VM for each independently arriving job:
- Stage 1 pre-assigns tasks cloud-first, then edges and devices; within each location, it uses LASTF to select a core and EDF to arrange execution.
- Stage 2 reassigns tasks from edges to devices to free resource capacity, then re-packs previously scheduled VM tasks.
- Stage 3 reassigns tasks from cloud to device or edge for resource-cost reduction.
- The paper's Algorithm 2 tests an **entire selected core's deadline feasibility**, with deadline-ordered jobs and accumulated slack. Its supplemental material reports a C implementation.
- Its objective includes count of deadline-satisfied tasks and resource utilization/cost rather than only mission-task late-window DVR.

This means a faithful implementation can require a known task set, mutable placements and a per-core reordering queue. Current E45 receives each task on arrival and maps each Cloudlet to a VM once; tasks are not recalled/reordered across VMs, and future tasks are not visible.

## Constructive information-boundary example
At time 0, one task arrives, with two nodes A (fast, valuable) and B (slow but adequate). The online mapper must assign it now. Two worlds share identical information at time 0, but at time 1:
- World X: a mission task arrives that can meet its deadline *only* if A remains free.
- World Y: no additional task arrives; using A for the first task is preferable for makespan.
An offline schedule with knowledge of future arrivals can choose different initial allocations for X versus Y. A deterministic online mapper seeing identical information at time 0 must choose the same initial node in both worlds. Thus an offline multi-stage optimum cannot in general be reproduced by a per-arrival mapper without future knowledge or later rescheduling. This is an information constraint, not a criticism of TSSLA.

## Safe comparison designs

**Option A — exact TSSLA as offline/oracle study:** reproduce original C code and assumptions, adapt to a separately specified task-set scheduling harness; label offline/oracle and report scheduling horizon, task visibility, preemption/reassignment rights and objective differences. Do not present as a same-information online control of CASPER. Stronger evidence would compare all algorithms under *the same modified system*.

**Option B — online reinterpretation of LASTF/EDF:** define an arrival-visible task queue, explicit dispatch epoch, deadline ordering, migration policy and CPU/network timing; implement the same scheduling opportunity for CASPER and all competitors. Label the new policy "online adaptation of Sang et al." rather than source-faithful TSSLA; test scheduler overhead and sensitivity to batch window. This is a substantial new experimental branch, not a one-line baseline.

**Option C — current E45 setting:** retain existing PRED_GREEDY, CASPER_FULL, CLOUD_ONLY, EDGE_FIRST as fair common-model controls. Select a published **irrevocable online resource-placement** policy matching arrival-only information for a truly independent baseline. Neither HEFT nor raw Max Slack nor a renamed MCT adds an independent comparator.

## Decision
**Do not insert original TSSLA as an online VM-mapper baseline into E45.** Preserve it on the offline/reference shortlist. Prioritize identifying and verifying a published irrevocable-arrival online placement method, then obtaining actual 5-scenario CloudSim pilot artifacts before multi-seed performance claims.

No new CloudSim performance result is claimed; frozen E4.6 untouched.
