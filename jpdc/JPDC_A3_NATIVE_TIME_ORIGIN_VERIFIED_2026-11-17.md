# VERIFIED — A3 exact CloudSimPlus v8.5.7 waiting-time meaning and clock origin

**Date:** 2026-11-17 US Central / successful CI 2026-11-18 UTC.
**Status:** SOURCE definition and NEW PASSIVE 24-case REAL JAVA confirmation — VERIFIED WITH LIMITS.
**Version:** Java 17 + CloudSimPlus 8.5.7 native binary and exact SHA-pinned publisher source JAR.
**Source audit GitHub run:** https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44228012730
**Source audit source commit:** 82f8cd43faf2d80b63d161ccc0df3cfde0dfc3c1
**Publisher source JAR SHA256:** 8d3efcacfc661b2f1e018e279761fc4ae1e5584a770b2022d20930568688966c.
**Successful new passive timing run:** https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44228414078
**Successful measurement code commit:** 4d082e8a36146be05746bcc39828396068bb8535
**Successful output artifact ID:** 14394061608
**Original artifact ZIP SHA256:** 6e23f0979d9c6bb1b91d21f098ca707efe3e7b465c94e7749d5e97765661775a — independently downloaded and rehashed in the analysis environment.
**A3 audit JSON SHA256:** 907e465ffa09e1fc540c410e509b956ec9558d3463546c7aa421daca97efd529

## Important EXACT source inspection

From publisher version 8.5.7 source file `org/cloudsimplus/cloudlets/CloudletAbstract.java`, lines **253–256**, method `getStartWaitTime` is defined:

```java
@Override
public double getStartWaitTime() {
    return dcArrivalTime > NOT_ASSIGNED ? getStartTime() - dcArrivalTime : NOT_ASSIGNED;
}
```

Here `dcArrivalTime` is **Datacenter arrival**, not by definition an arbitrary queue-reference or VM schedule-call timestamp. Native FIFO reference in A2 uses the actual scheduler `cloudletSubmitInternal` callback clock, so before A3 the clocks were NOT independently shown to align. Public Cloudlet v8.5.7 API also distinguishes `getDcArrivalTime` and `getStartTime` (simulation seconds). Source-only inspection does not prove dynamic branch execution.

The exact original `CloudletSchedulerAbstract.java` source separately confirms submit-side `cloudletSubmitInternal` and waiting-list promotion in `updateProcessing` / `moveNextCloudletsFromWaitingToExecList`. It does not claim these callback paths have identical semantics or FIFO ordering.

## Real 24-case controlled A3 clock-origin measurement

Frozen A2 Java harness duplicated into isolated `NativeA3TimeOriginDiagnostic.java` on the same 24 configurations and 288 jobs, without changing source task arrivals, services, min-event intervals, VM/host configuration or original scheduling library. In one **same finish callback** per job, log original A2 finish row plus an A3 row with Datacenter arrival, native start, native returned waiting and finish clock. In the same CI job run unmodified original A2 harness; strip only A3 rows and require byte-exact original A2 control log. Repeat instrumented run and require byte-exact source data. Independent Python `audit_native_a3_clock_origin.py` checks the exact native `startTime-dcArrivalTime=wait` identity and source/CSV jobs.

**Verified results from PASS run44228414078**:
- 24 / 24 configurations, **288 / 288** jobs accounted for.
- **0 / 288** observed cases had different `dcArrivalTime` and native `cloudletSubmitInternal` callback time (tolerance 1e-6 ms). Measured max abs difference **0.0 ms** at original printed precision.
- Native `startTime - dcArrivalTime` equals native `getStartWaitTime` for every job within 1e-5 ms.
- Thus observed *submit-to-native-start* wait also equals native reported wait on ALL this fixed A2 design.
- The previously measured overall maximum native-vs-capacity-matched FIFO requested-service wait gap **remains 246.0 ms**, even when accounting for this clock origin.
- Instrumented Java trace with A3_CLOCK rows stripped **byte-for-byte equals** a fresh uninstrumented original A2 Java source execution. Full new trace and computed JSON each byte-identical on second instrumented repeat.
- This excludes DATACENTER_ARRIVAL ↔ SCHEDULER_SUBMIT timestamp mismatch as a cause of A2 discrepancies **in these specific fixed 24 cases**; it is NOT a general guarantee all CloudSimPlus setups or broker/network configurations have the same origin.

## First unsuccessful CI and fix — preserved, not hidden

[Run44228241419](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44228241419) fully executed Java and produced successful initial 24-case numerical audit with same zero timestamp mismatch, but the **full instrumented trace repeat check failed**: original A3 version registered **two separate finish listeners per job**, whose relative callback invocation order changed between runs (`A2_FINISH` and `A3_CLOCK` swapped), even though corresponding measured numbers were identical. Root cause of failure is in the new observation log ordering, NOT proven dynamic scheduling nondeterminism. [Fixed source commit4d082e8a](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/commit/4d082e8a36146be05746bcc39828396068bb8535) emits both rows in **one finish listener**. Repeat now passes. No A2 workload input was changed and no old failures were erased.

## Scientific consequences for Program A

**Permitted:** A2's native wait versus analytical FIFO requested-service discrepancy is NOT attributable to a different measured Datacenter arrival versus scheduler-submit clock in the 24 fixed experiments. Prior posthoc native-duration sensitivity remains valid (requested FIFO worst 246ms; post-completion service FIFO worst154ms; residual >1ms in all24). The measured discrepancy still reflects differences between event-driven runtime and specified event-independent reference, but **unique causal attribution to admission, update cadence or CPU service accounting is NOT established**. Do not infer CloudSimPlus bug or actual application SLA impact.

**Still prohibited:** treating instrumented `EXEC` membership as a physical CPU start event, treating these synthetic 288 job observations as 288 independent random sources, claiming policy superiority or general real-world IIoT validity. Old 30k Java↔Python strict-FCFS fidelity gate **FAIL** and Stage65 safety **FAIL** remain unchanged. Original FGCS code frozen.

**Recommended manuscript wording:** `getStartWaitTime` is defined as `getStartTime()-getDcArrivalTime()`; in the fixed 24-case A3 observer control, `getDcArrivalTime` equals original scheduler submit clock for 288/288 jobs. The mismatch is therefore not a timestamp-origin artifact in these samples, though native execution-duration inflation and event-driven queue processing remain confounded. Report this as targeted reproducibility check, NOT a new scheduling result.

**Next priority:** revise manuscript A v0.4 with exact method definition, new A3 controls, closest prior-art caveats. Only pursue further native probes if the specific remaining scientific claim requires it; no open-ended simulation campaigns.
