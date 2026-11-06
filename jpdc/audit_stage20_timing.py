#!/usr/bin/env python3
"""Read-only original Stage19 versus passive Stage20 event-source parity.

No new task timings are selected; preserves negative physical result.
"""
import argparse,csv,json,math
from pathlib import Path

CASES=("NEAR_ORIGINAL_EVENT_GAP","LATE_AFTER_COMPLETION_CONTROL")
def records(path,prefix):
    x={c:dict(submits=[],outcomes={},finishes=[],updates=[]) for c in CASES}
    for raw in Path(path).read_text().splitlines():
        if not raw.startswith(prefix):continue
        r=next(csv.reader([raw]))
        case=r[1]
        if case not in x:raise AssertionError(("unexpected case",case))
        typ=r[0][len(prefix):]
        if typ=="SUBMIT": x[case]["submits"].append(r[2:])
        elif typ=="OUTCOME":
            assert len(r)==6
            index=int(r[2]);assert index not in x[case]["outcomes"]
            x[case]["outcomes"][index]=r[3:]
        elif typ=="FINISH":x[case]["finishes"].append(r[2:])
        elif typ=="UPDATE":x[case]["updates"].append(r[2:])
    return x
def run(original,current):
    old=records(original,"STAGE19_")
    new=records(current,"STAGE20_")
    out=[]
    for case in CASES:
        o=old[case];n=new[case]
        assert len(o["submits"])==len(n["submits"])==6
        assert sorted(o["outcomes"])==sorted(n["outcomes"])==[0,1,2]
        # Physical scientific parity MUST hold; only diagnostic additional traces differ.
        assert o["submits"]==n["submits"],("passive scheduler snapshots interfered",case)
        assert o["outcomes"]==n["outcomes"],("passive event logging changed outcomes",case)
        assert len(n["finishes"])==3 and len(n["updates"])>0
        finish={int(r[0]):r for r in n["finishes"]}
        assert set(finish)=={0,1,2}
        for i in range(3):
            assert int(finish[i][1])==int(n["outcomes"][i][0])
            assert math.isclose(float(finish[i][3]),float(n["outcomes"][i][1]),abs_tol=1e-9)
            assert math.isclose(float(finish[i][4]),float(n["outcomes"][i][2]),abs_tol=1e-9)
        first=n["finishes"][0]
        updates=[dict(phase=r[0],clock_ms=float(r[1]),running=r[2],waiting=r[3])
                 for r in n["updates"]]
        # Event-clock update may occur multiple times at same timestamp; retain every one.
        update_clocks=sorted(set(round(k["clock_ms"],9) for k in updates))
        first_finish=finish[0]
        item=dict(case=case,
                  first_requested_service_ms=float(first_finish[5]),
                  first_native_reported_execution_ms=float(first_finish[4]),
                  first_finish_callback_ms=float(first_finish[2]),
                  first_native_wait_ms=float(first_finish[3]),
                  third_submission_ms=float(n["submits"][4][1]),
                  scheduler_update_events=len(updates),
                  unique_update_clocks_ms=update_clocks,
                  original_stage19_submit_and_outcome_parity=True,
                  first_execution_over_nominal_ms=round(float(first_finish[4])-float(first_finish[5]),9))
        print("STAGE20_CAUSAL_TIMING_EVIDENCE",json.dumps(item,sort_keys=True))
        out.append(item)
    print("JPDC_STAGE20_ORIGINAL_NATIVE_TIMING_PARITY_PASS")
    return dict(status="PASS",cases=out,limits="Native update and finish observational only; cannot infer why reported execution exceeds ideal service from clocks alone")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original",required=True);p.add_argument("--current",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();result=run(a.original,a.current)
    path=Path(a.out);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
