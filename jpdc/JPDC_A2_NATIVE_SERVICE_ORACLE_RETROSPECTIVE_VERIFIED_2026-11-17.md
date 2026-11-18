# VERIFIED — Retrospective A2 native service-duration confound diagnostic

**Date:** 2026-11-17 local (GitHub CI 2026-11-18 UTC).
**Analysis type:** posthoc, reuses ORIGINAL already-spent 24-case native Java A2 workload. **NO NEW Java experiment** and no independent source seed.
**Frozen analysis protocol:** [JPDC_A2_NATIVE_SERVICE_ORACLE_RETROSPECTIVE_PROTOCOL_2026-11-17.md](JPDC_A2_NATIVE_SERVICE_ORACLE_RETROSPECTIVE_PROTOCOL_2026-11-17.md) commit **6f287daf9fe3a6be39501cb70597c52a23617d1a** before this retrospective calculation.
**New source:** [audit_a2_retrospective_native_service_oracle.py](audit_a2_retrospective_native_service_oracle.py)
**Actual successful retrospective CI:** [run 44216958536](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44216958536); source commit **7a646d3abeb7e63001ca2f5fedf16d74db5ee427**; CI job 134509084320.
**New archive:** artifact **14389320788**, uploaded ZIP SHA256 reported by GitHub Actions **2535bc3a99bf12e9a289b94d894a78eaf578531ab492820cca8a98fdc52895c4**. This new ZIP was **not independently downloaded/rehashed in this analysis**; original source A2 artifact14387238746 was independently hashed in prior audit.
**Original genuine Java source run:** [44215741883](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/44215741883), pinned original native.log SHA256 **9fb08d07fe9741772b0de59a837046d0152362d3724da04daf02ccbc3d879391**; primary audit.json SHA256 **433035fa66895fa2d47b8e48757e2edbe68849a2947c9ea79474a43e27b06266**. CI validates both original file hashes and byte-exact original native_repeat.log.

## Motivation and design

A2's predeclared FIFO reference uses requested CPU service length. Original CloudSimPlus 8.5.7 native logs also contain a **reported total execution time** which is sometimes different; e.g., BURSTY_S2_5MS_P1 job2 requested 5ms but native reported 20ms execution. This posthoc audit reproduces A2 exact submitted timestamp/order and capacity-matched earliest-server FIFO recurrence twice: with original **requested** length, and with the job's **native-reported total execution duration known ONLY after completion**. The latter is a hindsight upper-information *service oracle* reference, **not a realizable forecast or physical measured CPU service**.

## Results — original archive, all cases

- **24/24 original cases and 288/288 original jobs analyzed**. All 24 original 12-job cases verified against previous requested-service primary JSON.
- **250/288 jobs** had native-reported total execution duration different from requested service by more than 1e-6 ms. This is evidence of service-duration/accounting mismatch, not evidence of processor speed measured on hardware.
- The largest across-case maximum native waiting discrepancy against requested-service FIFO was **246 ms**; after changing only FIFO service to POSTHOC native-reported total execution, the largest across-case maximum was **154 ms**.
- All **24/24** cases still had a maximum native waiting discrepancy greater than **1 ms** under the hindsight reported-service reference. Native duration mismatch alone cannot reconcile native queue waiting with strict reference FIFO accounting.
- At preregistered synthetic deadlines (native observed submission+25ms / +50ms), native-vs-requested-reference classification disagreements were **86/288** and **107/288** respectively; native-vs-hindsight-service reference disagreements were **58/288** and **78/288**, respectively.
- These quantities do **not** support a causal attribution of how much of the original 246ms gap was due to one internal method. Oracle errors can increase in individual cases because changing service lengths changes reference waiting trajectory and server assignments.

## Representative full-case maxima, all values milliseconds

| Case | Requested-service reference: max abs wait gap | Hindsight-reported-service reference: max abs wait gap |
|---|---:|---:|
| BURSTY_S0_1US_P1 | 157.018 | 104.010 |
| BURSTY_S0_5MS_P1 | 118.000 | 80.000 |
| BURSTY_S2_5MS_P1 | **246.000** | **154.000** |
| BURSTY_S2_1US_P2 | 33.004 | 26.801 |
| STAGGERED_S0_1US_P1 | 87.011 | **105.003** |
| STAGGERED_S0_5MS_P1 | 171.000 | 111.000 |
| STAGGERED_S0_1US_P2 | 24.000 | **33.998** |
| STAGGERED_S2_5MS_P2 | 60.000 | 44.800 |

The all-24-case machine-readable JSON source of truth is included in GitHub Actions artifact14389320788. Do not imply the representative rows substitute for checking the entire result.

## Manuscript-relevant conclusion and limitations

An appropriately narrow claim is: **Native reported waiting time in CloudSimPlus 8.5.7 differs from the study's declared FIFO reference over the fixed tested workloads; part of the difference is associated with native-reported execution duration exceeding requested service, but important residual disagreement remains even when a hindsight FIFO reference is supplied those native durations.** Other mechanisms include event update cadence, admission/list promotion and the meaning of reported start wait. Causal isolation is NOT established. The native execution list is not a physical CPU start event; the synthetic deadline margins are NOT field deadlines. None of this proves Java/Python cross-runtime parity, a CloudSimPlus defect, or superiority of a scheduling policy.

### Original negative gates preserved

Original 30k Java↔Python strict-FCFS wait max9.12140093294972ms > prereg5ms **FAIL**, Stage65 independent policy safety **FAIL**. Original FGCS E42/E4.6 and rejected Stage64 code remain frozen. Future policy research Program B not started.

**Next:** revise A manuscript Abstract, Methods, Results, Discussion, Limitations and bibliography to explicitly expose this service-duration confound, not launch more exploratory simulator matrices before JPDC novelty/venue go/no-go.
