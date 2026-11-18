# SIMPAT v1.2 — Scientific editor's evidence-based GO/NO-GO gate (2026-11-18)

**User-locked exact title:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation
**Selected journal:** Simulation Modelling Practice and Theory (Elsevier).
**Real current manuscript:** [v1.2](SIMPAT_MANUSCRIPT_V12_CONSTRUCT_CLAIM_AUDITED_2026-11-18.md).
**Peer-review-style internal methodological audit:** [seven substantive checks](SIMPAT_V12_REVIEWER_CONSTRUCT_AUDIT_2026-11-18.md).
**Actual static QA:** [successful GitHub Actions run44344757396](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44344757396). This checks source/table and prescribed wording, not scholarly originality or acceptance.

## Decision: HOLD actual journal submission pending scientific significance

A1 (native callback trace) + A2 (24 native 8.5.7 SpaceShared cases; 288 completions, difference to event-independent FIFO max246ms, descriptive mean abs49.0961ms, deadline classification disagreements86/288 and107/288) + posthoc service duration adjustment (250/288 mismatches; max154ms) + A3 timestamp-origin audit (288/288 fixed cases matching) form a defensible **bounded descriptive simulator measurement**. Independent repeat and static QA materially improve internal reproducibility.

**BUT the critical causal/novelty gap remains:** the analytical comparator and native event-driven scheduler are consciously non-equivalent, so proving nonzero differences does not itself establish a surprising model pathology, new scheduling algorithm, simulation-science advance or error against physical truth. Older CloudSim papers already identify service duration/accounting issues, analytical-vs-simulator checks and queue models. It is plausible a SIMPAT editor would ask “What actionable simulator modelling principle is established beyond confirming two distinct models give different numbers?”. That question is **not yet adequately answered** by a 24-cell single-VM fixed synthetic experiment. Scientific adequacy needs actual author judgement, not more confidence from repeat runs.

## Changes made now — do not overinterpret
- v1.2 adds the explicit construct-level non-equivalence explanation, clarifies native total duration is a simulator-reported post-completion quantity rather than independent physical service, separates two synthetic deadline constructors, downgrades editorial status of separate FGCS CASPER manuscript to author confirmation, and distinguishes durable git files from potentially expiring GitHub Actions artifacts.
- Original A1/A2/A3 measured results, source artifact hashes and all source cases were NOT changed.
- All four files involved (v1.2 paper, audit, QA and workflow) were genuinely committed and the CI verified SUCCESS.
- Old original 30k strict Java/Python parity FAIL and Stage65 safety FAIL unchanged, Program B independent RESERVED/NOT STARTED.

## Smallest viable next research decision

Before commissioning another experiment, formulate an explicit *falsifiable, non-tautological* simulation-methods claim that present data could demonstrate, and check it against prior papers, for example a derived **trace-level accounting invariant**, a condition under which event-cadence and reference agreement are predictable, or a verifiable precondition to avoid incorrect queue predictions. **Do not pretend the present 24-case study proves such a new theorem.** If no substantive finding can be extracted, alternative article type/venue may be more suitable, or the research may need one *predeclared* new intervention with independently verified outcomes. User may also choose to discontinue this manuscript to prioritize the independently new CASPER Program B; nothing has been started there.

## Remaining author/editorial blockers
- Author-verified source/citation completeness, nearest 2017 cloud-autoscaling full-text assessment if accessible.
- Confirm full FGCS manuscript overlap/status and whether editor must see a copy.
- Exact corresponding author/coauthor approved identities/order, author contributions, funding/COI, correct Elsevier generative AI use statement and full-paper author approval.
- Final persistent archive of runnable code + original outputs (not exclusively time-limited Actions), copyright/licensing, journal-specific format and accessible vector figure.
- No submission yet, no acceptance estimate or guarantee. December 20, 2026 is internal *conditional* target, not a scientific deadline.

**Do not advance to another version number without real scientific or publication progress.**
