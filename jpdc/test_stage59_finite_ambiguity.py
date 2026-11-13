#!/usr/bin/env python3
"""Stage59 exhaustive predeclared two-world/two-node algebra and contracts."""
import itertools
import json
from finite_ambiguity_deadline_stage59 import NODES, select


def embed(a,b,other=100.0):
    return [float(a),float(b)]+[float(other)]*(NODES-2)


def brute_two_node(a0,a1,b0,b1,deadline):
    # Independent direct 2-candidate enumeration of lexicographic objective.
    # Other 19 nodes fixed at 100 and therefore cannot win for 1..8 costs.
    conditions=[]
    for j in (0,1):
        w1=(a0,a1)[j]
        w2=(b0,b1)[j]
        missed=int(max(w1,w2)>deadline)
        regret=max(w1-min(a0,a1),w2-min(b0,b1))
        conditions.append((missed,regret,(a0,a1)[j],j))
    return min(conditions)[-1]


def run():
    # Indistinguishable latent states: both choices can be optimal only in
    # their own physical world, so no deterministic causal universal optimum.
    A=embed(10,12)
    B=embed(40,12)
    d=select(A,[A,B],20)
    assert d.node==1 and d.nominal_greedy_node==0
    assert d.switched_from_nominal and d.robust_feasible_in_given_worlds
    assert d.worst_case_deadline_miss==0
    assert d.worst_case_latency_regret_ms==2
    assert all(max(2*(1-p/15), 28*(p/15)) >= 28/15-1e-12 for p in (0,1,15))
    # For randomized node0 probability 1/15, the worst expected regret is 28/15.
    assert abs(2*(1-1/15)-28/15)<1e-12

    nominal=embed(10,12)
    assert select(nominal,[nominal],20).node==0
    tie=embed(10,10)
    assert select(tie,[tie],10).node==0
    assert not select(embed(40,50),[embed(40,50)],20).robust_feasible_in_given_worlds
    # No unobserved true affected-node set or future service belongs to API.
    try:
        select(nominal,[A,B],20,actual_future_world=B)
    except TypeError:
        pass
    else:
        raise AssertionError("unexpected oracle parameter accepted")

    invalid=[
        (nominal,[],20),
        (nominal,[[1.,2.]],20),
        (nominal[:-1],[A],20),
        ([float("inf")]+nominal[1:],[A],20),
        (nominal,[[float("nan")]+A[1:]],20),
        (nominal,[A],0),
        (nominal,[A],True),
        (nominal,[[True]+A[1:]],20),
        (nominal,[A],-1),
        (nominal,[A],float("inf")),
    ]
    for args in invalid:
        try: select(*args)
        except ValueError: continue
        raise AssertionError("malformed Stage59 ambiguity data accepted")

    checked=0
    switch_count=0
    feasible=0
    for a0,a1,b0,b1,deadline in itertools.product(range(1,9),repeat=5):
        A=embed(a0,a1)
        B=embed(b0,b1)
        res=select(A,[A,B],deadline)
        expected=brute_two_node(a0,a1,b0,b1,deadline)
        assert res.node==expected,(a0,a1,b0,b1,deadline,res,expected)
        assert res.nominal_greedy_node==(0 if a0<=a1 else 1)
        candidate=max(a0 if res.node==0 else a1,
                      b0 if res.node==0 else b1)
        assert res.robust_feasible_in_given_worlds==(candidate<=deadline)
        assert res.worst_case_deadline_miss==int(candidate>deadline)
        calc=max((a0,a1)[res.node]-min(a0,a1),
                 (b0,b1)[res.node]-min(b0,b1))
        assert res.worst_case_latency_regret_ms==calc
        switch_count+=int(res.switched_from_nominal)
        feasible+=int(res.robust_feasible_in_given_worlds)
        checked+=1
    assert checked==32768
    output=dict(status="PASS",scientific_scope="finite hypothetical worlds only",
                exhaustive_two_node_two_world_fixtures=checked,
                nonalias_switch_cases=switch_count,
                robust_feasible_model_cases=feasible,
                genuine_source_seed_count=0,
                real_future_oracle_used=False,
                source_policy_efficacy_claim=False,
                original_java_python_parity_still_failed=True)
    print("JPDC_STAGE59_PROOF_CONTRACT",json.dumps(output,sort_keys=True))
    print("JPDC_STAGE59_AMBIGUITY_EXHAUSTIVE_PASS")
    return output


if __name__=="__main__":
    print(json.dumps(run(),sort_keys=True))
