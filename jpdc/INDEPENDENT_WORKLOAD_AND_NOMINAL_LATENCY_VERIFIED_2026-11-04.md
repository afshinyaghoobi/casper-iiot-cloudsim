# JPDC — independent Java-RNG workload and nominal latency model confirmed (2026-11-04)

## New source-independent components and frozen assumptions

The original E42 `makeNodes` and `makeTasks` model logic was recreated in standard-library Python, without importing Java, Java-generated candidate records or hidden generator state. The Python implementation includes the 48-bit `java.util.Random` LCG, two-interval nextDouble, cached Box-Muller nextGaussian, original median lognormal transform, scenario-conditional Poisson interarrival workload, heterogeneous tiered node properties, and nominal network/service latency formula. E42 frozen Git blob `34256ca7bff46f911cf20e8b94278fbd09175746`; E4.6 untouched.

- Predeclared **full source-independent workload/node parity**: `jpdc/INDEPENDENT_WORKLOAD_GENERATOR_PARITY_PREREG_2026-11-04.md`, commit `38cdd037cba54398b98f169ae31ff5f2812ebaad`.
- Python generation `jpdc/independent_workload_generator.py`, commit `19cbc37fa307dc0284cce3b903e7433f5baf8175`.
- Read-only Java original-method reflection harness `jpdc/java_tests/OriginalWorkloadReferenceHarness.java`, initially commit `5ce72f447e9b5f92035fc54006203175a4a13fd8`, later expanded for latency audit.
- Strict independent task/node audit `jpdc/audit_independent_workload_generation.py`, initially commit `3ad4910cf49ea69e46c078d29f2c28ab18b4e4a3`.

## Real original-code reference run #1 — source-independent workload PASS
Original workflow initially failed in run `41889216641` because the read-only reflection harness's direct Java classpath did not include CloudSim Plus dependencies. Fixed workflow to obtain the original Maven runtime classpath, commit `7442bdfc1da41150dbcae2a6dc594abfc548985f`. **Run 41889381945 SUCCESS**, original artifact **13353260680**. All exact 21 frozen scientific nodes passed, and **every one of 30,000 original task records × 5 named scenarios = 150,000** matched independently generated Python records: task index/class, deadline, workload units, input/output MB and actual generated arrival timestamps, under a strict 1e-8 absolute tolerance. Tests rejected deliberately corrupted original records; `JPDC_WORKLOAD_CORRUPTION_REJECTED_PASS`.

## Real original-code reference run #2 — prediction also PASS
Before execution registered nominal predictor parity `jpdc/INDEPENDENT_NOMINAL_PREDICTION_PARITY_PREREG_2026-11-04.md` commit `5b8a07b3c65d756210ec56a1fb46d1baec8fc353`: five original scenario streams, first 100 tasks of each, 21 nodes, **10500** Java-original `nominalNetworkMs`, `nominalServiceMs` and sum (zero VQ backlog) against Python values independently derived from its own generated task and node objects. The Java source is invoked reflectively with the original frozen code and is not changed. Compilation of the first expanded harness failed because a local temporary `n` variable collided with workload size `n` (run `41889710326`); fixed the harness in commit `c442a5816a14f1b7c4718a5955554bc2366adf4a` (variable renamed to `netMs`). No scientific parameter/acceptance modification.

Expanded original reflection harness commit `6ce9bc8d5d242efc8346c7efee476fc43f56df32`, strict independent predictor comparator `jpdc/audit_independent_workload_generation.py` updated `2982d5e9801caa501e064e5ee9b34e92e00e869a`, CI rerun `.github/workflows/jpdc-independent-workload-generator-parity.yml` commit **`764734b4d5e86087359a2af7f24c945af7615b88`**.

**Real Actions run 41889848805 SUCCESS**, job **126784019794**, artifact **13352852991** (~8 MB), printed `PASS 10500 original task-node nominal network+service+latency predictions matched independently`, `JPDC_ORIGINAL_WORKLOAD_INDEPENDENT_GENERATION_PARITY_PASS`, `JPDC_WORKLOAD_CORRUPTION_REJECTED_PASS`. Also rechecked all 150,000 original task records and the 21-node reference. Both the original Java reference and independently generated Python workloads use seed index40 / scientific seed4202202640.

## Scientific interpretation

**Newly verified independent source generation:** workload/node RNG seeds and per-task attributes for all original S0–S4 scenarios, with no original Java task-node records used as Python generator input. Independent nominal latency model matches 10500 Java original network/service/total predictions under **zero virtual-queue backlog**.

**Not yet demonstrated:** genuinely independent physical queue processing or backlogs, prediction on real nonzero backlog driven by independent task routes, calibration quantiles/feedback score generation, all-policy integration, a second simulator (e.g., YAFS), or statistically significant superiority. The independent prior strict chronological-FCFS physical queue replay `41773297282` remained FAILED at preregistered max error 9.1214ms >5ms (later CloudSim VM scheduler queue bypass observed). Confirmatory S2/S3 10-seed holdout p=.0625 and exploratory factorial p=.125 were both nonsignificant, unchanged. Previously observed original rank2 activation: 14 actual selected policy-task records in four original S3 HIGH seeds41–44; 14/14 selected task deadlines satisfied in post-selection descriptive follow-up, without rank1 counterfactual; rank3 unobserved.

## Next defensible integration step

Use independently generated Python workloads and nodes with independently implemented E17 memory, health detector, VirtualQueue, ranked decision semantics and a separate Python discrete-event/physical queue engine on a **prespecified previously untested** seed/scenario matrix. Define distinct timing semantics and acknowledge CloudSim SpaceShared bypass; do not quietly tune to match or relabel old strict-FCFS failure. Any second-simulator policy performance results should be reported at SEED level with uncertainty, baselines, and exact reproducibility. Adding calibration-score and physical-service/noise models as independent components precedes full external YAFS claim.

## Verified links
- Full workload generation CI PASS: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41889381945
- Expanded independent nominal latency CI PASS: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41889848805
- Native original output archive: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41889848805/artifacts/13352852991
