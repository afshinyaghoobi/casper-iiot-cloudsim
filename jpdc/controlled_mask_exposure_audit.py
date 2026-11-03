#!/usr/bin/env python3
"""Pre-intervention node-count mask selection and strict per-run S3 exposure audit."""
import argparse,csv,json,math
from collections import Counter
from pathlib import Path
NODES=21
def parse_exposure(path,seed_index):
    out=[]
    with open(path,newline="") as f:
        for row in csv.reader(f):
            if len(row)!=11 or row[0]!='JPDC_NETWORK_EXPOSURE' or row[1]!=str(4202202600+seed_index) or row[2]!='S3_HIDDEN_NETWORK_50LOSS' or row[3]!='CASPER_FULL':
                raise ValueError("invalid exposure contract")
            task,node=int(row[4]),int(row[5])
            if not 0<=task<30000 or not 0<=node<NODES:raise ValueError("invalid task/node")
            if row[6] not in ('true','false'):raise ValueError("bad mask flag")
            nums=tuple(map(float,row[7:11]))
            if any(not math.isfinite(x) for x in nums):raise ValueError("nonfinite")
            nominal,actual,mult,pred=nums
            if nominal<0 or abs(actual-nominal*mult)>1e-5:raise ValueError("bad network latency")
            if abs(mult-(2.0 if task>=10000 and row[6]=='true' else 1.0))>1e-9:raise ValueError("multiplier violation")
            out.append((task,node,row[6]=='true',nominal,actual))
    if len({t for t,*_ in out})!=len(out) or len(out)<1000:raise ValueError("missing/duplicate mission trace")
    return out
def mask(path,seed_index):
    values={}
    with open(path,newline="") as f:
        for r in csv.reader(f):
            if len(r)!=6 or r[:4]!=['JPDC_SHOCK_MASK',str(4202202600+seed_index),'S3_HIDDEN_NETWORK_50LOSS','CASPER_FULL']:
                raise ValueError("invalid mask contract")
            node=int(r[4])
            if node in values or not 0<=node<NODES or r[5] not in ('true','false'):raise ValueError("bad node")
            values[node]=r[5]=='true'
    if set(values)!=set(range(NODES)) or sum(values.values())!=6:raise ValueError("invalid six node mask")
    return {j for j,v in values.items() if v}
def choose(a):
    trace=parse_exposure(a.baseline_exposure,a.seed_index)
    counts=Counter(node for task,node,*_ in trace if task<10000)
    ranking=sorted(range(NODES),key=lambda j:(counts[j],j))
    low=sorted(ranking[:6]);high=sorted(ranking[-6:])
    if set(low)&set(high):raise ValueError("non-disjoint masks")
    Path(a.out_dir).mkdir(parents=True,exist_ok=True)
    p=Path(a.out_dir)
    (p/'low_nodes.txt').write_text(','.join(map(str,low))+'\n')
    (p/'high_nodes.txt').write_text(','.join(map(str,high))+'\n')
    (p/'pre_node_counts.json').write_text(json.dumps({'seed_index':a.seed_index,'node_counts':{str(j):counts[j] for j in range(NODES)},'pre_n':sum(counts.values()),'low_mask':low,'high_mask':high},indent=2)+'\n')
    print('MASK_SELECTION_PASS',a.seed_index,low,high, 'overlap pre',sum(counts[j] for j in low),sum(counts[j] for j in high))
def verify(a):
    original=json.loads(Path(a.selected).read_text())
    baseline_pre=original['node_counts']
    rows=[]
    for condition in ('baseline','low','high'):
        p=Path(a.out_dir)/condition
        trace=parse_exposure(p/'mission_network.csv',a.seed_index)
        selected=mask(p/'mask.csv',a.seed_index)
        if condition in ('low','high') and selected!=set(original[condition+'_mask']):
            raise ValueError('selected mask differs from logged mask')
        counts=Counter(node for task,node,*_ in trace if task<10000)
        if any(counts[j]!=baseline_pre[str(j)] for j in range(NODES)):
            raise ValueError('pre shock assignment differs from baseline')
        if any(affected!=(node in selected) for task,node,affected,*_ in trace):
            raise ValueError('mask flag mismatch')
        post=[v for v in trace if v[0]>=10000]
        late=sorted(post,key=lambda x:x[0])[-250:]
        if len(late)!=250:raise ValueError('late mission not 250')
        with (p/'results.csv').open(newline='') as f:official=list(csv.DictReader(f))
        if len(official)!=8 or len({r['policy'] for r in official})!=8:
            raise ValueError('official result rows invalid')
        full=next(x for x in official if x['policy']=='CASPER_FULL')
        row={'seed_index':a.seed_index,'condition':condition,
             'mask':','.join(map(str,sorted(selected))),
             'pre_mission_n':sum(counts.values()),
             'pre_overlap':sum(counts[j] for j in selected)/sum(counts.values()),
             'post_mission_n':len(post),
             'post_exposure':sum(x[2] for x in post)/len(post),
             'post_added_network_ms':sum(x[4]-x[3] for x in post)/len(post),
             'late_exposure':sum(x[2] for x in late)/250}
        for metric in ('late_eta','late_far','late_air','late_dvr','late_fwc','post_far','post_air','post_dvr','post_fwc'):
            row[metric]=float(full[metric])
        rows.append(row)
    arows={r['condition']:r for r in rows}
    if not arows['high']['pre_overlap']>arows['low']['pre_overlap']:
        raise ValueError("HIGH pre overlap not greater than LOW; report failure")
    # Post exposure is a manipulation outcome to be reported, NOT a failure
    # criterion, since post-shock routing can change under intervention.
    Path(a.output).write_text(json.dumps({'seed_index':a.seed_index,'conditions':rows,'post_exposure_manipulation_achieved':arows['high']['post_exposure']>arows['low']['post_exposure']},indent=2)+'\n')
    print('CONTROLLED_MASK_AUDIT_PASS',a.seed_index,'post_exposure_high_gt_low',arows['high']['post_exposure']>arows['low']['post_exposure'])
if __name__=='__main__':
    p=argparse.ArgumentParser()
    sub=p.add_subparsers(dest='cmd',required=True)
    c=sub.add_parser('choose');c.add_argument('--baseline-exposure',required=True);c.add_argument('--seed-index',type=int,required=True);c.add_argument('--out-dir',required=True)
    v=sub.add_parser('verify');v.add_argument('--selected',required=True);v.add_argument('--seed-index',type=int,required=True);v.add_argument('--out-dir',required=True);v.add_argument('--output',required=True)
    a=p.parse_args()
    (choose if a.cmd=='choose' else verify)(a)
