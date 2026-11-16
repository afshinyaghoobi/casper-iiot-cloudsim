#!/usr/bin/env python3
"""Offline original 500-object GCS manifest budget and unsafe SQLite resume gate.

No live network requests, no GCS gzip downloads. Existing original artifacts
only. It cannot certify a scientific holdout or future source-data costs.
"""
import argparse
import collections
import hashlib
import json
import re
import sqlite3
from pathlib import Path

PUBLISHER_SHA="16b557cb89893aea1d56a9b808dc301c9291602d9e47ea384bfd3fff7d3eac06"
CENSUS_SHA="88da8a61bf43c216f348e35c93d4ae60097ced6e96275d5f68f2c076ef98899c"
SQL_SHA="692059aca2d6b8621f84693490d71c9243d5a41b37f3c0b826101a34e10f0cb2"
SOURCE_SHA="0ca3c532707d1a291228d59c75d7831d654cd330579a4dc9e32cfa0685783025"
FILE_RE=re.compile(r"task_events/part-(\d{5})-of-00500\.csv\.gz\Z")
CAP=64*1024*1024
TOTAL=1624496362
EXPECTED_GENS={0:"1416266809487000",125:"1416266795647000",
               250:"1416266806161000",375:"1416266880306000",
               425:"1416266788374000"}
EVENTS={"SUBMIT":44330,"SCHEDULE":44290,"FINISH":26802,
        "KILL":13423,"FAIL":1241,"EVICT":725,"UPDATE_RUNNING":1}


def exact_publisher_manifest(metadata_dir):
    original=(metadata_dir/"publisher_metadata_original.json").read_bytes()
    census=(metadata_dir/"census.json").read_bytes()
    if hashlib.sha256(original).hexdigest()!=PUBLISHER_SHA:
        raise ValueError("publisher original metadata archive SHA changed")
    if hashlib.sha256(census).hexdigest()!=CENSUS_SHA:
        raise ValueError("publisher source census SHA changed")
    if (metadata_dir/"census_original.json").read_bytes()!=census:
        raise ValueError("publisher offline metadata replay differs")
    items=json.loads(original)
    prior=json.loads(census)
    if len(items)!=500:raise ValueError("not all 500 original GCS metadata objects")
    by_id={}
    for item in items:
        match=FILE_RE.fullmatch(str(item.get("name","")))
        if not match:raise ValueError("unexpected source filename")
        idx=int(match.group(1))
        if idx>=500 or idx in by_id:raise ValueError("duplicate source index")
        if item.get("bucket")!="clusterdata-2011-2":
            raise ValueError("GCS wrong publisher bucket")
        gen=str(item.get("generation",""))
        size=str(item.get("size",""))
        if not gen.isdecimal() or not size.isdecimal() or int(size)<=0:
            raise ValueError("source object generation/size invalid")
        if not item.get("crc32c") or not item.get("md5Hash"):
            raise ValueError("GCS original publisher checksums absent")
        by_id[idx]=dict(file_index=idx,name=item["name"],generation=gen,
             size_bytes=int(size),crc32c=item["crc32c"],md5_b64=item["md5Hash"])
    if sorted(by_id)!=list(range(500)):raise ValueError("missing source files")
    for i,g in EXPECTED_GENS.items():
        if by_id[i]["generation"]!=g:raise ValueError("historical source GCS generation changed")
    result=[by_id[i] for i in range(500)]
    if sum(row["size_bytes"] for row in result)!=TOTAL:raise ValueError("publisher original byte census mismatch")
    if prior["original_task_events_compressed_total_bytes"]!=TOTAL:
        raise ValueError("old source metadata document inconsistent")
    if prior["original_task_records_loaded"]!=0:
        raise ValueError("metadata inventory erroneously classified as source rows")
    return result


def batches(records,budget=CAP):
    if not isinstance(budget,int) or budget<=0:raise ValueError("invalid batch budget")
    output=[];cur=[];used=0
    for record in records:
        s=record["size_bytes"]
        if s<=0 or s>budget:raise ValueError("single source file exceeds frozen batch budget")
        if cur and used+s>budget:
            output.append(dict(batch_id=len(output),file_count=len(cur),
                compressed_bytes=used,indices=cur))
            cur=[];used=0
        cur.append(record["file_index"])
        used+=s
    if cur:output.append(dict(batch_id=len(output),file_count=len(cur),
                             compressed_bytes=used,indices=cur))
    return output


