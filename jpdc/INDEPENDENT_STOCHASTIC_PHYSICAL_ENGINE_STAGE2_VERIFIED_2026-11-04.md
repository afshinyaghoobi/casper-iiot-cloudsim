# JPDC Stage 2 independent stochastic physical engine — real CI verified (2026-11-04)

## Scope and provenance

The first independently executable Python physical event engine (Stage 1 run 41895984369 PASS; native strictly FIFO queues, 21 concurrent node servers, seed-derived tasks, virtual-queue telemetry computed from its own physical queue state) has now been expanded with **independently generated original-model stochastic compute service durations, deterministic hashed service noise, hidden compute/network impairments and affected-node masks**. This is a clean-room baseline **physical** engine with its own service starts, waits and completion times, not merely Python replay of original Java's recorded events.

Before any new test runs, `jpdc/INDEPENDENT_STOCHASTIC_PHYSICS_STAGE2_PREREG_2026-11-04.md` fixed the scientific scenarios, two seed indices [50,51], original 21 nodes, three baseline-only policies, original run size 12000, fixed source Java task-node physics reference selection and strict gates. The initial mistaken pair count "10080" was transparently corrected **before executing any tests** to **5040**, because 5 scenarios x 2 seeds x 24 source task indices x 21 nodes = 5040. The original enumerated task indices and acceptance thresholds did NOT change. Protocol commits `9837e8e88977afd6c29870eb7e0a148d641d1620`, arithmetic correction `da0ecb484ff1b6808175a4e744b58f2b0c91ed83`.

Source physics module `jpdc/independent_stochastic_physics.py`, commit `6c97e595eadb6b574457475cf6a4676b834cdf7f`, recreates frozen E42 `mix64` with unsigned-overflow 64-bit arithmetic, deterministic service noise (including rare heavy tail and clipped lower bound), original 6-node scenario mask Fisher-Yates Java LCG shuffle, and post-change-task (index >= 10000) compute service ×1/0.6 / network ×1/0.5 impairments, as applicable. It does not import original Java outcomes, raw traces or precomputed random values.

### Gate 2a — exact original source physical formula cross-language verification

Read-only Java reference calls ORIGINAL E42 methods `makeTasks`, `makeNodes`, `affectedMask`, `nominalServiceMs`, `actualServiceMs`, `nominalNetworkMs` without modifying original frozen file. Harness `jpdc/java_tests/OriginalStochasticPhysicsReferenceHarness.java` final commit `0545b479bc9a7452a860af83ac1134d0e7369e2e`. Strict Python independent comparator `jpdc/audit_independent_stochastic_physics.py` commit `9e99043e717aeea76eb273db549a56c0bb39a3a6`. All 10 original affected-mask configurations checked and all **5040** original task-node CPU and network physical quantities compared against independently generated Python workload and nodes; absolute tolerance 1e-8 ms, full counts and missing/duplicate/reordered inputs rejected.

**Real GitHub Actions 41899131122 SUCCESS**, job 126816539651, frozen source check and raw reference artifact **13357317327**. Printed `JPDC_INDEPENDENT_STOCHASTIC_PHYSICS_PARITY_PASS` and `JPDC_STOCHASTIC_PHYSICS_CORRUPTION_REJECTED_PASS`. Zero discrepancy beyond original preregistered numerical tolerance.

### Gate 2b — standalone stochastic physical event simulation

Original Stage1 engine `jpdc/independent_physical_event_engine.py` extended with optional `stochastic_seed` and `scenario` inputs, commit `f2941b50538d79dd1a2e54b9179f56d0b6a03a45`. Its ORIGINAL nominal physical mode remains default: original Stage1 regression explicitly retested in Stage2 CI. In stochastic mode, independent *physical CPU* completion uses original hashed service noise and compute shock, independent *actual network* includes node-specific bandwidth slowdown, while virtual queue prediction updates with **nominal** service and resets from the Python physical queue's own next-free estimates. Queue admission remains explicitly strictly FIFO, **different from observed CloudSimPlus SpaceShared behavior**.

Stage2 fixed driver `jpdc/run_independent_stochastic_engine_stage2.py` commit `59eaf8c812487d524bfe7f4446babadea2df0345`, physical and shock branch tests `jpdc/test_independent_stochastic_engine_stage2.py` commit `b3e444688fbb85bb9e89696267f44f59d8770c46`, workflow `.github/workflows/jpdc-independent-stochastic-engine-stage2.yml` commit `5c2a209ef087c8623b687ea4c17b53cf69bc72fe`.

