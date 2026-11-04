# JPDC full FGCS submission manuscript overlap audit VERIFIED — 2026-11-04

## Found original first paper (material change in source availability)
We located and directly read the user's prior Library upload **`FGCS-S-26-07417 (1).pdf`**, a 22-page Editorial Manager first-paper submission package. Its real research manuscript occupies PDF pages **4–19**; title *CASPER: Conformal Adaptive Scheduling for Uncertainty-Aware Online Dispatch in Cloud-Edge IIoT*. A same-title alternate `FGCS-S-26-07417.pdf` is also in the Library. This is a submitted manuscript draft; its presence does **not** mean an editor accepted/published the work. Only the former identified PDF was inspected for the detailed analysis.

Read original paper §1.1 contributions p.4; §3.1–3.5 Eqs.(1–7) pp.6–8; §4.1–4.5 Eqs.(8–10), all eight original policies Table2 and CASPER_FULL Algorithm1 pp.8–10; §5 Eqs.(11–12), candidate-family audit pp.10–12; §7 Discussion p.18, §8 Limitations p.18, §9–10 p.19. Direct comparison sources: `jpdc/JPDC_INTEGRATED_RESULTS_DISCUSSION_2026-11-03.md` (original Java continuation); `jpdc/JPDC_NATIVE_HOLDOUT_RESULTS_DISCUSSION_ADDENDUM_2026-11-04.md` (native independent ten-seed results); earlier provisional contribution charter. **This is an anchored comparison of the complete FGCS first paper to available JPDC drafts**, not a completed two-manuscript text-similarity report because no full revised second JPDC manuscript exists.

## Revised scientific originality conclusion
**HIGH overlap and NO-GO for current second paper as a new algorithm.** The first FGCS manuscript already contains all original CP quantiles / rank budget, virtual queues, E17 eta, health/probes, first-feasible top-three certificate routing and eight policies; it also already explains in its §7 Discussion that eta may improve **screening/coverage rather than executed deadlines**, the selected-node residual feedback may miss nonselected network-damaged candidates, pure network degradation is not detected by the service-ratio health check, one-step counterfactual family coverage does not simulate rerouted future queues, and health/probe effects are coupled. Its S3 lower empirical coverage is also an expressly acknowledged principal boundary.

Therefore the previously proposed JPDC working title **`When Adaptive Certificates Do Not Improve Deadline Completion: Exposure-Aware Validation of Cloud–Edge Scheduling`** is no longer recommended as a distinct novelty headline; the same central idea is already explained in FGCS. Retain the old proposed charter as historical documentation; do not silently rewrite it to suggest newness.

What is newly developed relative to first paper:
- post-original controlled pre-shock placement HIGH/LOW six-node fault-mask interventions and eta-clamp factorial (four original Java seeds, very small n, two-sided sign p=.125 NONsignificant);
- separately preregistered original Java adaptive ETA-vs-static ten disjoint seed30–39 test (two-sided sign p=.0625 NONsignificant);
- independently executing Python strict FIFO stochastic physical event engine with own 80k calibration, all original eight policies, ten reserved seed60–69 /4.8m task-policy executions; original prereg FULL-vs-GREEDY exact sign p=1.000 NONsignificant; not a different workload distribution or YAFS and not exact CloudSimPlus queue parity (old FIFO transfer 9.1214ms >5ms FAIL);
- observed native real rank2 FULL39, rank3 zero, which enhances mechanism visibility without rank2 counterfactual causal benefit.

These constitute methodological evaluation and falsification rather than a clearly novel routing algorithm or new conformal guarantee. A new paper would need a materially different formal pre-dispatch decision mechanism (not yet implemented) **or** a genuinely distinct causal systems-study design with independent randomized failures/other simulator/traces, and a new falsifiable question.

## Created and CI-verified repository files
1. `jpdc/FGCS_FULL_MANUSCRIPT_VS_JPDC_OVERLAP_AUDIT_2026-11-04.md` — **page/section/equation/table/Algorithm 1 mapping** with concrete duplication risk and new intervention boundaries; commit **`e7f07ef68531c4ba54e1fd30509a4c736e4464ec`**.
2. `jpdc/JPDC_REVISED_SUBMISSION_GATE_AFTER_FGCS_FULL_TEXT_2026-11-04.md` — supersedes previous provisional Path A title and distinguishes two genuine additional research options, commit **`416adefd93d7fea8d9b80dfeb5ef808bf95f35f3`**.
3. `jpdc/audit_full_fgcs_overlap_claims.py` — QA claims and manual FGCS document section anchors, negative original study outcomes, first-paper submitted status and original strict queue FAIL; commit **`734e0b39e3960f9d2daa681a62604492416cbe27`**.
4. `.github/workflows/jpdc-full-fgcs-overlap-audit.yml` — frozen E42 source hash, overlap/new contribution claim gate, original novelty and native manuscript scientific-number checks; commit **`5918e997486e0e127e0980331098ea82aa5a14f5`**.

**REAL GitHub Actions run `41925912142` COMPLETED SUCCESS**, job `126910140177`, evidence artifact **`13369975776`**. Exact success markers: `JPDC_COMPLETE_FGCS_FULL_TEXT_OVERLAP_QA_PASS`, `JPDC_NOVELTY_CLAIM_BOUNDARY_AUDIT_PASS`, `JPDC_NATIVE_HOLDOUT_MANUSCRIPT_NUMERIC_AND_CLAIM_AUDIT_PASS`, `JPDC_FULL_FGCS_TEXT_OVERLAP_AND_FROZEN_RESULTS_QA_PASS`. The Python CI checks the **committed human-reviewed overlap document** and existing numerics; it does not access the user's private FGCS PDF or perform automated PDF similarity checking, and must never be represented as such.

Frozen original E42 Git blob `34256ca7bff46f911cf20e8b94278fbd09175746` verified unchanged; E4.6 untouched. No science, seeds, thresholds, original p-values or outcomes modified. Prior native and original Java nonsignificant findings preserved.

## Scientific next step
Decide whether to *create and prove a genuinely new pre-dispatch scheduling control* (first-paper Algorithm1 treated explicitly as prior baseline) or design a rigorously independent causal resource-degradation experiment. Do not write a submission-ready positive-results abstract before having new data. If aiming at a distinct algorithm, write a compact spec for new observable information state, constrained objective, mathematical proposition, complexity, paired baselines and placebo/ablation tests; preregister new development data before future untouched confirmatory evidence. Alternatively extend workload/fault source models and implement YAFS, but source model transfer alone is not algorithmic novelty.

## Provenance
Source original FGCS manuscript: user's Library `FGCS-S-26-07417 (1).pdf`, scanned/current-session parsed text, no full PDF copied or published into GitHub.
GitHub original overlap QA run: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41925912142
Artifact: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/41925912142/artifacts/13369975776
