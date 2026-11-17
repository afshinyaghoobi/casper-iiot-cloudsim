#!/usr/bin/env python3
"""Independent raw-native log audit of original Stage67 posterior service hypothesis."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

ORIGINAL_SHA="61d92e93812b20b473d70c9b3ba5a67f65af574fcd35c5e6a590f19a76b6e9eb"

def reconstruct(source):
    data=Path(source).read_bytes()
    if hashlib.sha256(data).hexdigest()!=ORIGINAL_SHA:
        raise ValueError("wrong original CloudSimPlus source")
    arrivals={};finish={}
    for row in csv.reader(data.decode("utf-8").splitlines()):
        if row[0]=="STAGE67_SUBMIT" and row[2]=="BEFORE":
            arrivals[(row[1],int(row[4]))]=float(row[3])
        elif row[0]=="STAGE67_FINISH":
            key=(row[1],int(row[2]))
            if key in finish:raise ValueError("duplicate native source finish")
            finish[key]=(float(row[4]),float(row[5]),float(row[6]),float(row[7]))
    cases=sorted({k[0] for k in finish})
    if len(cases)!=6 or len(arrivals)!=18 or len(finish)!=18:
        raise ValueError("not six complete original three-task cases")
    outcome={}
    for name in cases:
        end_request=end_report=None
        errors_req=[];errors_report=[];clock=[]
        for idx in range(3):
            key=(name,idx)
            submit=arrivals[key]
            f,wait,ex,requested=finish[key]
            if end_request is None:end_request=end_report=submit
            predicted_req=max(end_request,submit)-submit
            predicted_report=max(end_report,submit)-submit
            end_request=max(end_request,submit)+requested
            end_report=max(end_report,submit)+ex
            errors_req.append(abs(predicted_req-wait))
            errors_report.append(abs(predicted_report-wait))
            clock.append(abs((f-submit)-(wait+ex)))
        outcome[name]=dict(requested=max(errors_req),reported=max(errors_report),
                           clock=max(clock))
    return outcome

def audit(raw,audit_path):
    expected=json.loads(Path(audit_path).read_text())
    values=reconstruct(raw)
    cases=expected["cases"]
    if {c["case"] for c in cases}!=set(values):raise ValueError("primary source case mismatch")
    for c in cases:
        v=values[c["case"]]
        if abs(v["requested"]-c["max_abs_requested_service_fcfs_wait_residual_ms"])>1e-6:
            raise ValueError("primary requested-service FIFO reference inconsistent")
        if abs(v["reported"]-c["max_abs_native_service_fcfs_wait_residual_ms"])>1e-6:
            raise ValueError("primary reported-service FIFO reference inconsistent")
        if v["clock"]>1e-6 or c["max_abs_clock_accounting_error_ms"]>1e-6:
            raise ValueError("original Java wait/finish accounting identity incorrect")
    mismatch=sum(v["reported"]>1 for v in values.values())
    if mismatch!=expected["native_reported_service_fcfs_discrepant_cases"]:
        raise ValueError("reported service unresolved count mismatch")
    return dict(status="PASS",source_cases=6,source_native_jobs=18,
                native_service_unreconciled_gt1ms_cases=mismatch,
                all_native_submit_finish_accounting_identities_hold=True,
                original_java_python_30k_parity="FAIL",stage65_safety="FAIL",
                classification="INDEPENDENT_RECOMPUTATION_SAME_SPENT_NATIVE_LOG")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--native",required=True)
    p.add_argument("--primary",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    result=audit(a.native,a.primary)
    Path(a.out).write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print("JPDC_INDEPENDENT_NATIVE_SERVICE_FCFS_DIAGNOSTIC_PASS",json.dumps(result,sort_keys=True))
