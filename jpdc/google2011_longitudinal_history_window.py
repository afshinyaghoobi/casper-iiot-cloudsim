#!/usr/bin/env python3
"""Original publisher Google Borg v2.1 job/task event history within one fixed window.

No population estimates, physical CPU-service observation, network payload
measurement, IIoT domain or deadline-based policy experiment.
"""
import argparse
import collections
import csv
import hashlib
import io
import json
import re
import statistics
import urllib.parse
import urllib.request
import zlib
from pathlib import Path

BUCKET="clusterdata-2011-2"
KEY="task_events/part-00375-of-00500.csv.gz"
LIMIT_COMPRESSED=262144
LIMIT_INFLATED=1048576
SELECT_ROWS=1024
COLUMNS=13
CODES={0:"SUBMIT",1:"SCHEDULE",2:"EVICT",3:"FAIL",4:"FINISH",5:"KILL",
       6:"LOST",7:"UPDATE_PENDING",8:"UPDATE_RUNNING"}
TERMINAL={"EVICT","FAIL","FINISH","KILL","LOST"}
METADATA_URL=("https://storage.googleapis.com/storage/v1/b/"+BUCKET+
    "/o/"+urllib.parse.quote(KEY,safe="")+
    "?fields=name,bucket,generation,size,crc32c,md5Hash,updated")


def get_metadata():
    with urllib.request.urlopen(urllib.request.Request(
        METADATA_URL,headers={"User-Agent":"CASPER-JPDC-Google2011-Original-Window/1.0"}),timeout=30) as r:
        m=json.load(r)
    if m.get("name")!=KEY or m.get("bucket")!=BUCKET:
        raise ValueError("original GCS object metadata is not preregistered source")
    if not str(m.get("generation","")).isdigit() or int(m.get("size","0"))<LIMIT_COMPRESSED:
        raise ValueError("original GCS generation/size missing")
    return m


def get_prefix(metadata):
    url="https://storage.googleapis.com/"+BUCKET+"/"+KEY
    request=urllib.request.Request(url,headers={
        "Range":f"bytes=0-{LIMIT_COMPRESSED-1}",
        "Accept-Encoding":"identity",
        "User-Agent":"CASPER-JPDC-Google2011-Original-Window/1.0"})
    with urllib.request.urlopen(request,timeout=40) as resp:
        header=dict(http_status=resp.status,content_range=resp.headers.get("Content-Range"),
                    content_length=resp.headers.get("Content-Length"),etag=resp.headers.get("ETag"))
        raw=resp.read(LIMIT_COMPRESSED)
    if header["http_status"]!=206 or len(raw)!=LIMIT_COMPRESSED:
        raise ValueError("publisher did not provide exact frozen 256KiB HTTP206 range")
    if header["content_range"]!=f"bytes 0-{LIMIT_COMPRESSED-1}/{metadata['size']}":
        raise ValueError("publisher GCS original Content-Range mismatch")
    return raw,header


