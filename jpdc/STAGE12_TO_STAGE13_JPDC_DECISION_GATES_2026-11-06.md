# JPDC continuation — Stage 12→13 research decision gate (2026-11-06)

## Non-negotiable scientific framing
Primary target: a standalone, defensible JPDC contribution, NOT a pre-decided positive result. CCGrid conference split is out of scope. Original FGCS CASPER/E42, E4.6 and all prior negative results remain unchanged. Stage 11 and Stage 12 seed83 are *development only*, never clean holdout.

## Gate A — Stage 12 completed evidence
Accept only a successful GitHub Actions run with attached, reproducible original-source logs and node episodes. Require byte-identical rerun and exact legacy policy metric parity to Stage 6; all 12,000 E2E reports per arm; observer-rule re-computation matches every accepted-event alarm; no affected-source truth reaches controller. Examine all six affected S3 nodes in both preregistered policies, including absent and quarantined episodes. If workflow status cannot be verified, label unverified. Do not convert descriptive seed83 counts into statistical significance.

## Gate B — observational scientific finding
Report separately:
(1) node exposure through dispatch,
(2) E2E coverage,
(3) valid pre/post comparable histories at the feedback delivery instant,
(4) alarms supported by stated L and epsilon,
(5) elapsed times from first affected dispatch and first delivered affected report.
Do not claim known physical shock onset, source-consistent independent fault detection, practical network deployment, or sensitivity/false alarm guarantees. Alternative detector assumptions and delayed/out-of-order feedback must be treated explicitly.

## Gate C — algorithmic contribution decision, before confirmatory validation
After diagnosing Gate B, define a distinct scheduling decision mechanism with causal state updates only from completed E2E observations. Specify cost of observability/probing, stale information, unavailable nodes, competing deadline risk, unknown-network uncertainty, and fallback on empty history. Compare against original CASPER_FULL and nonconformal network residual/probe policies, plus relevant published baselines identified through literature review. Pre-register metrics and seeds before testing; development/confirmation cohorts disjoint. Preserve failure cases and negative comparisons.

## Gate D — independent, credible scheduling evidence
No JPDC performance claim until full scheduling (not merely shadow) is implemented and evaluated on paired source-generated workloads, with repeated independent scientific seeds and uncertainty intervals. Include miss-rate (primary), tail latency, mean latency, probing expenditure, node coverage, and false alarm/decision effects. Clearly state when an improvement is negligible or statistically inconclusive. Stress varying shock locations, severity, arrival rate, delayed or missing feedback, task heterogeneity and switching/probing costs. No tuning on confirmatory holdout.

## Gate E — physical model validity
The current 21-node Python strict-FCFS simulator is not equivalent to CloudSimPlus Java SpaceShared. The prior native vs Java queue parity failed (9.1214ms versus 5ms gate), and Stage 11 uses a stylized CPU-then-network duration that doubles RTT and transfer time in S3. Fix incompatible queue assumptions or explicitly present separate simulation domains rather than asserting parity. External traces or independent simulator verification desirable; never claim nonexistent YAFS validation.

## Publication decision
Proceed to writing JPDC only if a separately evidenced, defensible novel algorithm/insight survives Gates C–E. If policy gains are absent, consider an honest diagnostic/methodology paper in another suitable venue rather than forcing JPDC claims. No fabricated p-values, novelty, deadlines, completion status or acceptance probabilities.
