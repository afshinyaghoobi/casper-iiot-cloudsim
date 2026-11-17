# VERIFIED — New real CloudSimPlus native arrival-shift queue counterfactual (2026-11-17)

## Scope and preregistration

The hypothesis was preregistered BEFORE the new Java observations in jpdc/NATIVE_ARRIVAL_SHIFT_QUEUE_COUNTERFACTUAL_PREREG_2026-11-17.md, commit **358f47d0e4a4569d518fc75d94706196b4548f4f**. The new independent Java class src/main/java/org/casperiiot/jpdc/NativeArrivalOffsetCounterfactual.java (initial commit **b2757a226eae74cf21580cb935f9ace0eaba89ca**, output reporting fix **af7cf2312ddc886622984515d4663364cf11b724**) runs genuine CloudSimPlus 8.5.7 SpaceShared scheduling. The original FGCS CASPER E42/E4.6, Stage50/67 Java source, and rejected Stage64 policy remain unchanged.

Six fixed experiments: one host processing element and one 1PE VM, three requested CPU lengths **8.099623 / 4.730689 / 9.120283 ms**, jobs0/1 unchanged requested arrival offsets **0 / 5.318920 ms**, job2 at **4.0997406, 8.0997406, 18.0997406 ms** crossed with simulator minimum event time **1us and 5ms**. Source order and native WAIT/EXEC list contents observed directly during passively logged submit/update callbacks. Direct bypass requires a job already submitted before another still WAIT when the later job is in native EXEC at the SAME snapshot. Native EXEC-list membership does not prove precise hardware CPU start.

This is a NEW **real Java simulator microexperiment with fixed synthetic workload**, not external independent IIoT trace, new scheduler policy, Java/Python 30k parity success or CASPER efficacy.

## Two completed actual CI runs and independently inspected artifacts

**Original Java GitHub Actions run44153953054**: COMPLETE SUCCESS, source head **f29ff0c0fee9db35eb31c3c610ac0e94c7285088**, original artifact ID **14360786041**, artifact ZIP SHA256 **9c421b365f22e37413b564384e713de6dcb2c34ee4b4d5b3cc1fdad8b031889e**, downloaded and independently inspected. Native complete raw log SHA256 **b80536e332b04ffeb0285005b38a95563bac36c29201fc8f93693efc95e5c250**, original primary audit.json SHA256 **4d4454a11b59420c0ff17b064d7988f2bcd0f927e2cfa4ff3600b9ac7a6579a0**. Both native log and primary audit were exactly byte-identical to repeats. All **six native cases**, three jobs each, **18/18 genuine CloudSimPlus Cloudlets finished**, with native source contract PASS.

**Independent archive-only audit run44154416030**: COMPLETE SUCCESS, code SHA **6f3415ae168b13a8d56aeedcc58f962286f94f1a**, output artifact ID **14359333960**, ZIP SHA256 **ab9972d7dfbe35998b7cd67dcf7d265e3e04bd1123065fb756db202fd1337804**, downloaded and inspected. Independent audit.json SHA256 **aaf53a9870e819930172e78bd5f9aed14443239c479b387c4333e63bf42e6108**. Alternate implementation jpdc/independent_original_native_arrival_audit.py independently reparsed the original prior Java native.log without importing primary parser or rerunning Java; all six original native submission orders, recorded task wait times and same-snapshot bypass counts matched primary.

## Main quantitative results

| Third task nominal arrival | Minimum event gap | Actual Java submission order | Later EXEC while earlier WAIT? | Maximum Java wait minus requested strict FIFO absolute residual (ms) |
|---|---|---|---|---:|
| EARLY4, 4.0997406ms | 1us | 0 → 2 → 1 | NO | 30.883717 |
| EARLY4, 4.0997406ms | 5ms | 0 → 2 → 1 | NO | 35.879717 |
| ORIGINAL, 8.0997406ms | 1us | 0 → 1 → 2 | NO | 35.273311 |
| ORIGINAL, 8.0997406ms | 5ms | 0 → 1 → 2 | YES | 24.1204006 |
| LATE10, 18.0997406ms | 1us | 0 → 1 → 2 | NO | 30.0038824 |
| LATE10, 18.0997406ms | 5ms | 0 → 1 → 2 | YES | 45.0000000 |

At ORIGINAL 5ms, Cloudlet2 entered native EXEC at **1013.0997406ms** while earlier-submitted Cloudlet1 was WAIT; direct native AFTER submit event and three additional source snapshots (total4) independently observed. At LATE10 5ms, identical type of overtaking occurred when Cloudlet2 entered native EXEC at **1023.0997406ms**, with Cloudlet1 WAIT; again four snapshots. EARLY4 has actual native submission order **0→2→1**, so Cloudlet2 cannot be called a later-arriving bypass of job1; no overtaking was observed for that scenario. No overtaking in any 1us case, although substantial strict FIFO waiting errors persisted.

This shows sensitivity to changed third-job arrival and native minimum event gap in the FIXED three-job simulator setting. It neither proves the cloud simulator is faulty nor isolates one unique mechanism among event callback cadence, scheduler list-state ordering and wait-accounting semantics. This result cannot establish independent queue-model parity in the original 30k case, and the ORIGINAL case is a reuse of previously spent microdata, not a new held-out source.

## Scientific negatives and next step

Original **30k Java SpaceShared↔Python strict FCFS max waiting discrepancy 9.12140093294972ms > predeclared5ms remains FAIL**. Original Stage65 prospective independent partial-minimax safety **FAIL**, Stage56 nine unfinished native cloudlets and Stage61 full21 READY0/4840 remain; E42 original Git blob **34256ca7bff46f911cf20e8b94278fbd09175746** and rejected Stage64 policy Git blob **24d495dba4d29f8fe070ad6539b20361a7193cc6** still protected. No measured real factory IIoT deadline/packet bytes/hardware CPU, no full500 original Google source scan and no independent new scheduling method success.

Next legitimate work: inspect actual CloudSimPlus v8.5.7 scheduler source transitions and independently predeclare one isolated native callback/cadence intervention in Java. Do not retrofit these six outcomes as a positive policy-efficacy result.
