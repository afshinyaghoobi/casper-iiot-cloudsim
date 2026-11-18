# SIMPAT v1.3 milestone: verified exploratory paired-case metric discordance — 2026-11-18

**Author-approved unchanged title:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation
**Target journal:** Simulation Modelling Practice and Theory (Elsevier).
**Current actual working manuscript:** [v1.3 with qualified exploratory subsection 5.6](SIMPAT_MANUSCRIPT_V13_EXPLORATORY_METRIC_CHECK_2026-11-18.md).

## New meaningful, though LIMITED empirical posthoc check
- Using the archived previously audited **24-row A2 primary CSV**, formed **12** matched pairs keeping arrival family, deterministic jitter variant and event-gap fixed while comparing one versus two VM PEs.
- **Max absolute native-vs-FIFO wait-model discrepancy decreased in 12/12 pairs**, yet synthetic deadline classification disagreement at submit+25ms **increased in 8**, decreased in1 and was unchanged in3; at +50ms it increased5/decreased4/tied3. Example BURSTY_S0_1US 157.018→25.005ms max absolute wait-model discrepancy, but +25ms model disagreement increases **1/12→5/12**.
- Matched 1µs→5ms event gap comparison: max absolute wait-model difference up10/down2/tied0.
- This is an **observed within-fixture counterexample** to treating one maximum absolute wait-error statistic as a monotone surrogate for thresholded *completion-model disagreement*. It is NOT a new scheduling algorithm, new external IoT data, a CloudSimPlus bug, a PE-caused real delay, a population estimate, a causal isolation, or a preregistered matched-pair prediction. This analysis was designed **AFTER** seeing the fixed A2 results; main original A2 design existed before but new paired analysis did not.
- Transparent source and qualification [exploratory matched-pair report](SIMPAT_A2_POSTHOC_MATCHED_METRIC_DISCORDANCE_2026-11-18.md). [Committed auditor](audit_simpat_a2_matched_metric_discordance.py) and **real successful CI run44348268134** verify counts; **real successful v1.3 combined CI run44348702818** verifies exact locked title, existing 12 citations/24-cell source, publication approval still pending and matched metric calculations. No new native Java experiments executed.

## Decision
- This increment addresses an actionable **metric-selection risk**, not the larger editorial originality concern. We cannot claim full **SIMPAT acceptance readiness**, since a non-tautological significant **generalizable method** or independent IoT applicability remains unproven. Submission gate remains **HOLD** pending author approval and scientific judgement, not simply formatting.
- A1/A2/A3 original simulations and no change of numbers; posthoc execution differences250/288 and hindsight max154ms; A3 origin equal288/288. Earlier strict30k Java/Python parity FAIL and Stage65 safety FAIL unchanged. Future Program B independently reserved/not started.
- Next science step, *only if needed*: mine original per-job **signed completion-time differences and threshold margins** to see whether there is a concrete, falsifiable interpretation beyond a counterexample; preregister and independently audit if claiming predictive generality. Do NOT infer this from case-level max wait aggregate. Otherwise complete author-verified editorial paperwork and reconsider article scope/venue.
