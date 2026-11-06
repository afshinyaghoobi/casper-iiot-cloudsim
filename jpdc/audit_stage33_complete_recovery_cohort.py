#!/usr/bin/env python3
"""Stage33 all-or-nothing four-seed post-alarm recovery evidence audit."""
import argparse,json,statistics
from pathlib import Path
SEEDS=(509,510,511,512)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
POLICIES=("PRED_GREEDY","CASPER_FULL")
p=argparse.ArgumentParser();p.add_argument("--input",required=True);p.add_argument("--out",required=True)
a=p.parse_args()
byseed={}
for file in Path(a.input).rglob("seed_*.json"):
    obj=json.loads(file.read_text())
    seed=obj["seed"]
    assert seed in SEEDS and seed not in byseed,("unexpected duplicate source seed",seed)
    assert obj["status"]=="PASS" and obj["independent_scientific_units"]==1
    assert obj["task_policy_evaluations"]==48000 and obj["all_four_original_stage6_parity"]
    rows={(r["scenario"],r["policy"]):r for r in obj["rows"]}
    assert len(rows)==4 and set(rows)=={(sc,po) for sc in SCENARIOS for po in POLICIES}
    byseed[seed]=rows
assert tuple(sorted(byseed))==SEEDS,("INCOMPLETE frozen cohort",sorted(byseed))
summaries=[]
for scenario in SCENARIOS:
    for policy in POLICIES:
        s2=scenario==SCENARIOS[0]
        rows=[byseed[s][(scenario,policy)] for s in SEEDS]
        short=[]
        for seed,r in zip(SEEDS,rows):
            q=r["post_mission"];high=r["post_high"];allpost=r["post"]
            assert r["original_stage6_exact_parity"]
            assert allpost["n"]==2000 and q["n"]>0 and high["n"]>0
            short.append(dict(seed=seed,alarm_clock_ms=r["alarm_clock_ms"],
                post_available=allpost["available_fraction"],post_mission_available=q["available_fraction"],
                post_high_available=high["available_fraction"],
                post_mission_recovered=q["recovered_issued"],
                post_mission_original=q["original_issued"],
                post_mission_rebuild_abstain=q["post_alarm_rebuild_abstained"],
                post_mission_n=q["n"],
                post_mission_issued_inclusion=q["all_issued_inclusion"],
                post_recovered_inclusion=allpost["recovered_issued_inclusion"],
                recovery_contexts=len(r["first_recovery_by_context"]),
                gates=r["frozen_operational_gates"]))
        gate_keys=("S2_post_MISSION_issued_at_least_half","S2_post_HIGH_issued_at_least_half") if s2 else ("S3_zero_CPU_alarms","S3_MISSION_issued_at_least_90pct")
        summary=dict(scenario=scenario,policy=policy,independent_scientific_seeds=list(SEEDS),
            seed_rows=short,
            mission_availability_mean=statistics.mean(x["post_mission_available"] for x in short),
            mission_availability_min=min(x["post_mission_available"] for x in short),
            mission_recovered_counts=[x["post_mission_recovered"] for x in short],
            mean_post_availability=statistics.mean(x["post_available"] for x in short),
            mean_post_recovered_inclusion_only=statistics.mean(
                [x["post_recovered_inclusion"] for x in short if x["post_recovered_inclusion"] is not None])
                if any(x["post_recovered_inclusion"] is not None for x in short) else None,
            frozen_gate_pass_counts={k:sum(bool(x["gates"][k]) for x in short) for k in gate_keys})
        summaries.append(summary)
        print("JPDC_STAGE33_FOUR_SEED_RECOVERY_RESULT",json.dumps(summary,sort_keys=True),flush=True)
out=dict(status="PASS",all_frozen_seeds_present=True,seeds=list(SEEDS),
         independent_scientific_units=4,dependent_task_policy_evaluations=192000,
         limitation="source-specific descriptive interval availability and coverage, not deadline safety or distribution-free guarantee",
         rows=summaries)
dest=Path(a.out);dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text(json.dumps(out,sort_keys=True,indent=2)+"\n")
print("JPDC_STAGE33_ALL_FOUR_SEEDS_CAUSAL_RECOVERY_AUDIT_COMPLETE_PASS")
