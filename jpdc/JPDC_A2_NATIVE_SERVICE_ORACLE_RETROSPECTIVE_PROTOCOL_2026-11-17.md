# RETROSPECTIVE DIAGNOSTIC PROTOCOL — A2 waiting discrepancy under native-reported service durations

**Status:** Analysis protocol, explicitly POSTHOC on already observed/spent 24-case original Java source run 44215741883. **No new Java run, no new independent source seed, no prospective confirmation.**

Scientific motivation discovered while checking manuscript: the native A2 log for BURSTY_S2_5MS_P1 reports job2 requested 5ms CPU but native 20ms total execution; some later tasks similarly have reported total execution substantially above original requested lengths. Therefore the A2 maximum 246ms discrepancy between native WAIT and FIFO reference with *requested service* may reflect both service-duration accounting and callback/queue semantics. Do not label all 246ms "queue-only" or causal event-granularity effect.

Original artifact ID14387238746; zip SHA256 1d29943e5e48d27f65eed186df23ff22d3dd7bdab381ebe63fca88dba1e3bb4b. Analyze ORIGINAL archived raw native.log, not re-simulated or selected subset. Compare on all 24 cases and 288 jobs. Use identical native observed submit order/time and one- or two-PE earliest-server FIFO rule as preregistered A2. Two reference recurrences:

1. **Requested reference**: FIFO service original CPU requested ms; previously audited A2 reference.
2. **Hindsight native-reported-service oracle**: FIFO service equals each job's native *total execution time* recorded after completion; strictly retrospective, not a feasible predictive scheduler and not a physical CPU benchmark.

For every case report native-vs-FIFO wait max absolute and mean absolute under both references, percent of jobs whose reported execution differs from requested by >1e-6ms, max service inflation and service differences by event gap/capacity/family. Distinguish deadline comparisons: primary previously reported classifications use requested FIFO service, but secondary hindsight reference finish uses native-reported service and must be clearly flagged oracle.

Decision question: If reported-service oracle reduces wait discrepancies, classify duration mismatch as a contributor. If residual remains >1ms, reported-service length alone cannot explain native wait. Report all cells and negative cases, including increased oracle error, no favorable posthoc selection. No p-values pretending 24 fixed scenarios are iid, no claims of simulator bug, hardware CPU time, Java/Python parity fix or CASPER efficacy.

New deterministic Python script and independently check algebra/row-count as possible. Preserve original failed 30k gate and Stage65 safety FAIL. Completion: commit script and numeric report using actual archived 24-case native.log, not manually guessed. Then correct working manuscript abstract/discussion to explain this confound. 
