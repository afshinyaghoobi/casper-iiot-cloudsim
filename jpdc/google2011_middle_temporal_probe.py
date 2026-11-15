#!/usr/bin/env python3
"""Read ONE preregistered real GCS middle-partition prefix; offline source audit.

Never silently substitute another source, consume >256KiB compressed, or
claim a representative arrival distribution or IIoT deadline performance.
"""
import argparse
import collections
import csv
import hashlib
import io
import json
import statistics
import urllib.parse
import urllib.request
import zlib
from pathlib import Path

from google2011_original_bounded_rows import (
    BUCKET, MAX_COMPRESSED, MAX_INFLATED, MAX_ROWS, HEADERS, EVENT_NAMES,
    retrieve_prefix, verify_original_prefix
)

EXACT_KEY = "task_events/part-00250-of-00500.csv.gz"
METADATA_URL = ("https://storage.googleapis.com/storage/v1/b/" + BUCKET +
                "/o/" + urllib.parse.quote(EXACT_KEY, safe="") +
                "?fields=name,bucket,generation,size,crc32c,md5Hash,updated")


def fetch_exact_metadata():
    req = urllib.request.Request(METADATA_URL, headers={
        "User-Agent": "CASPER-JPDC-MIDDLE-TEMPORAL-AUDIT/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        doc = json.load(response)
    if doc.get("bucket") != BUCKET or doc.get("name") != EXACT_KEY:
        raise ValueError("official GCS metadata does not match preregistered target")
    if not str(doc.get("generation","")).isdigit() or int(doc.get("size","0")) < MAX_COMPRESSED:
        raise ValueError("invalid object generation/size")
    return doc


def same_original_records(prefix, storage):
    """Audit actual physical rows again to derive semantics beyond old parser."""
    base = verify_original_prefix(prefix, storage_metadata=storage)
    assert storage["name"] == EXACT_KEY
    assert len(prefix) == MAX_COMPRESSED
    inflated=zlib.decompressobj(16+zlib.MAX_WBITS).decompress(prefix,MAX_INFLATED)
    last=inflated.rfind(b"\n")
    if last<0:raise ValueError("no complete actual source records")
    all_rows=list(csv.reader(io.StringIO(
        inflated[:last+1].decode("utf-8","strict"),newline="")))
    sample=all_rows[:MAX_ROWS]
    assert len(sample)==MAX_ROWS
    assert all(len(x)==len(HEADERS) for x in sample)
    times=[];submit={};pairs=[];seen_events=collections.Counter()
    for i,row in enumerate(sample):
        event=int(row[5]);key=(int(row[2]),int(row[3]));at=int(row[0])
        if event<0 or event>=len(EVENT_NAMES):raise ValueError("wrong v2.1 event")
        seen_events[EVENT_NAMES[event]]+=1
        times.append(at)
        if event==0 and key not in submit:
            submit[key]=at
        elif event==1 and key in submit:
            if at<submit[key]:raise ValueError("SCHEDULE earlier than observed SUBMIT")
            pairs.append(dict(job_task_index_in_sample=i,
                submit_time_us=submit[key],schedule_time_us=at,
                schedule_minus_submit_us=at-submit[key]))
    assert times==sorted(times)
    assert dict(sorted(seen_events.items()))==base["event_type_counts"]
    if pairs:
        spans=[x["schedule_minus_submit_us"] for x in pairs]
        pair_stats=dict(count=len(pairs),min_us=min(spans),
                        max_us=max(spans),median_us=statistics.median(spans))
    else:
        pair_stats=dict(count=0,status="NO_PAIRED_SUBMIT_SCHEDULE_IN_PREFIX")
    return {
        **base,
        "sampling_note":"PURPOSEFULLY_SELECTED_MIDDLE_PARTITION_FIRST_128_ROWS_NOT_REPRESENTATIVE",
        "exact_preregistered_partition_index":250,
        "new_nonzero_temporal_source_event_count":sum(x>0 for x in times),
        "nonzero_time_exploratory_gate":(
            "PASS" if any(x>0 for x in times) else "NO_NONZERO_TEMPORAL_OBSERVATIONS"),
        "observed_schedule_rows":seen_events["SCHEDULE"],
        "observed_submit_rows":seen_events["SUBMIT"],
        "within_prefix_observed_submit_schedule_pairs":pair_stats,
        "physical_CPU_service_measurement_available":False,
        "first128_original_source_rows_not_an_independent_source_seed":True,
        "source_note":"No deadline, per-task measured network bytes or native Java scheduler validation",
    }


def main():
    cli=argparse.ArgumentParser()
    cli.add_argument("--out-dir",required=True)
    cli.add_argument("--reparse-only",action="store_true")
    args=cli.parse_args()
    target=Path(args.out_dir);target.mkdir(parents=True,exist_ok=True)
    if args.reparse_only:
        metadata=json.loads((target/"original_storage.json").read_text())
        http=json.loads((target/"original_http.json").read_text())
        raw=(target/"original_prefix.gz").read_bytes()
    else:
        metadata=fetch_exact_metadata()
        raw,http=retrieve_prefix(metadata)
        if http["http_status"]!=206 or len(raw)!=MAX_COMPRESSED:
            raise ValueError("original 206 byte range not honored for exact middle source")
        expected=f"bytes 0-{MAX_COMPRESSED-1}/{metadata['size']}"
        if http["content_range"]!=expected:
            raise ValueError("original GCS HTTP Content-Range does not match official size")
        (target/"original_storage.json").write_text(json.dumps(metadata,sort_keys=True,indent=2)+"\n")
        (target/"original_http.json").write_text(json.dumps(http,sort_keys=True,indent=2)+"\n")
        (target/"original_prefix.gz").write_bytes(raw)
    if metadata.get("name")!=EXACT_KEY:
        raise ValueError("expected exact preregistered object key")
    report=same_original_records(raw,metadata)
    report["original_GCS_HTTP"]=http
    report["exact_object_generation"]=str(metadata["generation"])
    (target/"audit.json").write_text(json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_GOOGLE2011_MIDDLE_ORIGINAL_PROVENANCE",
          json.dumps({key:report[key] for key in
              ("source_public_object_uri","source_gzip_prefix_sha256",
              "exact_object_generation","time_min_microseconds",
              "time_max_microseconds","new_nonzero_temporal_source_event_count",
              "observed_submit_rows","observed_schedule_rows",
              "within_prefix_observed_submit_schedule_pairs",
              "nonzero_time_exploratory_gate")},sort_keys=True))
    print("JPDC_GOOGLE2011_MIDDLE_REAL_SOURCE_PREFIX_AUDIT_PASS")


if __name__=="__main__":
    main()
