# Stage58 VERIFIED negative: classic least-inflight online DEV controls (2026-11-13)

## After-result **technical marker-only fix** — full original method reproducibility confirmed

Following original [run43478398443](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43478398443) CI FAILURE and unchanged-original-source audit-only [run43478912668](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43478912668) SUCCESS, corrected **ONLY** the stale `JPDC_STAGE51_...` source log-marker strings to `JPDC_STAGE58_...` in the DEV runner. Fix commit `bdd1b53ac258f963863438d9e1e83490d783d851`. Neither baseline code nor simulator physics, seed protocol, calibrated data or outcome JSON structure changed.

The corrected original-workflow [**run43479230750**](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43479230750) completed **SUCCESS for both seed1311 and seed1312**, causal selector contract, frozen E42 hash, Stage6 original GREEDY/FULL JSON parity, both full scientific-source repetitions and byte-identical JSON/log reruns. Corrected artifacts `jpdc-stage58-classic-load-seed-1311` ID **14063404983**, `...-1312` ID **14064715952** were downloaded and compared directly with archived original red-workflow source artifacts. **The full scientific source.json files are BYTE-FOR-BYTE IDENTICAL to the originals for both seeds**, not merely same aggregate counts. Seed1311 SHA256 `f887d293905a4277e0bae1eb923fabd88d1b273387272ea51e17abbab24e52d7`; seed1312 SHA256 `50a5ad504174a00bab27a6aea233b26f2aa3696d7a8532c477ee1a076ae23c48`. Therefore amended code produces no new independent science, and negative DEV conclusions below remain exactly unchanged.

**Preserve original run's FAILURE status in historical audit**. The subsequent audit-only and corrected technical replay successes do not retroactively change its recorded CI conclusion.

## Scientific status, provenance and limitations
**This is 2-source-seed DEV ONLY, n=2 independent seed streams**, not independent holdout or journal-level significance evidence. Original before-outcome preregistration `jpdc/STAGE58_CLASSIC_LEAST_INFLIGHT_DEV_PREREG_2026-11-13.md`, commit `d0ad7f07f18d0b33159daae75f3242ca73458ac8`; independent pure scorer `jpdc/classic_least_inflight_stage58.py`, isolated strict-FCFS source `jpdc/independent_physical_classic_load_stage58.py`, tests `jpdc/test_stage58_classic_baseline.py` and runner `jpdc/run_stage58_classic_dev.py`. Controls:
- `LEAST_INFLIGHT` argmin `(running+waiting,j)`.
- `CAPACITY_WEIGHTED_LEAST_INFLIGHT` argmin `((running+waiting+1)/nominal_cpu_capacity,j)`.
Both are *traditional least-connections-class adaptations*; neither reproduces Wu et al. (2026) DFAQ-LB (elastic queue capacity regulation, multidimensional VM health, migration) or any original author software. No task deadline, hidden shock mask, future service, or future arrivals used for routing. Standard PRED_GREEDY and frozen CASPER_FULL are source-matched exact controls.

**Original GitHub Actions [run43478398443](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43478398443) finished overall FAILURE**, because the workflow grepped `JPDC_STAGE58_DEV_SOURCE_COMPLETE_PASS` whereas the cloned DEV runner still printed stale `JPDC_STAGE51_DEV_SOURCE_COMPLETE_PASS` — a marker labeling/CI wiring error. It is **not** a scientific claim that overall original workflow succeeded. Both original scientific source experiments had already reached their end, wrote 8 policy/scenario rows each, passed original Stage6 PRED_GREEDY/CASPER_FULL exact JSON parity and causal unit test, and wrote `source.json`, `repeat.json`, `source.log`, `repeat.log` with byte-identical repeated files. Original git source commit **67818b1765c221c85a8d7e0cede107b74ccc8a1a**, unchanged for both sources; original archived artifact IDs seed1311 **14064152713**, seed1312 **14063234628**. Stale emitted `STAGE51` string labels are *cosmetic source labels*, do not make Stage51 a second run.