**Real GitHub Actions 41899450893 SUCCESS**, job 126817645355, artifact **13357632521**. All frozen test gates PASS:
- Stage1 regression baseline candidate sets, FIFO queue promotion, same-time event order, concurrent physical node service, malformed workload rejection;
- Stochastic CPU service changes actual physical completion; full postshock original scenario branch coverage with >10000 tasks per scenario; missing physical scenario input fails closed;
- **18 original independent physics simulations × 12000 tasks = 216000 policy-task outcomes**, covering all 3 original shock scenarios S2/S3/S4, both original seed indices 50/51 and all three baseline-only policies;
- **all 18 full results byte-identically reproduced on a second complete execution**;
- Original source code frozen SHA E42 `34256ca7bff46f911cf20e8b94278fbd09175746`, E4.6 unchanged.

### Actual descriptive Stage2 output — independent strict-FCFS physical baseline model ONLY

| Seed | Scenario | Policy | Mean latency ms | Mean wait ms | MISSION deadline misses | Postshock dispatches to affected nodes |
|---|---|---|---:|---:|---:|---:|
| 50 | S2 | CLOUD_ONLY | 72.991804 | 2.142699 | 190 | **0** |
| 50 | S2 | EDGE_FIRST | 280.757577 | 156.224920 | 397 | 627 |
| 50 | S2 | PRED_GREEDY | 59.174360 | 4.725334 | 19 | 228 |
| 50 | S3 | CLOUD_ONLY | 81.227109 | 2.142699 | 248 | 1592 |
| 50 | S3 | EDGE_FIRST | 158.860801 | 36.997664 | 354 | 367 |
| 50 | S3 | PRED_GREEDY | 63.421459 | 4.670439 | 25 | 1571 |
| 50 | S4 | CLOUD_ONLY | 73.665500 | 2.447132 | 194 | **0** |
| 50 | S4 | EDGE_FIRST | 903.515892 | 777.906607 | 397 | 610 |
| 50 | S4 | PRED_GREEDY | 60.690596 | 4.867935 | 20 | 199 |
| 51 | S2 | CLOUD_ONLY | 69.935621 | 7.198637 | 128 | 1336 |
| 51 | S2 | EDGE_FIRST | 427.105733 | 291.778765 | 529 | 330 |
| 51 | S2 | PRED_GREEDY | 54.490360 | 1.628205 | 3 | 723 |
| 51 | S3 | CLOUD_ONLY | 69.202413 | 5.925913 | 104 | 274 |
| 51 | S3 | EDGE_FIRST | 275.061331 | 140.299276 | 514 | 494 |
| 51 | S3 | PRED_GREEDY | 54.655517 | 1.450407 | 3 | 390 |
| 51 | S4 | CLOUD_ONLY | 74.730743 | 8.051356 | 177 | 705 |
| 51 | S4 | EDGE_FIRST | 1064.191041 | 928.714384 | 529 | 203 |
| 51 | S4 | PRED_GREEDY | 60.194700 | 2.737958 | 25 | 1097 |

**Important:** For seed50 CLOUD_ONLY S2 and S4, NO task was dispatched to any damaged node after the change point (zero exposure); these runs cannot show direct affected-node physical degradation for that policy. The full matrix has nonzero shock exposure and a valid independent physical engine, but does not imply every policy/scenario run experienced affected-node service.

## What remains to establish before JPDC efficacy

**Not yet integrated:** independent physical calibration phase, native nonconformity score/quantile generation from simulator outcomes, rank-aware policy/health/probes/E17 feedback inside the simulator, an independent CASPER_FULL comparative experiment, statistically valid prespecified unseen-seed holdout, or YAFS. These are *baseline-only* independent simulator tests. Task records inside any given policy run are dependent; only **two** distinct seeds here; no performance superiority p-values or causal policy comparison may be inferred.

Original CloudSim queue semantics contain directly verified SpaceShared FIFO-bypass cases; the initial separately preregistered independent Python strict chronological-FCFS queue fidelity test `41773297282` remains **FAILED**, max wait 9.1214ms > fixed 5ms threshold. This new independent queue model is deliberately distinct and cannot retrospectively repair that failure. Original confirmatory disjoint 10-seed S2/S3 holdout p=.0625 and earlier exploratory factorial p=.125 remain nonsignificant.

## Evidence links
- Physics source-formula parity: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41899131122
- Stage2 independent engine success: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41899450893
- Stage2 artifact https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41899450893/artifacts/13357632521
