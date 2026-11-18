#!/usr/bin/env python3
"""Retrospective A2 native-reported service oracle diagnostic. Uses original A2 native.log.
Not a prospective calibration, scheduling oracle, randomized holdout, or CloudSim bug proof.
"""
import argparse,csv,json,math,statistics
from pathlib import Path
SERVICE=(8,13,5,19,7,11,17,6,14,9,16,10)
def audit(raw):
    cases={}
    for line in Path(raw).read_text().splitlines():
        if not line.startswith("A2_"):continue
        row=next(csv.reader([line]));kind=row[0];name=row[1]
        group=cases.setdefault(name,{"sub":[],"finish":{},"complete":0})
        if kind=="A2_SUBMIT" and row[2]=="AFTER":
            group["sub"].append((int(row[4]),float(row[3])))
        elif kind=="A2_FINISH":
            idx=int(row[2]);job=int(row[3])
            if job!=idx or idx in group["finish"]:raise ValueError("bad finished job")
            group["finish"][idx]=tuple(map(float,row[4:]))
        elif kind=="A2_DONE":
            if row[2]!="12":raise ValueError("unfinished jobs")
            group["complete"]+=1
    if len(cases)!=24:raise ValueError("missing cases")
    result=[]
    for name,g in sorted(cases.items()):
        sub=g["sub"];finish=g["finish"]
        if g["complete"]!=1 or len(sub)!=12 or set(i for i,_ in sub)!=set(range(12)) or set(finish)!=set(range(12)):
            raise ValueError("incomplete native input "+name)
        pes=int(name.rsplit("_P",1)[1])
        free_requested=[sub[0][1]]*pes;free_native=[sub[0][1]]*pes
        abs_requested=[];abs_oracle=[];inflation=[]
        disagree_req={25:0,50:0};disagree_oracle={25:0,50:0}
        for idx,t in sub:
            native_finish,native_wait,native_service,nominal_arr,requested=finish[idx]
            if not all(math.isfinite(v) for v in (t,native_finish,native_wait,native_service,nominal_arr,requested)):
                raise ValueError("nonfinite values")
            if abs(requested-SERVICE[idx])>1e-6:raise ValueError("wrong service request")
            ir=min(range(pes),key=lambda i:(free_requested[i],i))
            io=min(range(pes),key=lambda i:(free_native[i],i))
            ref_start=max(t,free_requested[ir]);oracle_start=max(t,free_native[io])
            free_requested[ir]=ref_start+requested;free_native[io]=oracle_start+native_service
            abs_requested.append(abs(native_wait-(ref_start-t)))
            abs_oracle.append(abs(native_wait-(oracle_start-t)))
            inflation.append(native_service-requested)
            for m in (25,50):
                n=native_finish>t+m+1e-8
                disagree_req[m]+=int(n!=(free_requested[ir]>t+m+1e-8))
                disagree_oracle[m]+=int(n!=(free_native[io]>t+m+1e-8))
        result.append({
            "case":name,
            "max_abs_wait_requested_ms":round(max(abs_requested),9),
            "max_abs_wait_native_service_oracle_ms":round(max(abs_oracle),9),
            "mean_abs_wait_requested_ms":round(statistics.mean(abs_requested),9),
            "mean_abs_wait_native_service_oracle_ms":round(statistics.mean(abs_oracle),9),
            "count_service_duration_differs":sum(abs(x)>1e-6 for x in inflation),
            "max_positive_service_inflation_ms":round(max(inflation),9),
            "deadline25_disagree_requested":disagree_req[25],
            "deadline25_disagree_oracle":disagree_oracle[25],
            "deadline50_disagree_requested":disagree_req[50],
            "deadline50_disagree_oracle":disagree_oracle[50]})
    return {
      "status":"RETROSPECTIVE_DIAGNOSTIC",
      "cases":24,"completed_jobs":288,
      "service_length_differs_jobs":sum(x["count_service_duration_differs"] for x in result),
      "max_abs_requested_ms":max(x["max_abs_wait_requested_ms"] for x in result),
      "max_abs_oracle_ms":max(x["max_abs_wait_native_service_oracle_ms"] for x in result),
      "oracle_residual_gt_1ms_cases":sum(x["max_abs_wait_native_service_oracle_ms"]>1 for x in result),
      "deadline_disagreement_requested_25ms":sum(x["deadline25_disagree_requested"] for x in result),
      "deadline_disagreement_oracle_25ms":sum(x["deadline25_disagree_oracle"] for x in result),
      "deadline_disagreement_requested_50ms":sum(x["deadline50_disagree_requested"] for x in result),
      "deadline_disagreement_oracle_50ms":sum(x["deadline50_disagree_oracle"] for x in result),
      "original_30k_crossruntime_parity":"FAIL","stage65_safety":"FAIL",
      "oracle_uses_after_completion_service_not_realtime_observable":True,
      "results":result}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--native",required=True);ap.add_argument("--out",required=True)
    args=ap.parse_args()
    result=audit(args.native)
    Path(args.out).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="results"},sort_keys=True))
if __name__=="__main__":main()
