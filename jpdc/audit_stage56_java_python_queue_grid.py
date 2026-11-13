#!/usr/bin/env python3
"""Stage56 real Java CloudSimPlus SpaceShared vs independent strict FCFS audit.

Diagnostic differences are expected and must never be silently "corrected".
"""
import argparse
import json
import math
from pathlib import Path

PROFILE_OFFSETS={
    "ISOLATED":(0,75,150,225,300,375,450,525,600,675,750,825),
    "BURST":(0,.2,.4,.6,.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2),
    "WAVES":(0,5.318920,8.0997406,25,25.5,30,50,55.4,55.6,75,80,84)
}
SERVICES=(8.099623,4.730689,9.120283,6.4,11.3,4.5,7.2,12.7,3.6,10.2,5.1,8.8)
GAPS=(.000001,.005,.02)
N=12


def number(s):
    v=float(s)
    assert math.isfinite(v) and v>=0, s
    return v


def parse_ids(v):
    ids=[int(x) for x in v.split(";") if x]
    assert all(x>=0 for x in ids)
    assert len(ids)==len(set(ids))
    return ids


def audit(lines):
    assert "JPDC_STAGE56_NATIVE_GRID_COMPLETE" in lines, "missing native completion"
    allcases={}
    for profile,offsets in PROFILE_OFFSETS.items():
        for gap_ix,gap in enumerate(GAPS):
            name=f"{profile}_{gap_ix}"
            events=[]
            before={}
            after={}
            finishes={}
            outcomes={}
            case_records=[]
            ends=[]
            for seq,line in enumerate(lines):
                if not line.startswith("STAGE56_"):
                    continue
                p=line.split(",")
                if len(p)<2 or p[1]!=name:
                    continue
                kind=p[0]
                if kind=="STAGE56_CASE":
                    assert len(p)==5
                    case_records.append((p[2],number(p[3]),int(p[4])))
                elif kind=="STAGE56_END":
                    assert len(p)==5
                    ends.append([int(x) for x in p[2:]])
                elif kind=="STAGE56_SUBMIT":
                    assert len(p)==7
                    _,_,phase,ts,cid,exec_s,wait_s=p
                    assert phase in ("BEFORE","AFTER")
                    ts=number(ts)
                    cid=int(cid)
                    assert cid>=0
                    record=dict(seq=seq,kind="SUBMIT_"+phase,clock_ms=ts,
                                cloudlet=cid,exec_ids=parse_ids(exec_s),
                                waiting_ids=parse_ids(wait_s))
                    events.append(record)
                    if phase=="BEFORE":
                        assert cid not in before
                        before[cid]=record
                    else:
                        assert cid in before and cid not in after
                        assert abs(before[cid]["clock_ms"]-ts)<=1e-6
                        after[cid]=record
                elif kind=="STAGE56_UPDATE":
                    assert len(p)==6
                    _,_,phase,ts,exec_s,wait_s=p
                    assert phase in ("BEFORE","AFTER")
                    events.append(dict(seq=seq,kind="UPDATE_"+phase,
                                       clock_ms=number(ts),
                                       exec_ids=parse_ids(exec_s),
                                       waiting_ids=parse_ids(wait_s)))
                elif kind=="STAGE56_FINISH":
                    assert len(p)==5
                    ix,cid=int(p[2]),int(p[3])
                    assert ix not in finishes and cid>=0
                    finishes[ix]=(cid,number(p[4]))
                elif kind=="STAGE56_OUTCOME":
                    assert len(p)==8
                    ix,cid=int(p[2]),int(p[3])
                    assert ix not in outcomes and cid>=0
                    outcomes[ix]=dict(cloudlet=cid,native_wait_ms=number(p[4]),
                                      native_execution_ms=number(p[5]),
                                      arrival_offset_ms=number(p[6]),
                                      requested_service_ms=number(p[7]))
                else:
                    raise AssertionError(("unknown stage56 record",line))
            assert case_records==[(profile,gap,N)],(name,case_records)
            assert ends==[[N,N,N]],(name,ends)
            assert len(before)==len(after)==len(finishes)==len(outcomes)==N
            assert set(outcomes)==set(finishes)==set(range(N))
            outcome_ids=[outcomes[i]["cloudlet"] for i in range(N)]
            assert len(set(outcome_ids))==N
            assert set(outcome_ids)==set(before)==set(after)
            for i in range(N):
                assert finishes[i][0]==outcome_ids[i]
                assert abs(outcomes[i]["arrival_offset_ms"]-offsets[i])<1e-6
                assert abs(outcomes[i]["requested_service_ms"]-SERVICES[i])<1e-6
                assert finishes[i][1]+1e-6>=before[outcome_ids[i]]["clock_ms"]
            assert events
            # A scheduler observes an event stream in native time; prohibit time reversal.
            for prev,next_event in zip(events,events[1:]):
                assert next_event["clock_ms"]+1e-6>=prev["clock_ms"],(name,prev,next_event)
            assert sum(e["kind"]=="UPDATE_BEFORE" for e in events)==sum(
                e["kind"]=="UPDATE_AFTER" for e in events)
            assert any(e["kind"]=="UPDATE_BEFORE" for e in events)
            ids=set(outcome_ids)
            for e in events:
                ex=e["exec_ids"];wa=e["waiting_ids"]
                assert set(ex).issubset(ids) and set(wa).issubset(ids)
                assert len(ex)<=1 and not (set(ex)&set(wa))
            # Independently predicted strict FIFO from native observed submits ONLY.
            ordered=sorted(ids,key=lambda cid:(before[cid]["clock_ms"],before[cid]["seq"]))
            by_id={outcomes[i]["cloudlet"]:i for i in range(N)}
            previous_finish=0.0
            ideal={}
            for cid in ordered:
                arrival=before[cid]["clock_ms"]
                start=max(previous_finish,arrival)
                wait=start-arrival
                ideal[cid]=wait
                previous_finish=start+SERVICES[by_id[cid]]
            rows=[]
            first_exec={}
            for e in events:
                for cid in e["exec_ids"]:
                    first_exec.setdefault(cid,(e["clock_ms"],e["seq"]))
            assert set(first_exec)==ids,("some jobs never seen executing",name)
            exec_order=sorted(ids,key=lambda cid:first_exec[cid][1])
            rank={cid:i for i,cid in enumerate(ordered)}
            # rank inversions in first-seen execution list, not verified physical CPU start.
            inversions=sum(rank[exec_order[i]]>rank[exec_order[j]]
                           for i in range(N) for j in range(i+1,N))
            for i in range(N):
                out=outcomes[i]
                cid=out["cloudlet"]
                observed=out["native_wait_ms"]
                observed_start=first_exec[cid][0]
                submitted=before[cid]["clock_ms"]
                rows.append(dict(index=i,cloudlet_id=cid,
                    native_scheduler_submit_ms=submitted,
                    native_wait_ms=observed,ideal_strict_fcfs_wait_ms=ideal[cid],
                    wait_signed_difference_ms=observed-ideal[cid],
                    first_observed_exec_ms=observed_start,
                    wait_minus_first_exec_observation_ms=observed-(observed_start-submitted),
                    native_execution_ms=out["native_execution_ms"],
                    requested_service_ms=out["requested_service_ms"]))
            errs=[abs(x["wait_signed_difference_ms"]) for x in rows]
            allcases[name]=dict(profile=profile,clock_gap_s=gap,task_count=N,
                native_admission_id_order=ordered,native_first_exec_id_order=exec_order,
                exec_first_observation_pair_inversions=inversions,
                mean_absolute_wait_difference_ms=sum(errs)/N,
                max_absolute_wait_difference_ms=max(errs),
                count_wait_difference_gt_1ms=sum(x>1 for x in errs),
                count_wait_difference_gt_5ms=sum(x>5 for x in errs),
                max_native_wait_minus_exec_observation_ms=max(
                    abs(x["wait_minus_first_exec_observation_ms"]) for x in rows),
                rows=rows)
    assert len(allcases)==9
    return dict(status="PASS",native_runtime="CloudSimPlus 8.5.7 Java17 SpaceShared",
                independent_reference="Python strict FCFS, native observed scheduler submission clocks",
                task_observations=9*N,
                fixture_cases=9,
                original_30k_queue_wait_fidelity="STILL FAIL, not retested",
                stage52_CPU_harm="PRESERVED",
                no_software_or_scheduler_changes_to_E42_E46=True,
                cases=allcases)


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    obj=audit(Path(a.input).read_text().splitlines())
    p=Path(a.out);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+"\n")
    for name,case in sorted(obj["cases"].items()):
        print("JPDC_STAGE56_NATIVE_VS_IDEAL",name,
              "MAX_AE",case["max_absolute_wait_difference_ms"],
              "GT5",case["count_wait_difference_gt_5ms"],
              "INVERSIONS",case["exec_first_observation_pair_inversions"])
    print("JPDC_STAGE56_REAL_NATIVE_VS_INDEPENDENT_FCFS_AUDIT_PASS")
