# Gate 2 start — honest online EFT reference (2026-10-28)

## Scientific motivation
The 30-seed queue-weighted holdout (40281748580; statistics 40281798985) confirms selected S2/S4 advantages **only versus the homemade queue-weighted heuristic**, within the same synthetic generator. It does not test strong independent literature baselines or external generalization.

Literature relevant to selecting *appropriate* comparators:
- Topcuoglu, Hariri, Wu (2002), HEFT / CPOP, IEEE TPDS 13(3):260–274, DOI 10.1109/71.993206. **Offline DAG ranking and insertion**: not equivalent to online independent-task dispatch, so do NOT label a stripped-down policy as faithful HEFT.
- Keqin Li (2024), 'Scheduling independent tasks on multiple cloud-assisted edge servers with energy constraint', JPDC 184:104781, DOI 10.1016/j.jpdc.2023.104781. Its objective and energy-constrained formulation differ from CASPER; direct faithful replication would require checking full algorithm and compatible experiment semantics.
- Evaluation of Task Scheduling Algorithms in Heterogeneous Computing Environments (2021), Sensors 21(17):5906, DOI 10.3390/s21175906. Discusses Min-Min and Max-Min for heterogeneous cloud-edge contexts, with different information/decision protocols.

## Concrete implementation
- `jpdc/online_eft_reference.py`: deterministic online earliest-finish-time candidate selection among heterogeneous nodes, with only currently available free times, predicted service times and transfer estimates; stable low-node-index tie handling; no hidden disturbance oracle or lookahead.
- `jpdc/test_online_eft_reference.py`: seven specified correctness/edge-case assertions, including tie handling, backlogs, communication delay, arrival ordering and invalid speeds.
- `.github/workflows/jpdc-online-eft-reference.yml`: CI runner for the tests.
- **Status:** Source files and tests committed. New CI success is NOT verified. This Python reference has NOT been integrated into the CloudSim Java simulator and has NO measured benchmark performance versus CASPER. It must not be called HEFT, SOTA or an established JPDC-quality comparator.

## Next technical gate before a fair benchmark
1. Verify tests run successfully.
2. Audit Java candidate-selection inputs and non-oracular state available at decision time, including whether tasks are independent or carry DAG precedence.
3. Port the precise EFT selection semantics into a new isolated generated E45 policy, without editing E4.6.
4. Match seeds, workload, metrics, timing and candidate sets, and explicitly measure computational overhead. Predefine study hypotheses before evaluation.
5. Separately attempt a **literature-faithful** baseline whose assumptions match CASPER's workload model, or label incompatibilities clearly.

This stage moves baseline readiness forward but provides **no new empirical superiority evidence**.
