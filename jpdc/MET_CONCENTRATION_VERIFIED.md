# MET online adaptation: dispatch concentration diagnostic

Run: https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/40265017907

All 3 jobs completed successfully after correcting a nonunique patch anchor in jpdc/met_concentration_patch.py. The earlier run 40264672049 failed at instrumentation assertion before scientific execution; its results are invalid.

## Measured outcome
For each of three scientific seeds (4202202600, 4202202601, 4202202602), in each of five scenarios S0-S4, the adapted online MET dispatch rule sent **20,000 of 20,000 post-change tasks to a single node**: usedNodes=1, maxNodeShare=1.0, all 15 seed-scenario combinations. These are direct dispatch counter observations, not inferred from DVR.

Because MET chooses minimum nominal service duration without network or queue awareness and node capacities are fixed within a seed, selection always goes to the same fastest-capacity node. This accounts for concentration and is consistent with the dramatic late deadline violation from the MET 3-seed pilot (run 40225852493), but the audit did not independently quantify queue times or establish causal attribution of all violations.

## Interpretation guardrails
MET here is a specifically adapted online minimum-execution-time-only mapping rule, not a reproduction of the source literature's full static heterogeneous task mapping experiment. It should not be promoted as a strong published online scheduling comparator. CASPER superiority to advanced literature baselines remains untested.

Next: implement a documented queue/network-aware comparator with deterministic decision tests, and undertake 30 paired seed evaluation only after validating fairness and decision parity.
