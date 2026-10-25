# JPDC baseline fidelity and next experiments

## Source
Topcuoglu, Hariri, Wu (2002), Performance-Effective and Low-Complexity Task Scheduling for Heterogeneous Computing, IEEE TPDS 13(3), 260-274. DOI 10.1109/71.993206; https://ieeexplore.ieee.org/document/993206/

Original HEFT schedules DAG tasks using upward-rank priority, earliest-finish processor assignment, and insertion scheduling. It is not equivalent to online one-task-at-a-time minimum predicted completion time.

## Baseline integrity requirements
1. Preserve immutable E4.6 frozen release.
2. Clearly label PRED_GREEDY and the independently devised deadline-capacity-preserving heuristic as synthetic experimental comparators; do not claim either is a reproduced published algorithm.
3. Claim HEFT only with explicit DAG precedence, upward-rank prioritization, earliest-finish resource selection, and insertion; otherwise use the name online EFT-inspired policy and say that it is not original HEFT.
4. Run all methods with the same workload instances, observed information, and resource model; verify decisions on small deterministic examples before scaling.
5. Predefine 30 paired seeds and Holm comparison families; publish DVR, empirical FWC, tail latency, and scheduling overhead.
6. Report failure to reach nominal 99 percent FWC in hidden network shock S3, without claiming coverage guarantees.
7. Topology scaling and 21/N resource normalization are simulator-specific sensitivity tests, not proof of independent topology or real-world generalization.
8. Future high-value studies: honest DAG HEFT benchmark with new DAG generator, and out-of-generator or real trace validation. These need separately documented workloads and protocols.

## Evidence
E4.6 immutable release v1.0.0-casper-iiot-e46.
Branch jpdc-seed0-repro-20261024.
Compute-and-bandwidth scaled topology: run 40220265552 (60 of 60 successful jobs).
Thirty-seed paired aggregation: run 40220707805 (2400 new and 1200 frozen rows, 60 comparisons).

## Wording for paper
In controlled synthetic Cloud-Edge workloads, deadline violation is sensitive to infrastructure configuration while coverage in the hidden network-shock scenario remains below nominal 99 percent. Resource normalization does not separately identify a causal node-count effect.
