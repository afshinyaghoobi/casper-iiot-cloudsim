# SIMPAT A2 — Exploratory matched-configuration metric discordance (2026-11-18)

**Exact user-approved title remains:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation.

**Status:** Genuine new **POSTHOC DESCRIPTIVE analysis** of the original A2 verified static table; **NO new Java simulation**, no new subject sample, no statistical inference and no preregistered research hypothesis. Original A2 protocol fixed 2 arrival families ×3 timing variants ×2 event gaps ×2 PE capacities = 24 synthetic configurations ×12 jobs =288. All measurements are *differences of two defined models*, not actual IoT completion errors. Original [A2 primary source table](manuscript_a2_primary_24_cases_2026-11-18.csv) is tied to original audited Java CI [run44215741883](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44215741883) and [primary A2 audit](JPDC_A2_BOUNDED_GENERALIZATION_VERIFIED_2026-11-17.md).

## Reproducible computation and outcome
[Auditor source](audit_simpat_a2_matched_metric_discordance.py); [actual successful GitHub CI run44348268134](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44348268134). Comparator holds family, deterministic variant and event gap fixed, switches from **1PE to2PE**, thus 12 matched **configuration pairs**. For each pair, calculate sign of change in (i) maximum per-case absolute native-vs-FIFO wait discrepancy, (ii) number of native-vs-FIFO classifications that disagree for fixed synthetic submit+25ms, and (iii) count for submit+50ms.

| Primary A2 construct | Changes when 1PE→2PE across 12 matched configuration pairs |
|---|---:|
| Within-case max absolute wait disagreement | **decreases 12 / increases 0 / unchanged 0** |
| Number of classification disagreements at synthetic +25ms | **increases 8 / decreases 1 / unchanged 3** |
| Number of classification disagreements at synthetic +50ms | **increases 5 / decreases 4 / unchanged 3** |

**Concrete witnessed counterexample:** in BURSTY_S0_1US (12 jobs), max absolute wait disagreement drops **157.018ms (1PE)→25.005ms (2PE)**, while synthetic +25ms classification disagreement count rises **1/12→5/12**. Therefore the *ordering of two configurations by maximum waiting difference* does not necessarily agree with their ordering by the *count of completion-deadline classification disagreements*. This is true **only for defined fixed test cases**; not a claim of a causal effect of more CPU in physical/real IoT systems.

A separate matched **min event gap 1μs→5ms** comparison holds family, variant, PE fixed (12 pairs) and finds maximum absolute wait disagreement increases in **10** pairs, decreases in **2**, ties **0**. This rejects a naive unqualified monotonicity statement even inside this tiny fixed design; it does not establish a generic CloudSimPlus runtime theorem or physical event-resolution performance effect.

## Scientific interpretation and limits
1. This is **not** evidence that adding VM capacity causes worse performance: the diagnostic counts *model disagreement* at synthetic deadlines, not actual deadline misses. Moreover changing PE capacity changes both native system behavior and analytical FIFO calculations, and there is no external truth. The gap metric is a maximum wait-error magnitude; the classification metric evaluates crossing a *completion-time boundary* and is sensitive to threshold, completion clock and direction. They need not co-vary.
2. The finding adds a **measurement-construct caution** beyond the generic statement “two non-equivalent models differ”: a **single scalar maximum waiting difference is not sufficient to order synthetic deadline classification disagreements** under matched configurations. It is an observed counterexample to a *possible* monotonic surrogate assumption; we have not shown anyone in the prior literature makes that assumption, nor a universally novel theoretical result.
3. Both metrics were chosen in original A2 preregistration, but **this particular matched-pair hypothesis and posthoc comparison were NOT preregistered**. Must be labeled exploratory and replicated with a future independent dataset before predictive/general claims.
4. The 12 pairs are related deterministic simulation fixtures, not independent samples. No significance tests, confidence intervals or extrapolated populations; no causal mechanism attribution.
5. The **largest case error** cannot by itself predict classification disagreement: a small number of jobs near fixed thresholds can disagree despite lower worst-case wait gap, while larger wait gaps may occur far from thresholds. Distinguishing the signed *completion-time* difference and distance to threshold for the affected jobs requires original per-job data, not a case-level max-wait scalar alone. No unsupported empirical decomposition was performed.
6. This is a small **additional defensible observation**, not evidence that SIMPAT's high journal novelty bar is satisfied. [Existing editorial gate](SIMPAT_V12_SCIENTIFIC_GO_NOGO_CHECKPOINT_2026-11-18.md) remains **HOLD** for a significant nontrivial scientific contribution and full author approval. **Do not fabricate novel algorithm or claim runtime bug.**

## Data provenance and integrity
CI code loads the stable 24-row original data file, enforces unique case keys and correct group balancing, asserts independently the observed counts and worst-case values, then logs directions and a concrete example. The CI result is a static **source-backed derived analysis**, not new execution or external empirical validation. Original 30k strict Java↔Python parity FAIL and Stage65 safety FAIL remain unchanged. Program B remains reserved, not started.

**Decision for manuscript:** one narrow optional subsection or discussion sentence may report this finding explicitly **exploratory**, with no p-values and no causal/novelty inflation. If authors wish to advance this as the *main* paper contribution, first define and test a falsifiable theoretical or data-backed explanation rather than merely counting threshold crossings.
