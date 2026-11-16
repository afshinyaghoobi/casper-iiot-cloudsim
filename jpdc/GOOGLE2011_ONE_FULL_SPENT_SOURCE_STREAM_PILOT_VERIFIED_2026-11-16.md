# VERIFIED — one full previously spent original Google Borg2011 task-events gzip streaming feasibility pilot (2026-11-16)

## Why this was the highest-value legitimate next check
The original Google Cloud Storage `task_events/` metadata-only census established exactly **500 original source files totaling 1,624,496,362 compressed bytes (1.512930GiB)**, but could not verify full file integrity, identify job/task keys across the files or measure streaming resources. This pilot froze **one already previously sampled** original partition `gs://clusterdata-2011-2/task_events/part-00375-of-00500.csv.gz`, avoiding any new independent scientific seed and avoiding all-500-file download. Goal: measured **whole source gzip** integrity, complete original source CSV rows and bounded memory/elapsed resource feasibility. No CASPER algorithm experiment.

**Prospective protocol** `jpdc/GOOGLE2011_COMPLETE_PART375_STREAM_PILOT_PREREG_2026-11-16.md` committed **de7978f4b4aac0811abdba47e335cd3ce69fa77a**, BEFORE first whole-file acquisition. Fixed original source GCS version **1416266880306000**, original compressed object size **1,502,643 bytes**, strict one-file source acquisition, <=128MiB uncompressed source, <=2,000,000 records, original source version Google 2011 v2.1, no source reselection on failures, full object SHA256/MD5/CRC32C publisher checks, one independently reparsed archived original artifact. Original E42 and frozen rejected Stage64 Git blobs protected. Previously used FIRST1024 source rows were already known from [original source run43735040240](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43735040240), and thus this is NOT an external confirmation cohort.

## Original full official source technical evidence
Source implementation `jpdc/google2011_full_spent_partition_stream_pilot.py` commit **34c6a073ca5bb43c7462a48330333413a1b36dd9**, checksum and synthetic test-only fixtures `jpdc/test_google2011_full_spent_partition_stream_pilot.py` commit **d0bb1b7c09f9496db5381f031d845f727a398364**. Source [**GitHub Actions run43928939896**](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43928939896) **COMPLETE SUCCESS** at source SHA **46970403eab2de84f84176649add0219c1ef4f70**. Original source-run artifact ID **14256968650**, `jpdc-google2011-part375-one-original-complete-gzip-pilot`, archive ZIP sha256 **bf1d00ecf941db5cbfef29410147c61543d7789ce83cd2d8437072960fc557c4**, downloaded and inspected from genuine GitHub Actions. The artifact preserves complete genuine source `original_full.gz`, publisher metadata, HTTP info, source audit and offline audit, and synthetic fixture stdout. The original genuine source compressed full object SHA256 **0ca3c532707d1a291228d59c75d7831d654cd330579a4dc9e32cfa0685783025**, original full metadata MD5 base64 **IzyU5Xp/vQFQAVWLrz3nGg==** and CRC32C base64 **U66X4w==**, compared to **all original downloaded compressed bytes** (not merely a 256KiB prefix); strict gzip terminal trailer integrity PASS. Original `source_audit.json` SHA256 **432162dda5f33b25ba5384c2fbb9953ba33c426f7004d25e1cd1bbd400d7e9ea**. Online source and offline reparse agree on scientific source fields; volatile benchmark time/RSS and source acquisition time intentionally not byte compared.

### Exact complete source measured observations (one original source file)
| Field | Actually verified from entire original part375 |
|---|---:|
| Complete original source event records | **130,812** |
| Original compressed file bytes | **1,502,643** |
| Complete uncompressed source CSV bytes | **14,973,713** |
| Original distinct job IDs within this one file | **1,838** |
| Original distinct `(job_id,task_index)` identities | **44,979** |
| Original event `SUBMIT` | **44,330** |
| Original event `SCHEDULE` | **44,290** |
| Original event `FINISH` | **26,802** |
| Original event `KILL` | **13,423** |
| Original event `FAIL` | **1,241** |
| Original event `EVICT` | **725** |
| Original event `UPDATE_RUNNING` | **1** |
| Missing source `machine_id` | **49,607 rows** |
| First time `time_us` | **1,879,800,290,193** |
| Last time `time_us` | **1,884,810,781,196** |
| Observed single-file time width | **5,010.491003 seconds (~83.51 min)** |
| Actual Github-hosted runner source GET wall time (one run) | **0.340783 seconds** |
| Original source full streaming parse elapsed (one run) | **0.295517 seconds** |
| Peak reported Linux runner RSS | **33,724 KiB (~32.93MiB)** |

