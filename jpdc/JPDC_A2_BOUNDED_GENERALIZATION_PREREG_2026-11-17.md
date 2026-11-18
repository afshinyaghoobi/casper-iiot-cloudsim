# Program A2 — PRE-REGISTERED bounded cloud-edge simulator-semantics generalization

**Status as of 2026-11-17: EXPERIMENT PROTOCOL FROZEN; NO NEW A2 JAVA RUN OR RESULTS.** This protocol specifies all primary independent scenario combinations before their outputs. This is not a new scheduling policy test, not an IIoT field trace and not a cure for original Java/Python non-parity.

## Scientific question / contribution boundary
Do native CloudSimPlus 8.5.7 one- and two-PE SpaceShared scheduling outcomes differ from an explicitly specified event-independent FIFO list-scheduling abstraction when same service/arrival input and native callback cadence differ? Does the descriptive discrepancy depend on workload burstiness, min-event granularity and PE capacity? Characterize *measured differences*, not necessarily a bug or a guarantee. This bounded 12-job study broadens but does not replace earlier fixed 3-Cloudlet case.

## Frozen factors and sample structure
- Native binary: **org.cloudsimplus:cloudsimplus:8.5.7**, Java 17, same nominal VM MIPS / utilization = 100%, synthetic CPU-only jobs with one requested PE per job. Host enough PE capacity for VM. Use CloudSimPlus SpaceShared scheduler; no original FGCS policy changes.
- **Workload family (2):** STAGGERED and BURSTY, 12 jobs in each run. STAGGERED nominal arrivals job index i at **3*i milliseconds** after 1.000 s base time; BURSTY nominal arrivals 4 groups of three jobs, group g at **12*g milliseconds** after base (same-time arrivals must preserve predetermined index submission order or be treated explicitly with stable ID ordering; document actual order).
- **Service lengths (ms)** for index i: **[8,13,5,19,7,11,17,6,14,9,16,10]**, held fixed across families and cases. With randomization offset below no service or class changes.
- **Replicate perturbations (3 fixed synthetic sources):** seed labels s0,s1,s2 add deterministic timing jitter to arrivals: s0=[0]*12, s1=[0,0.4,0.8,0,0.4,0.8,0,0.4,0.8,0,0.4,0.8] ms, s2=[0.8,0.4,0,0.8,0.4,0,0.8,0.4,0,0.8,0.4,0] ms. Synthetic fixed scenarios, NOT independent population-level random sources and NOT previously unseen real-world IIoT records; no significance test implying random-population inference.
- **Simulator minimum event time (2):** 0.000001 s (1us) and 0.005 s (5ms).
- **VM PEs (2):** 1PE and 2PE; each task requests 1PE. For 2PE, reference is a two-server FIFO capacity queue, NOT 1-server FCFS.
- Full factorial **2 families × 3 deterministic variants × 2 gaps × 2 capacities = 24 cases × 12 = 288 real Cloudlets** expected to complete. Do not drop poor/missing cases. Predeclare no extra factor tuning from results.

## Explicit reference scheduler and synchronization
Use the **actual native observed broker/scheduler submission timestamps**, not assumed nominal requested delays. Sort by actual submitted timestamp, break exact ties by actual observed submission order then stable job ID. For m in {1,2} identical FIFO servers, let next_free initially equal each actual first-submit timestamp, allocate the next job in actual order to the earliest-available server (tie by server index). Reference wait = max(0,server_available - actual_submit). Advance selected server by exact requested service (ms), without CloudSim event cadence, VM-level time quantum or additional datacenter overhead. Reference is a **declared abstraction**; neither runtime is intrinsically ground truth.
Timing origin is CloudSim simulator clock, use native observed submit and finish timestamps; record actual execution-list WAIT/EXEC transition, native wait and service, deadline classification. For computational outcomes, report native-reported wait and observed completed simulation finish, with no physical CPU claim.
Do not label native-vs-reference mismatches a CloudSim defect without documented contract violation; 2PE observational concurrency may differ from simplistic FIFO server model.

## Predeclared primary/secondary outcomes
- **Primary:** across all jobs within each 24-case cell, maximum absolute native reported start-wait time minus reference FIFO start-wait (ms). Also report absolute and signed mean error per cell; denominators 12 jobs.
- **Secondary:** number of job IDs whose observed native finish exceed deterministic relative deadline **arrival +25ms** and **arrival +50ms**, versus reference completion from actual submit+reference wait+requested service, and disagreement counts per cell. These are deliberately arbitrary sensitivity thresholds, not measured IIoT deadlines.
- **Secondary:** per-job native execution-list admission ordering, any same-snapshot older WAIT/newer EXEC membership, rate of unfinished Cloudlets (should be zero; nonzero = explicit failure), chronological submit/update callbacks.
- **Aggregation:** case-level descriptive medians/ranges across the three fixed variants; no inferential p-values or confidence intervals claiming random source representativeness. Display all 24 cases, not only extreme gaps.

## Conditions, controls and stopping / invalidity
- Freeze this protocol and its Git commit BEFORE new Java A2 experiment.
- New isolated Java harness, unmodified CloudSimPlus dependency and original E42/E4.6/Stage64/65 code. Record exact Java source commit, archive SHA, source artifact hashes.
- Java completion conservation **12/12 each case** and total **288/288** required for complete dataset; otherwise label FAIL, preserve partial logs.
- Deterministic exact rerun native log; if repeat differs, report as nonrepeatable rather than silently retrying/tuning.
- Alternate independent parser implements FIFO recurrence without importing primary calculation; discrepancies yield FAIL with both reports attached.
- If native actual arrival ordering differs from nominal in bursty case, use actual observed order as stated, explicitly report tie/cadence. Different observed arrivals are part of native semantics, not grounds to discard cases.
- Retain original Java-Python 30k gap 9.12140093294972ms >5ms FAIL and Stage65 policy safety FAIL; this A2 task does not try to pass the old gate, and **no algorithm effectiveness is measured**.
- If no meaningful patterns beyond isolated 3-job microcase occur, report it, reconsider Program A journal/scope, never manufacture a positive JPDC conclusion.

## Required artifacts before calling A2 COMPLETE
1. Prospective frozen protocol (this file, commit).
2. New isolated genuine Java simulation outputs for all 24 cells with exact code hash and execution run.
3. Primary and independent audits of waits, reference recurrence, deadline outcomes and all losses.
4. Readable manuscript figures/tables (24-case matrix + representative raw event diagram) and result limitations.
5. Verified A2 evidence report, updated [two-paper index](TWO_PAPER_RESEARCH_PROGRAM_INDEX_2026-11-17.md), [restart handoff](CHAT_RESTART_HANDOFF.md), and [long handoff](CURRENT_RESEARCH_HANDOFF.md).

**Publication gate:** method contribution must be demonstrably distinct from already submitted FGCS CASPER manuscript; this protocol is insufficient alone to guarantee JPDC suitability.
