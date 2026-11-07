# JPDC Stage36 — exact selective-risk identifiability audit VERIFIED, 2026-11-06

## Verified engineering, no new physics or claimed scheduling gain
Prospective Stage36 assumptions and finite-counterexample contract **committed before unit CI outcomes** in `jpdc/STAGE36_SELECTIVE_TRANSFER_IDENTIFIABILITY_PREREG_2026-11-06.md`, commit `0c5b3a37c4213ae3dfad1eb852c328ffb85274b7`. New exact rational mathematical auditor `jpdc/audit_stage36_selective_transfer_limits.py` and deterministic tests `jpdc/test_stage36_selective_transfer_limits.py`; workflow `.github/workflows/jpdc-stage36-selective-transfer-theory.yml`.

Actual GitHub Actions [42339845846](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42339845846): **SUCCESS**, marker `JPDC_STAGE36_SELECTIVE_RISK_NO_FREE_LUNCH_AND_TV_CONTRACT_PASS` and `JPDC_STAGE36_FROZEN_MATH_EXHAUSTIVE_REGRESSION_PASS`; frozen original E42 blob SHA `34256ca7bff46f911cf20e8b94278fbd09175746` unchanged, original E4.6 untouched. Stage34 negative transfer, Stage32 recovery and Stage28 nonnetwork q regression unit suites all PASS. Stage36 unit logs byte-identical in repeat run. Verified **830** bounded finite integer intervals and **1125** finite exact-rational donor/target distribution/interval combinations. No new policy physics, source seed, deadline-miss measurement, or statistical inference.

## Result 1: model-specific deterministic no-free-lunch is a known identifiability limitation, NOT a new theorem
At the instant a deterministic online selector decides from causal history H (past completed MISSION and HIGH CPU-only and total nonnetwork error labels, alarm and telemetry histories), it may abstain or issue a finite [L,U]. If the conditional future target-MISSION score distribution is completely unconstrained, an environment can generate a future target error U+1 while retaining exactly the same observable history H. The issued interval then misses with conditional probability 1 in that environment. The alternate environment can assign all target errors zero. Even 10 or 1000 prior same-class matching errors is compatible with the unseen adverse future under unrestricted drift. Hence **for a deterministic finite interval issued on that H**, worst-case target conditional miscoverage over unrestricted future laws is 1. This is explicitly not a theorem about all randomized procedures, known bounded error support, distribution-free *marginal* conformal validity under exchangeability, or real scheduling deadline safety.

Unit checker establishes every enumerated interval of integer width<20 on q-domain {0,20} fails to cover both potential future outcomes, and constructs the unconditional future U+1 for any bounded interval. Do not call this a novel JPDC theorem.

## Result 2: conditional donor-to-target probability transfer (proof uses known total variation inequality)
If [L,U] is issued before the future q and one has TRUE history-conditional donor and target distributions P_H and P_M, external assumptions
`P_H(q notin[L,U] | H)<=r`
and
`TV(P_M(.|H),P_H(.|H))<=delta`
imply
`P_M(q notin[L,U] | H)<=min(1,r+delta)`.
This follows immediately from TV's supremum over events and is therefore an elementary conditional lemma, **not new mathematical novelty**. The issuer may depend on H but not future target q. Real Stage34 checks absolute median diff<=2ms and last10 MISSION labels within HIGH empirical interval; those do NOT establish a bound on the entire conditional distributions' TV, nor an externally verified donor conditional r. Thus NO Stage34 proxy interval can honestly be called `certified` from these observations.

Tight example verified with **exact Fractions**: q domain {0,20}, donor P(0)=0.9, P(20)=0.1; target P(0)=0.7,P(20)=0.3; I=[-1,1]. Donor miss r=.10, TV=.20, actual target miss=.30 =r+delta. The risk gap may be greater under unbounded future drift.

## Result 3: separate interval availability, selective miscoverage, abstention cost
Given issue indicator A_t, true future full nonnetwork q_t and issued interval I_t, define availability `sum A/N`; selective miscoverage `sum A * 1(q_t outside I_t) / sum A`, **undefined** (not zero) if no issuance; issued-miss frequency `sum A*miss/N` (may decrease merely by abstaining); and a fixed external cost `J = c_abst * sum(1-A)/N + lambda * sum A*miss/N`. All arithmetic exact and offline; this is an accounting objective, NOT a deployed new scheduling method or an algorithmic optimum. A routing fallback/abstention is not automatically safe or costless.

Example verified: issue/abstain/issue, true q {20,20,0}, issued intervals {[0,0],none,[0,0]}, availability2/3, selective miscoverage1/2, issued-miss frequency1/3, with c_abst=1/4 and lambda=2 total J=1/12+2/3=3/4. All-abstain has undefined selective miscoverage, availability0 and cost c_abst (not "100% accuracy").

## Existing literature and required novelty gate
Do not imply class-conditional conformal uncertainty, temporal adaptation or selective output is novel:
- Gibbs & Candès, JMLR 2024, *Conformal Inference for Online Prediction with Arbitrary Distribution Shifts*, https://jmlr.org/papers/v25/22-1218.html
- Bao et al., JMLR 2025, *CAP: A General Algorithm for Online Selective Conformal Prediction with FCR Control*, https://jmlr.org/beta/papers/v26/24-0452.html
- Hore et al., JRSSB 2025, *Conformal Prediction with Local Weights: Randomization Enables Robust Guarantees*, https://doi.org/10.1093/jrsssb/qkae103
- Gibbs, Cherian & Candès, 2023, *Conformal Prediction with Conditional Guarantees*, https://arxiv.org/abs/2305.12616
- *Selective Classification Under Distribution Shifts*, TMLR 2024, https://pmc.ncbi.nlm.nih.gov/articles/PMC12470254/

Stage34/35 independent HIGH-to-MISSION proxy validation remains mixed: source seed513–516 S2 PRED_GREEDY MISSION availability mean increased from 31.02% to38.82%, operational >=50% gate only1/4 and that seed had **NO CPU alarm**; CASPER_FULL mean77.04% to89.03% but3/4 seeds had NO alarm; selected proxy empirical 20/22,12/12 and47/47 are sparse and **not guarantees**. Stage29 S2 q risk coverage under CPU shock FAILED independent n4 MISSION (~63.35% seed mean), Stage31/33 alarms and recovery have large MISSION abstention. Stage23 network-only routing benefit appeared only on single development seed88 S3, while S2 degraded; Stage16 earlier old guard n8 S3 p=.375 NOT significant. CloudSimPlus vs Python queue parity FAILED registered threshold9.1214ms>5ms. No real data or genuine JPDC journal-ready novelty yet.

## Immediate research decision
**No further "guarantee" language until an assumption-backed donor/target conditional shift bound is proposed and empirically falsifiable.** The known no-free-lunch means Stage34 cannot simultaneously ensure MISSION coverage and forced interval availability under unrestricted shift. Options: (i) treat class transfer as an empirical risk/availability method with explicit failure costs, no theorem of validity; or (ii) specify a physically interpretable target-donor coupling assumption (e.g. bounded per-node CPU slowdown and bounded queue prediction discrepancy), then test whether independent actual CPU trace/model supports it. To become an original JPDC scheduling algorithm require more than known distribution-shift conformal or elementary TV lemma: a new scheduling objective/algorithm coupled to delayed CPU/E2E network evidence, credible adaptive baselines, actual paired deadline outcomes and alternative queue semantics/real trace.
