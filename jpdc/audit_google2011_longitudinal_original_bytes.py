#!/usr/bin/env python3
"""Independent archived ORIGINAL Google Borg2011 1024-event audit.

This parser does NOT import or call the original window parser and DOES NOT
retrieve additional external rows. Single deliberately selected source window
is not an IID sample, factory IIoT workload, or independent scheduler trial.
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

SOURCE_COMMIT="25e20c96f1df8beec98fc50dcc7ab4f12908e6bb"
ORIGINAL_SHA256="b859de1786db4acb5e7c9c128131445eae9fe8aab9dbcc407c1621e9b6da8f1c"
ORIGINAL_AUDIT_SHA256="436ac0003dfa30966c9b27e51122c65e0c2fafc4866d14656d7e7929552a605f"
SOURCE_KEY="task_events/part-00375-of-00500.csv.gz"
EVENTS=("SUBMIT","SCHEDULE","EVICT","FAIL","FINISH","KILL","LOST",
        "UPDATE_PENDING","UPDATE_RUNNING")
TERMINAL={"EVICT","FAIL","FINISH","KILL","LOST"}


def independent_audit(d):
    assert (d/"source_commit.txt").read_text().strip()==SOURCE_COMMIT
    raw=(d/"original_prefix.gz").read_bytes()
    assert len(raw)==262144 and hashlib.sha256(raw).hexdigest()==ORIGINAL_SHA256
    archived=(d/"audit.json").read_bytes()
    assert archived==(d/"audit_first.json").read_bytes()
    assert hashlib.sha256(archived).hexdigest()==ORIGINAL_AUDIT_SHA256
    reported=json.loads(archived)
    meta=json.loads((d/"source_metadata.json").read_text())
    http=json.loads((d/"source_http.json").read_text())
    assert meta["bucket"]=="clusterdata-2011-2"
    assert meta["name"]==SOURCE_KEY
    assert meta["generation"]=="1416266880306000"
    assert int(meta["size"])==1502643
    assert http["http_status"]==206 and http["content_range"]=="bytes 0-262143/1502643"
    plain=zlib.decompressobj(16+zlib.MAX_WBITS).decompress(raw,1048576)
    assert len(plain)==1048576
    lines=plain[:plain.rfind(b"\n")+1].decode("utf-8")
    rows=list(csv.reader(io.StringIO(lines,newline="")))[:1024]
    assert len(rows)==1024 and all(len(x)==13 for x in rows)
    events=collections.Counter()
    missing=collections.Counter()
    jobs=collections.Counter()
    history={}
    waiting={}
    execution_seen=set()
    classifications=collections.Counter()
    matches=collections.Counter()
    delays=collections.defaultdict(list)
    delay_jobs=collections.defaultdict(set)
    keyset=set()
    times=[]
    terminals_with=terminals_without=0
    for r in rows:
        t=int(r[0]);job=int(r[2]);task=int(r[3]);typ=int(r[5])
        assert t>=0 and job>=0 and task>=0 and 0<=typ<=8
        if times:assert t>=times[-1]
        times.append(t)
        key=(job,task)
        keyset.add(key)
        jobs[job]+=1
        event=EVENTS[typ]
        events[event]+=1
        if not r[4]:missing["missing_machine_id"]+=1
        if not r[9]:missing["missing_cpu_request"]+=1
        if r[1]:missing["nonempty_missing_info"]+=1
        previous=history.get(key)
        if event=="SUBMIT":
            if previous is None:category="FIRST_OBSERVED_SUBMIT_LEFT_CENSORED"
            elif previous in TERMINAL:category="RESUBMIT_AFTER_OBSERVED_TERMINAL"
            else:category="SUBMIT_AFTER_OTHER_HISTORY"
            assert key not in waiting
            waiting[key]=(t,category)
            classifications[category]+=1
            if previous in TERMINAL:
                classifications["TERMINAL_PREDECESSOR_"+previous]+=1
            execution_seen.discard(key)
        elif event=="SCHEDULE":
            if key in waiting:
                start,category=waiting.pop(key)
                assert t>=start
                matches["MATCHED_OBSERVED_SUBMIT_TO_SCHEDULE"]+=1
                matches[category]+=1
                delays[category].append(t-start)
                delay_jobs[category].add(job)
            else:matches["SCHEDULE_WITHOUT_OBSERVED_PENDING_SUBMIT"]+=1
            execution_seen.add(key)
        elif event in TERMINAL:
            if key in execution_seen:terminals_with+=1
            else:terminals_without+=1
            execution_seen.discard(key)
            assert key not in waiting # none of 1024 genuine original observations
        history[key]=event
    assert len(times)==1024
    assert sum(events.values())==1024
    assert sum(classifications[k] for k in
        ("FIRST_OBSERVED_SUBMIT_LEFT_CENSORED","RESUBMIT_AFTER_OBSERVED_TERMINAL",
         "SUBMIT_AFTER_OTHER_HISTORY"))==events["SUBMIT"]
    assert matches["MATCHED_OBSERVED_SUBMIT_TO_SCHEDULE"]+matches[
        "SCHEDULE_WITHOUT_OBSERVED_PENDING_SUBMIT"]==events["SCHEDULE"]
    classified={}
    for key in ("FIRST_OBSERVED_SUBMIT_LEFT_CENSORED","RESUBMIT_AFTER_OBSERVED_TERMINAL",
                "SUBMIT_AFTER_OTHER_HISTORY"):
        vals=delays[key]
        classified[key]=dict(count=len(vals),distinct_source_jobs=len(delay_jobs[key]),
                             min_us=min(vals) if vals else None,
                             median_us=statistics.median(vals) if vals else None,
                             max_us=max(vals) if vals else None)
    assert events=={"SUBMIT":355,"SCHEDULE":331,"KILL":169,"FINISH":152,"FAIL":9,"EVICT":8}
    assert classifications["RESUBMIT_AFTER_OBSERVED_TERMINAL"]==112
    assert classifications["TERMINAL_PREDECESSOR_KILL"]==95
    assert classifications["TERMINAL_PREDECESSOR_FAIL"]==9
    assert classifications["TERMINAL_PREDECESSOR_EVICT"]==8
    assert matches["MATCHED_OBSERVED_SUBMIT_TO_SCHEDULE"]==324
    assert len(waiting)==31
    assert len(jobs)==73
    assert len(set().union(*delay_jobs.values()))==47
    for source_field,expected in (
        ("event_type_counts",dict(events)),
        ("missing_field_counts",dict(missing)),
        ("submit_classification_counts",dict(classifications)),
        ("matched_schedule_classification_counts",dict(matches)),
        ("matched_submit_schedule_gap_descriptive_us",classified)):
        assert reported[source_field]==expected,(source_field,"original-vs-independent mismatch")
    assert reported["right_censored_pending_submit_keys"]==len(waiting)
    assert reported["distinct_source_jobs"]==len(jobs)
    assert reported["distinct_job_task_keys"]==len(keyset)
    assert reported["terminal_events_with_observed_schedule"]==terminals_with
    assert reported["terminal_events_without_observed_schedule"]==terminals_without
    assert reported["original_Stage65_scientific_safety"]=="FAIL"
    assert reported["original_Java_Python_cross_runtime_fidelity"]=="FAIL"
    return dict(status="PASS",source="ORIGINAL_GOOGLE_BORG_2011_PART375_ARCHIVED_BYTES",
        original_raw_prefix_sha256=ORIGINAL_SHA256,
        original_audit_sha256=ORIGINAL_AUDIT_SHA256,
        source_generation=meta["generation"],rows_verified=1024,
        source_jobs=len(jobs),job_task_keys=len(keyset),
        event_type_counts=dict(sorted(events.items())),
        submit_type_counts=dict(sorted(classifications.items())),
        matched_schedules=dict(sorted(matches.items())),
        delay_by_observed_submit_type=classified,
        source_jobs_with_matched_delays=len(set().union(*delay_jobs.values())),
        unmatched_schedule_events=matches["SCHEDULE_WITHOUT_OBSERVED_PENDING_SUBMIT"],
        pending_at_window_end=len(waiting),
        source_window_left_right_censoring=True,
        source_jobs_not_IID_events=True,
        no_new_source_download=True,
        no_sched_policy_or_IIoT_deadline_validation=True,
        original_Stage65_scientific_safety="FAIL",
        original_Java_Python_cross_runtime_fidelity="FAIL")


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original-dir",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    result=independent_audit(Path(a.original_dir))
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print("JPDC_GOOGLE2011_INDEPENDENT_LONGITUDINAL_SOURCE_AUDIT",json.dumps(result,sort_keys=True))
    print("JPDC_GOOGLE2011_ORIGINAL_1024_ROWS_SECOND_PARSER_PASS")
