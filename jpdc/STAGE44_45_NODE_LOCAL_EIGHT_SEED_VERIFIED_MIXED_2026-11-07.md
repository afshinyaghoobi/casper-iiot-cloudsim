# JPDC Stage44–45 — NODE-LOCAL causal hotspot detector, eight-source-seed independent result VERIFIED MIXED (2026-11-07)

## Original hypothesis, code, provenance
User specifically asks for practical **incremental JPDC scheduling contribution**, not extreme theorem novelty; user supplied 6 accepted 2026 FGCS/JPDC full-text PDFs already in `jpdc/references_2026_six_uploaded.bib`. Stage43 GLOBAL selector on 8 independent source seeds801–808 S3 network-mode>=5% in only4/8 vs prereg6/8, S3 gated19 vs FULL22 missed MISSION deadlines, sign p=.5. This motivated per-node evidence rather than global pooling, **not posthoc numerical threshold tuning on 801–808**.

Stage44 prospective prereg before dev results `jpdc/STAGE44_NODE_LOCAL_REGIME_PREREG_2026-11-07.md` commit `49d357e2bb245ba43e5ee3474b9ddf238b7f26c5`. New `jpdc/causal_node_regime_selector_stage44.py`, `jpdc/test_causal_node_regime_stage44.py`, isolated `jpdc/independent_physical_node_local_regime_stage44.py`, and runner. 21 node-specific CPU service ratio only on **CPU finish**, 21 node-specific network ratio only after **E2E delivery**. Per-node badness actual/nominal>=1.5; first12 reports fixed baseline and last12 current, flag if >=5/12 current bad and current minus baseline>=.25. At issue choose 6 lowest PRESENT predicted latency nodes, node-index ties, network mode if >=1 flagged network and none CPU in these6; otherwise original FULL. NORMAL/HIGH always original CASPER_FULL; MISSION NETWORK routes with original Stage38 E2E-only/CPU+E2E penalty and nominal2ms budget. Original FULL MISSION fallback on missing/ambiguous. No hidden affected node set, shock task-index threshold or scenario label enters algorithm, no hard deadline/90% uncertainty certification. Original FGCS E42 git blob SHA `34256ca7bff46f911cf20e8b94278fbd09175746`, E4.6 unchanged. Only strict native Python FCFS source model, NOT Java CloudSimPlus queue equivalence.

Stage44 [real DEV CI 42430050383](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42430050383) SUCCESS seeds97–98, both scenarios, 6 policies×12k tasks, 288k DEPENDENT task-policy records, n2 DEVELOPMENT scientific source seeds. Original Stage6, frozen Stage38 and global Stage42 JSON exact parity and repeated byte identical, node-hotspot causality adversarial unit. S2 new NodeLocal vs FULL seed97 5 vs5 /94 MISSION, seed98 1 vs1 /97; S3 seed97 0 vs0 /94, seed98 3 vs6 /97; network-mode source issue counts S2 zero, S3 1865 and1961. This motivated prospective independent cohort, not an independent conclusion.

## Stage45 INDEPENDENT fixed eight-source cohort
Preregistered in `jpdc/STAGE45_EIGHT_SEED_NODE_LOCAL_HOLDOUT_PREREG_2026-11-07.md` BEFORE outcomes commit `f56a9d60944841e019c0b88323567f6377f3dc37`. Exactly 8 new independent source scientific seeds **901–908**, original Stage3 80k calibration per seed, S2 CPU40-loss and S3 NETWORK50-loss, six frozen policy arms (PRED_GREEDY, CASPER_FULL, global Stage42 gated combined, old Stage38 ungated combined, new Stage44 node-local E2E and node-local combined), 12k tasks each => **1,152,000 DEPENDENT task-policy observations, independent n8 source seeds**. Exact Stage6, Stage38 and Stage42 policy JSON parity each source, no changed original E42/physics, causal node observations.

Initial [GitHub Actions run 42430334460](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42430334460): all **8/8 scientific source seed jobs SUCCESS**, preserved eight individual uploaded artifacts, BUT aggregate audit **FAILED** before stats because one metadata key name mismatched: runner wrote `dependent_task_policy_observations`, auditor read `task_policy_dependent_observations`. Scientific source policy, fixed seeds, source outputs and thresholds NOT changed. Only one audit key fixed in commit `b2a77d1443e4d93d6b8a6dc7aae721f041190580`; recovery protocol `jpdc/STAGE45_AUDIT_ONLY_RECOVERY_PROTOCOL_2026-11-07.md` preserves this exact provenance. [Recovery CI run 42430594069](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42430594069) **SUCCESS**: downloaded ALL EIGHT original source artifacts by fixed original run-id42430334460, no physical reruns, and corrected all-or-nothing audit PASS `JPDC_STAGE45_EIGHT_ORIGINAL_SOURCE_ARTIFACTS_RECOVERED_AUDIT_SUCCESS`. This is truthful software repair, not additional science/independent data.