To preserve the original source outcomes without another physics rerun or changing any policy, audit-only recovery [**run43478912668**](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43478912668), code SHA `c7a0cf60dce86671c608f59ce6471d90e1fa6274`, **SUCCESS**. It fetched both original artifact ZIPs by exact run ID, asserted original source commit SHA, exact repeated JSON/log per source, and executed `jpdc/audit_stage58_dev_cohort.py` twice with exactly byte-identical audit.json. Original recovery artifact **14064905121** `jpdc-stage58-original-dev-cohort-audit-only`, downloaded and independently inspected. Audit JSON SHA256 **ce20020641c73637060822e9ffec5dfd0063dad919ddbad09fe5f7d8c25a09a3**. **Original experiment CI status remains failure; subsequent audit-only recovery status success.** No original positive/negative results modified.

## Complete predeclared DEV outcome
Two source seeds 1311/1312, each 80,000 stationary task calibration, 2 shocks S2/S3, 4 policies, 12,000 tasks per deployment = **192,000 dependent policy-task observations**. POST-shock MISSION task counts per source seed1311 **105**, seed1312 **90**; pooled **195** per scenario (not independent for inference). Integer deadline misses:

| Scenario | Method | Seed1311 misses /105 | Seed1312 misses /90 | Pooled misses /195 | Pooled delta vs CASPER_FULL (positive=harm) |
|---|---|---:|---:|---:|---:|
| S2 CPU40% | PRED_GREEDY | 3 | 4 | 7 | -1 |
| S2 CPU40% | CASPER_FULL | 3 | 5 | **8** | 0 |
| S2 CPU40% | LEAST_INFLIGHT | 33 | 24 | **57** | +49 |
| S2 CPU40% | CAPACITY_WEIGHTED_LEAST_INFLIGHT | 30 | 37 | **67** | +59 |
| S3 network50% | PRED_GREEDY | 3 | 4 | 7 | 0 |
| S3 network50% | CASPER_FULL | 3 | 4 | **7** | 0 |
| S3 network50% | LEAST_INFLIGHT | 26 | 28 | **54** | +47 |
| S3 network50% | CAPACITY_WEIGHTED_LEAST_INFLIGHT | 76 | 68 | **144** | +137 |

**Both distinct controls are dramatically worse in each DEV seed and fault regime**, despite keeping lower queue wait on some sources. For illustrative seed1311 S3, CASPER_FULL mean all-task wait 3.608ms and mean all-task latency53.797ms; LEAST_INFLIGHT mean wait 0ms but mean latency125.830ms, with POST MISSION misses26 vs3. The observation is consistent with ignoring CPU/network transfer and task deadline, but no task-by-task causal explanation has been verified. Weighted least-inflight may favor high-capacity remote nodes despite large network delays. This is an interpretation hypothesis, not proof without matched traces. All methods route to all 21 nodes, no hidden affected-node information. Dispatch switches vs contemporaneous PRED_GREEDY in original baseline source are huge (~11.3k–11.9k of 12k), satisfying **non-alias** criterion.

## Research decision
- Stage58 engineering source and audit **verified**, but classic simple least-inflight comparators are **negative controls**, not candidates to replace CASPER, no sign test / CI computed from n2 DEV.
- Preserve their honest poor performance to show the need for end-to-end workload-aware placement rather than claiming all 'load balancing' is equivalent.
- This does not constitute faithful reproduction of **DFAQ-LB**; that paper includes dynamic queue/health/migration mechanics, not these classic controls.
- Maintain earlier independent Stage52 S2 no-harm FAIL for queue-pressure methods and posthoc Stage54 Holm caution. Stage56 original 20ms completion FAIL and Stage56B 99/108 completion remain separately real. Original 30k Java SpaceShared vs Python strict-FCFS wait max deviation9.12140093294972ms>5ms still FAIL. E42/E4.6 unchanged.
- **NEXT**: a literature-faithful distinct published algorithm must have accessible actual pseudocode and implementable comparable causal state; do not add another simplistic pseudo-DFAQ-LB baseline. A next structurally different CASPER policy also needs mathematical motivation, new DEV seeds and prospective disjoint holdout after frozen code, ideally genuine external/independent runtime validation.

Author/context source: Wu et al., *Future Generation Computer Systems* 182 (2026) 108460, DOI 10.1016/j.future.2026.108460, https://www.sciencedirect.com/science/article/pii/S0167739X26000944 . Original paper performance numbers cannot be transferred to this task model.
