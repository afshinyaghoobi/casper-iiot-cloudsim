#!/usr/bin/env python3
"""Independent original Google2011 source-identity lifecycle & split safety gate.

Runs on exact ORIGINAL archived gzip bytes only, not the original source
parser, not a new dataset, and not a source-independent scheduler trial.
"""
import argparse
import collections
import csv
import hashlib
import io
import json
import zlib
from pathlib import Path

GCS_KEYS=("task_events/part-00125-of-00500.csv.gz",
          "task_events/part-00425-of-00500.csv.gz")
ORIGINAL_COHORT_SHA256="cdaa040a3f02efac37779c8edbf0a8a0b46d01e39a5f8ac3c70d33eb5675efc5"
ORIGINAL_PREFIX_HASHES=(
    "0b1db05d81b085b5a1c3b456605e7976dde8793e8a4895e587e129988c58c604",
    "5a600640ddf5a137e776f524995365595e73398fa8049c23888c859c9851c6ff")
PUBLISHER_DOCUMENTED_RESTART_JOB=6253771429
EVENT_NAMES=("SUBMIT","SCHEDULE","EVICT","FAIL","FINISH","KILL","LOST",
             "UPDATE_PENDING","UPDATE_RUNNING")


def split_gate(group_sets, *, complete_frames_verified=False,
               temporal_embargo_verified=False):
    """Never certify a full, disjoint source cohort from prefix evidence alone."""
    if len(group_sets)<2:
        raise ValueError("need >=2 cohorts")
    normalized=[set(group) for group in group_sets]
    intersections=set()
    for a in range(len(normalized)):
        for b in range(a+1,len(normalized)):
            intersections.update(normalized[a]&normalized[b])
    job_disjoint_in_supplied_records=not intersections
    full_source_ready=(job_disjoint_in_supplied_records and
                       complete_frames_verified and temporal_embargo_verified)
    return dict(
        observed_shared_jobs=len(intersections),
        job_disjoint_in_supplied_records=job_disjoint_in_supplied_records,
        full_source_job_disjointness_certified=bool(full_source_ready),
        split_status=("FULL_SOURCE_SPLIT_CERTIFIED" if full_source_ready
                      else "NOT_CERTIFIED_FOR_INDEPENDENT_HOLDOUT"),
        warning="Unknown entire-job lifecycle and right/left-censoring when frames are only prefixes")


def original_rows(path,source_index):
    source=path/f"source_{source_index}"
    m=json.loads((source/"metadata.json").read_text())
    h=json.loads((source/"http.json").read_text())
    if m["name"]!=GCS_KEYS[source_index] or m["bucket"]!="clusterdata-2011-2":
        raise AssertionError("source identity differs from fixed Google original")
    if h["status"]!=206 or h["content_range"]!=f"bytes 0-262143/{m['size']}":
        raise AssertionError("original Google source range mismatch")
    raw=(source/"original_prefix.gz").read_bytes()
    if len(raw)!=262144 or hashlib.sha256(raw).hexdigest()!=ORIGINAL_PREFIX_HASHES[source_index]:
        raise AssertionError("original source compressed SHA or bytes altered")
    decompressor=zlib.decompressobj(16+zlib.MAX_WBITS)
    plain=decompressor.decompress(raw,1048576)
    stop=plain.rfind(b"\n")
    if stop<0:raise ValueError("no complete original CSV")
    records=list(csv.reader(io.StringIO(plain[:stop+1].decode("utf-8"),newline="")))[:1024]
    if len(records)!=1024:raise ValueError("not full fixed source cohort")
    byjob=collections.defaultdict(lambda:dict(indices=set(),events=collections.Counter(),times=[]))
    timestamps=[]
    for row in records:
        if len(row)!=13:raise ValueError("expected v2.1 13-field original")
        time=int(row[0]);job=int(row[2]);task=int(row[3]);ev=int(row[5])
        if min(time,job,task)<0 or not 0<=ev<=8:raise ValueError("malformed original event")
        if timestamps and time<timestamps[-1]:raise ValueError("out-of-order source time")
        timestamps.append(time)
        state=byjob[job]
        state["indices"].add(task)
        state["events"][EVENT_NAMES[ev]]+=1
        state["times"].append(time)
    return dict(byjob=byjob,times=timestamps,
                compressed_prefix_sha256=ORIGINAL_PREFIX_HASHES[source_index],
                original_generation=str(m["generation"]))


