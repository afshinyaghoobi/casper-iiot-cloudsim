#!/usr/bin/env python3
"""Stochastic engine fixtures: physically distinct completion and no silent shock."""
from independent_physical_event_engine import simulate,run
from independent_workload_generator import nodes
from independent_stochastic_physics import affected_nodes,physical_durations,service_noise

seed=4202202650
n=nodes(seed)
def make_task(i,t):
    return ('S2_HIDDEN_COMPUTE_40LOSS',i,'MISSION',1000.0,12.0,.1,.02,t)

base=simulate([make_task(0,1000.0)],n,'CLOUD_ONLY',True)
shock=simulate([make_task(0,1000.0)],n,'CLOUD_ONLY',True,
               stochastic_seed=seed,scenario='S2_HIDDEN_COMPUTE_40LOSS')
assert shock['status']=='PASS'
assert shock['trace'][0]['cpu_ms']!=base['trace'][0]['cpu_ms']
chosen=shock['trace'][0]['node']
cpu,net=physical_durations(seed,make_task(0,1000.0),n[chosen],
                           'S2_HIDDEN_COMPUTE_40LOSS',affected_nodes(seed,'S2_HIDDEN_COMPUTE_40LOSS'))
assert abs(shock['trace'][0]['cpu_ms']-cpu)<1e-9
assert abs(shock['trace'][0]['network_ms']-net)<1e-9
print('PASS stochastic service noise physically controls independent finish')

# Run a complete postshock fixed-shock physical system: all original task IDs
# and arrivals originate from the independent generator, no recorded Java trace.
for sc in ('S2_HIDDEN_COMPUTE_40LOSS','S3_HIDDEN_NETWORK_50LOSS','S4_COMPOUND'):
    x=run(50,sc,'PRED_GREEDY',10010,True,stochastic=True)
    assert x['tasks']==10010 and len(x['trace'])==10010
    assert len(x['affected_nodes'])==6
    assert all(r['cpu_ms']>0 and r['network_ms']>0 and r['wait_ms']>=0 for r in x['trace'])
print('PASS all 3 native original scenario shocks on >10000-task independent physical queues')

try:simulate([make_task(0,1000.0)],n,'CLOUD_ONLY',stochastic_seed=seed)
except ValueError:print('PASS reject ambiguous mixed nominal/stochastic configuration')
else:raise AssertionError('accepted physics with scenario absent')
print('JPDC_INDEPENDENT_STOCHASTIC_ENGINE_CONTRACT_PASS')
