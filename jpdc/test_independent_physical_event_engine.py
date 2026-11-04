#!/usr/bin/env python3
"""Independent physical event engine correctness and negative fixtures."""
import json
from independent_physical_event_engine import simulate,run
from independent_workload_generator import nodes

node_specs=nodes(4202202650)
for j in (19,20):
    row=list(node_specs[j])
    row[3]=100000.0
    node_specs[j]=tuple(row)

def task(i,when,work=100):
    return ('S0_STATIONARY',i,'MISSION',300.0,work,.01,.01,when)

output=simulate([task(0,1000),task(1,1000.01,30),
                 task(2,1000.02,30)],node_specs,'CLOUD_ONLY',True)
rows=output['trace']
assert [r['node'] for r in rows]==[18,18,18]
assert rows[0]['start_ms']==1000
assert abs(rows[1]['start_ms']-rows[0]['finish_ms'])<1e-9
assert abs(rows[2]['start_ms']-rows[1]['finish_ms'])<1e-9
print('PASS older waiting job promoted before new admissions')

duration=task(0,1000)[4]/node_specs[18][1]*12.0
tie=simulate([task(0,1000),task(1,1000+duration,10)],
             node_specs,'CLOUD_ONLY',True)['trace']
assert abs(tie[1]['wait_ms'])<1e-9
print('PASS completion precedes arrival at equal clock')

for policy,allowed in [('CLOUD_ONLY',range(18,21)),
                       ('EDGE_FIRST',range(12)),('PRED_GREEDY',range(21))]:
    result=run(50,'S0_STATIONARY',policy,250,True)
    assert len(result['trace'])==250
    assert sum(result['by_criticality'].values())==250
    assert sum(result['node_dispatch_counts'])==250
    assert all(x['node'] in allowed for x in result['trace'])
print('PASS baseline routing and complete event conservation')

for bad in ([task(0,1000),task(1,999)],
            [task(0,1000,-1)],[task(0,float('nan'))]):
    try:simulate(bad,node_specs,'CLOUD_ONLY')
    except ValueError:pass
    else:raise AssertionError('accepted malformed source workload')
print('PASS corrupt workload rejected')

a=run(50,'S1_LAMBDA_X2','PRED_GREEDY',1000)
b=run(50,'S1_LAMBDA_X2','PRED_GREEDY',1000)
assert json.dumps(a,sort_keys=True)==json.dumps(b,sort_keys=True)
print('JPDC_INDEPENDENT_EVENT_ENGINE_CONTRACT_PASS')
