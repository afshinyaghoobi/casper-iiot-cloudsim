#!/usr/bin/env python3
"""Descriptive multi-seed paired CASPER_FULL vs HEALTH_STATIC audit.

This comparison alone does not prove a causal eta effect. To establish the
intervention, separately run and pass verify_eta_clamp_pilot.py.
"""
import argparse,csv,math,statistics
from collections import defaultdict

SCENARIOS=('S0_STATIONARY','S1_LAMBDA_X2','S2_HIDDEN_COMPUTE_40LOSS','S3_HIDDEN_NETWORK_50LOSS','S4_COMPOUND')
POLICIES=('CASPER_FULL','CASPER_HEALTH_STATIC')
METRICS=('late_dvr','p99_late_latency_ms')

def analyze(paths):
    rows=defaultdict(dict)
    for path in paths:
        with open(path,newline='') as f:
            reader=csv.DictReader(f)
            required={'seed','scenario','policy','tasks','cloudsim_completion',*METRICS}
            if not reader.fieldnames or not required.issubset(reader.fieldnames):
                raise ValueError('missing CSV columns')
            for row in reader:
                if row['scenario'] not in SCENARIOS or row['policy'] not in POLICIES:
                    continue
                seed=int(row['seed'])
                key=(row['scenario'],row['policy'])
                if key in rows[seed]:
                    raise ValueError(f'duplicate {seed} {key}')
                if int(row['tasks'])!=30000 or float(row['cloudsim_completion'])!=1.0:
                    raise ValueError('incomplete run')
                values={m:float(row[m]) for m in METRICS}
                for m,v in values.items():
                    if not math.isfinite(v) or v<0 or (m=='late_dvr' and v>1):
                        raise ValueError(f'invalid {m}')
                rows[seed][key]=values
    expected={(s,p) for s in SCENARIOS for p in POLICIES}
    if len(rows)<2:
        raise ValueError('at least two paired seeds required')
    for seed,panel in rows.items():
        if set(panel)!=expected:
            raise ValueError(f'incomplete matched panel seed {seed}')
    out=[]
    for scenario in SCENARIOS:
        for metric in METRICS:
            delta=[rows[k][(scenario,'CASPER_FULL')][metric]
                   -rows[k][(scenario,'CASPER_HEALTH_STATIC')][metric] for k in sorted(rows)]
            out.append({'scenario':scenario,'metric':metric,'n':len(delta),
                'mean_delta_full_minus_static':statistics.mean(delta),
                'sd_delta':statistics.stdev(delta),
                'wins_full':sum(x<0 for x in delta),
                'ties':sum(x==0 for x in delta)})
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('csv',nargs='+')
    args=p.parse_args()
    for row in analyze(args.csv):
        print(row)
