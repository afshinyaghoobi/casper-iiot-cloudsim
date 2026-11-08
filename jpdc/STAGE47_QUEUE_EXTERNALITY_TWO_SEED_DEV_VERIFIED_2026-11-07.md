# JPDC Stage47 causal shared-queue externality gate — real 2-seed DEVELOPMENT source VERIFIED, 2026-11-07

## Provenance
Method preregistration BEFORE source DEV outcomes: `jpdc/STAGE47_CAUSAL_QUEUE_EXTERNALITY_GATE_PREREG_2026-11-07.md`, commit `97610d8077a422c882ba890d7cda4378e15559eb`. New `jpdc/queue_externality_gate_stage47.py` and adversarial `jpdc/test_queue_externality_gate_stage47.py`, isolated original-physics source clone `jpdc/independent_physical_queue_guard_stage47.py`, runner `jpdc/run_stage47_queue_guard_development.py`. CPU service outcome only at CPU finish, E2E network outcome only after delivered; no scenario/affected mask/true future as routing input. Original E42 Git blob SHA `34256ca7bff46f911cf20e8b94278fbd09175746`, original E4.6 untouched.

Original Stage44 node-local disturbance detection unchanged. In NETWORK mode, MISSION may leave original CASPER_FULL source route only if frozen Stage37 corrected proposed node: is healthy at issue, nominal pred <= FULL chosen+2ms, current virtual predicted FCFS backlog <= FULL backlog, corrected-score apparent delivered positive benefit >=3ms, corrected candidate <=deadline−2ms and original FULL nominal <=deadline. E2E-only and combined variants separate. NORMAL/HIGH always original FULL. No coverage/false positive/safety or guaranteed deadline claims. This is a structural *attempt* at queue interference control; virtual predicted backlog is NOT an upper bound on downstream real FCFS externality.

[**Actual GitHub Actions Stage47 run42433569355**](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/42433569355) **SUCCESS BOTH science development seeds99 &100, causal adversarial unit, Stage37/44 regression, exact source Stage6 original policy JSON and frozen Stage42/44 policy JSON parity, two byte-identical native-source reruns.** 2 NEW DEV source seeds99 and100, original 80000 Stage3 calibration per seed, S2 hidden CPU40%-loss and S3 hidden network50%-loss, six policy arms×12000 tasks×two scenarios =288000 DEPENDENT task-policy evaluations, scientific DEV n=2. No independent validation claim.

## Actual POST MISSION missed deadlines per scenario and seed
| Seed | Shock | POST mission denominator | PRED_GREEDY | Original CASPER_FULL | prior Global Stage42 combined | prior NodeLocal Stage44 combined | NEW QueueGuard E2E-only | NEW QueueGuard CPU+E2E |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
|99|S2 CPU|99|8|6|6|6|6|6|
|100|S2 CPU|108|8|6|6|6|6|6|
|99|S3 NETWORK|99|5|5|5|5|5|5|
|100|S3 NETWORK|108|3|3|2|2|3|2|
|**Pooled descriptive S2**||**207**|**16**|**12**|**12**|**12**|**12**|**12**|
|**Pooled descriptive S3**||**207**|**8**|**8**|**7**|**7**|**8**|**7**|

New Stage47 combined vs FULL: S2 identical12 vs12; S3 combined7 vs8 (only one seed improved one mission, other tie). Stage47 combined vs UNGUARDED NodeLocal is identical actual post missed counts across all development arms, so the guard has NOT shown a new empirical deadline benefit beyond Stage44 in this small sample. New E2E-only gives NO observed aggregate S3 miss benefit vs FULL. These DEV results have essentially no inferential power, no statistical superiority.

## Counts, actual route interventions and reasons
In both S2 source seeds, node-local detector never entered NETWORK mode for any MISSION, so both Stage47 policies accepted 0 route switches and matched original FULL.
In S3 seed99: queue gate receives95 MISSION NETWORK-mode proposals: E2E-only accepted5, denied due extra predicted virtual backlog2, unchanged proposal88; combined accepted4, denied backlog3, insufficient evidence corrected gain2, unchanged proposal86. Both post mission miss count5 equal original FULL5.
In S3 seed100: 97 MISSION NETWORK-mode proposals: E2E-only accepted11, denied backlog2, unchanged proposal84, post miss3 equal FULL3; combined accepted12, denied backlog1, unchanged84, post miss2 vs FULL3. Gates never illegally exceeded predeclared budget. Original Stage37 proposal generation counts include self-unchanged routes, so gate 'calls' is NOT equal to switches.

Original Native Python strict FCFS model, and original Python-vs-Java CloudSimPlus SpaceShared WAIT parity registered **FAILED max9.1214ms>5ms**. No real IIoT workload trace and no fully reproduced contemporary DFAQ-LB/AUHS original executable baseline yet. Six user-supplied FGCS/JPDC 2026 full-text publication metadata remain in `jpdc/references_2026_six_uploaded.bib` and English Related Work draft.

## Development gate and next step
A priori development selection rule: average S2 no worse than original FULL **PASS**; aggregate S3 stricter lower miss count than FULL **PASS** (combined7 vs8); at least one actual S3 switch **PASS**. This is eligible for an untouched independent source COHORT science test, NOT proven method. E2E-only S3 gate FAIL (8 vs8). NEW independent scientific source seeds MUST be disjoint from DEV99–100 and prior holdouts601–608,701–708,801–808,901–908; no adjustment of Stage47 code/thresholds after seeing these new results.

Do not misleadingly say Stage47 beats frozen Stage44: it is tied on dev post MISSION missed deadlines. Stage47 might still be worthwhile if it consistently limits harmful rerouting in a new independent cohort, but that is a prospective hypothesis.
