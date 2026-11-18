# SIMPAT v2.2 — BH1 one-page independent model specification, two controls, and feasibility decision

**Exact unchanged title:** Queue-Wait and Execution-Time Semantics in CloudSimPlus 8.5.7: Implications for IoT Scheduling Simulation

**Status:** 2026-11-18; **design-only thought experiment**, not Java simulation, experimental preregistration independent of previous A1/A2 outcomes, proof of novelty, or alteration of manuscript v2.2. This delivers the explicitly requested next step of `SIMPAT_V22_PREEXPERIMENT_INDEPENDENT_BEHAVIORAL_VALIDATION_GATE_2026-11-18.md`.

## 1. Independent abstract scheduler specification

Assume ONE identical server (one PE), three one-PE nonpreemptive jobs with fully known nominal arrival times a_j and deterministic requested service times p_j, zero overhead, continuous clock, no simulator-specific event quantization. The queue is ordered by ascending (arrival time, input index). At any service release, the **eager-FIFO** abstract machine selects the oldest waiting eligible job before accepting a newly arriving job at the same time; a task that arrives during an occupied interval joins WAIT. At coincident completion and arrival timestamps, *completion and waiting-list promotion precede the new admission*. Server starts are determined by max(arrival, availability). These are declared independent **normative abstract choices**, not a claim that CloudSimPlus 8.5.7 guarantees them.

A contrasting **phase-deferred** conceptual machine uses exactly the same arrivals, services, capacity and FIFO waiting-list order, but at a coincident completion and arrival instant handles completion (releases capacity), then checks the new direct submission for free capacity, and only afterward promotes older WAIT entries. This constructed order can admit a new task with an older waiting task still queued. It is a **conceptual event-order baseline**, not newly proposed scheduler policy; it may resemble documented stock submit/update method sequencing and is not established to be the actual event order of CloudSimPlus for these inputs.

**Prohibited predictive inputs:** observed native WAIT/EXEC state at submission, new-job eligibility return, future native duration, future completion callbacks, or thresholds retrospectively selected from actual outcome. No API implementation-specific predicate P is used to choose controls.

## 2. Two deliberately simple CONTROLS with analytically specified outcomes

Use one-PE, nonpreemptive fixed-service jobs A/B/C, with times in ms relative to time origin. These numbers are **hypothetical, newly written for design**; no claim that they have been run or checked against the historical dataset.

| Control | (a_A,p_A); (a_B,p_B); (a_C,p_C) | Eager-FIFO predictions (job starts A,B,C; wait B,C) | Phase-deferred predictions | Diagnostic meaning |
|---|---|---|---|---|
| **C+ agreement** | (0,10); (2,4); (15,3) | starts (0,10,15); waits (8,0), finishes A=10 B=14 C=18 | Same starts/finishes, since WAIT is empty when C arrives | Positive *compatibility* control, cannot distinguish phase order |
| **C- phase-order disagreement** | (0,10); (2,4); (10,3) | starts (0,10,14); waits (8,4), finishes A=10 B=14 C=17 | If **completion→new direct admission→waiting promotion** at t=10: starts A=0,C=10,B=13; B waits 11 and C waits 0, finishes A=10 C=13 B=17 | Negative *model compatibility* control under **assumed event-phase order**, not a verified CloudSimPlus outcome |

The critical C- event sequence is conditional. If the real engine instead executes waiting promotion before C submission, or schedules callbacks at shifted timestamps, its observable outcome can match eager-FIFO. Published SpaceShared API does not promise unconditional cross-event FIFO service and the above conceptual alternatives are not evidence of a native library bug. **For native execution outcomes the expected class is presently UNKNOWN**, not secretly labeled C- positive.

**Manually verifiable reference:** C+ server busy [0,10] A, [10,14] B, idle [14,15], [15,18] C. C- eager server busy [0,10] A, [10,14] B, [14,17] C. C- deferred server busy [0,10] A, [10,13] C, [13,17] B. The conceptual C- arrival ties the completion clock, so a native test must explicitly account for scheduler/event priority and timestamp coalescing. No inference of physical CPU start from EXEC list membership is permitted.

## 3. Failure/identifiability and competition with existing methods

- C+ is only an arithmetic sanity control. A result that matches both abstract machines cannot select a behavioral theory or validate a general-purpose method.
- C- distinguishes **two models whose phase order has already been defined to differ**. Therefore the disagreement itself is virtually **by construction**. It is useful as a falsification fixture for a *specific event-order implementation*, not novel theoretical science.
- Current logs do not contain a general implementation-independent rule that takes input-only event timing and forecasts stock CloudSimPlus branch/event priority. 8.5.7 documentation already describes separate submit and waiting-promotion paths. To predict a particular native C- outcome requires either specifying native event ordering independently and testing it (a version-specific test) or using native internals (circular for claims of simulator-independent model generalization).
- No externally validated model, second simulation engine, real traffic trace or independently measured physical event order is present. Thus **BH1 model-independence/transfer and journal-level novelty gates currently FAIL/NOT ESTABLISHED**. This is an epistemic assessment, not a statement that such a model can never exist.
- Existing literature already addresses queueing vs simulation model differences, verification/validation and CloudSim accuracy; an event-order thought experiment without transferability does not establish significant originality for SIMPAT.

## 4. Explicit decision

**NO-GO for automatically running BH1 as a purported novelty-creating experiment.** The two controls can be stated and predicted analytically, but BH1's key requirement — *an independently grounded, non-tautological transferable rule that makes a differential native prediction beyond existing FIFO and stock semantics* — is **not satisfied by this design**. Re-running similar native inputs cannot close the novelty gap by itself.

**Recommended next worthwhile work:** stop synthesizing additional control fixtures; consider rigorous **editorial restructuring** of manuscript v2.2 into a candid exact-version empirical case study with a tighter RQ1/RQ2 focus, archival evidence and an explicit negative RQ3 result. Confirm current SIMPAT article types and editorial fit before preparing a formal submission. If the author requires a substantial full-length methodological contribution, this is an explicit **research redesign decision**, not another open-ended seed-sweep instruction.

**Preserved:** A1/A2/A3 native evidence; A1 eight-case P TP2 FP0 TN6 FN0 (bounded); failed 5ms>1us input-only H (1/4 vs1/4); old strict30k Java/Python parity FAIL; Stage65 safety FAIL; current v2.2 title and original data; separate CASPER Program B RESERVED/NOT STARTED. No DOI, journal submission, author approvals or new Java execution claimed.
