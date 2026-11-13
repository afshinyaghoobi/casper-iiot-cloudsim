#!/usr/bin/env python3
"""Stage52 all-or-nothing eight independent source seed paired outcome auditor."""
import argparse,json,math
from pathlib import Path

SEEDS=tuple(range(1101,1109))
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL","QUEUE_PRESSURE_05","QUEUE_PRESSURE_E2E_05")
N=12000

def exact_sign(deltas):
    nonzero=[d for d in deltas if d!=0]
    k=len(nonzero)
    pos=sum(d>0 for d in nonzero)
    neg=k-pos
    if not k:return dict(non_tied=0,better=0,worse=0,ties=len(deltas),p_two_sided=1.0)
    smaller=min(pos,neg)
    p=min(1.0,2*sum(math.comb(k,j) for j in range(smaller+1))/(2**k))
    return dict(non_tied=k,better=neg,worse=pos,ties=len(deltas)-k,p_two_sided=p)

def audit(sources):
    assert set(sources)==set(SEEDS),("missing/duplicate independent sources",list(sources))
    data={}
    for seed in SEEDS:
        obj=sources[seed]
        assert obj["status"]=="PASS" and obj["seed_index"]==seed
        assert obj["source_task_observations"]==N*len(SCENARIOS)*len(POLICIES)
        assert obj["methods_not_authors_original_DFAQ_LB"] is True
        assert len(obj["rows"])==8
        for row in obj["rows"]:
            assert row["seed"]==seed and row["scenario"] in SCENARIOS and row["policy"] in POLICIES
            key=(seed,row["scenario"],row["policy"])
            assert key not in data
            assert 0<=row["post_mission_deadline_misses"]<=row["post_mission_n"]
            if row["policy"] in POLICIES[2:]:
                d=row["baseline"]
                assert d and d["label"]==row["policy"] and d["decisions"]==N
                assert d["authors_original_DFAQ_LB_implementation"] is False
            else:assert row["baseline"] is None
            data[key]=row
    assert len(data)==len(SEEDS)*len(SCENARIOS)*len(POLICIES)
    summaries=[]
    for sc in SCENARIOS:
        for seed in SEEDS:
            assert len({data[(seed,sc,p)]["post_mission_n"] for p in POLICIES})==1
        for method in POLICIES:
            rows=[data[(seed,sc,method)] for seed in SEEDS]
            ds_full=[data[(seed,sc,method)]["post_mission_deadline_misses"]-
                     data[(seed,sc,"CASPER_FULL")]["post_mission_deadline_misses"] for seed in SEEDS]
            ds_greedy=[data[(seed,sc,method)]["post_mission_deadline_misses"]-
                     data[(seed,sc,"PRED_GREEDY")]["post_mission_deadline_misses"] for seed in SEEDS]
            summaries.append(dict(scenario=sc,policy=method,
                misses=sum(x["post_mission_deadline_misses"] for x in rows),
                post_mission_n=sum(x["post_mission_n"] for x in rows),
                paired_delta_vs_full=ds_full,paired_delta_vs_greedy=ds_greedy,
                mean_paired_delta_vs_full=sum(ds_full)/len(ds_full),
                exact_sign_vs_full=exact_sign(ds_full),
                per_source=[dict(seed=seed,post_n=rows[i]["post_mission_n"],
                    post_misses=rows[i]["post_mission_deadline_misses"],
                    switches_vs_greedy=(rows[i]["baseline"] or {}).get("switches_vs_pred_greedy"),
                    mean_latency_ms=rows[i]["mean_latency_ms"],
                    mean_wait_ms=rows[i]["mean_wait_ms"]) for i,seed in enumerate(SEEDS)]))
    def get(sc,p):return next(x for x in summaries if x["scenario"]==sc and x["policy"]==p)
    gates={}
    for method in POLICIES[2:]:
        gates[method]=dict(
            s2_mean_miss_delta_no_harm=get(SCENARIOS[0],method)["mean_paired_delta_vs_full"]<=0,
            s3_strict_mean_benefit=get(SCENARIOS[1],method)["mean_paired_delta_vs_full"]<0,
            s3_two_sided_sign_p_below_005=get(SCENARIOS[1],method)["exact_sign_vs_full"]["p_two_sided"]<0.05)
    return dict(status="PASS", scientific_independent_source_seed_n=len(SEEDS),
        source_seeds=list(SEEDS), dependent_task_policy_observations=len(SEEDS)*len(SCENARIOS)*len(POLICIES)*N,
        original_java_python_queue_fidelity="previously FAILED and not addressed",
        no_author_DFAQ_LB_reproduction=True,gates=gates,source_summaries=summaries)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source-dir",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    d=Path(a.source_dir)
    src={}
    for seed in SEEDS:
        path=d/f"jpdc-stage52-holdout-seed-{seed}"/"source.json"
        assert path.is_file(),path
        src[seed]=json.loads(path.read_text())
        other=path.with_name("repeat.json")
        assert other.read_bytes()==path.read_bytes()
        log=path.with_name("source.log")
        assert log.read_bytes()==path.with_name("repeat.log").read_bytes()
    obj=audit(src)
    out=Path(a.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+"\n")
    for row in obj["source_summaries"]:
        print("JPDC_STAGE52_EIGHT_SOURCE_COHORT",json.dumps(row,sort_keys=True),flush=True)
    print("JPDC_STAGE52_ALL_EIGHT_SOURCE_COHORT_AUDIT_PASS",flush=True)
