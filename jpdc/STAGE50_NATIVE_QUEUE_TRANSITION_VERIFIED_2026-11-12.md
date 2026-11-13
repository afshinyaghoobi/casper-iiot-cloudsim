# Stage50 verified native queue transition trace — real CloudSimPlus 8.5.7 (2026-11-12 US Central / GitHub UTC 2026-11-13)

## Verified original experiment
- Pre-outcome preregistration: `jpdc/STAGE50_QUEUE_TRANSITION_TRACE_PREREG_2026-11-12.md`, commit `c0215e0088950c5faf6faba176077a23683b193c`.
- [Actual GitHub Actions run 43362375409](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43362375409): **completed / success**, event push, source SHA `7c3ed0a4bb60294466f8792d78ac32f0aa9d1e03`, job `transitions` **success**. Java 17 Maven compile, frozen original E42 blob guard, synthetic positive/negative parser contract, three genuine CloudSimPlus 8.5.7 native event cases, source trace auditor, and byte-identical full Java/native+JSON repeat **all passed**.
- Independently retrieved the original job log and actual GitHub artifact **ID 14008945839**, named `jpdc-stage50-native-transitions-all-clocks`, uploaded successfully (SHA256 zip digest `73c0e249a42dfe8aeee3df6fb70c21f7b11be2ac52d69f85ff8b5d48309e0813`). Read artifact `native.log`, `native_repeat.log`, `audit.json`, `audit_repeat.json`, `source_commit.txt` and independently checked that both repeated data pairs are byte-for-byte identical and the source SHA matches the workflow run. GitHub log PASS markers: `JPDC_STAGE50_SYNTHETIC_PARSER_CONTRACT_PASS`, `JPDC_STAGE50_NATIVE_QUEUE_TRANSITION_AUDIT_PASS`, `JPDC_STAGE50_NATIVE_TRANSITIONS_BYTE_IDENTICAL_PASS`.
- This is real event-trace evidence, **NOT** proof that the separate 30k Python strict FCFS vs original Java SpaceShared wait parity has been repaired. Earlier registered max error **9.12140093294972 ms > 5 ms** remains a **FAIL**.

## Direct native observations
Three fixed tasks, CPU demand [8.099623,4.730689,9.120283] ms, submission arrival offsets [0,5.318920,8.0997406] ms. Single processing-element CloudSim SpaceShared VM. Native clocks are **milliseconds**. Ideal strict single-server FCFS reference starts from native scheduler's *observed submission clock*, using requested CPU service. Native wait is CloudSim's own `getStartWaitTime()`; observed EXEC-list insertion is **not** proven exact CPU physical start.

| CloudSim minimum event gap (s) | Native observed EXEC-list order | Native wait task0 (ms) | Native wait task1 (ms) | Native wait task2 (ms) | Ideal FCFS wait task1 / task2 (ms) |
|---|---|---:|---:|---:|---:|
| 0.000001 | 0→1→2 | 0 | 22.782703 | 40.0038824 | 2.780703 / 4.7305714 |
| 0.005 | **0→2→1 (non-FCFS)** | 0 | 26.9011036 | 0 | 2.780703 / 4.7305714 |
| 0.02 | **0→2→1 (non-FCFS)** | 0 | 62.780703 | 0 | 2.780703 / 4.7305714 |

Native first observed WAIT/EXEC timestamps:
- 1us: task1 WAIT at 1005.319920, EXEC at 1028.102623; task2 WAIT at 1008.1007406, EXEC at 1048.104623.
- 5ms: task1 WAIT at 1010.318920, EXEC at 1037.2200236; task2 enters EXEC immediately upon its scheduler submission at **1013.0997406**, preceding task1 despite earlier task1 WAIT.
- 20ms: task1 WAIT at 1025.318920, EXEC at 1088.099623; task2 enters EXEC on submission at **1028.0997406** before older waiting task1.

**Matched-clock diagnostic:** for all nine task-case rows, CloudSim reported native wait equals (first observed EXEC-list timestamp − native scheduler submission timestamp) within rounding (max absolute discrepancy about `1.3e-13 ms`). This establishes a concrete micro-fixture operational correspondence for these instrumented states but **does not establish general semantic equivalence across all tasks or exact CPU-start clock**.

The observed departures from ideal FCFS for task1 are:
- 1us: +20.002000 ms (native 22.782703 vs ideal 2.780703).
- 5ms: +24.1204006 ms (native 26.9011036 vs ideal 2.780703).
- 20ms: +60.0000000 ms (native 62.780703 vs ideal 2.780703).

For task2: +35.2733110 ms at 1us (native40.0038824 vs ideal4.7305714); **−4.7305714 ms** in both 5ms and 20ms cases (native zero despite ideal positive). This is consistent with a bypass of the already WAIT-listed task1 in these observed traces. These are native scheduler *list snapshots*; they are not proof that the CloudSimPlus library is incorrect. Scheduling policy and simulation event cadence both matter; a strict Python FCFS comparator may have a different queue discipline and physical event-time semantics.

## Scientific decision
Stage50 **technical/trace study COMPLETE and independently verified**. This micro-evidence supports a plausible queue-discipline and event-cadence mechanism for cross-engine wait discrepancies, but the original 30k-case registered parity failure remains unresolved. No new MISSION deadline effect, holdout evidence, IIoT real trace, or superiority claim. Frozen CASPER E42 and E4.6 and Stage48 negative incremental method result preserved. Do not change numeric tolerances to relabel parity as passing.

## Next priority
1. Prospectively define task-matched observables on the **original large native workload**, preserving IDs, per-node shared queue list states, incoming submission, wait-list bypass and callbacks; quantify proportion and conditions of bypass, and test whether it accounts for the original 30k per-task wait disagreement. An instrumented *diagnostic* clone is preferable to modifying E42/E4.6.
2. Independently develop and report a transparent modern **DFAQ-LB-inspired** baseline, explicitly not a faithful reproduction of authors' unprovided original code; compare paired source seeds and avoid reusing consumed holdout seeds as new independent claims.
3. Retain all cross-engine failures, adverse deadline cases, original seeds and protected source hashes.
