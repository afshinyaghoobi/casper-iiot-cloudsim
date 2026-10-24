# JPDC CASPER — Network severity generalization protocol (exploratory)

Status: **PILOT RUN REQUESTED, NOT YET SCIENTIFICALLY VALIDATED**.
Parent: E4.6 frozen release `v1.0.0-casper-iiot-e46`.
Pilot: `jpdc-network-generalization.yml`; 3 scientific seeds and 3 levels of retained bandwidth.

## Scope
This is a **network shock severity robustness test**, not topological, external-trace, or workload generalization. Do not present it as evidence of generalization to independent testbeds.

For S3 and S4 only, scale actual network delay and counterfactual actual network latency consistently to retained bandwidth fractions 0.25, 0.50, and 0.75. Other scenarios and calibration remain unchanged. No selection of the best parameter based on pilot outcomes.

## Prespecified verification gates
1. All 9 jobs (3 retention levels × 3 seeds) complete and produce 40 distinct scenario-policy rows each.
2. K and eta configuration and all frozen source modules stay unchanged.
3. The 50%-retained-bandwidth condition agrees with original E4.6 (all scientific fields, allowing hardware-sensitive mapper timing to differ) at each matched seed, scenario and policy.
4. S0, S1 and S2 must remain unaffected by the severity patch (scientific metrics equal to frozen E4.6).
5. Keep all results including failures and S3 undercoverage; do not replace or overwrite E4.6.

## Exploratory outcomes
Primary descriptive endpoints: `late_fwc` and `late_dvr`; secondary: `late_air`, `p99_late_latency_ms`, `late_eta`. Compare differences *paired by scientific seed* within S3 and S4. Report paired uncertainty intervals and keep multiplicity explicit. Three seeds are a smoke test, not sufficient for statistical efficacy claims.

## Critical limitations
- S3 originally violates the 0.99 late family-wise coverage target. A conditional, empirical comparison does not repair the guarantee.
- The network multiplier modifies modeled communication delay, not actual network traffic in CloudSim; do not claim packet-level/network-stack validation.
- This protocol is **not a substitute** for externally sourced realistic workloads, independent topology distributions, or comparisons against strong published scheduling algorithms.
- Only after successful pilot verification consider a 30-seed confirmatory expansion. Treat all new versions as separate exploratory branches/results.
