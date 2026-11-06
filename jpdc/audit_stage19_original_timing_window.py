#!/usr/bin/env python3
"""Stage19 archived native run timing audit; marks invalid bypass window explicitly.

No new Java simulation, no retrospective arrival-time adjustment.
"""
import csv,json,math,sys
from pathlib import Path
runs={}
for line in Path(sys.argv[1]).read_text().splitlines():
    if not line.startswith(("STAGE19_OUTCOME,","STAGE19_SUBMIT,")):continue
    r=next(csv.reader([line]))
    if r[0]=="STAGE19_OUTCOME":
        _,case,ordinal,cloudlet_id,wait_ms,service_ms=r
        runs.setdefault(case,{}).setdefault("outcomes",{})[int(ordinal)]=dict(
            cloudlet_id=int(cloudlet_id),wait_ms=float(wait_ms),service_ms=float(service_ms))
    else:
        _,case,phase,clock,cloudlet,running,waiting=r
        runs.setdefault(case,{}).setdefault("snapshots",[]).append(dict(
            phase=phase,clock_ms=float(clock),cloudlet_id=int(cloudlet),
            running=[int(x) for x in running.split(";") if x],
            waiting=[int(x) for x in waiting.split(";") if x]))
for case in ("NEAR_ORIGINAL_EVENT_GAP","LATE_AFTER_COMPLETION_CONTROL"):
    d=runs[case];o=d["outcomes"];ss=d["snapshots"]
    assert set(o)=={0,1,2} and len(ss)==6
    third=ss[4]
    assert third["phase"]=="BEFORE" and third["cloudlet_id"]==o[2]["cloudlet_id"]
    first_start=1000.0+o[0]["wait_ms"]
    first_estimated_end=first_start+o[0]["service_ms"]
    first_running_at_third=o[0]["cloudlet_id"] in third["running"]
    feasible_window=(not first_running_at_third and o[1]["cloudlet_id"] in third["waiting"])
    res=dict(case=case,actual_first_service_ms=o[0]["service_ms"],
             originally_designed_first_service_ms=8.099623,
             first_start_ms=first_start,
             first_estimated_end_ms_from_reported_execution=first_estimated_end,
             third_submit_ms=third["clock_ms"],
             first_still_running_at_third=first_running_at_third,
             older_waiting_at_third=o[1]["cloudlet_id"] in third["waiting"],
             free_PE_while_old_waiting_condition_observed=feasible_window,
             finding=("NOT_AN_ACTUAL_BYPASS_OPPORTUNITY" if not feasible_window
                      else "ELIGIBLE_BYPASS_OPPORTUNITY"))
    print("STAGE19_ARCHIVED_VALIDITY",json.dumps(res,sort_keys=True))
    assert not feasible_window, "Original forensic observation changed; preserve records and reassess"
print("JPDC_STAGE19_ARCHIVED_WINDOW_VALIDITY_AUDIT_PASS")
