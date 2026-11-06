# Stage 12 — preregistered retrospective per-node diagnostic trace (2026-11-06)

## Purpose and scope
Explain the frozen Stage11 developmental S3 seed83 **6/6 delivered affected-node observations but 1/6 alarm** in CASPER_FULL and NEW_NETWORK_RESIDUAL_PROBE. This is an **exploratory post-outcome audit**, not an untouched holdout and not a new scheduler or performance claim. Stage11 prior evidence, original Stage6 policies, original E42 blob, E4.6, and numerical metrics are frozen.

## Fixed protocol
Use exactly S3_HIDDEN_NETWORK_50LOSS, seed83, 80,000 original native physical calibration records, 12,000 tasks, and the two policies CASPER_FULL and NEW_NETWORK_RESIDUAL_PROBE. No parameter tuning. Use Stage11 observer (L=.0001/ms, epsilon=0, noncausal older-generated reports quarantined). Instrument only E2E **post-delivery** decisions; record task index solely in offline trace payload, never pass it to observer. Keep all original outcomes exactly equal to the pre-instrumented Stage11/Stage6 output fields.

## Trace and offline outcomes
For all 21 nodes capture every E2E report with: node, task index, measurement/CPU finish time, delivery time, normalized excess z, accepted-history count before event, previous maximum measurement time, detector event kind, epoch, and count of prior accepted **pre-shock task** observations. Independently classify source-affected nodes **after simulation** using the frozen source mask. For each of six affected nodes report number of pre/postshock E2E reports, pre/post accepted, post quarantined, pre-to-post comparable pair available at delivery, alarms, and exact timing. Distinguish missing prehistory, quarantine, compatible under drift (if applicable), and alarms. Do not infer a causal onset timestamp from task index. Preserve raw node episodes and compact summaries as CI artifacts.

## Controls / gate
Assert new trace has precisely 12,000 delivered records per policy, no future information entered policy or detector, observer response names and matched summary counts agree with Stage11, and source policy results exactly match original Stage6. Frozen E42 git blob 34256ca7bff46f911cf20e8b94278fbd09175746. Run the exact diagnostic twice and compare JSON byte-for-byte. A failing gate means Stage12 findings are unverified. Report negative observations without seed selection or significance tests.