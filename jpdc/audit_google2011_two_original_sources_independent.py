#!/usr/bin/env python3
"""Independent raw archived GCS two-source overlap forensic — no source imports.

Do not confuse observed identity overlap with proof of persistent tasks,
underlying source-unit nonindependence, or measured scheduler efficacy.
"""
import argparse,csv,hashlib,io,json,zlib
from pathlib import Path
from collections import Counter

EXPECTED_COMMIT="3fb9fb1a72201df49a3708c4a7afac3579a82ff6"
EXPECTED_COHORT_SHA="cdaa040a3f02efac37779c8edbf0a8a0b46d01e39a5f8ac3c70d33eb5675efc5"
KEYS=("task_events/part-00125-of-00500.csv.gz",
      "task_events/part-00425-of-00500.csv.gz")
HASHES=("0b1db05d81b085b5a1c3b456605e7976dde8793e8a4895e587e129988c58c604",
        "5a600640ddf5a137e776f524995365595e73398fa8049c23888c859c9851c6ff")
EVENTS=("SUBMIT","SCHEDULE","EVICT","FAIL","FINISH","KILL","LOST","UPDATE_PENDING","UPDATE_RUNNING")


def verify(directory):
    assert (directory/"source_commit.txt").read_text().strip()==EXPECTED_COMMIT
    cohort_bytes=(directory/"cohort.json").read_bytes()
    assert cohort_bytes==(directory/"cohort_original.json").read_bytes()
    assert hashlib.sha256(cohort_bytes).hexdigest()==EXPECTED_COHORT_SHA
    original=json.loads(cohort_bytes)
    keys=[];jobs=[];times=[];summaries=[]
    for i,key in enumerate(KEYS):
        folder=directory/f"source_{i}"
        raw=(folder/"original_prefix.gz").read_bytes()
        assert len(raw)==262144 and hashlib.sha256(raw).hexdigest()==HASHES[i]
        metadata=json.loads((folder/"metadata.json").read_text())
        http=json.loads((folder/"http.json").read_text())
        assert metadata["bucket"]=="clusterdata-2011-2"
        assert metadata["name"]==key
        assert http["status"]==206
        assert http["content_range"]==f"bytes 0-262143/{metadata['size']}"
        inflated=zlib.decompressobj(16+zlib.MAX_WBITS).decompress(raw,1048576)
        end=inflated.rfind(b"\n")
        assert end>=0
        rows=list(csv.reader(io.StringIO(inflated[:end+1].decode("utf-8"),newline="")))[:1024]
        assert len(rows)==1024
        job_ids=set();task_keys=set();timestamps=[];events=Counter()
        for row in rows:
            assert len(row)==13
            at=int(row[0]);j=int(row[2]);t=int(row[3]);ev=int(row[5])
            assert at>=0 and j>=0 and t>=0 and 0<=ev<len(EVENTS)
            assert not timestamps or at>=timestamps[-1]
            timestamps.append(at);job_ids.add(j);task_keys.add((j,t));events[EVENTS[ev]]+=1
        assert len(job_ids)==original["sources"][i]["observed_jobs"]
        assert len(task_keys)==original["sources"][i]["observed_job_task_keys"]
        assert events==original["sources"][i]["event_counts"]
        assert timestamps[0]==original["sources"][i]["timestamp_min_us"]
        assert timestamps[-1]==original["sources"][i]["timestamp_max_us"]
        keys.append(task_keys);jobs.append(job_ids);times.append(timestamps)
        summaries.append(dict(source_key=key,real_source_sha256=HASHES[i],
            rows=1024,distinct_jobs=len(job_ids),distinct_task_keys=len(task_keys),
            time_min_us=timestamps[0],time_max_us=timestamps[-1],events=dict(sorted(events.items()))))
    shared_jobs=jobs[0]&jobs[1]
    shared_keys=keys[0]&keys[1]
    assert len(shared_jobs)==2
    assert len(shared_keys)==27
    assert {j for j,_ in shared_keys}==shared_jobs
    time_overlap=max(times[0][0],times[1][0])<=min(times[0][-1],times[1][-1])
    assert not time_overlap
    gap=max(times[0][0]-times[1][-1],times[1][0]-times[0][-1])
    assert gap==original["selected_timestamp_intervals_min_gap_us"]
    assert gap==1503299926144
    assert len(shared_jobs)==original["shared_job_id_count"]
    assert len(shared_keys)==original["shared_job_task_id_count"]
    assert original["sampled_overlap_classification"]=="OBSERVED_JOB_TASK_KEY_OVERLAP"
    assert original["full_partition_job_independence"]=="UNRESOLVED_FULL_SOURCE_INDEPENDENCE"
    assert original["original_stage65_safety"]=="FAIL"
    assert original["original_java_python_cross_runtime_parity"]=="FAIL"
    return dict(status="PASS",kind="INDEPENDENT_ARCHIVED_GCS_SOURCE_BYTES_AUDIT",
        original_cohort_sha256=EXPECTED_COHORT_SHA,
        no_new_source_retrieval=True,
        distinct_files_are_not_proven_independent_source_units=True,
        source_time_gap_us=gap,
        source_time_intervals_overlap=False,
        original_job_ids_shared=len(shared_jobs),
        original_job_task_pairs_shared=len(shared_keys),
        original_source_task_identity_reuse_explanation="UNRESOLVED",
        cannot_infer_full_trace_statistical_independence=True,
        no_scheduling_policy_efficacy=True,
        sources=summaries,original_stage65_safety="FAIL",
        java_python_cross_runtime_parity="FAIL")


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original-dir",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    result=verify(Path(a.original_dir))
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print("JPDC_TWO_SOURCE_INDEPENDENT_ORIGINAL_BYTES_AUDIT",json.dumps(result,sort_keys=True))
    print("JPDC_TWO_SOURCE_ORIGINAL_IDENTITY_OVERLAP_VERIFIED_PASS")
