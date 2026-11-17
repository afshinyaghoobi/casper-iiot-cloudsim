#!/usr/bin/env python3
"""Separate source-independent auditor of archived original queue transition report."""
import argparse,csv,json,zipfile,hashlib
from pathlib import Path

CASES=("EARLY4_1US","EARLY4_5MS","ORIGINAL_1US","ORIGINAL_5MS","LATE10_1US","LATE10_5MS")
ORIGINAL="b80536e332b04ffeb0285005b38a95563bac36c29201fc8f93693efc95e5c250"
def digest(b):return hashlib.sha256(b).hexdigest()
def ids(v):return set(int(i) for i in v.split(";")) if v else set()
def check(src,raw,report):
    native=Path(raw).read_bytes()
    if digest(native)!=ORIGINAL:raise ValueError("original source native log changed")
    data=json.loads(Path(report).read_text())
    if data["original_v857_source_jar_sha256"]!=digest(Path(src).read_bytes()):
        raise ValueError("wrong actual dependency publisher source version")
    with zipfile.ZipFile(src) as z:
        for label,part in data["source_inventory"].items():
            b=z.read(part["jar_path"])
            if digest(b)!=part["source_sha256"] or len(b)!=part["source_bytes"]:
                raise ValueError("original class source SHA mismatch")
            for method,listing in part["methods"].items():
                for item in listing:
                    if item["start_line"]<1 or item["end_line"]<item["start_line"]:
                        raise ValueError("invalid original source method source lines")
    records={x:[] for x in CASES}
    for fields in csv.reader(native.decode().splitlines()):
        if fields and fields[0]=="ARRIVALCF_SUBMIT" and fields[1] in records:
            records[fields[1]].append((fields[2],float(fields[3]),int(fields[4]),
                                       ids(fields[5]),ids(fields[6])))
    outcome=[]
    for case in CASES:
        accepted={};found=None
        for phase,clock,i,execution,waiting in records[case]:
            if phase=="AFTER":
                accepted[i]=clock
                for older in waiting:
                    for later in execution:
                        if older in accepted and later in accepted and accepted[older]<accepted[later]-1e-7:
                            if found is None:found=(i,older,later,clock)
        expected=next(x for x in data["first_direct_bypass_at_submit"] if x["case"]==case)
        if (found is not None)!=expected["direct_bypass_at_submit"]:
            raise ValueError("independent original bypass classification mismatch")
        if found:
            detail=expected["first_native_bypass_submit_transition"]
            if (found[0],found[1],found[2])!=(detail["job_just_submitted"],
                detail["older_wait_job"],detail["later_exec_job"]):
                raise ValueError("source state pair mismatch")
            if abs(found[3]-detail["time_ms"])>1e-6:raise ValueError("source clock mismatch")
        if len(accepted)!=3:raise ValueError("missing native submissions")
        outcome.append(dict(case=case,bypass=found is not None))
    return dict(status="PASS",source_files=3,original_native_cases=6,
        exact_original_source_classes_rehashed=True,
        direct_bypass_cases=[x["case"] for x in outcome if x["bypass"]],
        independently_reparsed_submission_transitions=True,
        java_python_30k_parity="FAIL",stage65_safety="FAIL",
        published_sources_not_a_dynamic_branch_trace=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for x in ("sources","native","primary","out"):p.add_argument("--"+x,required=True)
    a=p.parse_args();d=check(a.sources,a.native,a.primary)
    Path(a.out).write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print("JPDC_V857_SOURCE_AND_BYPASS_INDEPENDENT_AUDIT_PASS",json.dumps(d,sort_keys=True))
