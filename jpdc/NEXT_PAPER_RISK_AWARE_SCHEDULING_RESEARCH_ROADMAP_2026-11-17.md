# Research Program B — NEXT PAPER after the JPDC simulation-semantics manuscript

**Created:** 2026-11-17
**Status:** RESERVED / NOT STARTED / NO VERIFIED PERFORMANCE CLAIM
**Owner:** Research author; AI-assisted tooling is subordinate to author review.
**Priority:** AFTER Program A reaches an internally complete submission package. Only low-cost design notes may proceed meanwhile.
**Program A:** [JPDC Minimum-Submittable Manuscript Plan](JPDC_MINIMUM_SUBMITTABLE_PAPER_PLAN_2026-11-17.md)
**Program-wide index:** [TWO_PAPER_RESEARCH_PROGRAM_INDEX_2026-11-17.md](TWO_PAPER_RESEARCH_PROGRAM_INDEX_2026-11-17.md)

## 1. Research identity and tentative submission article

**Working title:** *Risk-Aware Online Cloud–Edge Scheduling under Selective Feedback and Queue Uncertainty*
**Paper type:** NEW scheduling method, clearly distinct from Program A's simulation-semantics/measurement study and FGCS's original CASPER algorithm.
**Target venue:** TBD only after a real original method and confirmatory results exist. JPDC, FGCS or another relevant journal are possibilities, not commitments.
**Research question:** Under partial, policy-dependent observation of node execution outcomes, can a NEW pre-dispatch online decision rule limit deadline-risk exposure, including stale/unobserved node states and queue prediction uncertainty, without violating a specified resource/safety budget? Study may yield negative findings. No promise of statistically significant gains.

## 2. Avoid duplication and salami slicing

The original FGCS CASPER paper already includes core conformal-like certificates, health/probes, controller, eight policy modes, synthetic scenarios and some limitations of chosen-node feedback, so NONE of those alone may be claimed as novel here.
Program A addresses experimental equivalence/nonequivalence of queue and discrete-event semantics; Program B must not republish its six-case Java mechanisms as a new algorithm result.
**New distinct contribution is only possible if** there is (1) an explicitly defined new decision rule/optimization or control mechanism, (2) an information-availability/causality contract, (3) appropriately separate evaluation and (4) new conclusions beyond FGCS and Program A. Reuse of code, simulator scaffolding and clearly cited background is allowed; reuse of identical result tables as novel evidence is not. Check actual first FGCS submitted text before finalizing originality claims: [FGCS overlap audit](FGCS_FULL_MANUSCRIPT_VS_JPDC_OVERLAP_AUDIT_2026-11-04.md).

## 3. Hypotheses (not yet experimentally verified)

- **H1 (method feasibility):** A bounded-complexity pre-dispatch policy can be implemented using ONLY causally observed delivered telemetry, with explicit stale/missing feedback handling and no oracle access to unchosen nodes.
- **H2 (risk/safety):** In prospective, disjoint source cohorts, the method meets predeclared noninferiority/no-harm conditions relative to its matched baseline (CASPER_FULL and at least one transparent distinct comparator). Failure is a reported result; never rebrand it as success.
- **H3 (selective feedback):** Controlled missingness/staleness and queue-estimation perturbations materially change policy behavior; quantify under preregistered regimes without posthoc cherry-picking.
- **H4 (generalization):** Confirmed improvements, if any, persist across distinct workloads/schedulers/perturbation regimes. No claim of generalization from synthetic in-model seeds alone.

## 4. Method candidates (DESIGN OPTIONS, NOT IMPLEMENTED METHOD)

Evaluate on paper before coding; select ONE and formally freeze BEFORE independent confirmation:
A. **Risk-budgeted safe routing:** choose between nominal baseline and alternative destination only if estimated risk reduction exceeds explicit uncertainty bound and a dynamic intervention budget remains.
B. **Feedback-coverage-aware selective routing:** abstain from risky reassignment when observed feedback does not cover the relevant candidate set; report coverage and intervention frequency explicitly.
C. **Queue-error-aware robust routing:** a constrained worst-case/ambiguity-set objective using causally estimated queue error with transparent fallback when ambiguity set support is insufficient.

These are hypotheses/design sketches, not novel by definition. Conduct a literature and FGCS-overlap check first. Do not recycle rejected Stage64/65 as a renamed successful method. Construct a counterexample or formal non-alias test showing the final rule differs from existing CASPER and nominal-greedy on feasible inputs. If method reduces to previous one under all permitted states, no separate algorithm contribution.

## 5. Stage-gated work packages

