# SIMPAT 8.5.7 — FROZEN independent-input event-phase prediction experiment, before Java execution

**Preregistered 2026-11-18 before writing/compiling/running a new holdout Java runner.** User title locked: **Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation**. Journal SIMPAT. Original A1 original six fixtures and A2 original 24 fixtures DO NOT CHANGE. This is an independent new **hand-designed synthetic input fixture set**, not a random representative population or real IoT data.

## Tested question and nonclaim
Can the specific *older WAIT / younger direct EXEC* observation, previously seen in 2 of 6 known A1 cases, be predicted and observed in **new independently configured three-job workloads**? More importantly, can a trace-only state predicate evaluated **before** new-job submission classify this native queue-state anomaly without using the downstream submit eligibility or AFTER state? The second test risks being a tautological restatement of documented admission behavior; success by itself will NOT count as a major journal contribution.

## Frozen input cases (new, not chosen after holdout results)
Each three-job case uses CloudSimPlus8.5.7, exactly one VM/one PE, same Java17/Maven MIPS=1,000,000,000 and base simulation time1s, utilization 100%, no network. Job indices 0,1,2 submit with delays BASE+arrival ms, lengths (in ms rounded to nearest integer MIPS length), no scheduling algorithm modification. Exactly **four independent hand-chosen service/arrival families**, each with 1μs and5ms minimum-event interval, giving **8 fixed cases**:

| Family | Service ms [job0,job1,job2] | Arrival ms [job0,job1,job2] | 2 event gaps |
|---|---|---|---|
| H_A | [7.35, 5.10, 6.65] | [0, 4.40, 7.42] | 1US, 5MS |
| H_B | [11.60, 3.75, 8.20] | [0, 6.85, 11.71] | 1US, 5MS |
| H_C | [5.85, 6.25, 4.90] | [0, 3.30, 6.17] | 1US, 5MS |
| H_D | [9.45, 7.10, 5.40] | [0, 5.85, 10.05] | 1US, 5MS |

Name convention H_A_1US,H_A_5MS,...,H_D_5MS. These numbers are *not* claimed sampled randomly; they were designed around plausible near-completion arrival conditions **without seeing these exact scenarios' results**. May have overlap in parameter structure with original A1 but have distinct service and arrivals. **Do not alter input case table after looking at results.** All 8 MUST count, including cases with no waiting or eligibility pattern.

## Explicit source-trace-only pre-submit predicate P (a descriptive prediction, not a physical law)
For each case, read exact Java instrumentation rows only (no AFTER admission and no FINISH outcomes):
1. An UPDATE before-event has job0 in EXEC and older job1 in WAIT, and within that same UPDATE a waiting-promotion eligibility call for job1 returns **false**.
2. That UPDATE returns with EXEC empty and job1 still WAIT (same timestamp group); no subsequent waiting-promotion transition removes job1 before the next submission of job2.
3. At the next SUBMIT **BEFORE** record for job2, EXEC is empty and job1 still WAIT. **All labels that could reveal the new job's outcome, such as `SUBMIT AFTER` or new job2 `ELIGIBILITY` and other later records, MUST NOT be used to define P.**

**Predicted label:** if P true, expect direct job2 admission into EXEC despite job1 still WAIT on the SUBMIT AFTER record. P false: do NOT automatically predict non-bypass (lack of observed precursor doesn't prove no other path); report P-negative bypasses as failures of sufficiency/coverage and report 2x2 descriptive confusion matrix if treating no-P as predicted no-bypass.

**Predeclared falsification:** Any P-positive with job2 *not* admitted directly while older job1 still WAIT counts against sufficiency. Any P-negative that nevertheless produces old-WAIT/young-EXEC undermines **coverage** and simplistic necessity. If P is always false or always true, **NO informative generalization**. If source trace records are missing or incomplete, technical QA FAIL. No posthoc changing thresholds to improve performance.

## Separate input-only hypothesis H (a weak exploratory generalization check)
Prior six-case evidence suggested anomalies only at 5ms gap. Before running these holdout cases, state a **weak input-only directional hypothesis**: the proportion of 5MS cases exhibiting old-WAIT/new-EXEC after job2 submit is greater than the analogous 1US cases among these **four matched family pairs**. If difference zero or reversed, H FAIL. Four pairs offer **zero population statistical generalizability**; do not report significance tests or general rule even if matches.

## Instrumentation / integrity gates
- Copy and preserve PASSIVE scheduler hooks from the original exact 8.5.7 A1 waiting promotion trace, changing only explicit case fixtures and log label to `HOLDOUT_`. No treatment and no source library modification. Record UPDATE-before/after, wait promotion-before/after, eligibility calls and new job SUBMIT-before/after, job completion/wait/service.
- Run same eight synthetic cases twice; require full native traces byte-identical. Java17 Maven compile and all3 Cloudlets complete each case; original E42 and failed Stage64 code-hash guards unchanged. Track exact Git SHA/run logs/artifact. If a single simulation fails or output differs, mark technical gate **FAIL**. Never omit that case or rewrite values.
- Build **independent Python trace parser**, check original case list exactly and 8 x3 outcomes. Compute P using only before-admission source evidence, label using after-admission state. Use no numeric posthoc time thresholds or stopping once positives appear.
- Report both P-positive label matches and P-negative positives, counts for 5MS/1US. Distinguish empty eligibility logs versus false eligibility; do not silently infer method calls.
- This does not independently validate A2 288-job FIFO discrepancy, IoT/IIoT network timing or real hardware, nor prove a bug/novel algorithm. Matching the documented method contract might make P basically trivial. **Scientific full-SIMPAT GO/NOGO stays HOLD** even if all eight match unless an independently novel simulation-evaluation principle is established.

Negative historical results: strict30k Java/Python parity FAIL; Stage65 safety FAIL. CASPER research Program B separate RESERVED/NOT STARTED. Document all failures; no favorable-run selection.
