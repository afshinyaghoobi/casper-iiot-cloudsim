# VERIFIED — prospectively selected real Google Borg 2011 v2.1 middle-file temporal and retry semantics (2026-11-15)

## Study scope and preregistration chronology
This is a **new publisher-original external production task-events sample** from the genuine Google Borg **DATACENTER** trace, NOT industrial IIoT workload data, NOT original physical CPU measurements, NOT real application deadlines/per-task transfer bytes, NOT a scheduling comparison, and NOT an independent source-seed efficacy study.

The exact test specimen and acceptance criteria were frozen in `jpdc/GOOGLE2011_MIDDLE_PARTITION_TEMPORAL_PREREG_2026-11-15.md`, **pre-outcome preregistration commit `911de729a7715b6c571978c4d5054c73513afc61`**: Google official GCS object `gs://clusterdata-2011-2/task_events/part-00250-of-00500.csv.gz` (index250 from expected500 partition names); original publisher GCS metadata must confirm existence and identity; bounded HTTP range first **262144 gzip bytes**, capped inflation **1048576 bytes**, take **first128 full source CSV event rows**, with 13 fields and original v2.1 event enum. This is *purposeful source-selection*, not randomized sampling. Original E42/E4.6 and Stage64 rejected policy frozen. Stage65 independent safety FAIL and original Java-Python queue parity FAIL remain unchanged.

## Genuine publisher source identity and original artifact
- Exact GCS original object: `task_events/part-00250-of-00500.csv.gz`, original generation **1416266806161000**, original file size **4715492** bytes, publisher reported CRC32C `lz+n2g==`, publisher MD5 `0uxqY2/lYdTlF3ZFMLqw0Q==`, object update `2014-11-19T17:02:54.515Z`.
- Corrected original [**GitHub source run43733748151**](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43733748151) **COMPLETE SUCCESS**, SHA `0137d6a6ad1cb48c468fd29f9edb4dd5d8f88346`, original artifact ID **14168989992**, digest sha256 `d8353f7463d1f2579f517f6f1c72918556b0772a7c74f9c9afe2637359c07bdc`, downloaded and independently inspected. Source HTTP206 `Content-Range: bytes 0-262143/4715492`, `Content-Length: 262144`. Exact original 256KiB compressed prefix SHA256 **`71a66cf47ea18b533e9f4adecca0965f1aad38fc3b668c85765609c05f1f51f5`**. Inflated exactly 1MiB bounded, 9183 complete lines within cap; **first128** analyzed. Offline local source reparse produced byte-identical original `audit_first.json` and `audit.json`, original audit SHA256 **`616fe2683696faf052bebe59bf076be97aa4d1dc4f4696ca4164cd83f1fbfaa8`**.
- Initial [original source run43733578202](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43733578202) also **SUCCESS** and retrieved the **same raw original bytes SHA256**; its output had a misleading inherited generic `sample_selection` label (“lexicographically first”) from previous Stage69/first-partition utility, even though `sampling_note`, actual GCS source URI and indexed selection were correct. Corrected **only the descriptive source provenance label** and added distinct source job counts in commit `0137d6a6ad1cb48c468fd29f9edb4dd5d8f88346` before the authoritative run; original sample rows, source hash, 256KiB/1MiB caps, source choice and criteria **unchanged**. Do not relabel a post-outcome provenance field correction as a new preregistered empirical study.
- Original 13-column schema, version Google2011 **v2.1**, includes event codes `SUBMIT=0`, `SCHEDULE=1`, `FAIL=3`, `FINISH=4`, `KILL=5`. Never use Google2019 v3 enum.

## Independently verified actual sampled source observations
| Quantity | Precisely observed in this 128-event contiguous prefix |
|---|---|
| Original real events audited | **128** (all with nonzero microsecond time) |
| Number of original unique job IDs | **11** |
| Distinct job/task ID pairs | **85** |
| Event `SUBMIT` | **33** |
| Event `SCHEDULE` | **36** |
| Event `FINISH` | **23** |
| Event `FAIL` | **28** |
| Event `KILL` | **8** |
| Missing machine ID | **36/128**; not converted to node 0 |
| Missing CPU request and nonempty `missing_info` | **0/128 each**, only within this selected prefix |
| Min timestamp | **1253400885155 microseconds** |
| Max timestamp | **1253403232545 microseconds** |
| Sampled temporal width | **2347390 microseconds = 2.347390s** |
| Matched `SUBMIT` followed by `SCHEDULE` on same source job/task ID | **12** |
| Unique jobs supplying these 12 matched cases | **2** |
| Matched first observed submit to next schedule gap, minimum | **2271807 microseconds = 2.271807s** |
| Median of these 12 gaps | **2272332.5 microseconds = 2.2723325s** |
| Matched gap, maximum | **2272691 microseconds = 2.272691s** |

