#!/usr/bin/env python3
"""Check original S3 Actions artifact CSV/JSON and physical network traces.
Download artifacts 13272215535,13271273184,13270784276,13272485400
and 13273915636,13273755094,13271869726,13272339554 to one directory;
name each github-actions-artifact-<ID>.zip.
Usage: python3 jpdc/audit_s3_original_actions_artifacts.py DIRECTORY
Python standard library only; this audits saved data, not a new simulation.
"""
import csv,io,json,math,pathlib,sys,zipfile
IDS={40:(13272215535,13273915636),41:(13271273184,13273755094),
     42:(13270784276,13271869726),43:(13272485400,13272339554)}
KEYS=('late_far','late_air','late_dvr','late_fwc','late_eta','post_far',
      'post_air','post_dvr','post_fwc')
def check(c,msg):
    if not c: raise AssertionError(msg)
def near(a,b,eps=5e-8):
    return math.isclose(float(a),float(b),abs_tol=eps,rel_tol=0)
def records(z,n): return list(csv.DictReader(io.StringIO(z.read(n).decode())))
def raw(z,n): return list(csv.reader(io.StringIO(z.read(n).decode())))
def result(z,n):
    r=records(z,n)
    check(len(r)==8 and len(set(x['policy'] for x in r))==8,n+' policy count')
    return {x['policy']:x for x in r}
def run(folder):
    totals={(mask,mode,k):0 for mask in ('low','high')
            for mode in ('adaptive','clamped') for k in ('far','air','dvr','fwc')}
    for seed,(mid,fid) in IDS.items():
        with zipfile.ZipFile(folder/f'github-actions-artifact-{mid}.zip') as a, zipfile.ZipFile(folder/f'github-actions-artifact-{fid}.zip') as b:
            physical=json.loads(a.read('paired_results.json'))
            factorial=json.loads(b.read('paired_summary.json'))
            pre=json.loads(a.read('pre_node_counts.json'))
            check(physical['seed_index']==factorial['seed_index']==pre['seed_index']==seed,'seed')
            check(physical['post_exposure_manipulation_achieved'],'exposure')
            counts={int(k):v for k,v in pre['node_counts'].items()}
            low=set(pre['low_mask']); high=set(pre['high_mask'])
            check(len(low)==len(high)==6 and low.isdisjoint(high),'disjoint masks')
            check(low==set(sorted(counts,key=lambda i:(counts[i],i))[:6]),'low selection')
            check(high==set(sorted((i for i in counts if i not in low),
                                   key=lambda i:(-counts[i],-i))[:6]),'high selection')
            check(sum(counts.values())==pre['pre_n'],'pre task count')
            p={x['condition']:x for x in physical['conditions']}
            for mask in ('baseline','low','high'):
                mr=raw(a,mask+'/mask.csv')
                check(len(mr)==21 and sorted(int(r[4]) for r in mr)==list(range(21)),'21 nodes')
                affected={int(r[4]) for r in mr if r[5]=='true'}
                check(len(affected)==6,'six affected')
                if mask!='baseline':check(affected=={'low':low,'high':high}[mask],'fixed masks')
                tr=raw(a,mask+'/mission_network.csv')
                early=[r for r in tr if int(r[4])<10000]
                late=[r for r in tr if int(r[4])>=10000]
                check(len(tr)==len(set(int(r[4]) for r in tr)),'unique trace tasks')
                check(all(int(r[1])==4202202600+seed and r[3]=='CASPER_FULL'
                          for r in tr),'trace identity')
                check(all((r[6]=='true')==(int(r[5]) in affected) for r in tr),'mask flags')
                check(all(near(r[9],2 if int(r[4])>=10000 and int(r[5]) in affected else 1)
                          for r in tr),'multiplier')
                check(all(near(r[8],float(r[7])*float(r[9]) ,2e-8) for r in tr),'network delay physics')
                check(len(early)==p[mask]['pre_mission_n'] and len(late)==p[mask]['post_mission_n'],'trace counts')
                check({i:sum(int(r[5])==i for r in early) for i in range(21)}==counts,'pre-shock routing parity')
                measured={'pre_overlap':sum(int(r[5]) in affected for r in early)/len(early),
                          'post_exposure':sum(int(r[5]) in affected for r in late)/len(late),
                          'post_added_network_ms':sum(float(r[8])-float(r[7]) for r in late)/len(late)}
                for k,v in measured.items():check(near(v,p[mask][k]),'trace-to-JSON '+k)
                original=result(a,mask+'/results.csv')
                for k in KEYS:check(near(original['CASPER_FULL'][k],p[mask][k]),'source CSV '+k)
                if mask=='baseline':continue
                adaptive=result(b,mask+'_adaptive.csv')
                fixed=result(b,mask+'_clamped.csv')
                for k in KEYS:
                    check(near(adaptive['CASPER_FULL'][k],original['CASPER_FULL'][k]),'cross-run '+k)
                    check(near(adaptive['CASPER_FULL'][k],factorial[mask]['adaptive'][k]),'adaptive '+k)
                    check(near(fixed['CASPER_FULL'][k],factorial[mask]['clamped'][k]),'clamped '+k)
                for policy in adaptive:
                    if policy=='CASPER_FULL':continue
                    for k in adaptive[policy]:
                        if k=='mean_mapper_us':continue
                        check(adaptive[policy][k]==fixed[policy][k], 'other-policy parity '+policy+':'+k)
                for mode,rows in (('adaptive',adaptive),('clamped',fixed)):
                    for k in ('far','air','dvr','fwc'):
                        count=float(rows['CASPER_FULL']['late_'+k])*250
                        check(near(count,round(count)),'integer late count')
                        totals[mask,mode,k]+=round(count)
            for k in ('far','air','dvr','fwc'):
                delta=(float(factorial['high']['adaptive']['late_'+k])-float(factorial['high']['clamped']['late_'+k])
                       -float(factorial['low']['adaptive']['late_'+k])+float(factorial['low']['clamped']['late_'+k]))
                check(near(delta,factorial['interaction']['late_'+k]),'factorial interaction')
        print('PASS seed',seed)
    expected={'low':{'adaptive':(0,14,1,992),'clamped':(0,11,1,990)},
              'high':{'adaptive':(3,125,45,835),'clamped':(33,11,44,3)}}
    for mask in expected:
        for mode in expected[mask]:
            check(tuple(totals[mask,mode,k] for k in ('far','air','dvr','fwc'))==expected[mask][mode],
                  'pooled counts '+mask+'/'+mode)
    print('PASS original eight Actions artifact sets and reported factorial counts')
if __name__=='__main__':
    if len(sys.argv)!=2:sys.exit(__doc__)
    run(pathlib.Path(sys.argv[1]))
