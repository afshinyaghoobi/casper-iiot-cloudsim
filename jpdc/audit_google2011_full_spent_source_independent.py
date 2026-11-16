#!/usr/bin/env python3
"""Independent original full Google2011 spent part375 byte parser.

NO import of source parser, NO live GCS, NO new sampling, NO actual scheduler
efficacy claim. Original publisher MD5 plus SHA and historical events checked.
"""
import argparse
import base64
import collections
import csv
import gzip
import hashlib
import json
from pathlib import Path

SOURCE_COMMIT="46970403eab2de84f84176649add0219c1ef4f70"
FULL_SOURCE_SHA="0ca3c532707d1a291228d59c75d7831d654cd330579a4dc9e32cfa0685783025"
ORIGINAL_AUDIT_SHA="432162dda5f33b25ba5384c2fbb9953ba33c426f7004d25e1cd1bbd400d7e9ea"
GENERATION="1416266880306000"
EVENTS=("SUBMIT","SCHEDULE","EVICT","FAIL","FINISH","KILL","LOST",
        "UPDATE_PENDING","UPDATE_RUNNING")


def audit(folder):
    if (folder/"source_commit.txt").read_text().strip()!=SOURCE_COMMIT:
        raise ValueError("wrong original CI commit")
    raw=(folder/"original_full.gz").read_bytes()
    if len(raw)!=1502643 or hashlib.sha256(raw).hexdigest()!=FULL_SOURCE_SHA:
        raise ValueError("original full file absent or source hash changed")
    meta=json.loads((folder/"source_metadata.json").read_text())
    if (meta["name"]!="task_events/part-00375-of-00500.csv.gz" or
        str(meta["generation"])!=GENERATION or int(meta["size"])!=len(raw)):
        raise ValueError("original GCS source metadata mismatch")
    if base64.b64encode(hashlib.md5(raw).digest()).decode()!=meta["md5Hash"]:
        raise ValueError("original whole-gzip MD5 disagrees")
    original_bytes=(folder/"source_audit.json").read_bytes()
    if hashlib.sha256(original_bytes).hexdigest()!=ORIGINAL_AUDIT_SHA:
        raise ValueError("original first auditor JSON altered")
    original=json.loads(original_bytes)
    count=0
    types=collections.Counter()
    missing_machine=0
    missing_cpu=0
    jobs=set()
    job_tasks=set()
    earliest=latest=previous=None
    prefix=collections.Counter()
    uncompressed=0
    # Independent CSV iterator; decompress full member through EOF, verifying
    # gzip trailer independently rather than reusing source code.
    with gzip.open(folder/"original_full.gz","rt",encoding="utf-8",newline="") as f:
        for row in csv.reader(f):
            if len(row)!=13:raise ValueError("original malformed v2.1 CSV record")
            t=int(row[0]);job=int(row[2]);task=int(row[3]);event=int(row[5])
            if min(t,job,task)<0 or event not in range(9) or (previous is not None and t<previous):
                raise ValueError("invalid source original event")
            if earliest is None:earliest=t
            previous=latest=t
            jobs.add(job);job_tasks.add((job,task))
            types[EVENTS[event]]+=1
            missing_machine+=int(not row[4])
            missing_cpu+=int(not row[9])
            count+=1
            if count<=1024:prefix[EVENTS[event]]+=1
            if count>2000000:raise ValueError("stream exceeds prereg row limit")
    # Byte size from a second streaming gzip decompression. The data are a
    # single ~15MB plaintext file; no more than prereg 128MB read.
    with gzip.open(folder/"original_full.gz","rb") as f:
        while True:
            chunk=f.read(65536)
            if not chunk:break
            uncompressed+=len(chunk)
            if uncompressed>128*1024*1024:raise ValueError("full stream inflation > cap")
    expected=dict(SUBMIT=44330,SCHEDULE=44290,FINISH=26802,KILL=13423,
                  FAIL=1241,EVICT=725,UPDATE_RUNNING=1)
    assert types==expected
    assert count==130812
    assert len(jobs)==1838
    assert len(job_tasks)==44979
    assert (earliest,latest)==(1879800290193,1884810781196)
    assert missing_machine==49607
    assert prefix=={"SUBMIT":355,"SCHEDULE":331,"KILL":169,
                    "FINISH":152,"FAIL":9,"EVICT":8}
    checks={
        "observed_full_original_source_row_count":count,
        "uncompressed_bytes":uncompressed,
        "distinct_original_job_ids":len(jobs),
        "distinct_original_job_task_keys":len(job_tasks),
        "event_type_counts":dict(sorted(types.items())),
        "min_timestamp_us":earliest,
        "max_timestamp_us":latest,
        "original_compressed_sha256":FULL_SOURCE_SHA,
    }
    for key,value in checks.items():
        if original[key]!=value:raise AssertionError("archived original report inconsistent: "+key)
    if original["missing_counts"]["missing_machine_id"]!=missing_machine:
        raise AssertionError("original missing machine count mismatch")
    if original["stage65_safety"]!="FAIL" or original["java_python_parity"]!="FAIL":
        raise AssertionError("original frozen negatives disappeared")
    return dict(status="PASS",classification="INDEPENDENT_REPARSE_OF_EXACT_ARCHIVED_ORIGINAL_BYTES",
        original_GCS_source_file="gs://clusterdata-2011-2/task_events/part-00375-of-00500.csv.gz",
        original_generation=GENERATION,
        original_full_gzip_SHA256=FULL_SOURCE_SHA,
        original_source_report_SHA256=ORIGINAL_AUDIT_SHA,
        original_complete_event_rows=count,
        original_unique_jobs=len(jobs),
        original_unique_job_task_keys=len(job_tasks),
        source_event_types=dict(sorted(types.items())),
        original_uncompressed_bytes=uncompressed,
        complete_source_gzip_trailer_verified=True,
        raw_source_and_report_consistent=True,
        source_independent_confirmatory_sample=False,
        complete_500_file_job_inventory_done=False,
        IIoT_network_and_real_deadline_observed=False,
        frozen_stage65_safety="FAIL",
        frozen_java_python_queue_parity="FAIL")


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original-dir",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    output=audit(Path(a.original_dir))
    d=Path(a.out);d.parent.mkdir(parents=True,exist_ok=True)
    d.write_text(json.dumps(output,indent=2,sort_keys=True)+"\n")
    print("JPDC_INDEPENDENT_SPENT_GOOGLE_FULL_GZIP_AUDIT",json.dumps(output,sort_keys=True))
    print("JPDC_INDEPENDENT_GOOGLE_ORIGINAL_FULL_GZIP_SOURCE_PASS")
