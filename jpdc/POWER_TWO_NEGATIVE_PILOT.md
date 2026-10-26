# Power-of-two predicted-latency online dispatch: 3-seed pilot

Action run: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/40275251519
All 3 seed jobs succeeded; 45 rows per seed with 9 policies and 5 scenarios. The independent experiment branch does not modify E4.6.

## Rule
Sample two distinct nodes deterministically per task (scientific seed and task index), then choose the lower predicted network-plus-queue-plus-service latency among them. This is a *heterogeneous online dispatch adaptation* of power-of-two sampling, not a reproduction of a complete published Cloud-Edge scheduler. It uses the same observable prediction vector as greedy but queries only two random candidates; computational cost benefit is not established by the current code, which calculates the full prediction vector before sampling.

## Pilot: mean late DVR (proportions), three seeds
|Scenario|CASPER_FULL|PRED_GREEDY|POWER_OF_TWO_PREDICTED|
|---|---:|---:|---:|
|S0|0.001333|0.001333|0.166667|
|S1|0.018667|0.017333|0.248000|
|S2|0.026667|0.036000|0.212000|
|S3|0.024000|0.022667|0.226667|
|S4|0.060000|0.062667|0.376000|

## Integrity and interpretation
This is a negative exploratory finding. Sampling only two of 21 heterogeneous nodes can omit suitable resources, and the present code has no measured compute overhead advantage because the full predicted-latency array is built first. Do not call this a competitive published scheduling baseline or a demonstration of superior CASPER scalability. The 3-seed means do not support statistical generalization.

Next: prioritize independent implementation fidelity and competitive online comparator rather than extending weak baselines to 30 seeds.
