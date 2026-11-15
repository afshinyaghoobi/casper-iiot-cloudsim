#!/usr/bin/env python3
"""Independent archival byte audit of preregistered Google2011 middle part250.

Uses NO imports from the acquisition program, no network access, no re-run of
the original production source and no synthetic observations.
"""
import argparse
import collections
import csv
import hashlib
import io
import json
import statistics
import zlib
from pathlib import Path

ORIGINAL_COMMIT="0137d6a6ad1cb48c468fd29f9edb4dd5d8f88346"
ORIGINAL_DATA_SHA="71a66cf47ea18b533e9f4adecca0965f1aad38fc3b668c85765609c05f1f51f5"
ORIGINAL_AUDIT_SHA="616fe2683696faf052bebe59bf076be97aa4d1dc4f4696ca4164cd83f1fbfaa8"
GCS_KEY="task_events/part-00250-of-00500.csv.gz"
EXPECTED_EVENTS={"SUBMIT":33,"SCHEDULE":36,"FINISH":23,"FAIL":28,"KILL":8}
EVENT_CODES={0:"SUBMIT",1:"SCHEDULE",2:"EVICT",3:"FAIL",4:"FINISH",5:"KILL",6:"LOST",
             7:"UPDATE_PENDING",8:"UPDATE_RUNNING"}


def independent_archive_audit(base):
    assert (base/"source_commit.txt").read_text().strip()==ORIGINAL_COMMIT
    original_bytes=(base/"original_prefix.gz").read_bytes()
    assert len(original_bytes)==262144
    assert hashlib.sha256(original_bytes).hexdigest()==ORIGINAL_DATA_SHA
    audit_bytes=(base/"audit.json").read_bytes()
    assert audit_bytes==(base/"audit_first.json").read_bytes()
    assert hashlib.sha256(audit_bytes).hexdigest()==ORIGINAL_AUDIT_SHA
    original=json.loads(audit_bytes)
    source=json.loads((base/"original_storage.json").read_text())
    headers=json.loads((base/"original_http.json").read_text())
    assert source["bucket"]=="clusterdata-2011-2"
    assert source["name"]==GCS_KEY
    assert source["generation"]=="1416266806161000"
    assert source["size"]=="4715492"
    assert headers["http_status"]==206
    assert headers["content_range"]=="bytes 0-262143/4715492"

    # Reinterpret compressed raw source independently from archived bytes:
    # don't call the original source parser or follow an arbitrary row summary.
    d=zlib.decompressobj(16+zlib.MAX_WBITS).decompress(original_bytes,1048576)
    assert len(d)==1048576
    last=d.rfind(b"\n")
    assert last>=0
    rows=list(csv.reader(io.StringIO(d[:last+1].decode("utf-8"))))[:128]
    assert len(rows)==128 and all(len(row)==13 for row in rows)
    times=[]
    events=collections.Counter()
    missing=collections.Counter()
    job_ids=set()
    keys=set()
    first_submit={}
    paired={}
    prior_types=collections.defaultdict(list)
    submit_predecessor={}
    for index,row in enumerate(rows):
        t=int(row[0]);job=int(row[2]);task=int(row[3]);kind=int(row[5])
        assert t>=0 and job>=0 and task>=0 and kind in EVENT_CODES
        times.append(t)
        job_ids.add(job)
        key=(job,task)
        keys.add(key)
        events[EVENT_CODES[kind]]+=1
        if row[1]!="":missing["nonempty_missing_info"]+=1
        if row[4]=="":missing["missing_machine_id"]+=1
        if row[9]=="":missing["missing_cpu_request"]+=1
        if kind==0 and key not in first_submit:
            first_submit[key]=t
            submit_predecessor[key]=prior_types[key][-1] if prior_types[key] else None
        elif kind==1 and key in first_submit and key not in paired:
            assert t>=first_submit[key]
            paired[key]=t-first_submit[key]
        prior_types[key].append(kind)
    assert times==sorted(times)
    assert events==EXPECTED_EVENTS
    assert len(keys)==85 and len(job_ids)==11
    assert len(first_submit)>=len(paired)==12
    assert len({j for j,_ in paired})==2
    assert missing["missing_machine_id"]==36
    assert all(v>0 for v in times)
    assert times[0]==1253400885155 and times[-1]==1253403232545
    spans=list(paired.values())
    # This is retrospective within the already selected original 128 rows.
    # Each observed SUBMIT->SCHEDULE is a resubmission after FAIL/KILL,
    # not evidence of the task's first-ever queue admission.
    predecessor_counts=collections.Counter(
        EVENT_CODES[submit_predecessor[k]] if submit_predecessor[k] is not None
        else "NO_PRIOR_EVENT_WITHIN_PREFIX" for k in paired)
    assert predecessor_counts=={"FAIL":9,"KILL":3}
    assert min(spans)==2271807 and max(spans)==2272691
    assert statistics.median(spans)==2272332.5
    assert original["sample_selection"]=="FIRST_128_COMPLETE_ROWS_OF_PREREGISTERED_PARTITION_INDEX_250"
    assert original["sampled_distinct_job_ids"]==11
    assert original["observed_pair_distinct_job_ids"]==2
    assert original["within_prefix_observed_submit_schedule_pairs"]["count"]==len(spans)
    assert original["within_prefix_observed_submit_schedule_pairs"]["median_us"]==statistics.median(spans)
    assert original["original_stage65_scientific_safety"]=="FAIL"
    assert original["original_java_python_30k_parity"]=="FAIL"
    assert not original["real_task_deadline_observed"]
    assert not original["real_per_task_network_bytes_observed"]
    assert not original["complete_external_dispatch_dataset_admitted"]
    return dict(
        status="PASS",provenance="ORIGINAL_GCS_MIDDLE_PART250_ARCHIVED_GZIP_BYTES",
        original_commit=ORIGINAL_COMMIT,
        raw_original_prefix_sha256=ORIGINAL_DATA_SHA,
        original_audit_sha256=ORIGINAL_AUDIT_SHA,
        source_gcs_key=GCS_KEY,
        additional_external_source_rows_retrieved=0,
        rows_reparsed=128,distinct_jobs=11,distinct_task_id_pairs=85,
        event_counts=dict(sorted(events.items())),
        nonzero_timestamp_rows=sum(t>0 for t in times),
        timestamp_min_us=min(times),timestamp_max_us=max(times),
        observed_matching_submit_schedule_pairs=len(spans),
        matching_pairs_distinct_jobs=2,
        matching_submit_predecessor_event_counts=dict(sorted(predecessor_counts.items())),
        all_12_pairs_are_resubmits_after_prior_fail_or_kill=True,
        first_ever_submission_delay_not_established=True,
        observed_schedule_minus_submit_median_us=statistics.median(spans),
        observed_schedule_minus_submit_min_us=min(spans),
        observed_schedule_minus_submit_max_us=max(spans),
        observed_schedule_minus_submit_not_cpu_start=True,
        no_population_arrival_rate_inference=True,
        no_independent_source_seed_claim=True,
        no_observed_deadline_or_network_bytes=True,
        scientific_stage65_safety="FAIL",
        original_java_python_queue_fidelity="FAIL")


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original-dir",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    result=independent_archive_audit(Path(a.original_dir))
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print("JPDC_GOOGLE2011_MIDDLE_INDEPENDENT_ARCHIVAL_AUDIT",json.dumps(result,sort_keys=True))
    print("JPDC_GOOGLE2011_MIDDLE_ORIGINAL_BYTES_SECOND_PARSER_PASS")