def audit(path):
    rawcohort=(path/"cohort.json").read_bytes()
    if rawcohort!=(path/"cohort_original.json").read_bytes():
        raise AssertionError("source first/offline cohort bytes differ")
    if hashlib.sha256(rawcohort).hexdigest()!=ORIGINAL_COHORT_SHA256:
        raise AssertionError("original validated cohort differs")
    prior=json.loads(rawcohort)
    src=[original_rows(path,i) for i in range(2)]
    common=set(src[0]["byjob"])&set(src[1]["byjob"])
    repeated_keys=sum(len(src[0]["byjob"][j]["indices"]&
                          src[1]["byjob"][j]["indices"]) for j in common)
    if len(common)!=prior["shared_job_id_count"] or repeated_keys!=prior["shared_job_task_id_count"]:
        raise AssertionError("original-source intersection differs")
    if len(common)!=2 or repeated_keys!=27:
        raise AssertionError("unexpected original source data")
    first=src[0]["times"];second=src[1]["times"]
    temporal_overlap=max(first[0],second[0])<=min(first[-1],second[-1])
    assert not temporal_overlap
    gap=max(first[0]-second[-1],second[0]-first[-1])
    if gap!=prior["selected_timestamp_intervals_min_gap_us"]:
        raise AssertionError("source temporal gap differs")
    shared_details=[]
    for j in sorted(common):
        x=src[0]["byjob"][j]
        y=src[1]["byjob"][j]
        shared_details.append(dict(
            anonymized_job_id_sha256=hashlib.sha256(str(j).encode("ascii")).hexdigest(),
            published_known_exception=(j==PUBLISHER_DOCUMENTED_RESTART_JOB),
            shared_task_indexes=len(x["indices"]&y["indices"]),
            per_source=[dict(unique_task_indices=len(q["indices"]),
                recorded_event_types=dict(sorted(q["events"].items())),
                first_observed_time_us=min(q["times"]),
                last_observed_time_us=max(q["times"])) for q in (x,y)]))
    gate=split_gate([src[0]["byjob"],src[1]["byjob"]],
        complete_frames_verified=False,temporal_embargo_verified=False)
    assert not gate["job_disjoint_in_supplied_records"]
    assert not gate["full_source_job_disjointness_certified"]
    return dict(
        status="PASS",kind="RECOMPUTED_FROM_FIXED_ORIGINAL_ARCHIVED_GCS_BYTES",
        full_trace_identifier_uniqueness_proved=False,
        original_cohort_sha256=ORIGINAL_COHORT_SHA256,
        original_source_prefix_hashes=list(ORIGINAL_PREFIX_HASHES),
        source_gcs_keys=list(GCS_KEYS),
        original_gcs_generations=[x["original_generation"] for x in src],
        original_records_reparsed=2048,
        observed_time_windows_overlap=temporal_overlap,
        observed_time_gap_microseconds=gap,
        overlapping_source_job_count=len(common),
        overlapping_source_job_task_count=repeated_keys,
        shared_jobs_with_shared_task_indexes=sum(d["shared_task_indexes"]>0 for d in shared_details),
        publisher_documented_restart_job_id=PUBLISHER_DOCUMENTED_RESTART_JOB,
        publisher_documented_restart_id_in_observed_intersection=(
            PUBLISHER_DOCUMENTED_RESTART_JOB in common),
        source_ID_recurrence_cause="UNRESOLVED_FROM_THESE_PREFIXES",
        per_shared_job=shared_details,
        independence_gate=gate,
        no_new_gcs_download=True,
        no_sched_algorithm_or_iiot_validation=True,
        original_stage65_safety="FAIL",
        original_java_python_parity="FAIL")


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original-dir",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    result=audit(Path(a.original_dir))
    f=Path(a.out);f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print("JPDC_2011_JOB_LIFECYCLE_INDEPENDENT_ORIGINAL_SOURCE",
          json.dumps(result,sort_keys=True))
    print("JPDC_2011_JOB_IDENTITY_AND_SPLIT_FAIL_CLOSED_PASS")
