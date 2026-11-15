#!/usr/bin/env python3
"""Two exactly preregistered original GCS Google2011 source-prefix overlap checks.

File indices are NOT independent statistical source seeds. The original
1024-row state-machine utility is reused without changing its source.
"""
import argparse
import csv
import hashlib
import io
import json
import urllib.parse
import urllib.request
import zlib
from pathlib import Path
import google2011_longitudinal_history_window as original

KEYS=("task_events/part-00125-of-00500.csv.gz",
      "task_events/part-00425-of-00500.csv.gz")
BUCKET="clusterdata-2011-2"
MAX_COMPRESSED=262144
MAX_INFLATED=1048576
ROWS=1024


def original_rows(raw):
    if len(raw)!=MAX_COMPRESSED:raise ValueError("bad original prefix size")
    decoded=zlib.decompressobj(16+zlib.MAX_WBITS).decompress(raw,MAX_INFLATED)
    pos=decoded.rfind(b"\n")
    if pos<0:raise ValueError("no complete original CSV")
    data=list(csv.reader(io.StringIO(decoded[:pos+1].decode("utf-8"),newline="")))
    if len(data)<ROWS:raise ValueError("not enough complete original rows")
    first=data[:ROWS]
    if any(len(row)!=13 for row in first):raise ValueError("wrong v2.1 schema")
    keys=set()
    jobs=set()
    times=[]
    for r in first:
        time=int(r[0]); job=int(r[2]); task=int(r[3]); code=int(r[5])
        if min(time,job,task)<0 or code not in range(9):
            raise ValueError("invalid v2.1 original row")
        if times and time<times[-1]:raise ValueError("timestamps out of order")
        times.append(time)
        keys.add((job,task))
        jobs.add(job)
    return dict(jobs=jobs,keys=keys,times=times,complete_lines=len(data))


def exact_gcs_metadata(key):
    url=("https://storage.googleapis.com/storage/v1/b/"+BUCKET+"/o/"+
         urllib.parse.quote(key,safe="")+
         "?fields=name,bucket,generation,size,crc32c,md5Hash,updated")
    req=urllib.request.Request(url,headers={"User-Agent":"JPDC-Original-Trace-Cross-Partition/1.0"})
    with urllib.request.urlopen(req,timeout=30) as r: doc=json.load(r)
    if doc.get("name")!=key or doc.get("bucket")!=BUCKET:
        raise ValueError("publisher metadata source mismatch")
    if not str(doc.get("generation","")).isdigit() or int(doc.get("size","0"))<MAX_COMPRESSED:
        raise ValueError("publisher original metadata invalid")
    return doc


def download_exact(key,meta):
    url="https://storage.googleapis.com/"+BUCKET+"/"+key
    req=urllib.request.Request(url,headers={
        "Range":f"bytes=0-{MAX_COMPRESSED-1}",
        "Accept-Encoding":"identity","User-Agent":"JPDC-Original-Trace-Cross-Partition/1.0"})
    with urllib.request.urlopen(req,timeout=40) as r:
        headers=dict(status=r.status,content_range=r.headers.get("Content-Range"),
                     content_length=r.headers.get("Content-Length"),etag=r.headers.get("ETag"))
        raw=r.read(MAX_COMPRESSED)
    if headers["status"]!=206 or headers["content_range"]!=(
        f"bytes 0-{MAX_COMPRESSED-1}/{meta['size']}") or len(raw)!=MAX_COMPRESSED:
        raise ValueError("original fixed range not honored")
    return raw,headers