## Actual POST-SHOCK MISSION misses, eight source seeds, no cherry-picking

| Source seed | POST MISSION tasks | S2 original CASPER_FULL | S2 NodeLocal E2E and Combined | S3 original CASPER_FULL | S3 NodeLocal E2E and Combined | S3 NodeLocal NETWORK dispatches/12k |
|---:|---:|---:|---:|---:|---:|---:|
|901|95|4|4|7|**3**|1942|
|902|94|6|6|4|4|47|
|903|111|0|0|15|**18 (HARMED +3)**|1944|
|904|120|2|2|4|**3**|1685|
|905|90|0|0|0|0|1953|
|906|118|0|0|0|0|1685|
|907|115|0|0|0|0|1931|
|908|118|1|1|0|0|0|
|**Pooled DEPENDENT counts only**|**861**|**13**|**13**|**30**|**28**|**11287 network-mode source dispatches**|

Both Stage44 NodeLocal E2E-only and NodeLocal CPU+E2E have identical POST MISSION miss counts in all8 S2 and S3 source seeds. No evidence CPU extra penalty contributes unique deadline improvement for this cohort.

S2 full source POST MISSION: GREEDY25, FULL13, Stage42 global gated13, Stage38 ungated19, Stage44 node-local13. All8 seed source Stage44 vs FULL tied (exact sign p undefined). Node-local NETWORK policy false activation S2 **0/12k all eight seeds**, prereg specificity proxy PASS. Source FULL S2 miss performance better than GREEDY25, but preserving FULL is not a new improvement.

S3: GREEDY31, FULL30, Stage42 global gated29, Stage38 ungated29, Stage44 NodeLocal E2E/combined28. Paired Stage44−FULL source seed differences **[-4,0,+3,-1,0,0,0,0]** (negative better). Mean −0.25 MISSION misses per independent seed (2/8 better, 1/8 worse, 5 ties), EXACT two-sided sign p=**1.0**. No statistically supported improvement, and a meaningful adverse seed903. Stage44 vs global average −0.125 miss per seed, negligible and not an independently demonstrated superior scheduler. Do NOT claim "significant improvement"; don't treat dependent 861 MISSION tasks as iid science units.

## Detector gate versus old Stage43
For S3 Stage44 source NETWORK mode dispatch counts by seed [1942,47,1944,1685,1953,1685,1931,0]. Preregistered >=5% of12k whole-source NETWORK issues (>=600) in >=6/8 independent seeds **PASS EXACT 6/8**. The previous global detector had passed its equivalent gate only4/8 in Stage43 separate seed cohort, **not a same-seed paired detector comparison**; Stage45 also computed frozen global Stage42 comparator on SAME seeds. Stage44 network regime positive 6 seeds but only 3 nonzero paired miss changes: improved seed901/904, harmed seed903. Detection coverage clearly improved in this fixed cohort, yet actual deadline efficacy remains mixed.

All Stage45 combined/E2E prereg gates:
- S2 no mean harm vs FULL PASS, S2 <=2 harmed PASS, S2 false-network-mode<=1% each PASS
- S3 strict mean lower misses than FULL PASS (28 vs30), S3 <=2 harmed PASS (1 harmed)
- S3 detector exposure>=5% in>=6 seeds PASS (6/8)
- S2 exact p<.05 NOT APPLICABLE (all tied)
- S3 exact p<.05 **FAIL (p1.0)**.
Thus operational detector and descriptive mean gates passed but **scientific efficacy claim NOT validated**. Don't promote Stage44 to a strong JPDC superior-scheduler conclusion or tune on these now-examined holdout seeds901–908 and call unchanged validation.

## Publication and method decision
Strong engineering unit causality and native reproducibility are real. Node-local detection solves an observed operational exposure limitation better than naive global pooling in this sample, but routing decision quality can still harm deadlines (+3 seed903). Next meaningful study: **outcome-driven causal task-level forensic** on heldout stage45 source artifacts (only diagnostic, NOT future holdout), inspect where network-mode routing caused extra MISSION misses and queue interference, then design a new policy on new DEV source seeds, with a new independent untouched cohort. Also build a credible published baseline adaptation and cross-model/trace validation; original Python FCFS vs Java CloudSimPlus8.5.7 SpaceShared queue fidelity preregistered FAIL 9.1214ms>5ms remains. User has already supplied six relevant FGCS/JPDC full-text 2026 articles, no new PDF needed yet.
