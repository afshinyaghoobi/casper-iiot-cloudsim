# JPDC one-page contribution charter — provisional Path A, 2026-11-04

**Identity:** systems-methodology and negative-results investigation of certification reliability vs task completion under policy-dependent exposure to hidden cloud/edge impairment. **Not** "CASPER 2.0" or a newly optimized scheduler based solely on the current frozen code.

## Working title
**When Adaptive Certificates Do Not Improve Deadline Completion: Exposure-Aware Validation of Cloud–Edge Scheduling**

Alternative for an eventual new-algorithm paper: no title committed until a distinct scheduling mechanism has been formalized and independently evaluated.

## Research question and falsifiable statements
**RQ1 (mechanism):** In the original event-driven CloudSim environment, how does holding the physical fault placement fixed while toggling E17 adaptive eta change the distribution of issued but incorrect certificates, abstentions, and realized deadline misses? Answer using existing registered/exploratory results and strict distinctions between quantities; no universal causal effect assertion from selected four-seed masks.

**RQ2 (replication boundary):** When original CASPER policy modules execute in an independently implemented 21-node Python strict FIFO event system with native calibration and source-compatible stochasticity, is the primary paired FULL-vs-PRED_GREEDY postshock deadline-miss effect reliably positive across previously untouched seeds? **Observed answer:** NO at alpha .05, original preregistered exact two-sided sign p=1.000 (five positive, four negative, one tie), even with positive descriptive mean difference of +0.3208 percentage points. A negative outcome is the reported outcome, not a failed computational run.

**RQ3 (reliability interpretation):** Which components of the experimental outcome support certificate conservatism as distinct from improved execution? Describe correct denominator, policy-dependent exposure, E17 eta activity, and rank2 usage; do not treat certificate reduction as proof of better deadline completion or a finite-sample guarantee under arbitrary shift.

## Evidence that must appear in the manuscript
Original Java disjoint ten-seed p=.0625 (nonsignificant); exploratory four-seed mask × eta p=.125 (nonsignificant); native 10-seed holdout p=1.000 (nonsignificant). Original strict Python-vs-CloudSim physical FCFS parity FAILED max 9.1214ms >5ms. Native deployment 160 policy/scenario runs /4.8million task-policy outcomes with **n=10 independent seeds**, not millions of independent samples. CASPER_FULL native rank2 39 / rank3 zero; health/eta mechanisms active; deadline misses for CASPER_FULL and CASPER_HEALTH_STATIC identical in overall native S2/S3 scenario summaries.

## Proposed contribution sentences (defensible if overlap gate passes)
1. "We empirically distinguish nominal fault severity from realized, policy-dependent workload exposure and show that the placement of degraded resources can dominate observed certificate behavior in the studied simulator settings."
2. "We quantify the tradeoff between incorrect deadline certificates and abstentions induced by adaptive uncertainty scaling under controlled fault placement, while explicitly reporting that deadline completion does not improve materially in those tested interventions."
3. "We provide an independently executing Python event-based replication that regenerates its own stochastic task completions and conformal calibration, and report a fully preregistered, statistically nonsignificant ten-seed scheduling comparison."

## Exclusions and submission gates
Do not say a **new CASPER routing algorithm** was invented, a **YAFS replication** has been completed, physical queue equivalence with CloudSim is proven, rank2 causally improves outcomes, rank3 activated, or adaptivity guarantees correctness under hidden drift.

Full original FGCS manuscript vs proposed JPDC manuscript section/equation/figure/code overlap mapping remains the *top blocking gate*. If duplicate core contributions dominate, this identity may also be inadequate for JPDC even if methodologically careful. Current novelty audit is preliminary rather than an exhaustive literature review. Investigate independent workload and network traces and a real second-simulator model, or design a mathematically distinct scheduling rule before authoring a positive-algorithm claim.

## Status
**Draft framing only. Not submission-ready.** Related technical novelty/claim matrix: `jpdc/JPDC_NOVELTY_ORIGINALITY_GATE_2026-11-04.md`. Original native results are locked in `jpdc/NATIVE_TEN_SEED_ALL_EIGHT_HOLDOUT_VERIFIED_2026-11-04.md`. Keep E42/E4.6 frozen.
