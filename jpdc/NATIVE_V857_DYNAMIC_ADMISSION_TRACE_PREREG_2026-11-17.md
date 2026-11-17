# PREREGISTRATION — Prospective native CloudSimPlus 8.5.7 dynamic admission / waiting-promotion trace

Date: 2026-11-17. Status: PROTOCOL ONLY; NOT EXECUTED. This is a new diagnostic, not evidence of scheduler efficacy or Java/Python fidelity.

## Prior observations (spent, not an independent holdout)
- Original real Java six-case arrival intervention: run 44153953054, native.log SHA256 b80536e332b04ffeb0285005b38a95563bac36c29201fc8f93693efc95e5c250.
- Direct submit-list transition in ORIGINAL_5MS at 1013.0997406ms and LATE10_5MS at 1023.0997406ms: BEFORE EXEC=[] WAIT=[1]; AFTER EXEC=[2] WAIT=[1].
- Source-only audit run 44159176587: exact publisher org.cloudsimplus:cloudsimplus:8.5.7:jar:sources archive sha256 8d3efcacfc661b2f1e018e279761fc4ae1e5584a770b2022d20930568688966c; abstract cloudletSubmitInternal and updateProcessing/waiting-promotion methods are distinct. Lexical inspection does NOT prove executed branches.

## Question and competing mechanisms
At the time a later Cloudlet is directly put in the EXEC list while an older one remains WAIT, does the runtime show a free-PE admission opportunity and a waiting promotion that was deferred until a subsequent update? Alternatives: different resource eligibility of the older job, event timing/aggregation and callback ordering, or observational clock semantics. Do not call any outcome a CloudSim bug without proving contract violation.

## Frozen design
Use unchanged real CloudSimPlus 8.5.7 binary, Java 17, same fixed three synthetic one-PE SpaceShared jobs and six configurations as the earlier arrival experiment: CPU requests [8.099623,4.730689,9.120283] ms; arrivals job0=0, job1=5.318920ms, job2=4.0997406/8.0997406/18.0997406ms; minimum event time 1 microsecond / 5 milliseconds. Workload is explicitly a *mechanism replication*, not an independent workload or blind effect-size estimate.
Create a NEW isolated subclass/Java main; do not alter the original six-case source or any E42/E4.6, Stage64/65 files. Override only methods whose exact 8.5.7 signatures, access and safe observer semantics are verified from publisher sources. Passive logs may inspect state before/after super calls; never insert/remove waiting or executing Cloudlets, dispatch jobs, or alter simulation timing from the logger.
On each observed submission and processing update record simulator clock, callback name and entry/exit, submitted job ID, ordered WAIT and EXEC IDs, job PEs, VM PE capacity, runtime accounting of occupied/free PEs IF official API exposes it without mutation, and next scheduled update delay when returned by super. If feasible without library patch, separately instrument the exact protected admission eligibility or waiting-promotion method and record its invocation/return; first verify no instrumentation changes method dispatch or scheduler semantics. If inaccessible, record method-level evidence as UNOBSERVED; do not fake it using list snapshots.
Write a bounded machine-readable trace and six-case outcomes; ensure all 18 Cloudlets finish and trace timestamps are finite and nondecreasing within each case (allow same-time callbacks). Include repeat determinism check and uninstrumented earlier-harness comparison on completion/wait/snapshot outcomes to detect observer effects. Fail the experiment rather than silently ignore a mismatch.
Controls: ORIGINAL_1US and LATE10_1US are prior non-bypass comparison cases; EARLY4 must preserve actual submission order 0 -> 2 -> 1 and MUST NOT be mislabeled later-job overtaking. Run the complete 3 x 2 matrix, not only positive cases.

## Primary mechanistic decision rule
Declare “dynamically observed direct admission with older waiting work” only when same-submit BEFORE and AFTER snapshots show an older actually submitted Cloudlet still WAIT and newly submitted later job in EXEC, with its submission callback identity intact. Declare “free-capacity explanation supported” only if actual method-level eligibility/free-PE evidence confirms the relevant admission decision during that same callback; list snapshots alone are insufficient. Declare “deferred waiting promotion observed” only if waiting-promotion callback is dynamically seen and ordered against the submit, not just present in publisher source. Report each other explanation as UNRESOLVED where not observed. Snapshot EXEClist != physical CPU starting instant.

## Independent validation and negative controls
A second parser that does not import the first must independently reconstruct six submission orders, direct transitions and callback sequencing from the native raw trace. It must reject truncated cases, duplicated/missing jobs, malformed IDs/timestamps, job out of ordering, and absence of expected positive/negative controls. Verify code SHA, Maven source/binary version, artifact hashes and deterministic repeat; archive logs and report any perturbation relative to the previous native harness. If passive extension changes outcomes, mark instrumentation INVALID, not a causal discovery.

## Original failure gates (immutable)
- Java SpaceShared vs Python strict FCFS original 30k max waiting gap 9.12140093294972 ms > preregistered 5ms: FAIL.
- Stage65 original independent prospective n=8 safety: FAIL. Stage56 9 unfinished, Stage61 0/4840 READY. No algorithm-performance, novelty, or external original-IIoT validation claims from this trace.
- Preserve original FGCS E42 Git blob 34256ca7bff46f911cf20e8b94278fbd09175746 and rejected Stage64 blob 24d495dba4d29f8fe070ad6539b20361a7193cc6.
- No new Google GCS scan, no network traffic inference, no implicit new seed.

## Completion gate
Mark COMPLETE only after a new real Java CI run, independent trace auditor, byte-checked archived artifacts, immutable source checks, and updated both handoffs. Otherwise retain explicit NOT EXECUTED / PARTIAL status.