def parse_original_prefix(raw,metadata,http=None):
    if metadata.get("name")!=KEY or metadata.get("bucket")!=BUCKET:
        raise ValueError("wrong publisher source")
    if not str(metadata.get("generation","")).isdigit() or int(metadata["size"])<len(raw):
        raise ValueError("invalid original object metadata")
    if len(raw)!=LIMIT_COMPRESSED or raw[:2]!=b"\x1f\x8b":
        raise ValueError("original fixed compressed prefix is missing/bad gzip")
    decompressor=zlib.decompressobj(16+zlib.MAX_WBITS)
    inflated=decompressor.decompress(raw,LIMIT_INFLATED)
    final=inflated.rfind(b"\n")
    if final<0:
        raise ValueError("no full source CSV lines")
    lines=inflated[:final+1].decode("utf-8","strict")
    original=list(csv.reader(io.StringIO(lines,newline="")))
    if len(original)<SELECT_ROWS:
        raise ValueError("fewer than preregistered 1024 full source event rows")
    rows=original[:SELECT_ROWS]
    # Per-source-key state. One observed submit pairs with at most one schedule.
    observed=collections.defaultdict(list)
    pending={}
    groups=collections.Counter()
    count=collections.Counter()
    missing=collections.Counter()
    kinds=collections.Counter()
    submit_types=collections.Counter()
    matched_types=collections.Counter()
    gaps=collections.defaultdict(list)
    matched_source_jobs=collections.defaultdict(set)
    times=[]
    distinct_keys=set()
    duplicate_submit_pending=0
    terminal_with_schedule=0
    terminal_without_schedule=0
    # pending[k] = (submit_timestamp, submit_class)
    observed_scheduled=set()
    for idx,r in enumerate(rows):
        if len(r)!=COLUMNS:
            raise ValueError(f"source row {idx} has {len(r)} columns, expected 13")
        t=int(r[0]);job=int(r[2]);task=int(r[3]);ev=int(r[5])
        if t<0 or job<0 or task<0 or ev not in CODES:
            raise ValueError(f"invalid original v2.1 row {idx}")
        if times and t<times[-1]:
            raise ValueError("publisher event chronology not monotone")
        times.append(t)
        k=(job,task)
        distinct_keys.add(k)
        groups[job]+=1
        e=CODES[ev]
        kinds[e]+=1
        count["total"]+=1
        if r[1]!="":missing["nonempty_missing_info"]+=1
        if r[4]=="":missing["missing_machine_id"]+=1
        if r[9]=="":missing["missing_cpu_request"]+=1
        if r[10]=="":missing["missing_memory_request"]+=1
        if r[11]=="":missing["missing_disk_request"]+=1
        if e=="SUBMIT":
            previous=observed[k][-1] if observed[k] else None
            if previous is None:label="FIRST_OBSERVED_SUBMIT_LEFT_CENSORED"
            elif previous in TERMINAL:label="RESUBMIT_AFTER_OBSERVED_TERMINAL"
            else:label="SUBMIT_AFTER_OTHER_HISTORY"
            if k in pending:duplicate_submit_pending+=1
            pending[k]=(t,label)
            submit_types[label]+=1
            if previous in TERMINAL:submit_types["TERMINAL_PREDECESSOR_"+previous]+=1
            observed_scheduled.discard(k)
        elif e=="SCHEDULE":
            if k in pending:
                start,typ=pending.pop(k)
                if t<start:raise ValueError("schedule before observed submit")
                gap=t-start
                gaps[typ].append(gap)
                matched_source_jobs[typ].add(job)
                matched_types[typ]+=1
                matched_types["MATCHED_OBSERVED_SUBMIT_TO_SCHEDULE"]+=1
            else:
                matched_types["SCHEDULE_WITHOUT_OBSERVED_PENDING_SUBMIT"]+=1
            observed_scheduled.add(k)
        elif e in TERMINAL:
            if k in observed_scheduled:
                terminal_with_schedule+=1
            else:
                terminal_without_schedule+=1
            observed_scheduled.discard(k)
            # terminal closes any prior pending submit; count separately
            if k in pending:
                count["PENDING_SUBMIT_TERMINATED_WITHOUT_MATCHED_SCHEDULE"]+=1
                pending.pop(k)
        observed[k].append(e)
    summaries={}
    for key in ("FIRST_OBSERVED_SUBMIT_LEFT_CENSORED",
                "RESUBMIT_AFTER_OBSERVED_TERMINAL","SUBMIT_AFTER_OTHER_HISTORY"):
        values=gaps[key]
        summaries[key]=dict(count=len(values),
            distinct_source_jobs=len(matched_source_jobs[key]),
            min_us=min(values) if values else None,
            median_us=statistics.median(values) if values else None,
            max_us=max(values) if values else None)
    matched=matched_types["MATCHED_OBSERVED_SUBMIT_TO_SCHEDULE"]
    assert matched+matched_types["SCHEDULE_WITHOUT_OBSERVED_PENDING_SUBMIT"]==kinds["SCHEDULE"]
    assert sum(v["count"] for v in summaries.values())==matched
    assert sum(submit_types[x] for x in summaries)==kinds["SUBMIT"]
    return dict(status="PASS",
        source_type="OFFICIAL_GOOGLE_BORG_2011_DATACENTER_ORIGINAL_EVENT_ROWS",
        source_uri=f"gs://{BUCKET}/{KEY}",
        source_version="google_borg_2011_v2.1",
        storage_generation=str(metadata["generation"]),
        original_object_bytes=int(metadata["size"]),
        metadata_crc32c=metadata.get("crc32c"),metadata_md5=metadata.get("md5Hash"),
        original_http=http or {},
        compressed_original_prefix_bytes=len(raw),
        compressed_original_prefix_sha256=hashlib.sha256(raw).hexdigest(),
        inflated_source_bytes_examined=len(inflated),
        complete_rows_in_first_inflated_megabyte=len(original),
        original_rows_audited=len(rows),
        selection="FIRST_1024_ROWS_OF_PRESELECTED_PART375_NONREPRESENTATIVE",
        first_timestamp_us=times[0],last_timestamp_us=times[-1],
        temporal_width_us=times[-1]-times[0],
        nonzero_timestamp_rows=sum(v>0 for v in times),
        distinct_source_jobs=len(groups),
        distinct_job_task_keys=len(distinct_keys),
        source_job_event_group_sizes_desc=sorted(groups.values(),reverse=True),
        event_type_counts=dict(sorted(kinds.items())),
        missing_field_counts=dict(sorted(missing.items())),
        submit_classification_counts=dict(sorted(submit_types.items())),
        matched_schedule_classification_counts=dict(sorted(matched_types.items())),
        matched_submit_schedule_gap_descriptive_us=summaries,
        matched_gaps_distinct_jobs=len(set().union(*matched_source_jobs.values())) if matched_source_jobs else 0,
        duplicate_submit_while_pending=duplicate_submit_pending,
        right_censored_pending_submit_keys=len(pending),
        terminal_events_with_observed_schedule=terminal_with_schedule,
        terminal_events_without_observed_schedule=terminal_without_schedule,
        pending_submit_terminated_without_matched_schedule=
            count["PENDING_SUBMIT_TERMINATED_WITHOUT_MATCHED_SCHEDULE"],
        exploratory_nonzero_timestamp_gate=("PASS" if any(v>0 for v in times) else "FAIL"),
        exploratory_within_window_pair_gate=("PASS" if matched>0 else "FAIL"),
        first_observed_submit_may_be_lifetime_retry=True,
        schedule_is_not_physical_cpu_start=True,
        network_bytes_observed=False,real_task_deadlines_observed=False,
        factory_IIoT_trace=False,representative_random_trace_sample=False,
        independently_validated_scheduler_performance=False,
        original_Stage65_scientific_safety="FAIL",
        original_Java_Python_cross_runtime_fidelity="FAIL")


def main():
    cli=argparse.ArgumentParser()
    cli.add_argument("--out-dir",required=True)
    cli.add_argument("--reparse-only",action="store_true")
    a=cli.parse_args()
    d=Path(a.out_dir);d.mkdir(parents=True,exist_ok=True)
    if a.reparse_only:
        m=json.loads((d/"source_metadata.json").read_text())
        h=json.loads((d/"source_http.json").read_text())
        raw=(d/"original_prefix.gz").read_bytes()
    else:
        m=get_metadata()
        raw,h=get_prefix(m)
        (d/"original_prefix.gz").write_bytes(raw)
        (d/"source_metadata.json").write_text(json.dumps(m,indent=2,sort_keys=True)+"\n")
        (d/"source_http.json").write_text(json.dumps(h,indent=2,sort_keys=True)+"\n")
    result=parse_original_prefix(raw,m,h)
    (d/"audit.json").write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_GOOGLE2011_LONGITUDINAL_ORIGINAL",json.dumps(result,sort_keys=True))
    print("JPDC_GOOGLE2011_LONGITUDINAL_SOURCE_AND_CENSORING_AUDIT_PASS")

if __name__=="__main__":main()
