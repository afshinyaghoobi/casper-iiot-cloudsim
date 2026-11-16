#!/usr/bin/env python3
"""Bounded public GCS object METADATA inventory: NO task data or object downloads.

No job-ID, timestamp, CPU-work, network or deadline information is present
in these metadata. Never certify actual source/holdout independence here.
"""
import argparse
import hashlib
import json
import re
import statistics
import urllib.parse
import urllib.request
from pathlib import Path

BUCKET="clusterdata-2011-2"
PREFIX="task_events/"
NAME_RE=re.compile(r"task_events/part-(\d{5})-of-00500\.csv\.gz\Z")
API=f"https://storage.googleapis.com/storage/v1/b/{BUCKET}/o"
MAX_PAGES=8
MAX_OBJECTS=2000
EXPECTED_COUNT=500

def fetch_only_metadata():
    items=[]
    token=None
    observed_tokens=set()
    pages=0
    while True:
        if pages>=MAX_PAGES:
            raise ValueError("publisher object listing unexpectedly exceeded page bound")
        params={"prefix":PREFIX,"maxResults":1000,
                "fields":"items(name,bucket,generation,size,crc32c,md5Hash,updated),nextPageToken"}
        if token is not None:
            params["pageToken"]=token
        url=API+"?"+urllib.parse.urlencode(params)
        req=urllib.request.Request(url,headers={"User-Agent":"JPDC-Google2011-Metadata-Census/1.0"})
        with urllib.request.urlopen(req,timeout=40) as response:
            doc=json.load(response)
        if not isinstance(doc,dict) or not isinstance(doc.get("items"),list):
            raise ValueError("invalid publisher listing payload")
        items.extend(doc["items"])
        if len(items)>MAX_OBJECTS:raise ValueError("publisher listing exceeded object cap")
        pages+=1
        next_token=doc.get("nextPageToken")
        if not next_token:break
        if next_token in observed_tokens:raise ValueError("repeated GCS page token")
        observed_tokens.add(next_token)
        token=next_token
    return items,pages

def summarize(items, *, page_count):
    if not isinstance(items,list):raise TypeError("items must be list")
    if page_count<1 or page_count>MAX_PAGES:raise ValueError("invalid pagination")
    ids=set()
    names=set()
    compact=[]
    for x in items:
        if not isinstance(x,dict):raise ValueError("nonobject in publisher listing")
        name=x.get("name","")
        match=NAME_RE.fullmatch(name)
        if not match:raise ValueError(f"unexpected original GCS part name: {name!r}")
        idx=int(match.group(1))
        if idx>=EXPECTED_COUNT or idx in ids or name in names:
            raise ValueError("duplicate/out-of-range original source part")
        ids.add(idx);names.add(name)
        if x.get("bucket") not in (None,BUCKET):
            raise ValueError("invalid publisher bucket field")
        gen=str(x.get("generation",""))
        size=str(x.get("size",""))
        if not gen.isdecimal() or not size.isdecimal() or int(size)<=0:
            raise ValueError("invalid original object version/size")
        compact.append(dict(
            name=name, index=idx, generation=gen,size_bytes=int(size),
            crc32c=x.get("crc32c"),md5Hash=x.get("md5Hash"),
            updated=x.get("updated")))
    compact.sort(key=lambda x:x["index"])
    missing=sorted(set(range(EXPECTED_COUNT))-ids)
    if len(compact)!=EXPECTED_COUNT or missing:
        raise ValueError(f"incomplete original file metadata inventory count={len(compact)} missing={missing[:12]}")
    sizes=[r["size_bytes"] for r in compact]
    canonical=json.dumps(compact,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode("utf-8")
    total=sum(sizes)
    return dict(
        status="PASS",
        source="ORIGINAL_PUBLIC_GOOGLE_GCS_LIST_OBJECTS_METADATA",
        publisher_bucket=BUCKET,
        requested_prefix=PREFIX,
        original_source_table="task_events",
        publisher_original_part_files=len(compact),
        original_expected_file_indices="00000..00499",
        original_file_manifest_sha256=hashlib.sha256(canonical).hexdigest(),
        original_file_manifest=compact,
        publisher_listing_pages=page_count,
        original_task_events_compressed_total_bytes=total,
        original_task_events_compressed_total_GiB=round(total/2**30,6),
        original_file_compressed_min_bytes=min(sizes),
        original_file_compressed_median_bytes=statistics.median(sizes),
        original_file_compressed_max_bytes=max(sizes),
        metadata_only=True,
        original_task_records_loaded=0,
        complete_original_job_key_inventory_verified=False,
        train_dev_holdout_source_independence_certified=False,
        benchmark_external_iiot_deadline_network_verified=False,
        original_stage65_scientific_safety="FAIL",
        original_java_python_queue_parity="FAIL")

def main():
    cli=argparse.ArgumentParser()
    cli.add_argument("--out-dir",required=True)
    cli.add_argument("--offline",action="store_true")
    a=cli.parse_args()
    out=Path(a.out_dir);out.mkdir(parents=True,exist_ok=True)
    if a.offline:
        items=json.loads((out/"publisher_metadata_original.json").read_text())
        pages=int((out/"publisher_page_count.txt").read_text())
    else:
        items,pages=fetch_only_metadata()
        (out/"publisher_metadata_original.json").write_text(json.dumps(items,sort_keys=True,indent=2)+"\n")
        (out/"publisher_page_count.txt").write_text(f"{pages}\n")
    result=summarize(items,page_count=pages)
    (out/"census.json").write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_GOOGLE2011_METADATA_CENSUS",json.dumps({
        k:v for k,v in result.items() if k!="original_file_manifest"},sort_keys=True))
    print("JPDC_GOOGLE2011_COMPLETE_TASK_EVENTS_OBJECT_METADATA_CENSUS_PASS")

if __name__=="__main__":main()
