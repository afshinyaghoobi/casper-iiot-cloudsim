#!/usr/bin/env python3
"""Audit actual native 3-job CloudSimPlus arrival-shift counterfactual snapshots."""
import argparse,csv,json,math
from pathlib import Path

CASES={f"{shift}_{gap}":(third,evt) for shift,third in
       (("EARLY4",4.0997406),("ORIGINAL",8.0997406),("LATE10",18.0997406))
       for gap,evt in (("1US",0.000001),("5MS",0.005))}
SERVICE=(8.099623,4.730689,9.120283)
PLANNED=(0.0,5.318920,0.0)
BASE=1000.0

def parse(path):
    states={k:dict(header=0,done=0,events=[],before={},after={},finished={},outcomes={}) for k in CASES}
    for line in Path(path).read_text().splitlines():
        if not line.startswith(("ARRIVALCF_","JPDC_ARRIVALCF_")):continue
        row=next(csv.reader([line]))
        tag=row[0]
        if tag=="JPDC_ARRIVALCF_NATIVE_SIX_CASES_COMPLETE":continue
        if len(row)<2 or row[1] not in states:raise ValueError("unexpected native case")
        k=row[1];g=states[k]
        if tag=="ARRIVALCF_CASE":
            g["header"]+=1
            if len(row)!=4 or abs(float(row[2].split("=")[1])-CASES[k][1])>1e-12:
                raise ValueError("wrong event gap")
        elif tag=="ARRIVALCF_CASE_DONE":
            g["done"]+=1
            if row[2:]!=["submissions=3","finishes=3"]:raise ValueError("source incomplete")
        elif tag=="ARRIVALCF_SUBMIT":
            if len(row)!=7:raise ValueError("bad submit source row")
            moment=row[2];now=float(row[3]);i=int(row[4])
            if i not in (0,1,2) or moment not in ("BEFORE","AFTER"):raise ValueError("bad submit id")
            if moment=="BEFORE":
                if i in g["before"]:raise ValueError("duplicate submit")
                g["before"][i]=now
            else:
                if i in g["after"]:raise ValueError("duplicate submit AFTER")
                g["after"][i]=now
            g["events"].append(dict(tag=tag,phase=moment,time=now,job=i,
                 exec_ids=ids(row[5]),wait_ids=ids(row[6])))
        elif tag=="ARRIVALCF_UPDATE":
            if len(row)!=6:raise ValueError("bad update source row")
            g["events"].append(dict(tag=tag,phase=row[2],time=float(row[3]),job=None,
                 exec_ids=ids(row[4]),wait_ids=ids(row[5])))
        elif tag=="ARRIVALCF_FINISH":
            if len(row)!=8:raise ValueError("bad finish source row")
            i=int(row[2]);native_id=int(row[3])
            if i!=native_id or i in g["finished"]:raise ValueError("bad finish")
            g["finished"][i]=tuple(map(float,row[4:]))
        elif tag=="ARRIVALCF_OUTCOME":
            if len(row)!=8:raise ValueError("bad native outcome")
            i=int(row[2]);native_id=int(row[3])
            if i!=native_id or i in g["outcomes"]:raise ValueError("bad native outcome ID")
            g["outcomes"][i]=tuple(map(float,row[4:]))
    return states

def ids(s):
    return [] if not s else [int(x) for x in s.split(";")]

def overtake(earlier,execution,waiting):
    """True only if a later actually SUBMITTED job executes ahead of older WAIT."""
    return [(a,b) for a in waiting for b in execution
            if a in earlier and b in earlier and earlier[a]<earlier[b]-1e-7]

