#!/usr/bin/env python3
"""Audit genuinely executed (not synthetic) Stage19 CloudSimPlus 8.5.7 microfixture."""
import argparse,json,csv,math
from pathlib import Path
CASES=("NEAR_ORIGINAL_EVENT_GAP","LATE_AFTER_COMPLETION_CONTROL")
ARRIVALS={"NEAR_ORIGINAL_EVENT_GAP":(0.,5.318920,8.0997406),
          "LATE_AFTER_COMPLETION_CONTROL":(0.,5.318920,10.)}
def audit(path):
    snapshots={c:[] for c in CASES}
    outcomes={c:{} for c in CASES}
    done={}
    lines=Path(path).read_text().splitlines()
    for line in lines:
        if not line.startswith(("STAGE19_","JPDC_STAGE19_")):continue
        xs=next(csv.reader([line]))
        if xs[0]=="STAGE19_SUBMIT":
            assert len(xs)==7 and xs[1] in CASES and xs[2] in ("BEFORE","AFTER")
            snapshots[xs[1]].append(dict(phase=xs[2],clock_ms=float(xs[3]),
                id=int(xs[4]),running=[int(i) for i in xs[5].split(";") if i],
                waiting=[int(i) for i in xs[6].split(";") if i]))
        elif xs[0]=="STAGE19_OUTCOME":
            assert len(xs)==6 and xs[1] in CASES
            outcomes[xs[1]][int(xs[2])]=dict(id=int(xs[3]),wait_ms=float(xs[4]),service_ms=float(xs[5]))
        elif xs[0]=="STAGE19_CASE_DONE":
            assert xs[1] in CASES and xs[1] not in done
            done[xs[1]]=(int(xs[2].split("=")[1]),int(xs[3].split("=")[1]))
    assert set(done)==set(CASES)
    result=[]
    for case in CASES:
        ss=snapshots[case];oo=outcomes[case]
        assert done[case]==(3,3)
        assert len(ss)==6 and set(oo)=={0,1,2}
        for ix in range(3):
            assert ss[2*ix]["phase"]=="BEFORE" and ss[2*ix+1]["phase"]=="AFTER"
            assert ss[2*ix]["id"]==ss[2*ix+1]["id"]==oo[ix]["id"]
            assert math.isclose(ss[2*ix]["clock_ms"],ss[2*ix+1]["clock_ms"],abs_tol=1e-8)
        b,a=ss[4],ss[5]
        bypass=(oo[1]["id"] in b["waiting"] and
                oo[1]["id"] in a["waiting"] and oo[2]["id"] in a["running"])
        start=[1000+ARRIVALS[case][i]+oo[i]["wait_ms"] for i in range(3)]
        order=sorted(range(3),key=lambda i:(start[i],i))
        item=dict(case=case,source_CloudSimPlus_857=True,submission_order=[oo[i]["id"] for i in range(3)],
                  starts_ms=start,observed_service_start_order_indices=order,
                  direct_admission_bypass_with_older_waiting=bypass,
                  third_before=b,third_after=a,
                  mission_scheduler_scope="microfixture only, no original E42")
        print("STAGE19_ACTUAL_MICRO_RESULT",json.dumps(item,sort_keys=True))
        result.append(item)
    print("JPDC_STAGE19_NATIVE_MICRO_EVENT_AUDIT_PASS")
    return dict(status="PASS",cases=result,original_strict_fcfs_queue_fidelity="FAIL 9.12140093294972ms >5ms")
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--log",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();x=audit(a.log)
    dest=Path(a.out);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
