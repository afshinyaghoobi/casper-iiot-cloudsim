#!/usr/bin/env python3
"""Strict eight-policy source-semantic fixtures without Java native data."""
from independent_casper_deployment_stage4 import route,POLICIES,POLICY_FLAGS
assert len(POLICIES)==8
task=("S2_HIDDEN_COMPUTE_40LOSS",11000,"MISSION",20.0,18.,.01,.01,1000.)
p=[1000.]*21;p[0]=10.;p[1]=11.;p[2]=12.;p[18]=4.;p[19]=5.;p[20]=6.
sigma=[1.]*21;alarms=[True]*21
for name,low,high in (("CLOUD_ONLY",18,21),("EDGE_FIRST",0,12),("PRED_GREEDY",0,21)):
    j,r,cert,family=route(task,p,alarms,sigma,[100.,1.,.2],3.,1.,name)
    assert low<=j<high and r==1 and not cert and not family
print("PASS original cloud/edge/greedy base eligibility and no CP")
# GLOBAL_CP must ignore ranked q; global q makes any candidate infeasible
alarm=[False]*21
j,r,cert,fam=route(task,p,alarm,sigma,[100.,.1,.1],100.,1.,"GLOBAL_CP")
assert j==18 and r==1 and not cert and fam[:3]==(18,19,20)
j,r,cert,fam=route(task,p,alarm,sigma,[100.,.1,.1],100.,1.,"RANKED_CP_STATIC")
assert j==19 and r==2 and cert
print("PASS global q vs rank-specific q first-feasible distinction")
for policy in ("CASPER_ADAPT_NO_HEALTH","CASPER_HEALTH_STATIC","CASPER_FULL"):
    assert POLICY_FLAGS[policy]["cp"]
    j,r,cert,fam=route(task,p,alarm,sigma,[100.,100.,.1],100.,1.,policy)
    assert j==20 and r==3 and cert
print("PASS original ranked rank3 path for all three CASPER variants")
for policy in ("CASPER_FULL","CASPER_HEALTH_STATIC"):
    j,r,cert,fam=route(task,p,alarms,sigma,[.1,.1,.1],.1,1.,policy)
    assert (j,r,cert,fam)==(18,1,False,())
for policy in ("GLOBAL_CP","CASPER_ADAPT_NO_HEALTH"):
    j,r,cert,fam=route(task,p,alarms,sigma,[.1,.1,.1],.1,1.,policy)
    assert cert and fam
print("PASS all-health-alarmed fallback solely for health policies")
for policy in POLICIES:
    try:route(task,p[:-1],alarm,sigma,[1.,1.,1.],1.,1.,policy)
    except ValueError:pass
    else:raise AssertionError("malformed state accepted "+policy)
print("JPDC_NATIVE_EIGHT_POLICY_DECISION_UNIT_PASS")
