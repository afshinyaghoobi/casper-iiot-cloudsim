#!/usr/bin/env python3
"""One bounded publisher-original Google Borg 2011 v2.1 task_events prefix audit.

NEVER claim a representative trace, complete factory IIoT workload, or a
deadline-aware policy test from this row prefix.
"""
import argparse
import collections
import csv
import hashlib
import io
import json
import re
import urllib.parse
import urllib.request
import zlib
from pathlib import Path

BUCKET = "clusterdata-2011-2"
PREFIX = "task_events/"
MAX_COMPRESSED = 262144
MAX_INFLATED = 1048576
MAX_ROWS = 128
HEADERS = ("time_us","missing_info","job_id","task_index","machine_id",
           "event_type","user","scheduling_class","priority","cpu_request",
           "memory_request","disk_request","different_machine_constraint")
EVENT_NAMES = ("SUBMIT","SCHEDULE","EVICT","FAIL","FINISH","KILL","LOST",
               "UPDATE_PENDING","UPDATE_RUNNING")
STORAGE_LIST = "https://storage.googleapis.com/storage/v1/b/clusterdata-2011-2/o"


def verify_original_prefix(prefix, *, storage_metadata, request_metadata=None):
    if not prefix.startswith(b"\x1f\x8b"):
        raise ValueError("not an original gzip header")
    if len(prefix) > MAX_COMPRESSED or not prefix:
        raise ValueError("bounded compressed prefix violated")
    if storage_metadata.get("bucket") != BUCKET:
        raise ValueError("wrong original storage bucket")
    key = storage_metadata.get("name", "")
    if not re.fullmatch(r"task_events/part-\d{5}-of-\d{5}\.csv\.gz", key):
        raise ValueError("unexpected original publisher task_events object name")
    if not str(storage_metadata.get("generation", "")).isdigit():
        raise ValueError("missing GCS generation identifier")
    original_size = int(storage_metadata["size"])
    if original_size < len(prefix):
        raise ValueError("original object smaller than downloaded prefix")
    # Truncated gzip is expected. zlib incremental decode DOES NOT require
    # the gzip checksum trailer to have arrived inside our bounded prefix.
    inflater = zlib.decompressobj(16 + zlib.MAX_WBITS)
    # Bounded prefix streaming: a 256-KiB compressed source block may expand
    # beyond our 1-MiB safety quota. Consume AT MOST the allowed inflated
    # bytes without rejecting the original source for compressing well.
    inflated = inflater.decompress(prefix, MAX_INFLATED)
    if len(inflated) > MAX_INFLATED:
        raise ValueError("inflation quota exceeded")
    # Only full newline-terminated original records are examined; do not
    # decode or parse an incomplete final CSV row.
    last_newline = inflated.rfind(b"\n")
    if last_newline < 0:
        raise ValueError("no complete original CSV line within bounded prefix")
    complete = inflated[:last_newline + 1].decode("utf-8", "strict")
    records = list(csv.reader(io.StringIO(complete, newline="")))
    if not records:
        raise ValueError("no original rows")
    selected = records[:MAX_ROWS]
    events = collections.Counter()
    missing = collections.Counter()
    seen_times = []
    unique_tasks = set()
    observed_submit = 0
    for index, row in enumerate(selected):
        if len(row) != len(HEADERS):
            raise ValueError(f"original task_events row {index} unexpected column count {len(row)}")
        if not row[0] or not row[2] or not row[3] or not row[5]:
            raise ValueError(f"original row {index} missing essential time/task/event")
        when = int(row[0])
        job = int(row[2])
        task = int(row[3])
        event = int(row[5])
        if when < 0 or job < 0 or task < 0 or not 0 <= event < len(EVENT_NAMES):
            raise ValueError("invalid actual task event, ID or time")
        observed_submit += int(event == 0)
        events[EVENT_NAMES[event]] += 1
        seen_times.append(when)
        unique_tasks.add((job, task))
        if row[1] != "": missing["nonempty_missing_info"] += 1
        if row[4] == "": missing["missing_machine_id"] += 1
        if row[9] == "": missing["missing_cpu_request"] += 1
        if row[10] == "": missing["missing_memory_request"] += 1
        if row[11] == "": missing["missing_disk_request"] += 1
        if row[12] == "": missing["missing_diff_machine_constraint"] += 1
    # Event files are timestamp-sorted according to publisher format notes;
    # fails closed if prefix contradicts expected monotonic property.
    if seen_times != sorted(seen_times):
        raise ValueError("original source prefix timestamps not monotone")
    return {
        "status":"PASS", "classification":"ACTUAL_PRODUCTION_TRACE_EVENT_ROWS_ONLY",
        "source_public_object_uri":"gs://" + BUCKET + "/" + key,
        "publisher_dataset_version":"google_borg_2011_v2.1",
        "official_bucket":BUCKET, "original_storage_generation":str(storage_metadata["generation"]),
        "original_object_size_bytes":original_size,
        "original_storage_crc32c":storage_metadata.get("crc32c"),
        "original_storage_md5":storage_metadata.get("md5Hash"),
        "original_storage_updated":storage_metadata.get("updated"),
        "retrieval":request_metadata or {},
        "source_gzip_prefix_sha256":hashlib.sha256(prefix).hexdigest(),
        "source_gzip_prefix_bytes":len(prefix),
        "inflated_bytes_inspected":len(inflated),
        "complete_rows_available_in_prefix":len(records),
        "original_rows_audited":len(selected),
        "sample_selection":"FIRST_COMPLETE_ROWS_OF_LEXICOGRAPHICALLY_FIRST_ORIGINAL_PARTITION",
        "time_min_microseconds":min(seen_times),
        "time_max_microseconds":max(seen_times),
        "distinct_job_task_pairs":len(unique_tasks),
        "observed_submit_event_rows":observed_submit,
        "event_type_counts":dict(sorted(events.items())),
        "missing_field_counts":dict(sorted(missing.items())),
        "original_cpu_request_is_measured_service":False,
        "real_per_task_network_bytes_observed":False,
        "real_task_deadline_observed":False,
        "external_IIoT_workload_established":False,
        "independent_policy_performance_established":False,
        "complete_external_dispatch_dataset_admitted":False,
        "original_stage65_scientific_safety":"FAIL",
        "original_java_python_30k_parity":"FAIL",
    }


