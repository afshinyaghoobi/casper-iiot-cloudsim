#!/usr/bin/env python3
"""Reconcile original S3 mask trace network outcomes and prediction semantics.

The final (11th) column is E45 pred[j], a prediction, NOT realized latency.
Run: python3 jpdc/trace_network_prediction_semantics.py DIRECTORY
DIRECTORY contains GitHub physical Actions artifact ZIPs with their original names.
No CloudSim run; no inference from tasks as independent seeds.
"""
import csv,io,json,pathlib,sys,zipfile
IDS={40:13272215535,41:13271273184,42:13270784276,43:13272485400}
def rows(z,arm):
    d={}
    for r in csv.reader(io.StringIO(z.read(arm+'/mission_network.csv').decode())):
        i=int(r[4])
        assert i not in d
        d[i]=r
    return d
def run(folder):
    out=[]
    for seed,aid in IDS.items():
        with zipfile.ZipFile(folder/f'github-actions-artifact-{aid}.zip') as z:
            base=rows(z,'baseline')
            for arm in ('low','high'):
                alt=rows(z,arm)
                assert base.keys()==alt.keys()
                for name,ids in (('pre',[i for i in base if i<10000]),
                                 ('post',[i for i in base if i>=10000])):
                    same=[i for i in ids if base[i][5]==alt[i][5]]
                    same_nominal=[i for i in same if base[i][7]==alt[i][7]]
                    same_pred=[i for i in same if base[i][10]==alt[i][10]]
                    changed_net=[i for i in same if abs(float(base[i][8])-float(alt[i][8]))>1e-6]
                    assert all(abs(float(alt[i][8])-float(alt[i][7])*float(alt[i][9]))<2e-8 for i in ids)
                    if name=='pre':
                        assert len(same)==len(ids)==len(same_nominal)==len(same_pred) and not changed_net
                    out.append({'seed':seed,'mask':arm,'period':name,'tasks':len(ids),
                        'same_node':len(same),'same_nominal_network':len(same_nominal),
                        'same_pred_j':len(same_pred),'changed_actual_network_same_node':len(changed_net),
                        'mean_actual_net_difference_ms':sum(float(alt[i][8])-float(base[i][8]) for i in ids)/len(ids)})
    for arm in ('low','high'):
        p=[r for r in out if r['mask']==arm and r['period']=='post']
        print(arm,'post_n',sum(x['tasks'] for x in p),'same_node',sum(x['same_node'] for x in p),
              'same_pred_j',sum(x['same_pred_j'] for x in p),
              'actual_network_changed_same_node',sum(x['changed_actual_network_same_node'] for x in p))
    print(json.dumps(out,indent=2))
if __name__=='__main__':
    if len(sys.argv)!=2:sys.exit(__doc__)
    run(pathlib.Path(sys.argv[1]))
