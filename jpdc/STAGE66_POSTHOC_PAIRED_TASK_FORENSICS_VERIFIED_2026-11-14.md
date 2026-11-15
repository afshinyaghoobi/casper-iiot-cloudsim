# Stage66 VERIFIED POSTHOC adverse-case paired task forensics — reproducible, NOT confirmatory (2026-11-14)

## Scope and original source provenance
**Explicitly retrospective** protocol after the original Stage65 independent n8 scientific SAFETY FAIL: `jpdc/STAGE66_POSTHOC_PAIRED_TASK_FORENSICS_PREREG_2026-11-14.md` commit `8b640e5a240db4fb49e23a3a15e4708e6ffea00a`. Four outcome-informed selected **spent** Stage65 seeds 1811,1815,1816,1818 × BOTH S2 CPU40%-loss and S3 network50%-loss, frozen original policies CASPER_FULL and PARTIAL_MINIMAX_FULL_FALLBACK, 12k jobs per original deployment, full original Stage3 80k source calibration per seed. **Zero new independent holdout or DEV source seeds**, no p-value, no method change.

Original frozen method exact Git blob `24d495dba4d29f8fe070ad6539b20361a7193cc6`, selector `338dd1de5c17028b3f60f1d635964b52e152df14`, builder `2bcb069b25964b2982e1f56de9725d2faa970762`, E42 `34256ca7bff46f911cf20e8b94278fbd09175746` guarded in CI. Original source and E4.6 untouched. Retrospective tracer `jpdc/run_stage66_paired_task_forensics.py` uses existing **unchanged** Stage64 `simulate(...,mission_audit_hook=...)` actual CPU-finish trace with task ID, deadline, selection, nominal cost, actual CPU, wait, network and end-to-end latency. Each old Stage65 seed source artifact was downloaded from original [run43661658894](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43661658894) (SHA `fd138174ac662b14a88421524f87b7dfa886c6fc`) and original JSON/repeated files checked. Both replays per seed reproduce Stage65 original exact source aggregate outcome/mean latency/wait/candidate diagnostic values.

**Actual [GitHub Actions run43662373211](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43662373211) SUCCESS, all four source forensic jobs**, source commit SHA `78b2518fe3d3233f7ee5d798a8a00017a7dfa4a9`. Original forensic source artifact IDs: seed1811 `14141085456`; 1815 `14141065547`; 1816 `14140702030`; 1818 `14140687088`. Each was downloaded and inspected, exact per-source repeat JSON/log byte equality. Complete independent *artifact-ONLY*, zero-simulator-rerun [**audit run43662466765**](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43662466765) **SUCCESS**, audit source `e225481a07fdaa16e81cf1da41d8e1c3a9b6d99e`, original audit artifact **14140717207** `jpdc-stage66-posthoc-original-task-cohort-audit` downloaded and independently inspected; ZIP digest sha256 `64b433d954a3e988b862b5cf57e8185f093faf81b5c41f735d48837f1461cd7b`. `cohort.json` and `cohort_repeat.json` bytes identical, JSON SHA256 **`c1b87bdc669cf998089af0eda3ae0216bc44fc941cf820a1ffc2d25063c3ed89`**. No source excluded and every one of 8 selected seed-shock contrasts matches the previous Stage65 reported original totals.

## Original paired task outcome decomposition
Pre/post relative to fixed source task index10000; `NEW_ONLY` means new method misses and FULL meets, `FULL_ONLY` means FULL misses and new meets. All discordant output entries retain both full task traces with original deadline, chosen node and physical components; the table shows complete discordant task IDs per phase.

| Spent seed | Shock | PRE FULL→NEW MISSION misses | POST FULL→NEW | ALL FULL→NEW | NEW_ONLY task IDs | FULL_ONLY task IDs |
|---|---|---|---|---|---|---|
|1811|S2 CPU|2→3|0→0|2→3|4385|none|
|1811|S3 network|2→3|1→1|3→4|4385|none|
|1815|S2 CPU|9→8|1→2|10→10|10306|841|
|1815|S3 network|9→8|4→1|13→9|none|841,10790,11001,11840|
|1816|S2 CPU|4→5|1→2|5→7|734,11756|none|
|1816|S3 network|4→5|1→1|5→6|734|none|
|1818|S2 CPU|0→1|0→0|0→1|6877|none|
|1818|S3 network|0→1|0→0|0→1|6877|none|

These are **8 outcome-selected seed×scenario configurations**, NOT an unbiased full-n8 estimate. The same task numbers occur before the shock in two scenarios for a given seed, because pre-shock synthetic policy histories coincide; do not count these as independent replications. Every recorded discordant task in these particular selected configurations also has a different observed assigned node between the two policy trajectories; **even this does not isolate the causal effect of that single routing choice** because earlier task decisions change both queue state and which feedback observations became available.