Source pipeline reads one generation-pinned object; counts fields/events under bounds. `SCHEDULE` means recorded scheduler placement, NOT actual CPU execution start. `cpu_request` is resource request, not measured execution work. No per-task measured network transfer or original application deadline fields are available; original source sample is Google **datacenter**, NOT industrial IIoT field trace. Differences in full-file counts versus previous first1024 counts reflect **coverage**, not new policy efficacy. One fast GitHub runner execution is **NOT evidence** that all500 objects can be acquired in (500×0.3) seconds; network, bottlenecks, retries, and object sizes vary, and external egress/pricing was not verified.

## Independent original-byte replay: no additional source acquisition
An alternate `jpdc/audit_google2011_full_spent_source_independent.py` commit **cb03fa82b61b10e86565ff90aa2a749d2e53ccc4** independently uses Python gzip+CSV to read the **archived source full gzip to EOF**, checks original raw SHA256 and MD5 vs official metadata, complete event counts and original published source audit JSON hash, full source distinct jobs/task keys and first1024 historical controls, independently verifies uncompressed bytes, and does **not** import or call the initial source reader or acquire any GCS bytes. [**Original artifact-only independent run43929341145**](https://github.com/afshinyaghoobi/casper-iiot-cloudsim/actions/runs/43929341145) **COMPLETE SUCCESS**, source SHA **669d157c7575293fa1dec3ecafeefadc34144659**, audit artifact **14257572863**, ZIP sha256 **c33988080d8069c297d5d61c057ba44cf74f7d3a6ce44c48f6cb1b4728b9a05e**, downloaded and inspected. Independent `audit.json` SHA256 **4ecdd6f20fd03ad79bab6997b296e3a336dacb2d29e4a2e43d99b402eb343ac8**, audit_repeat identical bytes and log. **Technical/archived original source software verification PASS. No independent physical or dataset replication.** Both CI workflows check original E42 Git blob **34256ca7bff46f911cf20e8b94278fbd09175746** and Stage64 rejected-method blob **24d495dba4d29f8fe070ad6539b20361a7193cc6**, unchanged.

## Scientific implication and next nonredundant work
The original source-data streaming method has now processed and verified **one COMPLETE file** while maintaining source hash identity and modest runner resources. This materially de-risks a future **complete task_events 500-file job-key/time inventory** (~1.513GiB compressed), but does **NOT** approve the cost/consumption or validate its completeness. Before full execution, freeze a source-data ingestion budget/time/error-retry plan against all 500 exact publisher original object generations/checksums, avoid unnecessarily retaining raw full trace in public artifacts, use bounded on-disk/SQLite grouping rather than unlimited Python sets, plan per-file outputs with deterministic original metadata and cross-file job identifiers, and decide how to manage source-ID overlap across 17-day gaps and restart attempts. A full 500-file scan is a *large new data processing action* and should be explicitly authorized or conducted under preestablished resource quotas, NOT inferred to be free from this one pilot.

**No change to manuscript scientific outcome:** original Stage65 source-n8 `PARTIAL_MINIMAX_FULL_FALLBACK` prospective safety FAIL (CPU sign p1.000, network p0.125), original Python vs native Java queue waiting max gap9.12140093294972ms>5ms FAIL, Stage56 nine Java Cloudlets unfinished, Stage61 full21-node 0/4840 READY, original n10 FULL vs PRED_GREEDY no confirmed statistical benefit and sample maxima not conformal calibrated. Original FGCS E42/E4.6 untouched. This original full source pilot did not evaluate scheduler policies, CPU service, deadlines or network delays.

**Next priority:** prepare a fully documented low-risk 500-file complete-inventory algorithm with bounded memory/disk and verifiable source grouping, budget/time/staging/resume design and fail-closed checks; no new arbitrary 1024-prefix samples. Update both permanent handoff files with report and original/audit artifact provenance.
