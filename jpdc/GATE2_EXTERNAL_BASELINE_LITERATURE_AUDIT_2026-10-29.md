# JPDC Gate 2 — Literature-grounded baseline selection audit (2026-10-29)

This note records externally verified sources and distinguishes original algorithm scope from adaptations. It is **not** a claim that these baselines have been implemented or run.

## Scientific comparator candidates

1. **Li (2024), JPDC 184, 104781**, "Scheduling independent tasks on multiple cloud-assisted edge servers with energy constraint", DOI: 10.1016/j.jpdc.2023.104781. Explicitly models independent tasks, heterogeneous edge/cloud compute and communication, with makespan (and separately an energy constraint). Strong *problem-family* match, but its static/list-scheduling setting and objective cannot be equated to online per-task deadline miss rates. Before implementation, extract full algorithm/pseudocode and map observable variables; do not claim literal replication until checked. Source: https://www.sciencedirect.com/science/article/pii/S074373152300151X

2. **Braun et al. (2001/technical report 2000)**, "A Comparison Study of Eleven Static Heuristics for Mapping a Class of Independent Tasks onto Heterogeneous Distributed Computing Systems." Original experiment is offline/static, independent meta-tasks, total execution time. Defines MET, MCT, Min-min, Max-min and others. Under our online arrivals, an *arrival-only MCT adaptation* is reasonable, but must be labeled an adaptation rather than the original offline approach. Source: https://docs.lib.purdue.edu/ecetr/19/

3. **Hussain et al. (2019)**, "Investigation of Cloud Scheduling Algorithms for Resource Utilization Using CloudSim," DOI: 10.31577/cai_2019_3_525. Compares ten heuristics in CloudSim using independent static jobs and makespan/throughput/utilization. Useful for implementation cross-check, **not** evidence that static Min-Min directly solves our online deadlines. Source: https://www.cai.sk/ojs/index.php/cai/article/view/2019_3_525

4. **Canon, Kong Win Chang, Robert, Vivien (2019 online / 2020 issue)**, "Scheduling independent stochastic tasks under deadline and budget constraints", DOI: 10.1177/1094342019852135. Has independent stochastic tasks and deadlines, but objective is expected number completed under budget and task execution IID; admission/interrupt decisions differ from per-arrival heterogeneous VM placement. A conceptual anchor, not a directly interchangeable policy. Source: https://journals.sagepub.com/doi/10.1177/1094342019852135

## Methodologically unsuitable as an unmodified independent-task online baseline

**Topcuoglu et al. (2002), IEEE TPDS 13(3), 260–274**, "Performance-effective and low-complexity task scheduling for heterogeneous computing," DOI: 10.1109/71.993206. HEFT/CPOP use task-graph precedence, upward/downward rank and insertion-based scheduling. The model is DAG, not a one-at-a-time independent-task dispatcher. A derived one-step earliest-finish-time mapper is an *adaptation* and must be labeled so; it is not literal HEFT. Source: https://ieeexplore.ieee.org/document/993206/

## Immediate comparator choice and protocol (no results yet)

**Priority A: Online Minimum Completion Time (MCT) adaptation.** At each arrival choose among eligible nodes the minimum estimated completion time using only information visible to the dispatcher at that instant: network transfer plus estimated queue delay plus service. State and freeze the queue estimator; evaluate both the arrival-only queue estimate and, separately if possible, an oracle-queue ceiling without implying oracle feasibility. Compare source-level decision rule against existing PRED_GREEDY first: if the formula and tie-break coincide, do *not* add an alias as an independent baseline.

**Priority B: deadline-slack / earliest-deadline-aware admission-and-placement control**, but only after finding an independently documented matching online formulation. A custom heuristic is an exploratory control, not external SOTA.

**Priority C: Li (2024) paper-faithful comparator**, contingent on a full-text algorithm review and explicit treatment of its original optimization horizon and objective. If it requires full workload foresight, report an offline/oracle reference *separately*; never compare it as if online information constraints were equal.

## Strict fairness

- Same task set, random seeds, resource heterogeneity, arrival order, shock visibility, network/cpu accounting and telemetry schedule.
- All methods must use the same information available at dispatch; oracle and offline methods labeled and grouped separately.
- Primary actual evaluation: mission late_dvr with scenario-wise paired-seed contrasts; also tail latency and mapper overhead. Include undesirable effects and computational costs.
- Avoid using one seed to tune a baseline; freeze policies before 30 paired seeds and independent holdout.
- E4.6 remains frozen. Nothing here asserts new CloudSim runs.
