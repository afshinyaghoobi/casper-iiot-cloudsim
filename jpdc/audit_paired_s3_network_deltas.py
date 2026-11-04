#!/usr/bin/env python3
"""Paired S3 mask network-only differences, from ORIGINAL physical Actions artifacts.

Usage: python3 jpdc/audit_paired_s3_network_deltas.py ARTIFACT_DIR
No new CloudSim run; no observed end-to-end task latency available in this trace.
Baseline has ITS OWN shock mask, so it is NOT an unshocked counterfactual.
"""
import csv,io,json,pathlib,sys,zipfile
IDS={40:13272215535,41:13271273184,42:13270784276,43:13272485400}

def load(z,arm):
    rows=list(csv.reader(io.StringIO(z.read(arm+'/mission_network.csv').decode())))
    result={}
    for x in rows:
        assert len(x)==11 and x[0]=="JPDC_NETWORK_EXPOSURE" and x[3]=="CASPER_FULL"
        task=int(x[4])
        assert task not in result
        result[task]=x
    return result

def main(folder):
    summaries=[]
    for seed,aid in IDS.items():
        with zipfile.ZipFile(folder/f'github-actions-artifact-{aid}.zip') as z:
            base=load(z,'baseline')
            for arm in ('low','high'):
                paired=load(z,arm)
                assert base.keys()==paired.keys()
                post=[]
                for task,a in base.items():
                    b=paired[task]
                    assert a[1]==b[1]==str(4202202600+seed)
                    same_node=a[5]==b[5]
                    delta=float(b[8])-float(a[8])
                    for row in (a,b):
                        assert abs(float(row[8])-float(row[7])*float(row[9]))<2e-8
                    if task<10000:
                        assert same_node and a[7:11]==b[7:11]
                    else:
                        if same_node:
                            assert a[7]==b[7]
                            physical_delta=float(b[7])*(float(b[9])-float(a[9]))
                            assert abs(delta-physical_delta)<2e-8
                        post.append((same_node,abs(delta)>1e-7,delta))
                assert post
                summaries.append(dict(seed=seed,arm=arm,n=len(post),
                    rerouted=sum(not x[0] for x in post),
                    changed_network=sum(x[1] for x in post),
                    mean_delta_ms=sum(x[2] for x in post)/len(post)))
    for arm in ('low','high'):
        r=[x for x in summaries if x['arm']==arm]
        n=sum(x['n'] for x in r)
        assert n==4040
        print('TOTAL',arm,'tasks',n,'rerouted',sum(x['rerouted'] for x in r),
              'changed_network',sum(x['changed_network'] for x in r),
              'paired_network_delta_ms',sum(x['n']*x['mean_delta_ms'] for x in r)/n)
    print(json.dumps(summaries,indent=2))
    print('PASS S3 paired original network traces; baseline is also shocked; prediction is not observed latency')

if __name__=="__main__":
    if len(sys.argv)!=2:sys.exit(__doc__)
    main(pathlib.Path(sys.argv[1]))
