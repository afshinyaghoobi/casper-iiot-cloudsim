# SIMPAT Program A — verified source-level observability gap and minimal prospective decision protocol

**2026-11-18; PRE-EXPERIMENT DESIGN ONLY.**
**Author-approved exact title remains:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation.
**Primary venue remains:** Simulation Modelling Practice and Theory. *Original A1/A2/A3 observations and negative 30k parity/Stage65 safety gates are frozen.*

## 1. Exact source inspection (completed, no speculation)

Actual tracked [NativeA2BoundedGeneralization.java](../src/main/java/org/casperiiot/jpdc/NativeA2BoundedGeneralization.java), originally executed under [A2 CI run44215741883](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44215741883), contains:
- A passive override of `cloudletSubmitInternal(CloudletExecution,double)` wrapping **exactly one** `super.cloudletSubmitInternal(...)` call;
- submission `BEFORE`/`AFTER` snapshots of `getCloudletExecList()` and `getCloudletWaitingList()`, and scheduler-submit clock;
- finished-job callback with `sim.clock()`, Cloudlet native `getStartWaitTime()`, `getTotalExecutionTime()`, requested `SERVICE[index]`;
- **NO override or timestamped event trace of `updateProcessing`**, **NO waiting-list-promotion-method trace**, and **NO direct per-job Cloudlet on-start listener**. A2 cannot by itself isolate the causal substep that moved jobs out of WAIT or determine whether the observed execution-list membership always corresponds to CPU work beginning at that exact clock.

The earlier [exact publisher 8.5.7 source-method audit](NATIVE_V857_SOURCE_MECHANISM_AUDIT_VERIFIED_2026-11-17.md) verified Java source JAR SHA256 `8d3efcacfc661b2f1e018e279761fc4ae1e5584a770b2022d20930568688966c`. It locates direct submit admission `CloudletSchedulerAbstract.cloudletSubmitInternal` near lines247–259, updateProcessing around477–495, and separate waiting promotion `moveNextCloudletsFromWaitingToExecList` near910–924. Those are **static source paths**, not dynamic branch-coverage confirmation.

**Scientific conclusion:** The present v1.5 empirical result distinguishes two constructed timing models and threshold sensitivity, but does not isolate whether *deferred waiting promotion*, *event cadence*, or *native-reported service duration* is the dominant underlying factor. That is a real observability/identification gap, not a request for cosmetic additional A2 seeds.

## 2. Candidate original scientific question, subject to an explicit GO decision

**RQ:** For fixed job submissions and requested work under CloudSimPlus8.5.7 SpaceShared, can exact native queue-transition instrumentation distinguish the contribution of *(i) direct admission after a submit event*, *(ii) waiting-list promotion after scheduled processing update*, and *(iii) service-duration accounting* to the discrepancy with the simplified, event-independent FIFO reference? What observable source-level precondition predicts an older WAIT job coexisting with a younger newly-admitted EXEC job in the A1 native six-case fixture?

**Hypothesis to TEST, NOT ASSERT:** Under matched work and one-PE resources, direct submit admission and queued WAIT promotion can be triggered at different points of the event callback sequence, even when the earlier waiting job exists. If a consistent **observed source-level eligibility and transition condition** explains the A1 anomaly in exact native traces, it is an actionable simulator-modeling precondition rather than the tautology that differently defined models produce different outputs.

**Competing null/explanations:** trace instrumentation changes original scheduling; observed order explained by a different clock origin; native execution-list membership is delayed/non-work state; waiting promotion has already happened by submit; difference is entirely requested-versus-native-reported execution duration; or callback ordering and event cadence have no reproducible isolation under configured tests.

## 3. Smallest acceptable prospective protocol — freeze before running any NEW Java simulation

### Step A — complete exact Java v8.5.7 API source preflight
- Confirm whether `updateProcessing`, `moveNextCloudletsFromWaitingToExecList`, `addWaitingCloudletToExecList`, and related eligibility hooks are actually overrideable in a **read-only passive subclass**, including method signatures/visibility/return value and whether an override preserves a **single** super-call.
- The 8.5.7 publisher source JAR hash above MUST match the exact selected binary version. If instrumentation requires modifying library internals, state it explicitly and preserve a byte-identical native control—not a concealed modification.
- Record all proposed callback labels and event clock units before execution. **Do not claim instrumentation exists until compilation and source preflight pass.**

### Step B — fixed counterfactual design
- Use only six original A1 three-job arrival/event-gap conditions, plus one **source-predeclared positive control** that demonstrates the logging can observe a known WAIT-to-EXEC transition (if supported), and one **negative control** where no transition occurs. Do not tune arrival times after observing results.
- Two native execution arms on identical CloudSimPlus binary, same Java/Maven environment, same inputs: **original uninstrumented control**; **new passive callback trace** wrapping exactly one superclass invocation for each hook.
- Preserve same native per-job arrival, request, start-wait, total reported execution, finish, original submit order, and state transitions (after removing trace-only lines). For original six-case historical comparisons, verify exact job IDs, rounding and source SHA; do not silently reuse A2 as if A1 and A2 fixtures were identical.
- Candidate true **causal intervention** must be defined in a **separate preregistration**, only after observational hook trace validates an identifiable manipulable transition. Modifying minimum event gap *alone* changes several simulator event paths; it is not a clean intervention on waiting promotion. A new run with additional log lines is not causal inference.

### Step C — predeclared gates
1. **Source/instrumentation fidelity:** exact original 8.5.7 source and binary; event traces consistent and deterministic across original and repeat; control versus passive trace differ only by named trace lines. Any disagreement beyond output formatting => **FAIL, stop scientific claims**.
2. **Actual observability:** at least one directly observed WAIT→EXEC promotion and one direct submit admission, with documented Java source-method origin, clock and before/after list states. If no safe hooks exist, **NOT IDENTIFIED**; do not infer branch execution from list snapshots.
3. **Outcome sanity:** every test job completes; source wait definition and reported service remain explicitly nonphysical; repeated runs identical; actual native→FIFO residual recomputed independently; control conditions defined up front.
4. **Mechanism claim:** branch/path difference may be claimed only when recorded events correspond to exact **executed** callback/method transitions; a source-level call-graph alone is **insufficient**. Even positive mechanism identification does NOT demonstrate real IoT model accuracy or a new scheduling policy.
5. **Negative or ambiguous outcome:** publish the negative finding in internal checkpoint and reconsider SIMPAT feasibility. No open-ended parameter sweep.
6. **Novelty gate:** independently compare any positive mechanism insight against published queueing/CloudSim validation papers and existing documented 8.5.7 implementation contract. If ordinary documented scheduler behavior, **NO new general methodological innovation** and **HOLD** for full SIMPAT submission.

## 4. Current publication decision

**HOLD before experimental execution or submission** until the required *exact source/API hook viability preflight* is completed and the candidate *non-tautological* research question is accepted as worth testing. No new Java code, altered CloudSim implementation, extra A2 sweep, manuscript version increment, user-approved title change, or claim of independent novelty was performed in this checkpoint.

A useful positive result would be a small mechanistically grounded condition under which a particular analytical queue prediction is invalid for a named event-driven scheduler setup. It would still need sufficient scientific contribution for SIMPAT and careful limits. A negative result should end unjustified further research on this first-paper direction, instead of padding case counts.

**Program B:** independent risk-aware future research RESERVED, NOT STARTED; not a backdoor contribution to Program A.