def check_source_db(conn,expect_index=375):
    """SQL counts are only a NECESSARY test; not an all-key identity proof."""
    integrity=conn.execute("PRAGMA integrity_check").fetchone()[0]
    if integrity!="ok":raise ValueError("SQLite structural corruption")
    entries=conn.execute("SELECT file_index,generation,original_sha256,row_count,bytes_plain,first_us,last_us,status FROM file_inventory").fetchall()
    if len(entries)!=1 or entries[0][:4]!=(375,EXPECTED_GENS[375],SOURCE_SHA,130812):
        raise ValueError("file_inventory completed source identity/size incorrect")
    if entries[0][4:7]!=(14973713,1879800290193,1884810781196) or entries[0][7]!="COMPLETE":
        raise ValueError("file_inventory source temporal/inflation identity incorrect")
    cjobs=conn.execute("SELECT COUNT(*) FROM job_presence WHERE file_index=375").fetchone()[0]
    ctasks=conn.execute("SELECT COUNT(*) FROM task_presence WHERE file_index=375").fetchone()[0]
    if (cjobs,ctasks)!=(1838,44979):raise ValueError("UNSAFE_RESUME_INTEGRITY_FAIL missing job/task row")
    if conn.execute("SELECT COUNT(*) FROM job_presence WHERE file_index<>375").fetchone()[0]:
        raise ValueError("unregistered source job rows")
    if conn.execute("SELECT COUNT(*) FROM task_presence WHERE file_index<>375").fetchone()[0]:
        raise ValueError("unregistered source task rows")
    orphan=conn.execute("""SELECT COUNT(*) FROM task_presence t
      LEFT JOIN job_presence j ON t.file_index=j.file_index AND t.job_id=j.job_id
      WHERE j.job_id IS NULL""").fetchone()[0]
    if orphan:raise ValueError("UNSAFE_RESUME_INTEGRITY_FAIL orphan task keys")
    counts=dict(conn.execute("SELECT event_type,n FROM event_counts WHERE file_index=375"))
    if counts!=EVENTS or sum(counts.values())!=130812:
        raise ValueError("UNSAFE_RESUME_INTEGRITY_FAIL event conservation")
    if conn.execute("SELECT COUNT(*) FROM event_counts WHERE file_index<>375").fetchone()[0]:
        raise ValueError("unregistered source events")
    return dict(status="PASS",file_index=375,source_job_count=cjobs,
        source_task_key_count=ctasks,source_event_count=sum(counts.values()),
        no_orphan_tasks=True,structural_integrity="ok",
        strength="NECESSARY_COUNTS_AND_RELATIONS_NOT_SUFFICIENT_FOR_WHOLE_SOURCE_IDENTITY")


def check_db_file(sqlfile):
    if hashlib.sha256(sqlfile.read_bytes()).hexdigest()!=SQL_SHA:
        raise ValueError("original completed source SQLite SHA mismatch")
    conn=sqlite3.connect("file:"+str(sqlfile.resolve())+"?mode=ro",uri=True)
    try:return check_source_db(conn)
    finally:conn.close()


def full_plan(meta_dir,sql_dir):
    records=exact_publisher_manifest(meta_dir)
    existing=check_db_file(sql_dir/"presence.sqlite")
    groups=batches(records)
    flat=[idx for g in groups for idx in g["indices"]]
    if flat!=list(range(500)):raise AssertionError("batch coverage/order missing")
    if sum(g["compressed_bytes"] for g in groups)!=TOTAL or max(g["compressed_bytes"] for g in groups)>CAP:
        raise AssertionError("batch compressed sum/cap mismatch")
    original_rows_sha=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return dict(status="PASS",classification="ORIGINAL_METADATA_ONLY_500_FILE_SOURCE_PREFLIGHT",
      bucket="clusterdata-2011-2",source_table="task_events",
      complete_original_object_metadata_count=500,planned_batches=len(groups),
      per_batch_compressed_budget_bytes=CAP,
      observed_original_compressed_total_bytes=TOTAL,
      observed_original_compressed_total_GiB=round(TOTAL/2**30,6),
      max_original_object_compressed_bytes=max(r["size_bytes"] for r in records),
      max_planned_batch_compressed_bytes=max(g["compressed_bytes"] for g in groups),
      original_publisher_metadata_json_sha256=PUBLISHER_SHA,
      original_metadata_manifest_canonical_sha256=original_rows_sha,
      existing_source_sqlite_sha256=SQL_SHA,
      existing_source_resume_integrity=existing,
      original_files=records,batches=groups,
      original_source_files_whole_contents_processed_during_this_stage=0,
      original_full_500_file_source_scan_executed=False,
      original_source_independent_holdout_certified=False,
      costs_or_future_egress_verified=False,
      original_stage65_safety="FAIL",original_java_python_parity="FAIL")


if __name__=="__main__":
    cli=argparse.ArgumentParser()
    cli.add_argument("--metadata-dir",required=True)
    cli.add_argument("--sqlite-dir",required=True)
    cli.add_argument("--out",required=True)
    a=cli.parse_args()
    result=full_plan(Path(a.metadata_dir),Path(a.sqlite_dir))
    p=Path(a.out);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print("JPDC_ORIGINAL_GCS_500_FILE_BATCH_PREFLIGHT",json.dumps({
      k:v for k,v in result.items() if k not in ("original_files","batches")},sort_keys=True))
    print("JPDC_ORIGINAL_GCS_500_FILE_SOURCE_PLAN_NO_DOWNLOAD_PASS")
