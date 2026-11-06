#!/usr/bin/env python3
"""Stage12 exploratory audit of Stage11 delayed per-node E2E feedback, seed83 S3.
All task-index and affected-node truth is used OFFLINE only, after simulate().
"""
import argparse,json,math
from pathlib import Path
from collections import defaultdict,Counter
from independent_physical_calibration_stage3 import calibrate
from independent_physical_network_epoch_shadow_stage11 import simulate
from independent_network_probe_stage6 import simulate as original_sim
from independent_stochastic_physics import affected_nodes

SEED=83
SCENARIO="S3_HIDDEN_NETWORK_50LOSS"
POLICIES=("CASPER_FULL","NEW_NETWORK_RESIDUAL_PROBE")
N=12000

def run():
    cal=calibrate(SEED,80000,include_reference=True)
    affected=affected_nodes(4202202600+SEED,SCENARIO)
    result=[]
    for policy in POLICIES:
        trace=[]
        row=simulate(SEED,SCENARIO,policy,cal,N,trace_hook=trace.append)
        prior=original_sim(SEED,SCENARIO,policy,cal,N)
        shadow=dict(row.pop("shadow_network_epoch"))
        assert row==prior,(policy,"policy output changed")
        assert len(trace)==N
        assert all(e["delivered_ms"]>=e["cpu_finish_ms"] for e in trace)
        assert all(a["delivered_ms"]<=b["delivered_ms"] for a,b in zip(trace,trace[1:]))
        assert sum(e["kind"]=="observed_incompatible_change_alarm" for e in trace)==shadow["alarm_count"]
        assert sum(e["kind"]=="late_measurement_quarantined" for e in trace)==sum(shadow["quarantined_reports_by_node"])
        grouped=defaultdict(list)
        for e in trace:
            grouped[e["node"]].append(e)
        episodes=[]
        for j in sorted(affected):
            es=grouped[j]
            accepted=[];pairs=0
            for e in es:
                # Source truth segmentation is OFFLINE and never returned to observer.
                e["postshock_task_offline"]=(e["task_index"]>=10000)
                e["affected_node_offline"]=True
                # An actionable comparable pre/post pair must be in accepted history
                # at arrival of a postshock report, not simply present eventually.
                before=[p for p in accepted if p["task_index"]<10000]
                e["prior_pre_accepted_at_delivery"]=len(before)
                if e["postshock_task_offline"] and before and e["kind"]!="late_measurement_quarantined":
                    pairs+=1
                if e["kind"]=="observed_incompatible_change_alarm":
                    accepted=[]
                if e["kind"]!="late_measurement_quarantined":
                    accepted.append(e)
            pre=[e for e in es if not e["postshock_task_offline"]]
            post=[e for e in es if e["postshock_task_offline"]]
            episodes.append(dict(node=j,pre_delivered=len(pre),post_delivered=len(post),
                pre_accepted=sum(e["kind"]!="late_measurement_quarantined" for e in pre),
                post_accepted=sum(e["kind"]!="late_measurement_quarantined" for e in post),
                post_quarantined=sum(e["kind"]=="late_measurement_quarantined" for e in post),
                post_with_prior_accepted_pre=sum(e["prior_pre_accepted_at_delivery"]>0 for e in post),
                comparable_accepted_post_pairs=pairs,
                alarms=sum(e["kind"]=="observed_incompatible_change_alarm" for e in es),
                first_post_e2e_ms=min((e["delivered_ms"] for e in post),default=None),
                first_alarm_ms=min((e["delivered_ms"] for e in es if e["kind"]=="observed_incompatible_change_alarm"),default=None),
                records=es))
        assert len(episodes)==6
        assert sum(x["post_delivered"]>0 for x in episodes)==shadow["affected_nodes_observed_postshock"]
        assert sum(x["alarms"]>0 for x in episodes)==shadow["affected_nodes_alarmed"]
        print("STAGE12_POLICY_PARITY_PASS",policy)
        print("STAGE12_NODE_SUMMARY",policy,[(x["node"],x["pre_delivered"],x["post_delivered"],x["comparable_accepted_post_pairs"],x["alarms"]) for x in episodes])
        result.append(dict(policy=policy,shadow_stage11=shadow,affected_node_episodes=episodes))
    return dict(status="PASS",scientific_scope="exploratory observed seed83 not holdout",seed_index=SEED,scenario=SCENARIO,arms=result)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",required=True)
    args=parser.parse_args()
    out=run()
    p=Path(args.out);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(out,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("JPDC_STAGE12_EXPLORATORY_PER_NODE_EPISODE_TRACE_PASS")
