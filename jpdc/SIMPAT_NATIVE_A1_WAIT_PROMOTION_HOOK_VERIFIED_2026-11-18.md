# SIMPAT Program A — genuinely new exact-8.5.7 six-case waiting promotion Java hook audit

**2026-11-18. FIRST HAND NEW JAVA EXECUTION, observational only.**
**Immutable author-approved first-paper title:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation.
**Target:** Simulation Modelling Practice and Theory.
**New protocol frozen before execution:** [SIMPAT_A1_A2_SOURCE_OBSERVABILITY_AND_MECHANISM_PROTOCOL_2026-11-18.md](SIMPAT_A1_A2_SOURCE_OBSERVABILITY_AND_MECHANISM_PROTOCOL_2026-11-18.md), first commit746176d1cae390b6e72a17d72c2f861f7e08f39c. **Caution:** original A1 six-case outcomes were known when this new method-level protocol was written, so this is a prospectively specified *instrumentation/analysis on known fixtures*, not an independent prospective holdout.
**Actual run [44359114031](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44359114031): SUCCESS**, GitHub artifact **14452799174**, output zip SHA256 rehashed in model's active container **101286081b90acf44d2b0eab43de770c98bbeffbd37f90a4ea0d9554dbf30d28**. Repeated newly instrumented original-Java execution was **byte-identical** to itself; filtering only `ARRIVALTRACE_PROMOTION` lines gives **byte-identical trace** to separately run original `NativeV857EligibilityCallbackTrace` original control. This is strong observational fidelity, **not an independent experiment on live deployment**.
Source new Java [NativeV857WaitingPromotionPassiveTrace.java](../src/main/java/org/casperiiot/jpdc/NativeV857WaitingPromotionPassiveTrace.java) clones six original A1 cases and adds exactly one `super.moveNextCloudletsFromWaitingToExecList(currentTime)` invocation, with BEFORE and AFTER WAIT/EXEC-list snapshots. Existing original A1 `cloudletSubmitInternal`, eligibility and `updateProcessing` hooks retained; new exact source based on original CloudSimPlus8.5.7 publisher source JAR SHA256 **8d3efcacfc661b2f1e018e279761fc4ae1e5584a770b2022d20930568688966c**. [Independent trace parser](audit_simpat_v857_wait_promotion_trace.py).

## First-hand new observations

- Six original A1 fixed three-job cases **all complete**, native source traced **33 actual method invocations** of `moveNextCloudletsFromWaitingToExecList`, of which **10 BEFORE→AFTER snapshots show at least one original WAIT job joining EXEC**. This is dynamic method execution evidence, not merely static source call inventory.
- Promotion-call counts: EARLY4_1US **6**, EARLY4_5MS **5**, ORIGINAL_1US **6**, ORIGINAL_5MS **5**, LATE10_1US **6**, LATE10_5MS **5**. Actual WAIT→EXEC transitions: **2,2,2,1,2,1**, respectively. The number of trace calls is not the number of job promotions.
- In `ORIGINAL_5MS`, the new direct submission of younger job2 at **1013.0997406ms** is observed with **BEFORE EXEC empty / WAIT={1}**, then **AFTER EXEC={2} / WAIT={1}**. The newly traced waiting-promotion method was previously called at **1013.099623ms** but still returned `EXEC={0},WAIT={1}` unchanged. Subsequent waiting-promotion checks at **1022.2200236ms** and **1028.099623ms** also retain younger job2 in EXEC and older job1 in WAIT. After an intervening completion/update, the older job1 is **actually promoted** from WAIT to EXEC by this method at **1037.2200236ms**.
- In `LATE10_5MS`, direct younger job2 admission with older job1 waiting occurs at **1023.0997406ms** (EXEC empty→{2}; WAIT stays{1}). Earlier waiting-promotion call at **1013.099623ms** had left job1 in WAIT. At **1028.099623ms** and **1043.099623ms**, the promotion method still leaves job1 in WAIT while job2 is EXEC. Job1 is actually promoted at **1058.099623ms**.
- These are direct **method entry/exit** and list-state observations with event clock numbers, not indirect inference from finish order. The old v8.5.7 static source confirms that the *direct submission* path calls `canExecuteCloudlet` and adds directly to EXEC or WAIT; a separate `updateProcessing` path calls `moveNextCloudletsFromWaitingToExecList`, as the new actual dynamic hook now observes.

| Case | Promotion method calls | Observed WAIT→EXEC promotions | Late job2 direct admission while old job1 WAIT? |
|---|---:|---:|---|
| EARLY4_1US | 6 | 2 | no |
| EARLY4_5MS | 5 | 2 | no |
| ORIGINAL_1US | 6 | 2 | no |
| **ORIGINAL_5MS** | **5** | **1** | **yes** |
| LATE10_1US | 6 | 2 | no |
| **LATE10_5MS** | **5** | **1** | **yes** |

**Mechanistic value:** We now establish that separate native code paths for *direct submit admission* and *deferred waiting-list promotion* were **actually executed** and can be observed in the two key original six-case fixtures. This gives credible executed-method context to the earlier WAIT/EXEC anomaly. It does **NOT** prove that the underlying reason is a bug, unfair scheduler, violated documented FIFO invariant, unique causal contributor to A2's 24-case FIFO waiting difference, or hardware CPU start instant. At those earlier promotion events, eligibility/free PEs and memory of exact scheduler status would need further isolated counterfactual verification to make a causal claim.

## Experimental integrity, negative outcomes, and next decision

- Original six-case control outcomes unchanged byte for byte when new log lines filtered, and repeat identical, **PASS**.
- Static existing A1 input fixtures were intentionally reused; these are **not six new independent datasets** and there was no custom arrival adjustment.
- All original A2 (24 cases288 Cloudlets) source outcomes and all A3 (288 arrival clock agreements) remain unchanged; new A1 hook observations do not explain all A2 discrepancies.
- Old independent 30k strict Java↔Python fidelity gate **FAIL**, Stage65 policy safety **FAIL**; no policy performance assertion; separate Program B RESERVED/NOT STARTED.
- **SIMPAT submission scientific GO/NOGO remains HOLD**. This new empirical *dynamic method-level explanation* is more substantive than algebraic threshold sweeping, but it may still simply reflect well-documented intended SpaceShared behavior, and no general independent simulator-evaluation *algorithm* or real IoT validation has been demonstrated. Scientific next action is a **predeclared narrow causal control** if needed: distinguish waiting eligibility from submit admission at identical event states and document an actionable precondition predicting when the analytical FIFO approximation breaks. Do not assume our already observed method path proves that answer.
