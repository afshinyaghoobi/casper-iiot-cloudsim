#!/usr/bin/env python3
"""Adversarial decision fixtures; no Java input, no original physical traces."""
from independent_casper_deployment_stage4 import route
from independent_physical_calibration_stage3 import calibrate

t=("S2_HIDDEN_COMPUTE_40LOSS",11000,"MISSION",50.0,18.0,.05,.01,90000.0)
pred=[1000.0]*21
pred[0]=10.0;pred[1]=11.0;pred[2]=12.0
sigma=[1.0]*21
alarm=[False]*21
node,rank,cert,family=route(t,pred,alarm,sigma,[50.0,1.0,50.0],1.0,1.0,"CASPER_FULL")
assert (node,rank,cert)==(1,2,True)
assert family==(0,1,2)
print("PASS actual rank2 certificate rescue with original first feasible ordering")
node,rank,cert,_=route(t,pred,alarm,sigma,[50.,50.,1.],1.,1.,"CASPER_FULL")
assert (node,rank,cert)==(2,3,True)
print("PASS actual rank3 certificate rescue synthetic branch")
node,rank,cert,_=route(t,pred,alarm,sigma,[50.,50.,50.],1.,1.,"CASPER_FULL")
assert (node,rank,cert)==(0,1,False)
print("PASS rank1 abstention when all ranked bounds infeasible")
alarm[0]=True
node,rank,cert,family=route(t,pred,alarm,sigma,[50.,1.,50.],1.,1.,"CASPER_FULL")
assert node!=0 and 0 not in family
print("PASS health-alarmed nodes excluded from ranked family")
alarm[:]=[True]*21
node,rank,cert,family=route(t,pred,alarm,sigma,[50.,1.,50.],1.,1.,"CASPER_FULL")
assert (node,rank,cert,family)==(0,1,False,())
print("PASS all-health-alarmed fallback abstention")
node,rank,cert,family=route(t,pred,alarm,sigma,[50.,1.,50.],1.,1.,"PRED_GREEDY")
assert (node,rank,cert,family)==(0,1,False,())
print("PASS baseline never creates certificate")
for policy in ("CASPER_FULL","CASPER_HEALTH_STATIC","PRED_GREEDY"):
    try:route(t,pred[:-1],alarm,sigma,[1.,1.,1.],1.,1.,policy)
    except ValueError:pass
    else:raise AssertionError("invalid policy vector accepted")
print("PASS malformed predictor vectors fail closed")

# Full native calibration reference is independently generated; never copied Java.
cal=calibrate(50,80000,include_reference=True)
assert cal["status"]=="PASS"
assert len(cal["reference_scores"])==cal["mission_score_count"]==sum(cal["rank_counts"])
assert len(cal["reference_scores"])>200
assert all(x>=0 for x in cal["reference_scores"])
print("PASS independent native calibration score stream available for E17")
print("JPDC_NATIVE_STAGE4_POLICY_UNIT_PASS")
