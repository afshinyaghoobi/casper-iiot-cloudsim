#!/usr/bin/env python3
"""Independent frozen E42 hashed service noise and hidden-shock physical model.

No Java runtime, reference trace, or precomputed original random sequence.
"""
import math
from independent_workload_generator import JavaRandom
MASK64=(1<<64)-1
NODE_MIX=0x9E3779B97F4A7C15
SCENARIOS={
 "S0_STATIONARY":(1.0,1.0),
 "S1_LAMBDA_X2":(1.0,1.0),
 "S2_HIDDEN_COMPUTE_40LOSS":(.60,1.0),
 "S3_HIDDEN_NETWORK_50LOSS":(1.0,.50),
 "S4_COMPOUND":(.60,.50)
}
ORDER=tuple(SCENARIOS)
def mix64(value):
    z=value&MASK64
    z=((z^(z>>30))*0xBF58476D1CE4E5B9)&MASK64
    z=((z^(z>>27))*0x94D049BB133111EB)&MASK64
    return (z^(z>>31))&MASK64

def service_noise(seed,task_index,node):
    h=mix64((seed^((task_index<<21)&MASK64)^(node*NODE_MIX))&MASK64)
    u1=(h>>11)*2**-53
    h=mix64((h+0xD1B54A32D192ED03)&MASK64)
    u2=(h>>11)*2**-53
    g=math.sqrt(-2*math.log(max(u1,1e-15)))*math.cos(2*math.pi*u2)*.28
    h=mix64((h+0x94D049BB133111EB)&MASK64)
    ut=(h>>11)*2**-53
    if ut<.08:
        h=mix64((h+0xBF58476D1CE4E5B9)&MASK64)
        ue=(h>>11)*2**-53
        g+=-math.log(max(1e-15,1-ue))*.7
    return max(g,-.8)

def affected_nodes(seed,scenario):
    if scenario not in SCENARIOS:raise ValueError("unrecognized scenario")
    c,b=SCENARIOS[scenario]
    if c>=1 and b>=1:return frozenset()
    rng=JavaRandom(seed^(0xBADC0FFE+31*ORDER.index(scenario)))
    arr=list(range(21))
    for i in range(20,0,-1):
        j=rng.next_int(i+1)
        arr[i],arr[j]=arr[j],arr[i]
    return frozenset(arr[:6])

def physical_durations(seed,task,node,scenario,affected):
    if scenario not in SCENARIOS:raise ValueError("unrecognized scenario")
    idx=task[1];j=node[0]
    cm,bm=SCENARIOS[scenario]
    compute=(1/cm if idx>=10000 and j in affected and cm<1 else 1.0)
    bandwidth=(1/bm if idx>=10000 and j in affected and bm<1 else 1.0)
    nominal=task[4]/node[1]*12.0
    cpu=max(.2,nominal*compute*(1+.18*service_noise(seed,idx,j)))
    net=(node[3]+(task[5]+task[6])*8000.0/node[2])*bandwidth
    if not math.isfinite(cpu) or cpu<=0 or not math.isfinite(net) or net<0:
        raise ValueError("unphysical simulated CPU/network")
    return cpu,net
