#!/usr/bin/env python3
"""One previously spent complete official Google2011 gzip partition; bounded pilot.

Never claims general workload independence, IIoT performance or calibrated
deadlines. No GCS full-trace download. Full gzip trailer and publisher hashes.
"""
import argparse
import base64
import collections
import csv
import gzip
import hashlib
import io
import json
import resource
import time
import urllib.parse
import urllib.request
from pathlib import Path

BUCKET="clusterdata-2011-2"
NAME="task_events/part-00375-of-00500.csv.gz"
GENERATION="1416266880306000"
EXPECTED_COMPRESSED_BYTES=1502643
MAX_UNCOMPRESSED=128*1024*1024
MAX_ROWS=2000000
EVENTS=("SUBMIT","SCHEDULE","EVICT","FAIL","FINISH","KILL","LOST",
        "UPDATE_PENDING","UPDATE_RUNNING")


def crc32c_bytes(data):
    polynomial=0x82f63b78
    table=[]
    for i in range(256):
        c=i
        for _ in range(8):
            c=(c>>1) ^ (polynomial if (c&1) else 0)
        table.append(c)
    value=0xffffffff
    for byte in data:
        value=table[(value^byte)&0xff]^(value>>8)
    return base64.b64encode(((value^0xffffffff)&0xffffffff).to_bytes(4,"big")).decode()


def metadata_original():
    url=("https://storage.googleapis.com/storage/v1/b/"+BUCKET+"/o/"+
         urllib.parse.quote(NAME,safe="")+"?fields=name,bucket,generation,size,crc32c,md5Hash,updated")
    with urllib.request.urlopen(urllib.request.Request(url,headers={
        "User-Agent":"CASPER-JPDC-Google2011-Spent-Full-Partition/1.0"}),timeout=30) as response:
        item=json.load(response)
    if item.get("name")!=NAME or item.get("bucket")!=BUCKET or (
        str(item.get("generation"))!=GENERATION) or (
        int(item.get("size",0))!=EXPECTED_COMPRESSED_BYTES):
        raise ValueError("publisher full-partition identity, generation or frozen size mismatch")
    if not item.get("md5Hash") or not item.get("crc32c"):
        raise ValueError("publisher full gzip integrity hashes unavailable")
    return item


def download_exact(item):
    url=("https://storage.googleapis.com/"+BUCKET+"/"+NAME+
         "?generation="+GENERATION)
    request=urllib.request.Request(url,headers={
        "Accept-Encoding":"identity",
        "User-Agent":"CASPER-JPDC-Google2011-Spent-Full-Partition/1.0"})
    start=time.perf_counter()
    with urllib.request.urlopen(request,timeout=60) as response:
        code=response.status
        data=response.read(EXPECTED_COMPRESSED_BYTES+1)
        header=dict(http_status=code,content_length=response.headers.get("Content-Length"),
                    etag=response.headers.get("ETag"),content_range=response.headers.get("Content-Range"))
    duration=time.perf_counter()-start
    if code!=200 or len(data)!=EXPECTED_COMPRESSED_BYTES or (
        header["content_range"] not in (None,"")):
        raise ValueError("original generation-pinned GET not complete or bounded")
    if header["content_length"] is not None and int(header["content_length"])!=EXPECTED_COMPRESSED_BYTES:
        raise ValueError("original Content-Length not equal publisher metadata")
    return data,header,duration