def summarize(groups):
    output=[]
    for k in CASES:
        g=groups[k]
        if (g["header"],g["done"])!=(1,1) or any(
             set(g[x])!={0,1,2} for x in ("before","after","finished","outcomes")):
            raise ValueError("missing source case jobs")
        if any(abs(g["before"][i]-g["after"][i])>1e-7 for i in range(3)):
            raise ValueError("submission clock before/after changed")
        snapshots=[]
        submitted={}
        events=g["events"]
        for e in events:
            if e["phase"]=="BEFORE" and e["tag"]=="ARRIVALCF_SUBMIT":
                # job not accepted until AFTER; BEFORE snapshot still reveals earlier jobs
                pass
            if e["phase"]=="AFTER" and e["tag"]=="ARRIVALCF_SUBMIT":
                submitted[e["job"]]=e["time"]
            if set(e["exec_ids"])&set(e["wait_ids"]):
                raise ValueError("same cloudlet in WAIT and EXEC simultaneously")
            if (len(e["exec_ids"])!=len(set(e["exec_ids"])) or
                len(e["wait_ids"])!=len(set(e["wait_ids"])) or
                (set(e["exec_ids"])|set(e["wait_ids"]))-{0,1,2}):
                raise ValueError("native list IDs invalid")
            # Inspect only accepted jobs; unsubmitted job cannot be a bypass
            if (set(e["exec_ids"])|set(e["wait_ids"]))-set(submitted):
                if e["tag"]!="ARRIVALCF_SUBMIT" or e["phase"]!="BEFORE":
                    raise ValueError("source native list included unsubmitted cloudlet")
            observations=overtake(submitted,e["exec_ids"],e["wait_ids"])
            for earlier,later in observations:
                snapshots.append(dict(phase=e["phase"],event=e["tag"],time_ms=round(e["time"],9),
                                      earlier_wait_job=earlier,later_exec_job=later))
        order=sorted(range(3),key=lambda i:(g["before"][i],i))
        prev=None;errors=[]
        rows=[]
        for i in order:
            arrival=g["before"][i]
            if prev is None:prev=arrival
            reference=max(0,prev-arrival)
            prev=max(prev,arrival)+SERVICE[i]
            finish,wait,exec_ms,req=g["finished"][i]
            outcome=g["outcomes"][i]
            expected_arr=(0.0,5.318920,CASES[k][0])[i]
            if abs(req-SERVICE[i])>1e-7 or abs(outcome[3]-SERVICE[i])>1e-7:
                raise ValueError("requested service changed")
            if abs(outcome[2]-expected_arr)>1e-7:
                raise ValueError("planned counterfactual arrival changed")
            if abs(outcome[0]-wait)>1e-7 or abs(outcome[1]-exec_ms)>1e-7:
                raise ValueError("native reported outcome differs from source FINISH")
            if abs(finish-arrival-wait-exec_ms)>1e-6:
                raise ValueError("native finish wait+exec accounting mismatch")
            if min(wait,exec_ms)<-1e-7 or not all(math.isfinite(x) for x in (arrival,finish,wait,exec_ms)):
                raise ValueError("invalid source native wait")
            errors.append(wait-reference)
            rows.append(dict(job=i,native_wait_ms=round(wait,9),
                             ideal_fcfs_requested_wait_ms=round(reference,9),
                             observed_submit_ms=round(arrival,9),
                             native_reported_execution_ms=round(exec_ms,9)))
        output.append(dict(case=k,expected_third_arrival_offset_ms=CASES[k][0],
                           min_event_sec=CASES[k][1],actual_native_submit_order=order,
                           all_3_native_finish=True,native_queue_list_overtaking=bool(snapshots),
                           overtaking_snapshots=snapshots[:20],
                           native_wait_minus_ideal_max_abs_ms=round(max(map(abs,errors)),9),jobs=rows))
    return dict(status="PASS",actual_native_cases=6,completed_cloudlets=18,
                native_overtaking_cases=sum(x["native_queue_list_overtaking"] for x in output),
                original_30k_crossruntime_parity="FAIL",stage65_safety="FAIL",
                native_bypass_does_not_prove_cpu_start=True,
                workload_is_fixed_synthetic_microcase=True,
                independent_iiot_test=False,cases=output)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--native",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    out=summarize(parse(a.native))
    Path(a.out).write_text(json.dumps(out,sort_keys=True,indent=2)+"\n")
    print("JPDC_ARRIVAL_SHIFT_REAL_NATIVE_AUDIT",json.dumps({k:v for k,v in out.items() if k!="cases"},sort_keys=True))

if __name__=="__main__":main()
