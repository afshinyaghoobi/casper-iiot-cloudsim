# Stage52 independent eight-source-seed queue-pressure comparator holdout — verified mixed/adverse result (2026-11-12 CST / 2026-11-13 UTC)

## Immutable source and original-run provenance
Prospectively frozen Stage52 protocol **BEFORE source outcomes**: `jpdc/STAGE52_EIGHT_SEED_QUEUE_COMPARATOR_HOLDOUT_PREREG_2026-11-12.md`, commit `e36883809dfc243541b7754f14935922dd1ba1da`. Original Stage51 pure selector Git blob `c0fdd686a451e528a68e7265cd8d3f2ac3bd9af9`, isolated Python simulator blob `249f71030c791472dfdba6ebe38e91ff58b06d9a`, frozen original E42 blob `34256ca7bff46f911cf20e8b94278fbd09175746`. Original E4.6 untouched. No parameter updates after Stage51 DEV seed101/102 outcome.

[Original GitHub Actions run **43369034814**](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43369034814) completed **8/8 SUCCESS individual genuine scientific source jobs** on new source seeds1101–1108. All frozen-source checks, 80,000 S0 calibration/seed, exact original Stage6 PRED_GREEDY and CASPER_FULL source JSON parity, causal policy tests, 12,000 tasks/scenario/policy, deterministic source JSON/log repeats **PASS**. Total **768,000 DEPENDENT task-policy observations**, **n=8 independent source seeds** (not 768,000 independent samples).

The original run overall status was **FAILURE only in final cohort-log tee**, not scientific computation: `tee: stage52-cohort/audit.log: No such file or directory`, because workflow did not create destination before piping. Original Python cohort auditor nevertheless printed `JPDC_STAGE52_ALL_EIGHT_SOURCE_COHORT_AUDIT_PASS` and wrote original artifact `audit.json` (original cohort artifact ID **14011413752**). This real CI failure is preserved, not relabeled success.

**Audit-only recovery**, no new physics, no source-seed reruns or changed parameters: [GitHub Actions run **43369267053**](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43369267053) **SUCCESS**, download of original 8 seed artifacts from original run 43369034814, creation of output directory, exact same Python cohort audit, deterministic double repeat. Recovery artifact ID **14011686807**. Downloaded and independently compared recovery `audit.json` to the original failed-job artifact `audit.json`; bytes are **IDENTICAL**, and recovered `audit_repeat.json` likewise byte-identical; SHA256 of identical JSON `cdd8929356a4ec12d6a44f5dc099a9d65fbf4bdb57cce106ef0c6bba88413af9`. Therefore independent Stage52 complete **science source and cohort audit are verified** despite original infrastructure-only failure.

## Complete predeclared per-seed postshock MISSION deadline misses
Same denominator per policy/scenario/seed. Source seed order 1101–1108.

| Source seed | POST MISSION n | S2 PRED_GREEDY | S2 CASPER_FULL | S2 QUEUE_PRESSURE_05 | S2 QUEUE_PRESSURE_E2E_05 | S3 PRED_GREEDY | S3 CASPER_FULL | S3 QUEUE_PRESSURE_05 | S3 QUEUE_PRESSURE_E2E_05 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|1101|90|0|0|1|1|6|6|4|3|
|1102|108|0|0|1|1|0|0|0|0|
|1103|95|2|1|2|2|2|1|2|2|
|1104|88|3|3|3|3|6|6|5|3|
|1105|92|2|1|3|3|3|3|2|1|
|1106|86|2|0|1|1|2|2|0|0|
|1107|96|6|1|5|5|1|1|0|**2**|
|1108|84|2|0|2|2|3|3|3|1|
|**Pooled descriptive**|**739**|**17**|**6**|**18**|**18**|**23**|**22**|**16**|**12**|

S2 QUEUE_PRESSURE_05 and E2E are identical 18/739: both are **worse than FULL 6/739 by +12 misses**, and even worse than PRED_GREEDY17/739 by +1. **Predeclared S2 no-mean-harm gate FAILED** for both baselines. Paired baseline-minus-FULL deltas per source seed **[+1,+1,+1,0,+2,+1,+4,+2]**. Exact two-sided sign p **0.015625**: seven worse, zero better, one tie (source-level, not task-level). This is compelling evidence of an adverse CPU-shock tradeoff in this cohort; statistical multiplicity/family limitations still apply.

S3 QUEUE_PRESSURE_05 16/739 vs FULL22/739, paired deltas **[-2,0,+1,-1,-1,-2,-1,0]**, five better, one worse, two ties, exact two-sided sign **p=0.21875** (NOT significant). Queue+delayed E2E 12/739 vs FULL22/739, paired deltas **[-3,0,+1,-3,-2,-2,+1,-2]**, five better, two worse, one tie; exact two-sided sign **p=0.453125** (NOT significant). The favorable pooled ten-miss S3 difference is **descriptive only**, not significant at .05. The E2E extension does not always improve: in seed1107 it produced **2 misses vs queue-only0 and FULL1**, and seed1103 both queue variants2 vs FULL1.

## Scientific decision
- **Stage52 source engineering and reproducibility COMPLETE and VERIFIED, with an audit-only CI recovery.**
- **Scientific acceptance as a general CASPER replacement: REJECT / no go.** Both new comparator baselines fail prospective CPU-shock no-harm gate, despite descriptive S3 reductions. No author-original DFAQ-LB reproduction; these remain queue-pressure and feedback-inspired simplified online comparators.
- Do not select queue+E2E as a better scheduler simply because S3 pooled misses 12 <22. Predeclared S3 paired tests are nonsignificant, and CPU shock shows clear adverse outcomes.
- Stage51 n2 favorable DEV did not generalize to safe all-scenario performance. No parameter refit on holdout1101–1108; these seeds are now **SPENT** for candidate modifications.
- The original registered 30k Python strict FCFS vs native CloudSimPlus SpaceShared waiting max deviation **9.12140093294972ms >5ms remains FAILED**. Stage50 mechanistic native trace and Stage52 Python experiments do not establish cross-engine parity, real IIoT generality or novel mathematical guarantees.

## Next higher-value scientific action
Keep the comparator frozen as a documented contrast and study the **different CPU and network fault behavior without threshold tweaks**: on already-consumed source seed1107 conduct an explicitly POSTHOC paired task-ID trace to explain why S2 queue+E2E worsened FULL by4 and why S3 queue+E2E worsened queue-only by2. The analysis must be labeled retrospective and must not count as independent validation. Consider structural workload/physical simulator sensitivity and fair published-method comparator mapping, instead of pursuing endless StageX tuning. Any genuinely new method needs fresh development and untouched holdout after predeclared design.
