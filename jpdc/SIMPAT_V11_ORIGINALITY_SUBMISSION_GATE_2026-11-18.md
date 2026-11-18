# SIMPAT scientific originality gate — v1.1 (2026-11-18)

**USER LOCKED exact manuscript title:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation
**Target only:** *Simulation Modelling Practice and Theory* (Elsevier).
**Current manuscript:** [v1.1, with corrected direct-source study](SIMPAT_MANUSCRIPT_V11_QUEUE_PRIOR_ART_2026-11-18.md).
**Static GitHub CI:** [successful run 44336435018](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44336435018), source checker [v1.1](check_simpat_v11_publication_packet.py), verifies user-approved title, **12 numbered references** (including Vondra/Šedivý2017), 24-case source table and SVG, 86/288 and107/288 artificial deadline differences, original max246ms, author approval still missing. This is NOT independent journal-editor evaluation.

## A decisive novelty boundary from newly accessed full text

[2019 Zakarya/Gillam full accessible manuscript](https://www.academia.edu/104290064/Modelling_resource_heterogeneities_in_cloud_simulations_and_quantifying_their_accuracy), especially §4.1 (*Simulation Models vs Analytical Models*) and §5/6, directly covers combining analytical/statistical accuracy comparisons and real workload/testbed evidence with a modified CloudSim. The previous **abstract-only** limitation is superseded for this paper; published DOI10.1016/j.simpat.2019.02.003. Also found **Vondra and Šedivý**, *Cloud autoscaling simulation based on queueing network model*, SIMPAT70:83–100 (2017), DOI10.1016/j.simpat.2016.10.005, *distinct from Vondra/Šedivý/Castro Wiley 2017*. The Vondra SIMPAT source was read to abstract/available publisher synopsis only, NOT full text. Both were added to [direct prior-art provenance report](SIMPAT_DIRECT_ZAKARYA_AND_VONDRA_PRIOR_ART_2026-11-18.md) and manuscript v1.1. Earlier [Mechalikh 2025 author-posted full paper](SIMPAT_MECHALIKH_FULLTEXT_AND_CALHEIROS_BIB_AUDIT_2026-11-18.md) already compared 24 simulator **tools** (not our 24 SpaceShared conditions).

**Editorial implication:** Our real contribution is an accurate, repeatable **version-specific simulator-construct diagnostic** with native Java logs and explicit *different* FIFO reference, not a generic new CloudSim verification methodology, physical validation, new queue algorithm, or discovered library defect. On official [SIMPAT publisher scope](https://shop.elsevier.com/journals/simulation-modelling-practice-and-theory/1569-190X), submitted articles must make **significant contributions** and applied-model studies transparently discuss model derivation/implementation/validation, including real-data validation where appropriate. **Significance and overall acceptance readiness remain a genuine unresolved scientific gate.** Do not force submission on a Dec20 internal planning date.

## Do not claim
- Original FGCS CASPER manuscript is published/accepted; own previous submitted draft distinct from this paper.
- Native reported waiting is necessarily physical CPU waiting; WAIT/EXEC membership is not start callback.
- “24 cases ×12 tasks” are independent sampled real IoT populations or errors against an external physical ground truth.
- 250/288 after-completion native-service mismatch implies standalone cause, or oracle154ms proves native scheduler bug.
- A3 288 identical datacenter-arrival and submit clock origin generalizes beyond the tested 1VM CPU-only inputs.
- Previous failed 30k Java-Python FCFS parity or Stage65 safety succeeded. Both remain FAIL.
- AI manuscript preparation declaration or funding and author positions approved without signed human confirmations.

## Specific next tasks, bounded
1. Inspect legitimate full 2017 Vondra Wiley and/or SIMPAT 2017 article if accessible; keep a source-access tier for each.
2. Perform critical author-oriented editorial assessment of whether a small 1VM synthetic version-locked diagnosis is a substantial *modeling insight*. If not, prefer candid journal-risk disclosure over arbitrary experiment expansion.
3. Final venue-specific style, source pinning/archival and figure legibility at column width; author approved title page / correspondence / conflicts / CRediT / GenAI statement / FGCS overlap. Avoid publishing or submitting before approval.
4. Program B reserved/not started; no new native simulations absent a critical research question.
