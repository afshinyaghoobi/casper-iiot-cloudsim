#!/usr/bin/env python3
"""Stage36 exhaustive finite-source counterexample and selective risk unit checks."""
from fractions import Fraction
from itertools import product
from audit_stage36_selective_transfer_limits import (
    DiscreteLaw,conditional_class_transfer_audit,
    indistinguishable_target_worlds,selective_metrics)

def invalid(fn):
    try:fn()
    except (ValueError,TypeError,ZeroDivisionError):return
    raise AssertionError("invalid model accepted")

def test():
    donor=DiscreteLaw.from_dict({0:Fraction(9,10),20:Fraction(1,10)})
    target=DiscreteLaw.from_dict({0:Fraction(7,10),20:Fraction(3,10)})
    d=conditional_class_transfer_audit(donor,target,(-1,1))
    assert d["donor_miscoverage"]==Fraction(1,10)
    assert d["target_miscoverage"]==Fraction(3,10)
    assert d["conditional_total_variation"]==Fraction(1,5)
    assert d["conditional_upper"]==Fraction(3,10) and d["inequality_tight"]
    print("PASS TV class-transfer conditional inequality exact tight: 10%+20%=30%")

    # Exhaustive two-point discrete possible future worlds, conditional on SAME
    # observed past: any bounded interval width<20 misses at least one future.
    support=(0,20)
    tested=0
    for lo in range(-25,26):
        for hi in range(lo,26):
            if hi-lo>=20:continue
            scenario=indistinguishable_target_worlds((0,0,0,0,0,0,0,0,0,0),(lo,hi),hi+1)
            assert scenario["adversarial_covered"] is False
            assert scenario["worst_case_conditional_miscoverage"]==1
            # A finite interval narrower than gap cannot cover both possible
            # futures if domain q is explicitly restricted to {0,20}.
            assert not all(lo<=q<=hi for q in support)
            tested+=1
    assert tested>200
    print("PASS exhaustive finite-interval two-future worlds under identical ten-label history",tested)

    for history in ((),(0,)*10,(0,)*1000,(20,0,20,0)):
        for interval in ((-1,1),(-10,10),(20,20),(-100000,100000)):
            scenario=indistinguishable_target_worlds(history,interval)
            assert scenario["causal_history"]==tuple(history)
            assert scenario["worst_case_conditional_miscoverage"]==1
    print("PASS arbitrarily long observed donor/target history cannot constrain unrestricted future target shift")

    # Ten observed MISSION errors and donor errors can coincide exactly;
    # the 11th unseen target can depart without changing available history.
    old_history=(0,)*10
    worlds=[indistinguishable_target_worlds(old_history,(-1,1),20),
            indistinguishable_target_worlds(old_history,(-1,1),100)]
    assert all(x["benign_covered"] and not x["adversarial_covered"] for x in worlds)
    print("PASS posterior donor/target sample agreement is not a conditional-TV certificate")

    # TV inequality must hold for arbitrary exact discrete probability vectors.
    vals=(-2,0,9)
    num=0
    for a,b in product(range(5),repeat=2):
        if a+b>4:continue
        A=(a,b,4-a-b)
        source=DiscreteLaw.from_dict({v:Fraction(x,4) for v,x in zip(vals,A)})
        for c,e in product(range(5),repeat=2):
            if c+e>4:continue
            B=(c,e,4-c-e)
            other=DiscreteLaw.from_dict({v:Fraction(x,4) for v,x in zip(vals,B)})
            for interval in ((-3,-1),(-1,1),(0,9),(-2,9),(9,9)):
                audit=conditional_class_transfer_audit(source,other,interval)
                assert audit["target_miscoverage"]<=audit["conditional_upper"]
                num+=1
    assert num==15*15*5
    print("PASS exhaustive 1125 discrete conditional risk-TV comparisons")

    z=selective_metrics([False,False],[0,20],[None,None],
                        abstention_cost=Fraction(1,4),miss_penalty=2)
    assert z["selected_miscoverage"] is None
    assert z["availability"]==0 and z["operational_loss"]==Fraction(1,4)
    x=selective_metrics([True,False,True],[20,20,0],[(0,0),None,(0,0)],
                        abstention_cost=Fraction(1,4),miss_penalty=2)
    assert x["availability"]==Fraction(2,3)
    assert x["selected_miscoverage"]==Fraction(1,2)
    assert x["unconditional_issued_miss_frequency"]==Fraction(1,3)
    assert x["operational_loss"]==Fraction(1,12)+Fraction(2,3)
    print("PASS selective issued-only risk versus unconditional issued-miss rate and abstention loss")

    invalid(lambda:DiscreteLaw.from_dict({0:Fraction(2,3),20:Fraction(1,2)}))
    invalid(lambda:DiscreteLaw.from_dict({0:-1,20:2}))
    invalid(lambda:DiscreteLaw.from_dict({0:True,20:0}))
    invalid(lambda:indistinguishable_target_worlds((0,),(0,2),1))
    invalid(lambda:selective_metrics([False],[0],[(0,0)]))
    invalid(lambda:selective_metrics([True],[0],[None]))
    invalid(lambda:selective_metrics([True],[0],[(0,0)],abstention_cost=-1,miss_penalty=2))
    invalid(lambda:conditional_class_transfer_audit(donor,target,(2,-1)))
    print("PASS reject invalid laws, action intervals and unpaired safety/cost accounting")

    print("JPDC_STAGE36_SELECTIVE_RISK_NO_FREE_LUNCH_AND_TV_CONTRACT_PASS")

if __name__=="__main__":test()
