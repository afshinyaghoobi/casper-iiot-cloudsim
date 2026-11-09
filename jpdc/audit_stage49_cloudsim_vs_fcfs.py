#!/usr/bin/env python3
"""Stage49 preregistered real CloudSimPlus857 vs ideal FCFS observed-submit audit."""
import argparse,json,math
from pathlib import Path

CASE_NAMES=("MICRO_1US","MICRO_5MS","MICRO_20MS")
EVENT_S=(0.000001,0.005,0.02)
SERVICE_MS=(8.099623,4.730689,9.120283)
ARRIVALS_MS=(0.,5.318920,8.0997406)
TOL=1e-7

def validate(lines):
    native={name:{"submit":[],"finish":{},"outcome":{},"updates":[],"case":None,"done":None}
            for name in CASE_NAMES}
    assert any(x.strip()=="JPDC_STAGE49_REAL_CLOUDSIM_857_THREE_CLOCK_CASES_COMPLETE" for x in lines)
    for ln in lines:
        if not ln.startswith("STAGE49_"):continue
        parts=ln.strip().split(",")
        tag,name=parts[:2]
        assert name in native,(tag,name)
        item=native[name]
        if tag=="STAGE49_CASE":
            assert item["case"] is None
            item["case"]=dict(part.split("=",1) for part in parts[2:])
        elif tag=="STAGE49_SUBMIT":
            if parts[2]!="BEFORE":continue
            _,_,_,t,idval,*_=parts
            item["submit"].append((float(t),int(idval)))
        elif tag=="STAGE49_FINISH":
            _,_,idx,idval,clock,wait,exec_ms,service=parts
            idx=int(idx)
            assert idx not in item["finish"]
            item["finish"][idx]=dict(id=int(idval),clock_ms=float(clock),
                native_wait_ms=float(wait),native_exec_ms=float(exec_ms),service_ms=float(service))
        elif tag=="STAGE49_OUTCOME":
            _,_,idx,idval,wait,exec_ms,arrival,service=parts
            idx=int(idx)
            assert idx not in item["outcome"]
            item["outcome"][idx]=dict(id=int(idval),native_wait_ms=float(wait),
                native_exec_ms=float(exec_ms),requested_arrival_ms=float(arrival),
                service_ms=float(service))
        elif tag=="STAGE49_UPDATE" and parts[2]=="BEFORE":
            item["updates"].append(float(parts[3]))
        elif tag=="STAGE49_CASE_DONE":
            assert item["done"] is None
            item["done"]=dict(part.split("=",1) for part in parts[2:])
    result=[]
    for idx,name in enumerate(CASE_NAMES):
        z=native[name]
        assert z["case"] is not None and z["done"] is not None
        assert len(z["submit"])==len(z["finish"])==len(z["outcome"])==3
        assert int(z["done"]["submissions"])==int(z["done"]["finishes"])==3
        assert math.isclose(float(z["case"]["minEventSec"]),EVENT_S[idx],abs_tol=1e-10)
        assert math.isclose(float(z["case"]["expectedDataCenterFloorMs"]),
            (EVENT_S[idx]+.01)*1000,abs_tol=1e-7)
        submit_by_id=dict((idval,clock) for clock,idval in z["submit"])
        assert len(submit_by_id)==3
        for n in range(3):
            f=z["finish"][n];o=z["outcome"][n]
            assert f["id"]==o["id"]
            assert all(math.isfinite(v) and v>=0 for v in
                (f["clock_ms"],f["native_wait_ms"],f["native_exec_ms"]))
            assert math.isclose(f["native_wait_ms"],o["native_wait_ms"],abs_tol=TOL)
            assert math.isclose(f["native_exec_ms"],o["native_exec_ms"],abs_tol=TOL)
            assert math.isclose(f["service_ms"],SERVICE_MS[n],abs_tol=TOL)
            assert math.isclose(o["service_ms"],SERVICE_MS[n],abs_tol=TOL)
            assert math.isclose(o["requested_arrival_ms"],ARRIVALS_MS[n],abs_tol=TOL)
        assert len(z["updates"])>=1
        by_id={z["finish"][n]["id"]:n for n in range(3)}
        fifo=[]
        previous=0.
        for clock,idval in sorted(z["submit"],key=lambda z:(z[0],z[1])):
            n=by_id[idval]
            ideal_start=max(previous,clock)
            wait=ideal_start-clock
            end=ideal_start+SERVICE_MS[n]
            fifo.append(dict(task_index=n,submission_clock_ms=clock,
                native_finish_callback_clock_ms=z["finish"][n]["clock_ms"],
                native_wait_ms=z["finish"][n]["native_wait_ms"],
                strict_fcfs_observed_submit_wait_ms=wait,
                absolute_wait_discrepancy_ms=abs(z["finish"][n]["native_wait_ms"]-wait),
                native_exec_ms=z["finish"][n]["native_exec_ms"],
                requested_cpu_demand_ms=SERVICE_MS[n],
                execution_minus_demand_ms=z["finish"][n]["native_exec_ms"]-SERVICE_MS[n],
                ideal_fcfs_finish_clock_ms=end))
            previous=end
        assert {x["task_index"] for x in fifo}=={0,1,2}
        first=next(x for x in fifo if x["task_index"]==0)
        if idx==0:
            assert abs(first["native_exec_ms"]-18.100623)<1e-5,("Stage20 original clock drift",first)
        updates=z["updates"]
        gaps=[updates[i]-updates[i-1] for i in range(1,len(updates))]
        result.append(dict(case=name,sim_min_event_sec=EVENT_S[idx],
            predicted_min_datacenter_update_delay_ms=(EVENT_S[idx]+.01)*1000.,
            first_job_native_service_ms=first["native_exec_ms"],
            first_job_ideal_demand_ms=SERVICE_MS[0],
            max_absolute_wait_discrepancy_ms=max(x["absolute_wait_discrepancy_ms"] for x in fifo),
            max_absolute_service_discrepancy_ms=max(abs(x["execution_minus_demand_ms"]) for x in fifo),
            distinct_update_clocks_ms=list(dict.fromkeys(updates)),
            observed_nonzero_update_gaps_ms=[x for x in gaps if x>1e-8],
            by_task=sorted(fifo,key=lambda x:x["task_index"])))
    print("JPDC_STAGE49_REAL_NATIVE_MICRO_AUDIT",json.dumps(
        [{k:v for k,v in x.items() if k not in ("by_task","distinct_update_clocks_ms",
            "observed_nonzero_update_gaps_ms")} for x in result],sort_keys=True),flush=True)
    return dict(status="PASS",physical_model="CloudSimPlus 8.5.7 SpaceShared",
        ideal_reference="strict single-server FCFS from observed native submissions and requested CPU demand",
        source_does_not_fix_prior_failed_30k_queue_parity=True,
        original_E42_and_E46_untouched=True,
        cases=result)

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--input",required=True);p.add_argument("--out",required=True)
    a=p.parse_args()
    source=Path(a.input).read_text().splitlines()
    obj=validate(source)
    f=Path(a.out);f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE49_NATIVE_CLOUDSIM_MATCHED_SUBMIT_FCFS_AUDIT_PASS")