**Important new post-outcome exploratory source-sequence check**: Independent raw-row event sequence analysis revealed that **all 12 matched pairs are resubmissions after an earlier terminal event within the same observed 128 rows**: **9** original per-task `FAIL → SUBMIT → SCHEDULE` sequences and **3** `KILL → SUBMIT → SCHEDULE` sequences. These represent **observed resubmission-to-rescheduling delays** under this narrow sample, **NOT the initial submission-to-first-placement queueing delay distribution** and NOT a generalized cluster latency estimate. Ten or more such events may share job/cluster incident context; only **two distinct jobs** supply the 12 matched examples. No causal claims about policy effects or observed physical service start follow. `SCHEDULE` denotes placement, not necessarily actual CPU-service start.

## Independent second original-bytes audit, not an independent sample
Independent source code `jpdc/audit_google2011_middle_original_bytes.py`, initial commit `ff5549e409ac2a701334c21f08302463469bfb2e`, directly reparses archived compressed original 256KiB gzip bytes with Python standard libraries and **does not import/call the source parser or download data anew**. It independently checks publisher GCS metadata/HTTP206, original source SHA, fixed13 columns, original audit checksum, 128 events counts, original timestamp range, 11 jobs, 85 task keys, 12 paired events across2 jobs, all stage65 negatives preserved. Initial [audit run43733872819](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43733872819) SUCCESS; after observing raw event sequences, added the explicit **retrospective descriptive** FAIL/KILL predecessor audit (not a change to source sampling or primary eligibility criterion), code commit **`93d1a36b8c77f3d2259615c152a04cba6b45360a`**.
- Final [**independent source-archive audit run43734005102**](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43734005102) **COMPLETE SUCCESS**, source SHA `93d1a36b8c77f3d2259615c152a04cba6b45360a`, artifact ID **14169373303**, ZIP digest sha256 **`48e2df09aacb286aa6513016d6fb9ce581a6ab3805eeabe899e8487df141fc90`**, downloaded and independently inspected. Audit JSON SHA256 **`10bd2a3237a41a5872a51b49a0e3ec968eebb94447a48db33bb641abcf4a587c`**, bytes match repeated independent audit JSON and stdout logs. The reparse of exact archival original row bytes confirmed 9 FAIL→SUBMIT→SCHEDULE, 3 KILL→SUBMIT→SCHEDULE, source 11 unique jobs and 2 unique paired jobs. No new source dataset downloaded for this independent check.

## Scientific inference and next decision
**New verified empirical result**: genuine Google 2011 task-event v2.1 rows at **nonzero timestamps** can be retrieved, source-verified and parsed; 12 matched observed resubmission-to-scheduling delays exist in the fixed sample with strong within-job dependence. This is a meaningful advance over the first128 initial all-zero events from partition0, but **does not establish a representative arrival-rate distribution, independent delay sample, physical CPU service, deadlines, per-task network bytes, or IIoT external validity**. This is a cross-domain real datacenter *observation* only, not an independent experimental scheduler result.

**Next most legitimate source study**: source-register a **wider, differently situated, still bounded** event window or a separate non-overlapping Google publisher partition and predeclare per-task longitudinal pairing, censoring treatment, resubmission/first-admission semantics, and source-job grouping. Make explicit time/source-period boundaries and deduplication for retried job/task keys. A representative workload would require a justified probabilistic sampling frame, not repeated cherry-picked 128-row samples. Do NOT manufacture "real deadline-aware IIoT" by adding synthetic network/deadlines and labeling them observed.

**Unresolved frozen blockers**: Stage65 prospective n8 PARTIAL method safety gate FAIL, CPU sign p1.000, NET p.125, harmed source seeds and six full-period adverse cells. Java CloudSimPlus SpaceShared↔Python strict FCFS 30k wait difference9.12140093294972ms>5ms FAIL; Stage56 native unfinished jobs FAIL; Stage61 full21 node0/4840 READY, sampled historical residual maxima not calibrated. Original FGCS E42/E4.6 and rejected Stage64 policy immutable. The absence of an independently proven robust scheduling method remains. Every subsequent material stage must update BOTH `jpdc/CHAT_RESTART_HANDOFF.md` and top of `jpdc/CURRENT_RESEARCH_HANDOFF.md`.
