# Online MET-adapted negative pilot: transparent evidence

## Scope and provenance
GitHub Actions: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/40225852493
Three successful jobs, 45 rows/job (9 policies x 5 scenarios), 135 total. All three jobs passed the small deterministic MET selection tests. Patch: jpdc/online_met_patch.py. The unchanged E4.6 release is the reference.

## Defining rule
For a task arriving online, ONLINE_MET_ADAPTED assigns it to the eligible node with the minimum *nominal service time*, ignoring network transfer delay and queue backlog. This is an online adaptation of minimum-execution-time selection, NOT a faithful reproduction of a static heterogeneous-computing batch MET benchmark and NOT HEFT. The specific model and trace conditions matter.

## Three-seed descriptive average late deadline violation rates
|Scenario|CASPER_FULL|PRED_GREEDY|ONLINE_MET_ADAPTED|
|---|---:|---:|---:|
|S0|0.001333|0.001333|0.261333|
|S1|0.018667|0.017333|1.000000|
|S2|0.026667|0.036000|0.536000|
|S3|0.024000|0.022667|0.445333|
|S4|0.060000|0.062667|1.000000|

## Interpretation
This adapted comparator is very weak on these synthetic tasks, with 100% late DVR in S1 and S4. This does not establish that CASPER exceeds strong published online schedulers. A hypothesis is that the rule ignores backlog and congests fast compute resources; this mechanism has not yet been verified by node-assignment traces. Do not attribute this failure to HEFT.

## Next diagnostic / comparator gate
Measure node-level dispatch distribution and backlog for MET on independent seed(s) without modifying original policy logic. Then seek independent online scheduler implementation with clear provenance and controlled information budget. Do not cherry-pick only weaker comparator results for JPDC publication. Retain negative pilots in appendix or methodological notes.
