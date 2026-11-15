# Stage65 VERIFIED — frozen partial minimax independent source n8 HOLDOUT FAILS prereg safety (2026-11-14)

## Integrity and chronology: original source evidence
**Prospective before-any-new-outcome preregistration**: `jpdc/STAGE65_PARTIAL_MINIMAX_EIGHT_SOURCE_HOLDOUT_PREREG_2026-11-14.md` commit `ad52574cb8bc829a635a42e8d4cd95a8ab8a69bf`, frozen independently after Stage64 two-source DEV PASS and prior to evaluating fresh Stage65 sources. Frozen code **exactly original** `jpdc/independent_physical_partial_live_stage64.py` Git blob `24d495dba4d29f8fe070ad6539b20361a7193cc6`, Stage62 selector Git blob `338dd1de5c17028b3f60f1d635964b52e152df14`, Stage60 causal world builder `2bcb069b25964b2982e1f56de9725d2faa970762`. Original E42/E4.6 source untouched (E42 blob `34256ca7bff46f911cf20e8b94278fbd09175746`).

**True independent never-used source seeds** `1811–1818`, each source seed independently calibrated S0 80k, two scenarios S2 CPU40%-loss/S3 network50%-loss, three policies original PRED_GREEDY, original CASPER_FULL, frozen `PARTIAL_MINIMAX_FULL_FALLBACK`, each deployment 12k tasks. Total **48 deployments, 576k DEPENDENT task-policy observations**, inferential unit **8 original source seeds**, not 576k independent samples. Strict original Stage6 full JSON parity for controls (after removing passive observation fields), CPU and E2E original event conservation per policy, no hidden future/oracle for selection, source/repeated JSON/log byte-identical.

- Original corrected frozen-hash guard [GitHub Actions run **43661658894**](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43661658894) **SUCCESS, all eight jobs**, source SHA `fd138174ac662b14a88421524f87b7dfa886c6fc`. An earlier infrastructure workflow [run43661632905](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43661632905) also ran; its policy was the same but source hash guard was initially ineffective. We immediately repaired guard to enforce actual frozen file blob hashes before relying on results; original validated source is the corrected guard run43661658894, not mixed across runs. Every original source artifact preserved by exact run ID: seeds1811 artifact14139894867, 1812 14140735758, 1813 14140192454, 1814 14140875288, 1815 14140890300, 1816 14139958005, 1817 14139718408, 1818 14140526317.
- Independent original **artifact-ONLY** [audit run **43661753183**](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43661753183) **SUCCESS** source `314b8ee9fc044644cd140f43ae5ca0bb9b55a5a0`. No re-simulation, no seed deletion: downloaded original artifacts, asserted source SHA and identical repeats, ran `jpdc/audit_stage65_holdout_cohort.py` twice with bytes identical. Original audit artifact ID **14140890374**, downloaded and independently inspected, ZIP digest sha256 `17b325ec0396e24fb3531e5d46d8e02702bd7e8ba70b09b35240a5afb393b60a`, `cohort.json` SHA256 `b52c5e29a93c4d46ca61ce2fc34cb1eea48f4c9cf270a3f194de4fb8e703e8c7`. **Technical and reproducibility PASS** but frozen **scientific promotion gate FAIL**.

## Exact per-source paired POSTshock MISSION results (misses: FULL→NEW)
| Original source seed | S2 CPU FULL→NEW | Delta NEW−FULL | S3 NET FULL→NEW | Delta NEW−FULL |
|---|---:|---:|---:|---:|
| 1811 | 0→0 | 0 | 1→1 | 0 |
| 1812 | 3→1 | -2 | 2→2 | 0 |
| 1813 | 6→6 | 0 | 12→6 | -6 |
| 1814 | 5→0 | -5 | 2→0 | -2 |
| 1815 | **1→2** | **+1 (HARM)** | 4→1 | -3 |
| 1816 | **1→2** | **+1 (HARM)** | 1→1 | 0 |
| 1817 | 8→6 | -2 | 9→3 | -6 |
| 1818 | 0→0 | 0 | 0→0 | 0 |
| **Dependent task count aggregate** | **24→17** | **-7** | **31→14** | **-17** |

**Original-source statistical unit n8:** S2 paired miss-count deltas `[0,-2,0,-5,+1,+1,-2,0]`, three favorable, two adverse and three ties, **exact two-sided sign p=1.0**, mean paired delta -0.875 misses per original source. S3 `[0,0,-6,-2,-3,0,-6,0]`, four favorable, zero adverse, four ties, **two-sided sign p=0.125**, mean delta -2.125 per source. Neither meets `p<0.05`. Zero significance claims from pooled dependent task counts; no p-value tuning or alternate selected-seed inference.

## Strict frozen all-period MISSION safety results
Original prereg additionally required **whole-deployment MISSION** candidate misses <= FULL for **all 16 seed×shock cells**, because Stage64 DEV previously showed an unfavorable all-period shift. This too FAILS. Source FULL→NEW:
- S2 1811 **2→3 (+1)**, 1812 4→2 (-2), 1813 15→15 (0), 1814 7→3 (-4), 1815 10→10 (0), 1816 **5→7 (+2)**, 1817 14→12 (-2), 1818 **0→1 (+1)**. Pooled dependent missions **57→53**.
- S3 1811 **3→4 (+1)**, 1812 3→3 (0), 1813 21→15 (-6), 1814 4→3 (-1), 1815 13→9 (-4), 1816 **5→6 (+1)**, 1817 15→9 (-6), 1818 **0→1 (+1)**. Pooled dependent missions **64→50**.
- Safety rule fails POSTshock S2 on **1815, 1816** and whole-deployment on six distinct scenario-source cells (S2 1811,1816,1818; S3 1811,1816,1818). Even though ≥4 postshock strict wins overall (7) and each scenario has ≥1 win, **combined prereg candidate acceptance FAILS** because no-harm is mandatory. The model is not recommended as journal-ready scheduler or proven improvement.

## Scientific interpretation and required next work
The new policy is genuinely distinct and may produce large positive descriptive network-shock gains, but also **predictable safety failures in individual CPU-shock seeds and preshock/whole-period misses**. Aggregate numbers obscure harmful cases. Missing at random cannot be assumed: original policy routes influence which nodes receive fresh CPU/E2E observations. The four-world historical sample maximum is **not** formally calibrated and Stage63's high chosen-node hit rate did not validate unselected counterfactual node costs or alternate policy safety. The currently frozen Stage64 partial-minimax policy **FAILS Stage65 independent confirmation** and **MUST NOT BE PROMOTED**. No rerunning Stage65 with tuned threshold then calling it untouched confirmation.

Keep original CASPER E42/E4.6 and prior negative evidence frozen: original independent native Python n10 CASPER_FULL vs PRED_GREEDY paired sign p=1.000, Stage52 simplified queue CPU harm, Stage58 traditional least-inflight DEV harms, Stage61 21-node full-world 0/4840 READY FAIL, original 30k Java SpaceShared vs Python strict-FCFS max waiting deviation9.12140093294972ms>5ms FAIL, Stage56 original Java native event-min20ms 9/12 unfinished. Original source strict-FCFS backend remains synthetic; no independent real IIoT trace, no native Java policy replication.

**Recommended next work**: Stop new holdouts/tuning on spent Stage65 cohort. A retrospective *source-level root-cause* audit on the identified harmful CPU/whole-period cells may help derive a separately justified new candidate with a new distinct DEV cohort and prospective future holdout, or prioritize manuscript/method limitations and external workload/engine validation. Do NOT use Stage65 original seed feedback to retrofit acceptance for this failed candidate.