def original_storage_discover():
    query = urllib.parse.urlencode({"prefix": PREFIX, "maxResults": 100, "fields": "items(name,bucket,generation,size,crc32c,md5Hash,updated),nextPageToken"})
    request=urllib.request.Request(STORAGE_LIST+"?"+query,headers={"User-Agent":"CASPER-JPDC-Original-Trace-Audit/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        obj=json.load(response)
    candidates=[item for item in obj.get("items",[]) if
                re.fullmatch(r"task_events/part-\d{5}-of-\d{5}\.csv\.gz",item.get("name",""))]
    if not candidates:
        raise RuntimeError("publisher GCS object listing inaccessible or lacks task_events partitions; NO original rows admitted")
    return min(candidates,key=lambda v:v["name"])


def retrieve_prefix(obj):
    key = obj["name"]
    url = "https://storage.googleapis.com/"+BUCKET+"/"+urllib.parse.quote(key, safe="/")
    request=urllib.request.Request(url,headers={
        "Range":f"bytes=0-{MAX_COMPRESSED-1}",
        "Accept-Encoding":"identity",
        "User-Agent":"CASPER-JPDC-Original-Trace-Audit/1.0"})
    with urllib.request.urlopen(request,timeout=40) as response:
        code=response.status
        data=response.read(MAX_COMPRESSED)
        meta={"http_status":code,"content_range":response.headers.get("Content-Range"),
              "etag":response.headers.get("ETag"),"content_length":response.headers.get("Content-Length")}
    if code not in (200,206):
        raise RuntimeError("original source retrieval status is not HTTP 200/206")
    if not data:
        raise RuntimeError("empty original publisher response")
    return data,meta


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out-dir",required=True)
    p.add_argument("--reparse-only",action="store_true")
    a=p.parse_args()
    folder=Path(a.out_dir);folder.mkdir(parents=True,exist_ok=True)
    if a.reparse_only:
        raw=(folder/"original_prefix.gz").read_bytes()
        manifest=json.loads((folder/"original_storage.json").read_text())
        request=json.loads((folder/"original_http.json").read_text())
    else:
        manifest=original_storage_discover()
        raw,request=retrieve_prefix(manifest)
        (folder/"original_prefix.gz").write_bytes(raw)
        (folder/"original_storage.json").write_text(json.dumps(manifest,sort_keys=True,indent=2)+"\n")
        (folder/"original_http.json").write_text(json.dumps(request,sort_keys=True,indent=2)+"\n")
    report=verify_original_prefix(raw,storage_metadata=manifest,request_metadata=request)
    (folder/"audit.json").write_text(json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_ORIGINAL_GOOGLE2011_BOUNDED_TASK_EVENTS_AUDIT",json.dumps(report,sort_keys=True))
    print("JPDC_ORIGINAL_GOOGLE2011_REAL_ROWS_SOURCE_AUDIT_PASS")
