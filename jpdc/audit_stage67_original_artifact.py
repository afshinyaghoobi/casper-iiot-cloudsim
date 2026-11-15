#!/usr/bin/env python3
"""Stage67 independent artifact-only source trace audit; never native resimulation."""
import argparse,hashlib,json,math
from pathlib import Path
from audit_stage67_native_service_scale import audit,NAMES,SCALES,EVENT_GAPS

def verify(d):
    assert (d/"native.log").read_bytes()==(d/"native_repeat.log").read_bytes()
    assert (d/"audit.json").read_bytes()==(d/"audit_repeat.json").read_bytes()
    original=json.loads((d/"audit.json").read_text())
    recomputed=audit((d/"native.log").read_text().splitlines())
    assert original==recomputed
    assert original["status"]=="PASS"
    assert original["original_30k_cross_engine_parity"]=="UNRESOLVED_FAIL"
    assert len(original["cases"])==6
    rows=[]
    for i,c in enumerate(original["cases"]):
        assert c["case"]==NAMES[i]
        assert c["requested_service_scale"]==SCALES[i]
        assert c["event_gap_s"]==EVENT_GAPS[i]
        assert len(c["rows"])==3
        assert c["bypass_observed"]==bool(c["bypass_evidence"])
        assert math.isfinite(c["max_abs_native_wait_vs_ideal_fcfs_ms"])
        assert c["max_abs_native_wait_vs_ideal_fcfs_ms"]>=0
        calculated=max(abs(r["reported_native_wait_ms"]-r["ideal_strict_fcfs_wait_ms"])
                       for r in c["rows"])
        assert abs(calculated-c["max_abs_native_wait_vs_ideal_fcfs_ms"])<=1e-9
        for e in c["bypass_evidence"]:
            assert e["older_submit_ms"]+1e-6<e["later_submit_ms"]
        rows.append(dict(case=c["case"],scale=c["requested_service_scale"],
             minimum_event_gap_sec=c["event_gap_s"],bypass=c["bypass_observed"],
             bypass_native_list_evidence_count=len(c["bypass_evidence"]),
             max_native_wait_vs_ideal_fifo_ms=c["max_abs_native_wait_vs_ideal_fcfs_ms"],
             native_wait_ms=[r["reported_native_wait_ms"] for r in c["rows"]],
             ideal_wait_ms=[r["ideal_strict_fcfs_wait_ms"] for r in c["rows"]]))
    assert len(rows)==6
    return dict(status="PASS",original_native_experiment_reexecuted=False,
         source_trace_sha256=hashlib.sha256((d/"native.log").read_bytes()).hexdigest(),
         original_audit_sha256=hashlib.sha256((d/"audit.json").read_bytes()).hexdigest(),
         original_thirty_k_java_python_parity_still_failed=True,
         new_scientific_IIoT_policy_effect_observations=0,cases=rows)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source-dir",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    result=verify(Path(a.source_dir))
    path=Path(a.out)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")
    for c in result["cases"]:
        print("JPDC_STAGE67_REAL_NATIVE_SOURCE_CASE",json.dumps(c,sort_keys=True))
    print("JPDC_STAGE67_ORIGINAL_NATIVE_ARTIFACT_INDEPENDENT_AUDIT_PASS")
