#!/usr/bin/env python3
"""Adversarial new routing state tests, including no premature network feedback."""
import math
from network_residual_risk_policy import (
    NetworkResidualRisk,nearest_rank_quantile,MIN_SAMPLES,WINDOW)
p=[20.0]*21
p[0]=10.0;p[1]=11.0
a=NetworkResidualRisk()
j,pen,active=a.choose(p)
assert j==0 and pen==0 and not active
print("PASS no network observation => original predictive greedy")
# The physical CPU-finish event may occur, but new risk cannot observe it;
# only the separately timestamped E2E network-feedback event calls observe.
for k in range(MIN_SAMPLES-1):
    a.observe_e2e(0,50.0,10.0,1000.0+k)
    assert a.choose(p)[0]==0
assert len(a.observations[0])==MIN_SAMPLES-1
assert a.choose(p)[0]==0
a.observe_e2e(0,50.,10.,1010.)
selected,pen,active=a.choose(p)
assert selected==1 and pen==0 and active
assert a.penalties()[0]==40
assert len(a.observations[0])==MIN_SAMPLES
print("PASS after 8 completed network feedbacks, network-risk step actually reroutes task")
b=NetworkResidualRisk()
for i in range(WINDOW+7):b.observe_e2e(2,2.0,5.0,2000+i)
assert len(b.observations[2])==WINDOW and b.penalties()[2]==0
assert nearest_rank_quantile([1,2,3,4,5,6,7,8,9,10])==9
print("PASS bounded 32-entry node memory, one-sided positive part and nearest rank 90th percentile")
try:a.observe_e2e(0,20.,10.,900.)
except ValueError:pass
else:raise AssertionError("out-of-order network feedback was accepted")
try:a.observe_e2e(0,1.,0.,3000.)
except ValueError:pass
else:raise AssertionError("invalid denominator was accepted")
try:a.choose([2.]*20)
except ValueError:pass
else:raise AssertionError("wrong predictor set size accepted")
try:a.choose([math.nan]+[2.]*20)
except ValueError:pass
else:raise AssertionError("bad predictor accepted")
try:a.observe_e2e(22,4.,1.,3000.)
except ValueError:pass
else:raise AssertionError("out-of-range affected node accepted")
print("PASS invalid inputs and out-of-order outcome ingestion fail closed")
# Strong observational causality: the state object has no input methods that
# accept true affected-node mask, future service or counterfactual outcomes.
assert all(not hasattr(a,key) for key in ("affected_nodes","physical_next","future_tasks"))
print("JPDC_NEW_NETWORK_RISK_PREDISPATCH_NO_LEAKAGE_UNIT_PASS")