## Directly measured adverse forensic examples (original FULL vs new PARTIAL)
Values (ms), actual task CPU-finish measurements from the *two complete policy trajectories*, not counterfactual same-state execution.

1. **S2 seed1815 task10306 POSTshock**: FULL node13 nominal46.32, deadline45.26, actual **44.544** = CPU20.084 + wait0 + network24.460 (meets). NEW node17 nominal50.21, actual **51.322** = CPU20.821 + wait5.000 + network25.502 (misses). Increased queue delay is the largest measured additive shift; network and CPU also increased. Prior chosen-node historical sample max has not been independently validated for this new node.
2. **S2 seed1816 task11756 POSTshock**: FULL node15 nominal38.07, deadline40.18, actual **37.104** = CPU22.380 + wait0 + network14.724 (meets). NEW node13 nominal29.44, actual **40.679** = CPU28.450 + wait0 + network12.228 (misses). Despite lower nominal prediction and lower actual network, observed actual CPU execution is +6.070ms on NEW; deviation from new nominal prediction material. This is CPU model/partial ambiguity uncertainty hypothesis, not a proven causal root cause.
3. **S2/S3 seed1818 task6877 PREshock**: FULL node12 nominal37.18, deadline41.93, actual **37.404** = CPU13.571 + wait0 + network23.834 (meets). NEW node15 nominal39.83, actual **43.570** = CPU8.583 + wait18.385 + network16.602 (misses). Even with lower CPU/network NEW, its contemporaneous **wait+18.385ms** dominates. Supports concern about queue/feedback path-dependent congestion.
4. **S2/S3 seed1811 task4385 PREshock**: FULL node17 nominal36.07, deadline40.66, actual **36.286** = CPU20.008 + wait3.318 + net12.960; NEW node15 nominal41.58, actual **41.820** = CPU20.642 + wait0 + net21.178 (miss). Higher network +8.218ms offsets 3.318ms saved in wait, plus slightly higher CPU.
5. **S2 seed1816 task734 PREshock**: FULL node12 actual51.054 deadline51.11 (meets); NEW node15 actual55.273 (misses); actual CPU31.130→41.078 (rises) despite actual network19.924→14.196 (falls). This explains the extra whole-period miss in both shock-labeled runs.
6. **S3 seed1815 tasks10790/11001/11840 POSTshock**: new policy successfully avoids FULL misses, e.g. FULL actual network52.380 vs NEW18.011 at 10790, while NEW CPU can increase (14.565→25.770); no broad claim that new policy universally improves network latency.

## What we can conclude and what remains unknown
- The Stage65 failures are **heterogeneous**: adverse examples include unexpected CPU duration, higher network transfer, and a sharply increased physical queue wait. It would be unsupported to claim one identified correctable parameter or all errors stem from the same cause.
- Pre-shock harms can occur in both S2 and S3, even when POSTshock results are tied or favorable; this directly validates why frozen Stage65 added the stricter whole-deployment no-harm check.
- All task-level miss differences in this selected cohort coincide with different routed nodes, **but the task's own-node change cannot be isolated from previous queue arrivals, queue backlog, and feedback history** by a comparison of two entire policy trajectories. This retrospective comparison is descriptive, and no unchosen node experimental potential outcomes exist under identical states.
- **Stage65 official independent holdout remains scientifically FAILED**: S2 postshock n8 FULL24→NEW17 pooled with actual harm seed1815,1816 and exact sign p1.000; S3 FULL31→NEW14 pooled exact sign p.125; six whole-period harmful seed×shock cells across all original n8 sources. The selected posthoc four-seed diagnostic does not override official n8 result, nor generate a new separate independent sample.
- Stage63 prior chosen-node historical sample-max descriptive coverage is not calibration, and observed subset missingness is policy-dependent; original external Java SpaceShared parity and real IIoT trace portability remain unvalidated. No modification to algorithm, original E42/E4.6 or threshold on known adverse seeds.

## Next scientifically valuable decision
**Do not immediately patch Stage64 based on these selected task IDs and call it confirmed.** Either (1) develop a new independently motivated *candidate* that explicitly considers what can be observed about CPU/service/queue while preserving no-future-leak restrictions and formally preregister NEW development sources, then reserve a fully disjoint future prospective holdout, or (2) focus on genuine independent workload/Java queue fidelity and manuscript reporting of the limitations and negative confirmation. A more insightful cross-runtime/trace validity study may be more publishable than additional incremental threshold variants.

See also permanent new-chat restart guide `jpdc/CHAT_RESTART_HANDOFF.md`; update it with Stage66 verified status and this report reference whenever checkpoint changes.
