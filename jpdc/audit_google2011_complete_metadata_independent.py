#!/usr/bin/env python3
"""Independent archived GCS LIST response audit; NO source-parser import or networking.

Original issuer archive run43926163146. Exact publisher metadata and previous
source object generations are checked without fetching any task-event rows.
"""
import argparse
import hashlib
import json
import re
import statistics
from pathlib import Path

ORIGINAL_RUN_SOURCE_SHA="2c64c66c02fe0f119ea1e265e8493af4648a332e"
ORIGINAL_METADATA_SHA256="16b557cb89893aea1d56a9b808dc301c9291602d9e47ea384bfd3fff7d3eac06"
ORIGINAL_CENSUS_SHA256="88da8a61bf43c216f348e35c93d4ae60097ced6e96275d5f68f2c076ef98899c"
PREFIX_PATTERN=re.compile(r"task_events/part-([0-9]{5})-of-00500\.csv\.gz\Z")
KNOWN_GENERATIONS={
    0:"1416266809487000",
    125:"1416266795647000",
    250:"1416266806161000",
    375:"1416266880306000",
    425:"1416266788374000",
}

def independent_manifest_check(folder):
    assert (folder/"source_commit.txt").read_text().strip()==ORIGINAL_RUN_SOURCE_SHA
    raw=(folder/"publisher_metadata_original.json").read_bytes()
    assert hashlib.sha256(raw).hexdigest()==ORIGINAL_METADATA_SHA256
    report_raw=(folder/"census.json").read_bytes()
    assert report_raw==(folder/"census_original.json").read_bytes()
    assert hashlib.sha256(report_raw).hexdigest()==ORIGINAL_CENSUS_SHA256
    items=json.loads(raw)
    report=json.loads(report_raw)
    assert int((folder/"publisher_page_count.txt").read_text())==1
    assert len(items)==500
    indices=set()
    sizes={}
    gens={}
    for item in items:
        assert item.get("bucket")=="clusterdata-2011-2"
        m=PREFIX_PATTERN.fullmatch(item["name"])
        assert m is not None
        n=int(m.group(1))
        assert n not in indices
        indices.add(n)
        sz=int(item["size"])
        assert sz>0 and str(item["generation"]).isdigit()
        sizes[n]=sz
        gens[n]=str(item["generation"])
        assert item.get("crc32c") and item.get("md5Hash")
    assert indices==set(range(500))
    for index,g in KNOWN_GENERATIONS.items():
        assert gens[index]==g,("known original source version changed",index)
    assert sum(sizes.values())==1624496362
    assert report["original_task_events_compressed_total_bytes"]==sum(sizes.values())
    assert report["original_task_events_compressed_total_GiB"]==round(sum(sizes.values())/2**30,6)
    assert report["original_file_compressed_min_bytes"]==min(sizes.values())
    assert report["original_file_compressed_max_bytes"]==max(sizes.values())
    assert report["original_file_compressed_median_bytes"]==statistics.median(sizes.values())
    assert len(report["original_file_manifest"])==500
    assert report["original_task_records_loaded"]==0
    assert report["original_stage65_scientific_safety"]=="FAIL"
    assert report["original_java_python_queue_parity"]=="FAIL"
    assert report["train_dev_holdout_source_independence_certified"] is False
    assert report["complete_original_job_key_inventory_verified"] is False
    return dict(
        status="PASS",
        original_official_gcs_metadata_sha256=ORIGINAL_METADATA_SHA256,
        original_census_sha256=ORIGINAL_CENSUS_SHA256,
        original_publisher_bucket="clusterdata-2011-2",
        original_task_events_files=len(indices),
        source_indexes_complete_00000_to_00499=True,
        total_original_task_events_compressed_bytes=sum(sizes.values()),
        total_original_task_events_compressed_GiB=round(sum(sizes.values())/2**30,6),
        metadata_original_source_generations_match_previous_real_samples=True,
        actual_source_rows_processed=0,
        task_events_complete_download_and_key_scan_not_done=True,
        true_train_dev_test_job_disjointness="NOT_CERTIFIED",
        stage65_safety="FAIL",
        java_python_queue_parity="FAIL",
        independent_software_recalculation_not_independent_data_acquisition=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original-dir",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    output=independent_manifest_check(Path(a.original_dir))
    dest=Path(a.out)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(output,sort_keys=True,indent=2)+"\n")
    print("JPDC_GOOGLE2011_INDEPENDENT_METADATA_ONLY",
          json.dumps(output,sort_keys=True))
    print("JPDC_GOOGLE2011_INDEPENDENT_ORIGINAL_500_OBJECTS_METADATA_PASS")
