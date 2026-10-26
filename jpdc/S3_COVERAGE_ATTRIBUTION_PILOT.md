# S3 post-shock conformal coverage attribution — exploratory 3-seed audit

Workflow run: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/40336007032
All 3 of 3 jobs completed successfully. Instrumentation: jpdc/s3_attribution_patch.py, injected after regenerating E45. Frozen E4.6 is untouched.

The passive counters examine CASPER_FULL mission arrivals after CHANGE_TASK in S3_HIDDEN_NETWORK_50LOSS, where hidden network loss affects selected infrastructure nodes. Each task's ranked Top-3 candidate family is checked for any true latency above its conformal upper bound. A 'family miss' is true if any candidate violates its bound, whether or not that candidate was selected.

|Scientific seed|Post-shock mission families|Family contains affected node|Family misses|Misses involving affected node|Total candidates|Affected candidate evaluations|
|---|---:|---:|---:|---:|---:|---:|
|4202202600|1019|986|310|310|3057|1001|
|4202202601|1015|649|23|23|3045|674|
|4202202602|1056|486|367|367|3168|508|
|Total|3090|2121|700|700|9270|2183|

In this 3-seed exploratory pilot, all 700 post-shock family misses included at least one violation on a network-affected node. No family misses appeared exclusively on unaffected nodes. The observed fraction of post-shock family misses is 700/3090 = 22.65%, **not** the late-window S3 FWC failure rate; use the existing published metric to report the latter.

This strong attribution supports a mechanistic explanation for family-wise coverage degradation in S3: the hidden change in actual network latency breaks the pre-shock nominal network prediction and the family-wise intervals miss at network-affected candidate nodes. This is not proof of unique causality, and the counters do not tell us the exact error decomposition or how soon eta adapts. Additional independent seeds are needed.

Do not describe this as a corrected 99% conformal guarantee. Do not retroactively tune S3 parameters to match the benchmark.
