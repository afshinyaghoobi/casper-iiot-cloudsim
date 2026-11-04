#!/usr/bin/env python3
"""Independent 48-bit Java Random/Box-Muller workload and node generator.

Does not import Java, Java trace arrays, or precomputed random values.
"""
import math

MASK=(1<<48)-1
class JavaRandom:
    def __init__(self,seed):
        self.state=(seed^0x5DEECE66D)&MASK
        self.gaussian_cache=None
    def bits(self,bits):
        self.state=(self.state*0x5DEECE66D+0xB)&MASK
        return self.state>>(48-bits)
    def next_int(self,bound):
        if bound<=0:raise ValueError('bound must be positive')
        if bound & (bound-1)==0:return (bound*self.bits(31))>>31
        while True:
            bits=self.bits(31)
            val=bits%bound
            # Java signed 32-bit rejection predicate
            if bits-val+(bound-1)<(1<<31):return val
    def next_double(self):
        return ((self.bits(26)<<27)+self.bits(27))/float(1<<53)
    def next_gaussian(self):
        if self.gaussian_cache is not None:
            result=self.gaussian_cache
            self.gaussian_cache=None
            return result
        while True:
            v1=2*self.next_double()-1
            v2=2*self.next_double()-1
            s=v1*v1+v2*v2
            if s<1 and s!=0:break
        mult=math.sqrt(-2*math.log(s)/s)
        self.gaussian_cache=v2*mult
        return v1*mult

def uniform(r,a,b):return a+(b-a)*r.next_double()
def lognormal(r,median,sigma):return math.exp(math.log(median)+sigma*r.next_gaussian())
def nodes(seed):
    r=JavaRandom(seed^0x51A7E123)
    out=[]
    for j in range(21):
        if j<12:
            cap=uniform(r,2.5,6);bw=uniform(r,80,250);rtt=uniform(r,2,10);sm=1.10
        elif j<18:
            cap=uniform(r,8,20);bw=uniform(r,150,600);rtt=uniform(r,8,28);sm=1.0
        else:
            cap=uniform(r,30,70);bw=uniform(r,300,1200);rtt=uniform(r,30,80);sm=.90
        vm_mips=max(1000,math.floor(cap*1000+0.5))
        out.append((j,cap,bw,rtt,sm,vm_mips))
    return out

SCENARIO_MULT={"S0_STATIONARY":1.0,"S1_LAMBDA_X2":2.0,"S2_HIDDEN_COMPUTE_40LOSS":1.0,
               "S3_HIDDEN_NETWORK_50LOSS":1.0,"S4_COMPOUND":2.0}
def tasks(seed,n,scenario,seed_salt=0xD3F10A77):
    if scenario not in SCENARIO_MULT:raise ValueError("scenario")
    r=JavaRandom(seed^seed_salt)
    now=1000.0
    for i in range(n):
        pm=SCENARIO_MULT[scenario] if i>=10000 else 1.0
        now+=(-math.log(max(1e-15,1-r.next_double()))/.12)/pm
        z=r.next_double()
        if z<.80:
            crit="NORMAL";deadline=uniform(r,500,2000)
            work=lognormal(r,25,.45);in_mb=lognormal(r,.40,.55);out_mb=lognormal(r,.08,.40)
        elif z<.95:
            crit="HIGH";deadline=uniform(r,100,500)
            work=lognormal(r,45,.50);in_mb=lognormal(r,1.0,.60);out_mb=lognormal(r,.20,.50)
        else:
            crit="MISSION";deadline=uniform(r,40,120)
            work=lognormal(r,18,.35);in_mb=lognormal(r,.05,.40);out_mb=lognormal(r,.01,.35)
        yield (scenario,i,crit,deadline,work,in_mb,out_mb,now)

def predicted_latency(task,node,backlog_ms):
    _,_,_,_,work,in_mb,out_mb,_=task
    _,cap,bw,rtt,_,_=node
    return rtt+(in_mb+out_mb)*8000/bw+backlog_ms+work/cap*12


def calibration_mission_ranks(seed,n=80000,burnin=10000):
    """Independently reconstruct E42 calibration rank-label shuffling.

    This is pre-CLOUDSIM randomized allocation, not the outcome calibration q.
    """
    if n<=burnin:raise ValueError("need post-burnin calibration tasks")
    indices=[t[1] for t in tasks(seed,n,"S0_STATIONARY",seed_salt=0xCA11B4A7)
             if t[1]>=burnin and t[2]=="MISSION"]
    ranks=[(i%3)+1 for i in range(len(indices))]
    rng=JavaRandom(seed^0xA11CE77)
    for i in range(len(ranks),1,-1):
        j=rng.next_int(i)
        ranks[i-1],ranks[j]=ranks[j],ranks[i-1]
    return dict(zip(indices,ranks))


def conformal_qhat(values,alpha):
    """Frozen E42 quantile definition; infinity means insufficient calibration."""
    if not 0<alpha<1:raise ValueError("alpha outside (0,1)")
    if not values:return math.inf
    if not all(math.isfinite(x) for x in values):raise ValueError("nonfinite calibration sample")
    sorted_values=sorted(values)
    k=math.ceil((len(values)+1)*(1-alpha))
    return sorted_values[k-1] if k<=len(values) else math.inf
