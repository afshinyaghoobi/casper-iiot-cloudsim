#!/usr/bin/env python3
"""SYNTHETIC metadata-only tests, never original observed source rows."""
from google2011_complete_file_metadata_census import summarize

def fake():
    return [dict(name=f"task_events/part-{i:05d}-of-00500.csv.gz",
                 bucket="clusterdata-2011-2",generation=str(100000+i),
                 size=str(i+1),crc32c="synthetic-fixture") for i in range(500)]

def rejected(f):
    try:f()
    except (ValueError,TypeError):return
    raise AssertionError("incorrectly approved corrupted metadata")

def main():
    base=fake()
    r=summarize(base,page_count=1)
    assert r["publisher_original_part_files"]==500
    assert r["original_task_events_compressed_total_bytes"]==sum(range(1,501))
    assert not r["train_dev_holdout_source_independence_certified"]
    assert not r["complete_original_job_key_inventory_verified"]
    assert r["original_task_records_loaded"]==0
    assert summarize(list(reversed(base)),page_count=1)["original_file_manifest_sha256"]==r["original_file_manifest_sha256"]
    rejected(lambda:summarize(base[:-1],page_count=1))
    rejected(lambda:summarize(base+[base[0]],page_count=1))
    rejected(lambda:summarize([{**base[0],"name":"task_events/part-00000-of-00501.csv.gz"}]+base[1:],page_count=1))
    rejected(lambda:summarize([{**base[0],"size":"0"}]+base[1:],page_count=1))
    rejected(lambda:summarize([{**base[0],"generation":None}]+base[1:],page_count=1))
    rejected(lambda:summarize([{**base[0],"bucket":"unrelated"}]+base[1:],page_count=1))
    rejected(lambda:summarize(base,page_count=9))
    print("JPDC_GOOGLE2011_SYNTHETIC_OBJECT_METADATA_NEGATIVE_TESTS_PASS")

if __name__=="__main__":main()
