#!/usr/bin/env python3
"""Stage34 read-only causal HIGH-to-MISSION proxy comparison on seed90.

Only uses original Stage27 fixed physical trace, never runs source physics.
All conditional inclusion percentages exclude abstained and therefore do not
imply improved hard-deadline reliability.
"""
import argparse,json,math
from collections import defaultdict
from pathlib import Path
from causal_high_mission_proxy_stage34 import CausalClassProxyRecovery as CausalRecoveryGuard
from replay_stage32_archived_recovery import one as strict_own_recovery
from replay_stage30_archived_cpu_alarm import run_one as frozen_stage30

def one(trace):
    truth={}
    timeline=[]
    for r in trace:
        i=r["task_index"]
        assert i not in truth and 0<=i<12000
        truth[i]=r
        timeline.extend(((r["arrival_ms"],2,i),(r["delivered_cpu_finish_ms"],0,i)))
    assert len(truth)==12000
    timeline.sort()
    g=CausalRecoveryGuard()
    decisions={}
    groups=defaultdict(lambda:dict(n=0,original_issued=0,recovered_issued=0,
                                   sparse_abstained=0,post_alarm_rebuild_abstained=0,proxy_issued=0,proxy_covered=0,proxy_missed=0,
                                   original_covered=0,recovered_covered=0,
                                   original_missed=0,recovered_missed=0,
                                   max_interval_violation_ms=0.))
    for clock,kind,idx in timeline:
        r=truth[idx]
        age=r["arrival_ms"]-r["last_queue_telemetry_ms"]
        if kind==2:
            d=g.query(clock,r["task_class"],age)
            assert not d.certified and not d.original.certified
            assert d.original.context==r["queue_model_context"]
            decisions[idx]=d
            g.dispatch(idx,r["node"],r["task_class"],clock,age,
                       r["predicted_wait_at_dispatch_ms"],r["predicted_cpu_at_dispatch_ms"])
        else:
            assert idx in decisions
            d=decisions[idx]
            y=g.finish(idx,r["node"],r["actual_start_ms"],clock)
            assert math.isclose(y,r["signed_nonnetwork_residual_ms"],rel_tol=0,abs_tol=1e-8)
            phase="post" if idx>=10000 else "pre"
            for key in (("all",),("phase",phase),("phase_class",phase,r["task_class"])):
                v=groups[key];v["n"]+=1
                if d.phase=="prealarm_original":
                    v["original_issued"]+=1
                    if d.original.lower_ms<=y<=d.original.upper_ms:v["original_covered"]+=1
                    else:
                        v["original_missed"]+=1
                        v["max_interval_violation_ms"]=max(v["max_interval_violation_ms"],
                            max(d.original.lower_ms-y,y-d.original.upper_ms))
                elif d.phase=="postalarm_recovered_descriptive":
                    v["recovered_issued"]+=1
                    if d.original.lower_ms<=y<=d.original.upper_ms:v["recovered_covered"]+=1
                    else:
                        v["recovered_missed"]+=1
                        v["max_interval_violation_ms"]=max(v["max_interval_violation_ms"],
                            max(d.original.lower_ms-y,y-d.original.upper_ms))
                elif d.phase=="postalarm_proxy_descriptive":
                    assert d.proxy_source=="HIGH" and r["task_class"]=="MISSION"
                    v["recovered_issued"]+=1
                    v["proxy_issued"]+=1
                    if d.original.lower_ms<=y<=d.original.upper_ms:
                        v["recovered_covered"]+=1
                        v["proxy_covered"]+=1
                    else:
                        v["recovered_missed"]+=1
                        v["proxy_missed"]+=1
                        v["max_interval_violation_ms"]=max(v["max_interval_violation_ms"],
                            max(d.original.lower_ms-y,y-d.original.upper_ms))
                elif d.phase=="prealarm_sparse":
                    v["sparse_abstained"]+=1
                else:
                    assert d.phase=="postalarm_rebuild"
                    v["post_alarm_rebuild_abstained"]+=1
    assert len(decisions)==g.frozen.base.dispatches==g.frozen.base.finishes==12000
    assert not g.frozen.base.pending
    if g.epoch is not None:assert not g.epoch.pending
    g.invariant()
    outgroups={}
    for key,v in sorted(groups.items()):
        assert v["n"]==sum(v[x] for x in ("original_issued","recovered_issued","sparse_abstained","post_alarm_rebuild_abstained"))
        assert v["original_issued"]==v["original_covered"]+v["original_missed"]
        assert v["recovered_issued"]==v["recovered_covered"]+v["recovered_missed"]
        assert v["proxy_issued"]==v["proxy_covered"]+v["proxy_missed"]
        issued=v["original_issued"]+v["recovered_issued"]
        outgroups["/".join(key)]={**v,
            "available_fraction":issued/v["n"],
            "original_issued_inclusion":v["original_covered"]/v["original_issued"] if v["original_issued"] else None,
            "recovered_issued_inclusion":v["recovered_covered"]/v["recovered_issued"] if v["recovered_issued"] else None,
            "all_issued_inclusion":(v["original_covered"]+v["recovered_covered"])/issued if issued else None,
            "proxy_inclusion":v["proxy_covered"]/v["proxy_issued"] if v["proxy_issued"] else None}
    return dict(alarm_trigger_clock_ms=g.frozen.first_alarm_delivery_ms,
                first_recovery_by_context=[dict(task_class=k[0],telemetry_age_band=k[1],
                                            first_issue_clock_ms=t,lag_since_alarm_ms=t-g.epoch_started_ms)
                                           for k,t in sorted(g.recovery_times.items())],
                epoch_cpu_labels=g.epoch_finished,
                proxy_issued=g.proxy_issued,
                proxy_recovery_times=[{"task_class":k[0],"age_band":k[1],"time_ms":t} for k,t in sorted(g.proxy_recovery_times.items())],
                original_issued=g.issued_original,recovered_issued=g.issued_recovered,
                sparse_abstentions=g.abstained_pre_sparse,rebuild_abstentions=g.abstained_rebuilding,
                groups=outgroups)