def scan_full_gzip(raw,item):
    if len(raw)!=EXPECTED_COMPRESSED_BYTES or raw[:2]!=b"\x1f\x8b":
        raise ValueError("not the exact frozen full source gzip")
    sha=hashlib.sha256(raw).hexdigest()
    md5=base64.b64encode(hashlib.md5(raw).digest()).decode()
    crc=crc32c_bytes(raw)
    if md5!=item["md5Hash"] or crc!=item["crc32c"]:
        raise ValueError("full original publisher MD5/CRC32C disagrees with downloaded bytes")
    count=0
    uncompressed=0
    types=collections.Counter()
    missing=collections.Counter()
    unique_jobs=set()
    unique_keys=set()
    min_time=max_time=last_time=None
    first1024=collections.Counter()
    t0=time.perf_counter()
    # gzip stream validates final CRC32 and uncompressed size on reading to EOF.
    with gzip.GzipFile(fileobj=io.BytesIO(raw),mode="rb") as source:
        for binary_line in source:
            uncompressed+=len(binary_line)
            if uncompressed>MAX_UNCOMPRESSED:
                raise ValueError("predeclared uncompressed budget exceeded")
            if len(binary_line)>16384:
                raise ValueError("source CSV line unreasonably long")
            line=binary_line.decode("utf-8","strict")
            if not binary_line.endswith(b"\n"):
                raise ValueError("unterminated original source CSV final line")
            parsed=list(csv.reader([line]))
            if len(parsed)!=1 or len(parsed[0])!=13:
                raise ValueError("original 13-column v2.1 schema mismatch")
            row=parsed[0]
            timestamp=int(row[0]);job=int(row[2]);task=int(row[3]);code=int(row[5])
            if min(timestamp,job,task)<0 or not 0<=code<=8:
                raise ValueError("negative time/key or invalid original v2.1 event")
            if last_time is not None and timestamp<last_time:
                raise ValueError("source file timestamps decrease")
            if min_time is None:min_time=timestamp
            last_time=timestamp
            max_time=timestamp
            types[EVENTS[code]]+=1
            if not row[4]:missing["missing_machine_id"]+=1
            if not row[9]:missing["missing_cpu_request"]+=1
            if row[1]:missing["nonempty_missing_info"]+=1
            unique_jobs.add(job);unique_keys.add((job,task))
            count+=1
            if count<=1024:first1024[EVENTS[code]]+=1
            if count>MAX_ROWS:raise ValueError("predeclared 2M row cap exceeded")
    elapsed=time.perf_counter()-t0
    if count<1024:raise ValueError("full source smaller than previous first1024 event prefix")
    # Recheck frozen previously sampled first 1024 rows: source was spent.
    assert first1024=={"SUBMIT":355,"SCHEDULE":331,"KILL":169,
                        "FINISH":152,"FAIL":9,"EVICT":8}
    return dict(status="PASS",
        observed_full_original_source_row_count=count,
        uncompressed_bytes=uncompressed,
        original_compressed_bytes=len(raw),
        original_compressed_sha256=sha,
        original_full_crc32c=crc,original_full_md5_b64=md5,
        complete_gzip_trailer_verified=True,
        min_timestamp_us=min_time,max_timestamp_us=max_time,
        distinct_original_job_ids=len(unique_jobs),
        distinct_original_job_task_keys=len(unique_keys),
        event_type_counts=dict(sorted(types.items())),
        missing_counts=dict(sorted(missing.items())),
        previous_prefix_first1024_event_types_match=True,
        source_scan_elapsed_seconds=round(elapsed,6),
        peak_RSS_linux_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        source_full_500_partition_scan=False,
        train_dev_holdout_job_disjointness_certified=False,
        no_measured_cpu_service_network_payload_or_real_deadline=True,
        stage65_safety="FAIL",java_python_parity="FAIL")


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out-dir",required=True)
    p.add_argument("--offline",action="store_true")
    a=p.parse_args()
    folder=Path(a.out_dir);folder.mkdir(parents=True,exist_ok=True)
    if a.offline:
        meta=json.loads((folder/"source_metadata.json").read_text())
        http=json.loads((folder/"source_http.json").read_text())
        raw=(folder/"original_full.gz").read_bytes()
        download_duration=None
    else:
        meta=metadata_original()
        raw,http,download_duration=download_exact(meta)
        (folder/"source_metadata.json").write_text(json.dumps(meta,indent=2,sort_keys=True)+"\n")
        (folder/"source_http.json").write_text(json.dumps(http,indent=2,sort_keys=True)+"\n")
        (folder/"original_full.gz").write_bytes(raw)
    if meta.get("generation")!=GENERATION or meta.get("name")!=NAME:
        raise ValueError("archive source metadata mismatch")
    report=scan_full_gzip(raw,meta)
    report["source_gcs"]="gs://"+BUCKET+"/"+NAME
    report["source_generation"]=GENERATION
    report["source_http"]=http
    report["acquisition_elapsed_seconds"]=round(download_duration,6) if download_duration is not None else None
    (folder/("audit_offline.json" if a.offline else "source_audit.json")).write_text(
        json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+"\n")
    # Runtime fluctuates and does NOT participate in deterministic comparisons.
    print("JPDC_GOOGLE2011_FULL_SPENT_PARTITION_STREAM",json.dumps(report,sort_keys=True))
    print("JPDC_GOOGLE2011_FULL_SPENT_SOURCE_STREAM_INTEGRITY_PASS")


if __name__=="__main__":main()
