#!/usr/bin/env python3
"""Stage-2 clean-room stochastic FCFS matrix: prespecified, baseline-only."""
import argparse,json
from pathlib import Path
from independent_physical_event_engine import run,POLICIES

SEEDS=(50,51)
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS","S4_COMPOUND")
N=12000

def main(out):
    rows=[]
    exposed=0
    for seed in SEEDS:
        for scenario in SCENARIOS:
            for policy in POLICIES:
                r=run(seed,scenario,policy,N,stochastic=True)
                assert r['status']=='PASS' and r['tasks']==N
                assert sum(r['by_criticality'].values())==N
                assert sum(r['node_dispatch_counts'])==N
                assert len(r['affected_nodes'])==6
                exposed+=r['postshock_affected_dispatches']
                rows.append(r)
                print("STOCH_ENGINE_RESULT",seed,scenario,policy,
                      "latency_ms",round(r['mean_latency_ms'],6),
                      "wait_ms",round(r['mean_wait_ms'],6),
                      "mission_misses",r['deadline_misses']['MISSION'],
                      "damaged_dispatches",r['postshock_affected_dispatches'])
    if len(rows)!=18 or sum(r['tasks'] for r in rows)!=216000:
        raise AssertionError('incomplete Stage2 matrix')
    payload={'status':'PASS','stage':'independent stochastic physical engine, three baselines only',
             'scientific_limit':'strict FCFS; NOT CloudSim equivalent or full CASPER validation',
             'seeds':list(SEEDS),'scenarios':list(SCENARIOS),
             'total_task_policy_evaluations':216000,
             'postshock_affected_dispatches':exposed,'rows':rows}
    p=Path(out);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(payload,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print("JPDC_INDEPENDENT_STOCHASTIC_ENGINE_STAGE2_PASS")
    if exposed==0:print("JPDC_STAGE2_SHOCK_EXPOSURE_ZERO_LIMITATION")
    else:print("JPDC_STAGE2_SHOCK_EXPOSURE_OBSERVED")

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True)
    main(p.parse_args().out)
