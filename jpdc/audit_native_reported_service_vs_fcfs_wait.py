#!/usr/bin/env python3
"""Independent retrospective source-native timing decomposition.

Reconsumes original CloudSimPlus 8.5.7 Stage67 native log; no Java rerun.
Native reported duration is a POSTHOC diagnostic, not a predictor.
"""
import argparse
import collections
import csv
import hashlib
import json
import math
from pathlib import Path

ORIGINAL_NATIVE_SHA="61d92e93812b20b473d70c9b3ba5a67f65af574fcd35c5e6a590f19a76b6e9eb"
ORIGINAL_HEAD="9c3bc5ae2dbd4d0b95b54b09cc8d9f3993ba9afc"
CASES=("SCALE_50_1US","SCALE_50_5MS","SCALE_100_1US","SCALE_100_5MS",
       "SCALE_200_1US","SCALE_200_5MS")

def parse_source(path):
    data=Path(path).read_bytes()
    if hashlib.sha256(data).hexdigest()!=ORIGINAL_NATIVE_SHA:
        raise ValueError("source original native evidence hash mismatch")
    groups={name:dict(quoted={},finish={},outcome={},header=0,done=0) for name in CASES}
    for line in data.decode("utf-8").splitlines():
        row=next(csv.reader([line]))
        if row[0]=="STAGE67_CASE":
            case=row[1]
            if case not in groups:raise ValueError("unexpected native case")
            groups[case]["header"]+=1
        elif row[0]=="STAGE67_SUBMIT" and row[2]=="BEFORE":
            case=row[1]
            idx=int(row[4]);clock=float(row[3])
            group=groups[case]
            if idx in group["quoted"]:raise ValueError("duplicate original submit")
            group["quoted"][idx]=clock
        elif row[0]=="STAGE67_FINISH":
            case=row[1];idx=int(row[2]);job=int(row[3])
            group=groups[case]
            if idx in group["finish"] or job!=idx:raise ValueError("duplicate/mismatched finish")
            group["finish"][idx]=dict(clock=float(row[4]),wait=float(row[5]),
                native_service=float(row[6]),requested_service=float(row[7]))
        elif row[0]=="STAGE67_OUTCOME":
            case=row[1];idx=int(row[2]);job=int(row[3])
            if idx in groups[case]["outcome"] or job!=idx:
                raise ValueError("duplicate/mismatched outcome")
            groups[case]["outcome"][idx]=(float(row[4]),float(row[5]),
                                         float(row[6]),float(row[7]))
        elif row[0]=="STAGE67_CASE_DONE":
            case=row[1];groups[case]["done"]+=1
            if row[2:]!=["submissions=3","finishes=3"]:
                raise ValueError("incomplete native case")
    for case,g in groups.items():
        if g["header"]!=1 or g["done"]!=1 or (
            set(g["quoted"])!=set(range(3)) or
            set(g["finish"])!=set(range(3)) or
            set(g["outcome"])!=set(range(3))):
            raise ValueError(f"source incomplete case: {case}")
        for idx in range(3):
            f=g["finish"][idx];o=g["outcome"][idx]
            if max(abs(x-y) for x,y in zip(o[:2],(f["wait"],f["native_service"])))>1e-7:
                raise ValueError("native outcome versus finish mismatch")
            if abs(o[3]-f["requested_service"])>1e-7:raise ValueError("native requested duration mismatch")
    return groups

