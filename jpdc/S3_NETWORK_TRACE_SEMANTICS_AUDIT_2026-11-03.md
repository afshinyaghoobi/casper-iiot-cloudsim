# S3 network trace semantics and reproducible paired diagnostic — 2026-11-03

## New verified finding and scientific correction
The generated E45 instrument `jpdc/instrument_s3_network_exposure_generated_e45.py` explicitly prints `pred[j]` as the last field in `JPDC_NETWORK_EXPOSURE`. Thus the eleventh CSV field is the model's **predicted** latency, **not the realized outcome latency**. An earlier negative-control report referred to that value as end-to-end observed latency; its documentation has been corrected. These traces do not provide a task-level replay of actual deadline success. Avoid any naive claim that task outcome latency = baseline pred[j] plus network-delay change.

## Direct cross-arm trace analysis (original Actions run 41719553340)
The original physical archives for seed indices 40,41,42,43 were analyzed across baseline/LOW/HIGH, pairing the same MISSION task index. The post-shock cohort comprises 4040 task indices per arm (1031,1004,975,1030 per seed). For LOW relative to baseline: 4025/4040 same selected node, 4025/4040 same `pred[j]`, and 340/4040 changed actual network delay on a task whose selected node matched. For HIGH relative to baseline: 4040/4040 same selected node, 4040/4040 same `pred[j]`, but **3685/4040 changed actual network delay**. This is descriptive task pairing only, not independent inferential n=4040.

For HIGH, the combination of a matching predicted value and changing realized network delay is expected from the logger's placement: `pred[j]` is printed alongside `actualNet`, but the former is not an observed outcome. The results help justify instrumenting separate observed completion time, deadline and certificate/abstention flags in a future generated E45 trace, while leaving the frozen science unchanged.

The exact negative-control test for pre-shock placement / prediction and network delays remains true: 2009 pre-shock task indices, 4018 arm-to-baseline matches. **Correction:** those 4018 comparisons do not establish equality of measured end-to-end task latency, because that variable was not recorded by the relevant logger.

## Reproduction
- New stdlib script: `jpdc/trace_network_prediction_semantics.py`, commit `22f7964667564381496497915cef506c08e020ae`.
- Local independent identical-logic execution completed against original archived physical ZIPs. Script: `python3 jpdc/trace_network_prediction_semantics.py DIRECTORY`.
- Source instrumentation: `jpdc/instrument_s3_network_exposure_generated_e45.py`; exact logger prints `nominalNetworkMs(t,nodes[j]),actualNet,netMult,pred[j]`.
- Existing original 8-artifact verbose audit was also rerun locally: **2100 assertions PASS**; existing negative control rerun: **2009 task IDs, 4018 exact pre-shock pairings PASS**.
- New committed trace semantic script has not been separately run by GitHub CI in this step; do not claim CI verification.

## Limits and next real experiment
This is new data-provenance / trace-semantics analysis, not independent simulator validation. Do not substitute `pred[j]` for observed latency or claim a network-only additive latency replay. For a meaningful trace-replay generalization experiment, define an independent simulator with explicitly instrumented actual task outcomes or generate a sidecar E45 trace of actual realized latency, cert flags and deadline. Freeze study protocol before running. The original disjoint registered holdout p=.0625 is unchanged and nonsignificant; exploratory four-seed factorial sign p=.125. E42/E4.6 unchanged.
