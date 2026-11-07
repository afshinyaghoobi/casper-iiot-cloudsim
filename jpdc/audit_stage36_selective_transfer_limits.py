#!/usr/bin/env python3
"""Stage36 exact finite-state identifiability and class-transfer *audit*, NOT a policy.

No predictive bounds are learned or certified. This tool only verifies
elementary conditional results under stated, externally unverified assumptions.
"""
from dataclasses import dataclass
from fractions import Fraction
from collections import Counter

@dataclass(frozen=True)
class DiscreteLaw:
    masses:tuple

    @classmethod
    def from_dict(cls, probabilities):
        if not isinstance(probabilities,dict) or not probabilities:
            raise ValueError("nonempty discrete law required")
        pairs=[]
        for outcome,weight in probabilities.items():
            if isinstance(outcome,bool) or not isinstance(outcome,int):
                raise ValueError("only integer outcomes in finite model")
            if isinstance(weight,bool):raise ValueError("invalid probability")
            mass=Fraction(weight)
            if not 0<=mass<=1:raise ValueError("probability outside [0,1]")
            pairs.append((outcome,mass))
        if sum((x[1] for x in pairs),Fraction(0))!=1:
            raise ValueError("probability mass must sum exactly to 1")
        return cls(tuple(sorted((k,v) for k,v in pairs if v)))

    def miss_probability(self, interval):
        lo,hi=validate_interval(interval)
        return sum((p for value,p in self.masses if not lo<=value<=hi),Fraction(0))

    def total_variation(self,other):
        a=dict(self.masses);b=dict(other.masses)
        return sum((abs(a.get(i,Fraction(0))-b.get(i,Fraction(0)))
                    for i in set(a)|set(b)),Fraction(0))/2

def validate_interval(interval):
    if (not isinstance(interval,(tuple,list)) or len(interval)!=2
            or any(isinstance(x,bool) or not isinstance(x,int) for x in interval)):
        raise ValueError("finite integer interval required")
    a,b=interval
    if a>b:raise ValueError("lower endpoint exceeds upper")
    return (a,b)

def conditional_class_transfer_audit(donor,target,interval):
    """Checks TV event implication for exact, GIVEN conditional laws.

    In real model no one knows the source/time-conditioned target distribution.
    The returned exact values are algebraic forensic truths, NOT certificates.
    """
    if not isinstance(donor,DiscreteLaw) or not isinstance(target,DiscreteLaw):
        raise TypeError("full conditional source/target laws required")
    lo,hi=validate_interval(interval)
    donor_miss=donor.miss_probability((lo,hi))
    target_miss=target.miss_probability((lo,hi))
    tv=donor.total_variation(target)
    upper=min(Fraction(1),donor_miss+tv)
    assert target_miss<=upper
    return dict(donor_miscoverage=donor_miss,target_miscoverage=target_miss,
                conditional_total_variation=tv,conditional_upper=upper,
                inequality_tight=target_miss==upper)

def indistinguishable_target_worlds(history,interval,alternative_error=None):
    """Same arbitrary causal past; futures 0 and out-of-interval shift.

    Only deterministic finite-interval decisions covered by this construction.
    """
    lo,hi=validate_interval(interval)
    if alternative_error is None:alternative_error=hi+1
    if isinstance(alternative_error,bool) or not isinstance(alternative_error,int):
        raise ValueError("invalid target future error")
    if lo<=alternative_error<=hi:
        raise ValueError("alternative must lie outside interval")
    h=tuple(history)
    # Any observed history may be the same in both source worlds.
    return dict(causal_history=h,issued_interval=(lo,hi),
                benign_future=0,adversarial_future=alternative_error,
                benign_covered=lo<=0<=hi,
                adversarial_covered=False,
                worst_case_conditional_miscoverage=Fraction(1),
                finite_issuance_without_assumptions_cannot_be_certified=True)

def selective_metrics(issued,realized,intervals,abstention_cost=None,miss_penalty=None):
    """Finite offline accounting; error for nonissued tasks not imputed as safe."""
    n=len(issued)
    if n==0 or len(realized)!=n or len(intervals)!=n:
        raise ValueError("matching nonempty issue/realized/interval sequences required")
    if any(not isinstance(v,bool) for v in issued):
        raise ValueError("issue flags must be booleans")
    for value,flag,interval in zip(realized,issued,intervals):
        if isinstance(value,bool) or not isinstance(value,int):
            raise ValueError("finite integer outcomes required")
        if flag:validate_interval(interval)
        elif interval is not None:raise ValueError("abstentions cannot masquerade as issued intervals")
    accepts=sum(issued)
    misses=sum(int(not intervals[i][0]<=realized[i]<=intervals[i][1])
               for i in range(n) if issued[i])
    result=dict(tasks=n,issued=accepts,abstentions=n-accepts,
                availability=Fraction(accepts,n),
                selected_miscoverage=(Fraction(misses,accepts) if accepts else None),
                unconditional_issued_miss_frequency=Fraction(misses,n),
                selected_miss_count=misses)
    if abstention_cost is not None or miss_penalty is not None:
        if (abstention_cost is None or miss_penalty is None or
            isinstance(abstention_cost,bool) or isinstance(miss_penalty,bool)):
            raise ValueError("both costs must be nonnegative rational values")
        cost=Fraction(abstention_cost)
        penalty=Fraction(miss_penalty)
        if cost<0 or penalty<0:raise ValueError("costs must be nonnegative")
        result["operational_loss"]=cost*Fraction(n-accepts,n)+penalty*Fraction(misses,n)
    return result