def run(directory,offline):
    summary=[]
    extracted=[]
    for index,key in enumerate(KEYS):
        dest=directory/f"source_{index}"
        dest.mkdir(parents=True,exist_ok=True)
        if offline:
            meta=json.loads((dest/"metadata.json").read_text())
            http=json.loads((dest/"http.json").read_text())
            raw=(dest/"original_prefix.gz").read_bytes()
        else:
            meta=exact_gcs_metadata(key)
            raw,http=download_exact(key,meta)
            (dest/"metadata.json").write_text(json.dumps(meta,sort_keys=True,indent=2)+"\n")
            (dest/"http.json").write_text(json.dumps(http,sort_keys=True,indent=2)+"\n")
            (dest/"original_prefix.gz").write_bytes(raw)
        if meta.get("name")!=key or meta.get("bucket")!=BUCKET:
            raise ValueError("wrong selected source")
        if http["status"]!=206 or http["content_range"]!=(
            f"bytes 0-{MAX_COMPRESSED-1}/{meta['size']}"):
            raise ValueError("original source content range mismatch")
        # Existing source state machine remains unchanged and is scoped
        # by the exact selected publisher key per call.
        before=original.KEY
        try:
            original.KEY=key
            detail=original.parse_original_prefix(raw,meta,http)
        finally:
            original.KEY=before
        indep=original_rows(raw)
        if detail["first_timestamp_us"]!=indep["times"][0] or (
            detail["last_timestamp_us"]!=indep["times"][-1]):
            raise AssertionError("original temporal result differs from reparse")
        if detail["distinct_source_jobs"]!=len(indep["jobs"]) or (
            detail["distinct_job_task_keys"]!=len(indep["keys"])):
            raise AssertionError("original key count differs from reparse")
        if detail["original_rows_audited"]!=ROWS:
            raise AssertionError("original selected row count")
        detail["selection"]="FIRST_1024_COMPLETE_ROWS_OF_FIXED_GCS_FILE_"+str(index)
        detail["source_not_independent_scientific_seed"]=True
        (dest/"source_audit.json").write_text(json.dumps(detail,sort_keys=True,indent=2)+"\n")
        summary.append(dict(source=key,source_generation=str(meta["generation"]),
            source_prefix_sha256=hashlib.sha256(raw).hexdigest(),
            timestamp_min_us=indep["times"][0],timestamp_max_us=indep["times"][-1],
            observed_jobs=len(indep["jobs"]),observed_job_task_keys=len(indep["keys"]),
            event_counts=detail["event_type_counts"],
            observed_submit_types=detail["submit_classification_counts"],
            source_missing=detail["missing_field_counts"],
            visible_submit_schedule_pairs=detail[
                "matched_schedule_classification_counts"].get(
                    "MATCHED_OBSERVED_SUBMIT_TO_SCHEDULE",0),
            visible_left_censored_schedules=detail[
                "matched_schedule_classification_counts"].get(
                    "SCHEDULE_WITHOUT_OBSERVED_PENDING_SUBMIT",0),
            pending_right_censored=detail["right_censored_pending_submit_keys"]))
        extracted.append(indep)
    a,b=extracted
    intersection_jobs=a["jobs"]&b["jobs"]
    intersection_keys=a["keys"]&b["keys"]
    overlap=max(a["times"][0],b["times"][0])<=min(a["times"][-1],b["times"][-1])
    if intersection_keys:
        result="OBSERVED_JOB_TASK_KEY_OVERLAP"
    elif intersection_jobs:
        result="OBSERVED_JOB_ID_OVERLAP"
    elif overlap:
        result="TIMESTAMP_WINDOWS_OVERLAP_NO_OBSERVED_JOB_ID_OVERLAP"
    else:
        result="NO_OBSERVED_JOB_ID_OR_TIME_OVERLAP_IN_SELECTED_PREFIXES"
    gap_us=0 if overlap else max(b["times"][0]-a["times"][-1],
                                a["times"][0]-b["times"][-1])
    return dict(status="PASS",verification="ORIGINAL_GOOGLE_GCS_TWO_FILE_SOURCE_PREFIXES",
        frozen_source_keys=list(KEYS),
        source_rows_per_file=ROWS,total_original_event_rows_examined=ROWS*2,
        all_data_from_one_original_2011_datacenter_trace=True,
        sources=summary,shared_job_id_count=len(intersection_jobs),
        shared_job_task_id_count=len(intersection_keys),
        selected_timestamp_intervals_overlap=overlap,
        selected_timestamp_intervals_min_gap_us=gap_us,
        sampled_overlap_classification=result,
        full_partition_job_independence="UNRESOLVED_FULL_SOURCE_INDEPENDENCE",
        prefixes_not_independent_holdout_seed=True,
        no_statistical_population_claim=True,
        no_real_network_or_deadline_fields=True,
        no_new_scheduling_policy_experiment=True,
        original_stage65_safety="FAIL",
        original_java_python_cross_runtime_parity="FAIL")


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out-dir",required=True)
    p.add_argument("--reparse-only",action="store_true")
    args=p.parse_args()
    directory=Path(args.out_dir);directory.mkdir(parents=True,exist_ok=True)
    result=run(directory,args.reparse_only)
    (directory/"cohort.json").write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print("JPDC_GOOGLE2011_SOURCE_TWO_FILE_OVERLAP",json.dumps(result,sort_keys=True))
    print("JPDC_GOOGLE2011_TWO_PARTITION_ORIGINAL_SOURCE_AUDIT_PASS")