def analyze(groups):
    cases=[]
    for case in CASES:
        g=groups[case]
        ordered=sorted(g["quoted"],key=lambda idx:(g["quoted"][idx],idx))
        if ordered!=[0,1,2]:raise ValueError("original native submit order mismatch")
        prev_requested=prev_native=None
        diffs_requested=[];diffs_native=[];identities=[];inflations=[]
        jobs=[]
        for idx in ordered:
            submit=g["quoted"][idx]
            obs=g["finish"][idx]
            req=obs["requested_service"]
            native=obs["native_service"]
            wait=obs["wait"]
            if not all(math.isfinite(x) for x in (submit,req,native,wait,obs["clock"])):
                raise ValueError("nonfinite original native clock/service")
            if min(req,native,wait)<-1e-7 or obs["clock"]<submit:
                raise ValueError("negative native resource or impossible clock")
            if prev_requested is None:prev_requested=prev_native=submit
            ideal_requested=max(0.0,prev_requested-submit)
            ideal_native=max(0.0,prev_native-submit)
            prev_requested=max(prev_requested,submit)+req
            prev_native=max(prev_native,submit)+native
            dreq=wait-ideal_requested
            dnative=wait-ideal_native
            identity=obs["clock"]-submit-(wait+native)
            inflation=native-req
            if abs(identity)>1e-6:raise ValueError("native wait+exec accounting not conserved")
            diffs_requested.append(dreq);diffs_native.append(dnative)
            identities.append(identity);inflations.append(inflation)
            jobs.append(dict(job_index=idx,observed_submit_ms=round(submit,9),
                native_finish_ms=round(obs["clock"],9),native_reported_wait_ms=round(wait,9),
                native_reported_execution_ms=round(native,9),requested_cpu_ms=round(req,9),
                ideal_requested_service_fcfs_wait_ms=round(ideal_requested,9),
                ideal_native_reported_service_fcfs_wait_ms=round(ideal_native,9),
                requested_fcfs_residual_ms=round(dreq,9),
                native_service_fcfs_residual_ms=round(dnative,9),
                native_execution_minus_requested_ms=round(inflation,9)))
        cases.append(dict(case=case,source_jobs=3,
            max_abs_requested_service_fcfs_wait_residual_ms=round(max(map(abs,diffs_requested)),9),
            max_abs_native_service_fcfs_wait_residual_ms=round(max(map(abs,diffs_native)),9),
            sum_native_exec_minus_requested_ms=round(sum(inflations),9),
            source_jobs_with_gt_0_001ms_exec_inflation=sum(abs(x)>0.001 for x in inflations),
            max_abs_clock_accounting_error_ms=round(max(map(abs,identities)),12),
            native_service_alone_insufficient_at_gt_1ms=any(abs(x)>1.0 for x in diffs_native),
            jobs=jobs))
    return dict(status="PASS",classification="RETROSPECTIVE_SPENT_NATIVE_CLOUDSIM_857_DIAGNOSTIC",
        source_original_native_log_sha256=ORIGINAL_NATIVE_SHA,
        original_native_cases=len(cases),original_native_jobs=sum(x["source_jobs"] for x in cases),
        requested_service_fcfs_discrepant_cases=sum(x["max_abs_requested_service_fcfs_wait_residual_ms"]>1.0 for x in cases),
        native_reported_service_fcfs_discrepant_cases=sum(x["native_service_alone_insufficient_at_gt_1ms"] for x in cases),
        overall_max_abs_native_service_fcfs_wait_residual_ms=max(
            x["max_abs_native_service_fcfs_wait_residual_ms"] for x in cases),
        native_accounting_identity_passes_all_cases=True,
        retrospective_requested_service_not_full_explanation=True,
        independently_validated_30k_java_python_queue_parity=False,
        new_original_source_seed=False,actual_new_native_java_experiment=False,
        independent_iiot_workload=False,
        stage65_safety="FAIL",original_java_python_30k_parity="FAIL",cases=cases)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--native",required=True)
    ap.add_argument("--repeat",required=True)
    ap.add_argument("--source-commit",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    if Path(args.native).read_bytes()!=Path(args.repeat).read_bytes():
        raise ValueError("original native repeats mismatch")
    if Path(args.source_commit).read_text().strip()!=ORIGINAL_HEAD:
        raise ValueError("original native source Git commit changed")
    result=analyze(parse_source(args.native))
    dest=Path(args.out);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print("JPDC_NATIVE_SOURCE_POSTHOC_SERVICE_WAIT_DECOMPOSITION",json.dumps(
        {k:v for k,v in result.items() if k!="cases"},sort_keys=True))
    print("JPDC_NATIVE_SIX_CASE_REPORTED_SERVICE_ONLY_INSUFFICIENT_DIAGNOSTIC_PASS")

if __name__=="__main__":main()
