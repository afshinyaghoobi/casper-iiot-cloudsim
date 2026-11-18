# SIMPAT submission cover-letter draft — author verification required

**Target:** Editorial Office, *Simulation Modelling Practice and Theory* (Elsevier)

**Subject:** Submission of “Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation”

Dear Editor,

We would like to submit our manuscript, “Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation,” for consideration in *Simulation Modelling Practice and Theory*.

The manuscript examines a specific reproducibility issue in simulation-based scheduling evaluation: whether waiting times and synthetic deadline classifications reported by CloudSimPlus 8.5.7 SpaceShared scheduling agree with a separately defined, capacity-matched, event-independent FIFO reference. It uses an instrumented six-condition Java admission study, a prespecified 24-condition native simulation involving 288 completed CPU-only Cloudlets, and independently audited post-completion duration and timestamp-origin checks. In the tested synthetic conditions, the largest within-case discrepancy in native-reported versus reference waiting time was 246 ms; a retrospective reference using native-reported execution durations still showed a largest discrepancy of 154 ms.

The study is intentionally bounded. It does not propose a new scheduling algorithm, claim a CloudSimPlus bug, or imply that the synthetic one-VM workloads establish real IoT or industrial-system deadline performance. Instead, it documents exact software-version and measurement-model differences with publicly traceable input definitions, control traces, scripts and tabulated outcomes. We believe this measurement-construct and reproducibility focus may be relevant to the journal's interest in simulation model comparison, verification and transparent computational experimentation.

**Before submission, the corresponding author must personally verify and replace this paragraph with truthful statements:** [Confirm originality and whether any substantially overlapping manuscript is under consideration elsewhere; disclose the separately submitted FGCS CASPER algorithm manuscript and precisely differentiate this work; verify all coauthors have approved the manuscript and submission; confirm conflicts, funding, ethics, data availability, and any publisher-specific statements.]

The original experiment scripts, frozen run identifiers, results and reproducibility checks are described in the manuscript and the source repository. We would be grateful for your consideration.

Sincerely,

[Corresponding author — confirmed name, affiliation and institutional email]

---

**NOT FOR DIRECT SUBMISSION.** The bracketed statements and author confirmations are mandatory and not independently known. Do not assert that the first FGCS manuscript has been accepted or published; its editorial status must be checked with the author. Do not submit this letter until manuscript, authorship, declaration and title-page details are confirmed. No editor or contact email has been invented.