| ID | Work package | Deliverables | Exit criteria |
|---|---|---|---|
| B0 | Freeze boundary after Program A | final Program A version/reference, novelty-overlap grid, frozen baseline repo commits | no duplicate abstract contribution |
| B1 | Focused related work + precise research question | 2-3 falsifiable contribution sentences, definitions of outcomes and observability, comparator feasibility matrix | distinct from FGCS and A on substance |
| B2 | Formal algorithm before performance tuning | mathematical decision rule, pseudo-code, complexity, data-flow/timestamp validity, safety budget; proof/counterexample of non-alias | implementable without future/counterfactual node information |
| B3 | Independent source contract | versioned source manifest, immutable train/dev/test split by independent original *source seed / workload*, workload provenance, fixed metrics/deadlines and negative controls | no seed overlap / reused holdout; prevent posthoc selection |
| B4 | Software implementation and unit controls | isolated new policy module and unit tests, causal observability guards, capacity/queue invariants, fallback correctness, missing/stale feedback tests | no modifications to frozen FGCS E42/E4.6 or rejected Stage64 |
| B5 | Bounded DEV evaluation | 2-4 new distinct development seeds/workloads, traces, ablations (risk/feedback/queue), failure cases, registered stop conditions | confirm viable method or stop/pivot; DEV never becomes confirmatory |
| B6 | Freeze protocol for holdout | predeclared primary metric, noninferiority margin (scientifically justified), secondary metrics, test, tie policy, samples, baseline set, failure rule | commit protocol BEFORE evaluating test sources |
| B7 | Independent prospective validation | disjoint multi-seed holdout with native/independent semantics explicitly scoped, paired source-level stats and intervals, full negatives | only claim benefits supported by holdout; Stage65 original failures retained |
| B8 | Replication and manuscript | independent numeric auditor, ablation, complexity, limitation/overlap, complete new manuscript | submission package meets target journal rules |

**Gate B5 failure path:** If DEV has repeated deadline harm or observability infeasibility, freeze as NEGATIVE and stop that candidate. May redesign on genuinely new DEV sources; never keep using same holdout. **Gate B7 failure path:** report negative result and choose a genuinely defensible negative-methodology article or stop; do not alter predeclared success metrics.

## 6. Evaluation contract (freeze before execution)

- Clearly define PRIMARY outcome at independent source level (e.g. MISSION deadline misses per source/regime), paired comparator and direction. Report throughput, latency, misses, intervention rate, stale observations, decision runtime and resource overhead as separate secondary outcomes.
- Distinguish total-period and post-shock windows without switching primary window after seeing outcomes; independently sample workload sources for train/dev/test; treat independent source seed, not tasks, as experimental unit.
- Include nominal greedy, CASPER_FULL (original), and one defensible structurally distinct implementable comparator. Do NOT label simplified queue heuristics as faithful published DFAQ-LB/AUHS reproductions.
- Log every attempted candidate destination, visibility mask, age of feedback, chosen fallback, queue estimator, decision score, pre-dispatch state and resulting chosen-node observed outcome; unchosen counterfactuals must not become “observed feedback.”
- Strict Java SpaceShared ↔ Python FCFS fidelity previously failed (max difference 9.12140093294972 ms > 5ms). Either use a single disclosed well-tested experimental semantics in primary evaluation, or a genuinely comparable native scheduler with explicit convergence/trace contract. Never assert Python=CloudSim.
- Workload: synthetic is acceptable as *synthetic*, but no invented physical IIoT deadlines/network packet measurements. Seek independent real workload with explicit mapping and provenance if feasible; do not make entire Google2011 500-part scan prerequisite.
- Do not assert a conformal coverage guarantee from historical maxima or selected-node hit fractions; any theorem must exactly match sampling assumptions and proof.

## 7. Tentative schedule, only AFTER A

- B0-B2: ~1-2 weeks for formal method + originality and small counterexample.
- B3-B5: ~2-3 weeks for clean new source split, implementation and bounded DEV.
- B6-B7: ~1-2 weeks for frozen disjoint holdout and independent audit.
- B8: ~2-3 weeks for manuscript and submission preparation.
- **Planning range: approximately 6-10 weeks after deliberate restart**, contingent on viable independent contribution; NOT a deadline or publication forecast. Important: do not divert Program A's December submission effort into B prematurely.

## 8. Archive, checkpoints and communication rule

- Keep a separate future paper manuscript directory and evidence ledger when B0 actually starts. Use distinct protocols, work products, source splits, run IDs and artifact hashes; linked old results must be labeled “PRIOR / SPENT”.
- Every future continuation should begin by reading [program index](TWO_PAPER_RESEARCH_PROGRAM_INDEX_2026-11-17.md) and current handoffs. If Program A is still active, default work there; Program B stays reserved unless explicitly authorized to switch focus.
- Never characterize this roadmap as a completed experiment, approved contribution, or guaranteed submission.