def main(original_path,output):
    old=json.loads(Path(original_path).read_text())
    assert old["status"]=="PASS" and old["scientific_seed"]==90 and len(old["rows"])==4
    rows=[]
    for a in old["rows"]:
        prior=frozen_stage30(a["trace"])
        own=strict_own_recovery(a["trace"])
        r=one(a["trace"])
        assert r["alarm_trigger_clock_ms"]==prior["alarm"]["alarm_clock_ms"]==own["alarm_trigger_clock_ms"]
        assert r["original_issued"]==prior["groups"]["all"]["issued"]
        assert r["sparse_abstentions"]==prior["groups"]["all"]["sparse"]
        assert r["recovered_issued"]+r["rebuild_abstentions"]==prior["groups"]["all"]["revoked"]
        assert r["recovered_issued"]>=own["recovered_issued"]
        assert r["proxy_issued"]==r["recovered_issued"]-own["recovered_issued"]
        assert r["rebuild_abstentions"]==own["rebuild_abstentions"]-r["proxy_issued"]
        post=r["groups"]["phase/post"]
        mission=r["groups"]["phase_class/post/MISSION"]
        high=r["groups"]["phase_class/post/HIGH"]
        compact=dict(scenario=a["stats"]["scenario"],policy=a["stats"]["policy"],
                     alarm_clock_ms=r["alarm_trigger_clock_ms"],
                     original_issued=r["original_issued"],recovered_issued=r["recovered_issued"],
                     sparse_abstentions=r["sparse_abstentions"],rebuild_abstentions=r["rebuild_abstentions"],
                     post=post,post_mission=mission,post_high=high,
                     proxy_issued=r["proxy_issued"],
                     strict_own_post_mission=own["groups"]["phase_class/post/MISSION"],
                     recovered_contexts=len(r["first_recovery_by_context"]))
        print("STAGE34_ARCHIVED_PROXY_RESULT",json.dumps(compact,sort_keys=True),flush=True)
        rows.append(dict(scenario=compact["scenario"],policy=compact["policy"],**r))
    x=dict(status="PASS",source_seed=90,source_original_run=42269844289,
           no_new_source_physics=True,scientific_independent_replicates=1,
           note="descriptive recovered intervals, abstentions never count as covered, no coverage guarantee",
           rows=rows)
    dest=Path(output);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE34_ARCHIVED_CAUSAL_PROXY_NEGATIVE_TRANSFER_REPLAY_PASS")
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--original",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();main(a.original,a.out)
