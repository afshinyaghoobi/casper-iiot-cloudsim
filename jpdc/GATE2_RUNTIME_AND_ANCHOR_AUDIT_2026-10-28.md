# JPDC Gate 2 — independent runtime and patch-anchor audit (2026-10-28)

## Executed checks
- In the available local environment: `javac /mnt/data/casper_gate2/java_test/RiskGreedyScoringTest.java` followed by `java -cp /mnt/data/casper_gate2/java_test RiskGreedyScoringTest` returned **`RISK_GREEDY_JAVA_SCORING_PASS 6 checks`**.
- Fetched research-branch frozen E4.2 Java campaign and the risk-greedy E45 patch via the GitHub connector.
- Static anchor audit: exact policy enum anchor occurs once; original non-CP dispatch branch anchor occurs once; eight original policies are present; patch references shared `fixedSigma` and only the generated `e45/E45Campaign.java`.
- Source blob of original Java campaign remains `34256ca7bff46f911cf20e8b94278fbd09175746`.
- Confirmed the original published S3 aggregation archive `github-actions-artifact-12739924675.zip` is available locally and includes `s3_all30_by_seed.csv` and `s3_all30_summary.json`. This archive is unrelated to the new risk-greedy pilot.

## Unresolved execution boundary
- Java compiler is installed, but `mvn` is not available in the current local runtime.
- `git ls-remote https://github.com/afshinyaghoobi/casper-iiot-cloudsim.git HEAD` failed due to DNS resolution of github.com.
- Connected GitHub tools do not expose workflow-dispatch or listing push-triggered workflow runs. Commit workflow lookup returned no *matching reported* runs; that is **not evidence that Actions did not run**.
- Consequently: no complete CloudSim pilot, no 5-scenario CSV, no independent result of risk-greedy versus CASPER is verified in this session.

## Action that unlocks data
The branch workflow `.github/workflows/jpdc-risk-greedy-pilot.yml` supports `workflow_dispatch` and includes before/after science-parity checks and failure diagnostics. It can be launched at:
`https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/workflows/jpdc-risk-greedy-pilot.yml`
using branch `jpdc-seed0-repro-20261024`. When a run ID becomes available, inspect run status, preserved `jpdc-risk-greedy-seed0-pilot` artifact, and verified CSV outcomes.

No other validator or pseudo-simulation result should be substituted for that empirical gate. Frozen E4.6 was not changed.
