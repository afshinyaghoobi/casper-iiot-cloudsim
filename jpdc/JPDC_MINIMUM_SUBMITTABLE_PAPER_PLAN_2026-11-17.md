# JPDC minimum-submittable paper plan (2026-11-17)

STATUS: PROPOSED STRATEGY, NOT A VERIFIED MANUSCRIPT NOR ACCEPTANCE FORECAST. Aim for an ethically defensible submission, not completion of the entire CASPER research program.

## Decision
Separate the first FGCS CASPER algorithm paper from a new JPDC systems-methodology article. Primary candidate: **"Event-Granularity and Queue-Admission Semantics in Cloud–Edge Scheduling Simulation: A Reproducible Cross-Model Study"** (working title). Main question: when do discrete-event admission/update semantics change waiting lists, deadline-sensitive outcome calculations and policy comparisons relative to an explicitly defined strict-FCFS reference? Do NOT claim a defect in CloudSimPlus or validate original Python as an equivalent runtime. This is a proposed distinct evaluation contribution, not assured JPDC acceptance. Align scope to JPDC distributed-system performance/evaluation and distinguish sufficiently from FGCS text before writing claims.

## Existing verified material
- Real Java CloudSimPlus 8.5.7 six-case synthetic arrival shift, 18/18 complete, native WAIT/EXEC snapshots show direct admission only in ORIGINAL_5MS and LATE10_5MS; independently audited.
- Publisher exact source path audit identifies distinct submit-side and waiting-promotion source paths; method branch/callback cause not dynamically proven.
- Original Java/Python 30k strict-FCFS max wait discrepancy 9.12140093294972ms > 5ms FAILED; Stage65 independent policy safety FAILED. Do not rehabilitate either.
- Stage68 draft exists: STAGE68_JPDC_MANUSCRIPT_VALIDITY_AND_NEGATIVE_RESULTS_DRAFT_2026-11-14.md. FGCS overlap audit warns against recycling CASPER/uncertainty certificate contribution.

## Bounded minimum original study needed
1. Finish the already preregistered dynamic admission/WAIT-promotion passive trace (protocol NATIVE_V857_DYNAMIC_ADMISSION_TRACE_PREREG_2026-11-17.md) as supporting mechanism, not entire paper.
2. A NEW prospective, independently audited simulation-semantics experiment with at least two distinct scheduler-relevant workload families (e.g. staggered and bursty arrivals), a manageable fixed matrix of event gaps and 1-PE/2-PE capacity conditions and an explicit same-input strict-FCFS comparator. Freeze actual design and metrics *before* running. Include completion conservation and per-run reproducibility.
3. Report absolute wait discrepancy and rank/order or deadline-classification changes under a small range of PREDECLARED deadline margins. If no difference observed, report no difference; do not retrofit thresholds, select only advantageous settings or assert general prevalence.
4. At least one independent analysis/parser plus exact code/seed/version references. Provide actual per-condition samples; descriptive uncertainty where the random seed is experimental unit. No inference from 18 Cloudlets as independent replications.
5. Assemble Introduction, focused related work and distinct FGCS-overlap table, question/hypotheses, model definitions, experimental protocol, results incl negatives, limitations, reproducibility, conclusion. Check journal author instructions, references, cover letter, ethics and journal AI policy before submission.

## Submission decision (not perfectionism)
SUBMIT when there is (a) a non-overlapping, technically clear and evidence-backed contribution with results broader than the present 3-job illustration, (b) all reported metrics directly trace to native outputs, (c) no unsupported policy superiority, CloudSim bug, field IIoT generality, or parity claim, (d) paper + figures/tables + references + author approvals comply with JPDC. No necessity to solve Stage65, simulate all 500 Google trace parts, run hardware, instrument every native private branch, or discover a better policy.
If comparative effect absent or study fails to yield a real contribution, pivot title and target journal rather than call a source-code audit alone a JPDC research paper.

## Time-boxed schedule from Nov 17, 2026
Nov 18–24: freeze manuscript question, FGCS originality table; implement/run dynamic trace and methodological experiment protocol.
Nov 25–Dec 3: run bounded new workloads, tests and independent audit; freeze figures/tables and negative outcomes.
Dec 4–11: write complete first manuscript version (not just snippets), literature and code/data availability.
Dec 12–18: independent numerical/overlap read, edit, submission package.
Target earliest plausible Dec 15–20 if all gates pass; pragmatic Dec 20–Jan 10 if revisions or holiday friction. These are planning estimates, not guarantees. A failure to establish contribution triggers pivot, not fabricated result. Review/editorial acceptance cannot be predicted.

## Keep separate second paper
Subsequent algorithm paper can use a genuinely new pre-dispatch decision rule, independent train/dev/test source seeds and prospective heldout evaluation, with different objective and empirical questions. Do not split one experiment into two minimally different papers or reuse exact results as new. Distinct title alone is NOT sufficient.
