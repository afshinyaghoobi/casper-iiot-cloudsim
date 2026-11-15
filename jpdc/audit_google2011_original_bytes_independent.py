#!/usr/bin/env python3
"""Independent original-artifact-only secondary forensic audit.

No source download, no simulator, no reused fake sample. Verify compressed
prefix and independently count original first 128 rows without importing
the source parser.
"""
import argparse,csv,gzip,hashlib,io,json,zlib
from pathlib import Path

EXPECTED_RAW_SHA256="4d5ea5b9f914c05fa6c2f2e192036cb05222b9b093b124e4b95c6215e53dccd2"
EXPECTED_ORIGINAL_AUDIT_SHA256="89094f08b9a66513911e2568029711ab8031ade6c124d62385e5bda7e94ff4d2"
EXPECTED_SRC_SHA="d45b3572233f7dfbc27e8470f18ca756a3586dc1"

def audit(folder):
    assert (folder/"source_commit.txt").read_text().strip()==EXPECTED_SRC_SHA
    raw=(folder/"original_prefix.gz").read_bytes()
    assert len(raw)==262144 and hashlib.sha256(raw).hexdigest()==EXPECTED_RAW_SHA256
    a=(folder/"audit.json").read_bytes()
    assert a==(folder/"audit_first.json").read_bytes()
    assert hashlib.sha256(a).hexdigest()==EXPECTED_ORIGINAL_AUDIT_SHA256
    original=json.loads(a)
    meta=json.loads((folder/"original_storage.json").read_text())
    http=json.loads((folder/"original_http.json").read_text())
    assert meta["name"]=="task_events/part-00000-of-00500.csv.gz"
    assert meta["generation"]=="1416266809487000"
    assert meta["size"]=="4139742"
    assert http["http_status"]==206 and http["content_range"]=="bytes 0-262143/4139742"
    assert original["publisher_dataset_version"]=="google_borg_2011_v2.1"
    dec=zlib.decompressobj(16+zlib.MAX_WBITS)
    inflated=dec.decompress(raw,1048576)
    assert len(inflated)==1048576
    complete=inflated[:inflated.rfind(b"\n")+1]
    rows=list(csv.reader(io.StringIO(complete.decode("utf-8"))))[:128]
    assert len(rows)==128
    assert all(len(r)==13 for r in rows)
    event_counts={}
    timestamps=[]
    missing_cpu=missing_info=0
    for r in rows:
        event=int(r[5]);assert 0<=event<=8
        event_counts[event]=event_counts.get(event,0)+1
        timestamps.append(int(r[0]))
        missing_cpu+=int(r[9]=="")
        missing_info+=int(r[1]!="")
    assert event_counts=={0:128}
    assert set(timestamps)=={0}
    assert missing_cpu==69 and missing_info==69
    assert original["observed_submit_event_rows"]==128
    assert original["missing_field_counts"]["missing_cpu_request"]==69
    assert original["missing_field_counts"]["nonempty_missing_info"]==69
    assert not original["complete_external_dispatch_dataset_admitted"]
    return dict(status="PASS",source_evidence="ORIGINAL_OFFICIAL_GCS_COMPRESSED_BYTES",
                no_new_source_download=True,source_file="gs://clusterdata-2011-2/"+meta["name"],
                sample_selection="FIRST_128_EVENTS_ALL_AT_TIMESTAMP_ZERO",
                inspected_original_task_events=128,submit_event_rows=128,
                missing_cpu_request_rows=missing_cpu,nonempty_missing_info_rows=missing_info,
                all_sample_times_zero=True,
                cannot_infer_empirical_arrival_rate=True,
                not_representative_trace_sample=True,
                recorded_true_deadlines=False,recorded_per_task_network_bytes=False,
                source_original_prefix_sha256=EXPECTED_RAW_SHA256,
                original_audit_sha256=EXPECTED_ORIGINAL_AUDIT_SHA256,
                failed_stage65_promotion="FAIL",failed_java_python_equivalence="FAIL")

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--original-dir",required=True);p.add_argument("--out",required=True)
    args=p.parse_args()
    v=audit(Path(args.original_dir));o=Path(args.out);o.parent.mkdir(parents=True,exist_ok=True)
    o.write_text(json.dumps(v,indent=2,sort_keys=True)+"\n")
    print("JPDC_GOOGLE2011_INDEPENDENT_ORIGINAL_BYTES_AUDIT",json.dumps(v,sort_keys=True))
    print("JPDC_GOOGLE2011_ORIGINAL_128_RECORDS_INDEPENDENT_AUDIT_PASS")
