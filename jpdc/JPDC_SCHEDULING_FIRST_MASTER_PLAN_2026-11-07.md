# JPDC scheduling-first MASTER PLAN from six 2026 published full texts (2026-11-07)

**Paper target:** Journal of Parallel and Distributed Computing (JPDC), with FGCS as scope-aligned alternative; not a separate CCGrid conference paper. This is a practical systems scheduling contribution, not a claimed new conformal theorem.

## 1. What is the paper trying to establish?
A lightweight, online, **MISSION deadline-aware cloud–edge IIoT scheduler** that makes decisions from only causally observable data. CPU service prediction residual becomes visible at CPU finish; network delay residual at E2E delivery. Such delayed evidence should improve real routing/deadline outcomes under CPU and network disruptions. The final claim, if supported, is a reproducible performance/engineering gain with clear ablation and constraints—not a perfect future class-conditional risk bound.

A standard-source simulator is only a testbed. No fabricated real factory deployment or guaranteed miss-free scheduling. Always distinguish:
- actual MISSION deadline miss counts,
- actual latency and FCFS queue wait,
- decisions changed from contemporaneous nominal greedy,
- CPU versus network feedback timing,
- optional interval/coverage diagnostics (NOT guarantees).

## 2. What has already been checked, and what FAILED?
- Stage37 DEV seed91, 10-arm actual physical deadline trial [42356350140](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42356350140): CPU-only S2 MISSION8 misses vs FULL4 and GREEDY6, despite lower all-task mean latency. Stage37b complete task-matched forensic [42356617921](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42356617921): six NEW MISSION misses and four SAVED vs GREEDY under CPU-only; task interference matters.
- Stage38 DEV seed92, revised MISSION-only CPU/E2E [42356954652](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42356954652): S2 MISSION2 misses vs FULL2 and GREEDY6, S3 MISSION2 vs FULL5 and GREEDY5; promising on ONE DEV seed only.
- Stage39 prospectively held-out eight source seeds601–608 [42357317014](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42357317014), all source original Stage6 exact parity and 8/8 complete:
  - S2 POST MISSION pooled candidate19 vs FULL17 vs GREEDY25 over779 dependent tasks. Paired seed candidate−FULL mean+0.25 (adverse),3 worsened/8, two better/8, sign p=1.0: **preregistered S2 non-harm gate FAIL**.
  - S3 candidate14 vs FULL27 vs GREEDY28 over779 dependent tasks. Seed paired mean−1.625,4 better,0 worse,4 ties, exact two-sided p=.125: **promising but NOT significant at .05**.
  - Thus the specific mission-only candidate does NOT meet criteria for final submission-ready method. Do not tune 601–608 and call those unchanged validation seeds.
- Stage29–36 uncertainty bounds cannot be certified during hidden CPU shift. Stage24 conditional dominance needs validated external q and network bounds. Do not promote diagnostics as scheduling novelty.
- Original Python strict FCFS vs Java CloudSimPlus8.5.7 SpaceShared queue wait parity **FAILED** (9.1214ms mismatch exceeds prereg 5ms). No independent simulator/reality claims yet.

## 3. Immediate next METHODS milestone (not another arbitrary stage count)
Design a **CASPER_FULL-anchored, deadline-slack- and feedback-freshness-aware reranker** for MISSION only, rather than a PRED_GREEDY-anchored residual penalty. Keep original ranked/health/adaptive feedback semantics; apply causally delivered CPU/E2E evidence to discriminate among original eligible candidates without sending NORMAL/HIGH traffic into new patterns. Critical hypotheses:
(a) preserve CASPER_FULL's S2 CPU resilience while using delivered network feedback to improve S3; (b) avoid switch churn and stale evidence; (c) do not turn nominal slack or historical quantile into an unconditional guarantee.

**Protocol:** preregister exact score/freshness/delay/budget and new DEV seed(s) BEFORE source data; retain PRED_GREEDY, CASPER_FULL and earlier Stage37/38 ablations. Measure paired actual MISSION deadlines and all source conservation, not just empirical q coverage. Negative/empty sample results are fully retained. Never change original FGCS E42/E4.6; original E42 source Git blob SHA `34256ca7bff46f911cf20e8b94278fbd09175746`.

## 4. Evidence bar before a JPDC submission
- First demonstrate candidate performance in NEW dev source tests, then freeze and evaluate on newly independent seed cohort disjoint from all earlier development and holdout seeds. Source seeds—not dependent tasks—are the scientific paired units; report actual misses, mean differences, exact sign tests where appropriate and uncertainty.
- Implement a credible additional scheduling baseline with semantics faithfully specified for OUR problem, e.g. a queue-congestion feedback heuristic inspired by DFAQ-LB. DO NOT label it a direct DFAQ-LB/AUHS reproduction unless equivalent algorithm and source assumptions are actually implemented and validated. Include an appropriate deadline heuristic baseline and frozen CASPER_FULL.
- Provide systematic ablations CPU/E2E/no-feedback/mission-only/all-class and measure decision overhead and switching. Include adverse S2, S3, no-shock and stronger shift/workload variation. Avoid claiming all algorithms will always improve every metric.
- Address queue physics with a credible second engine/queue semantics or appropriately limited sensitivity analysis; explicitly disclose the failed CloudSimPlus queue parity. Consider externally sourced workload traces for stronger evidence, distinguish actual versus synthesized.
- Compare final technical claims with the exact existing FGCS CASPER manuscript and report overlap accurately.

## 5. How the six user's 2026 papers are used NOW
Full author/DOI metadata verified from uploaded PDFs is committed as `jpdc/references_2026_six_uploaded.bib`, and a cautious manuscript-ready Related Work section as `jpdc/RELATED_WORK_MANUSCRIPT_DRAFT_SCHEDULING_FIRST_2026-11-07.md`. Additional evidence matrix `jpdc/RELATED_WORK_2026_SIX_FULL_TEXT_COMPARISON_2026-11-07.md`.
- Closest problem/method context: Wu et al., FGCS 2026 **DFAQ-LB**; Lei et al., JPDC 2026 **AUHS**.
- Related objective/representation/context: Abdellatief **NSGA3-WS**, Farabegoli et al. **IDHGQL**, Tao/Liu co-located cluster scheduling, Ayadi et al. **PriorityDRL**.
- Six papers are sufficient to start, **no additional paper PDF download needed now**. For fair direct reimplementation later, author source code or additional protocol/method supplements might matter more than another general related-work PDF.

**Stop criterion:** no new journal-ready originality/empirical superiority assertion without direct controlled scheduling effects that pass predetermined gates and reasonable model portability. The older extreme novelty-theory requirements are relaxed; scientific integrity is not.
