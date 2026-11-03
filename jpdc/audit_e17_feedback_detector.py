#!/usr/bin/env python3
"""Reconstruct frozen E17 feedback detector from generated-E45 completion trace.

Input has BOTH adaptive policies; fail closed on missing, duplicated, unordered, or
inconsistent observations. No source/science mutation and no inferred task independence.
"""
import argparse,csv,json,math
from collections import deque,defaultdict
from pathlib import Path

POLICIES=('CASPER_FULL','CASPER_ADAPT_NO_HEALTH')
FIELDS=('tag','seed','scenario','policy','task','score','reference_q95',
        'eta_at_dispatch','eta_before','eta_after',
        'alarm_before','alarm_after','age_before','age_after')
def audit(path,seed_index):
    groups=defaultdict(list)
    with open(path,newline='') as f:
        for row in csv.reader(f):
            if len(row)!=len(FIELDS):raise ValueError("wrong feedback width")
            d=dict(zip(FIELDS,row))
            if d['tag']!='JPDC_ETA_FEEDBACK' or d['scenario']!='S3_HIDDEN_NETWORK_50LOSS' or d['seed']!=str(4202202600+seed_index) or d['policy'] not in POLICIES:
                raise ValueError("unexpected provenance")
            for k in ('score','reference_q95','eta_at_dispatch','eta_before','eta_after'):
                d[k]=float(d[k])
                if not math.isfinite(d[k]):raise ValueError("nonfinite "+k)
            if d['score']<0 or d['reference_q95']<=0:raise ValueError("invalid score/reference")
            for k in ('alarm_before','alarm_after'):
                if d[k] not in ('true','false'):raise ValueError("invalid alarm flag")
            for k in ('task','age_before','age_after'):d[k]=int(d[k])
            groups[d['policy']].append(d)
    if set(groups)!=set(POLICIES):raise ValueError("missing adaptive policy")
    out=[]
    for policy,rr in groups.items():
        if len(rr)<1000 or len({r['task'] for r in rr})!=len(rr):raise ValueError("missing/duplicate observations")
        reference={r['reference_q95'] for r in rr}
        if len(reference)!=1:raise ValueError("reference must remain fixed")
        detector=deque(maxlen=50)
        alarm=False
        transition=-1
        first_alarm=None
        max_exceed=0
        pre=post=pre_exc=post_exc=0
        for r in rr:
            if (r['alarm_before']=='true')!=alarm or r['age_before']!=transition:
                raise ValueError(f"before state disagrees with replay for {policy} at {r['task']}")
            exceed=r['score']>r['reference_q95']
            detector.append(exceed)
            max_exceed=max(max_exceed,sum(detector))
            if not alarm and len(detector)==50 and sum(detector)>=12:
                alarm=True;transition=0;first_alarm=r['task']
            if transition>=0:transition+=1
            if (r['alarm_after']=='true')!=alarm or r['age_after']!=transition:
                raise ValueError(f"after state disagrees with replay for {policy} at {r['task']}")
            if r['task']<10000:pre+=1;pre_exc+=int(exceed)
            else:post+=1;post_exc+=int(exceed)
        out.append({'seed_index':seed_index,'policy':policy,'reference_q95':next(iter(reference)),
                    'pre_n':pre,'pre_exceed':pre_exc,'post_n':post,'post_exceed':post_exc,
                    'post_exceed_fraction':post_exc/post,'max_rolling_50_exceed':max_exceed,
                    'alarm_activated':alarm,'alarm_first_task':first_alarm,
                    'final_eta_after_feedback':rr[-1]['eta_after'],'final_transition_age':transition})
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--trace',required=True);p.add_argument('--seed-index',type=int,required=True);p.add_argument('--out',required=True)
    a=p.parse_args()
    rows=audit(a.trace,a.seed_index)
    Path(a.out).write_text(json.dumps(rows,indent=2)+'\n')
    print('JPDC_E17_DETECTOR_REPLAY_PASS',json.dumps(rows))
