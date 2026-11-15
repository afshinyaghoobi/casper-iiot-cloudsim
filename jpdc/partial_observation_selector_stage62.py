#!/usr/bin/env python3
"""Stage62 subset-only hypothetical ranking, never treats missing nodes as safe."""
from dataclasses import dataclass
import math
from causal_ambiguity_builder_stage60 import (NODES,CPU_MIN,NETWORK_MIN,
    MAX_AGE_MS,TELEMETRY_MAX_AGE_MS,num)

@dataclass(frozen=True)
class PartialChoice:
    status:str
    eligible_nodes:tuple
    nominal_greedy:int
    proposed_node:int|None
    unavailable:tuple
    conditional_only:bool=True
    empirically_calibrated:bool=False

def choose_partial(builder,now_ms,predicted_ms,nominal_network_ms,deadline_ms):
    now=num(now_ms)
    deadline=num(deadline_ms,positive=True)
    if now<builder.last_event: raise ValueError("retroactive decision")
    if len(predicted_ms)!=NODES or len(nominal_network_ms)!=NODES:
        raise ValueError("21-node finite current predictions required")
    p=tuple(num(x,positive=True) for x in predicted_ms)
    tuple(num(x,positive=True) for x in nominal_network_ms)
    greedy=min(range(NODES),key=lambda j:(p[j],j))
    fresh=builder.telemetry_time is not None and (
        now-builder.telemetry_time<=TELEMETRY_MAX_AGE_MS)
    unavailable=[]
    if not fresh: unavailable.append("TELEMETRY_MISSING_OR_STALE")
    eligible=[]
    for j in range(NODES):
        cpu_ok=(len(builder.cpu[j])>=CPU_MIN and
            builder.last_cpu_measurement[j] is not None and
            now-builder.last_cpu_measurement[j]<=MAX_AGE_MS)
        net_ok=(len(builder.net[j])>=NETWORK_MIN and
            builder.last_net_measurement[j] is not None and
            now-builder.last_net_measurement[j]<=MAX_AGE_MS)
        if not cpu_ok:unavailable.append(f"CPU_NODE_{j}_UNKNOWN_OR_STALE")
        if not net_ok:unavailable.append(f"E2E_NODE_{j}_UNKNOWN_OR_STALE")
        if cpu_ok and net_ok:eligible.append(j)
    if len(eligible)<2:unavailable.append("FEWER_THAN_TWO_ELIGIBLE_NODES")
    if greedy not in eligible:unavailable.append("GLOBAL_NOMINAL_GREEDY_NOT_OBSERVED")
    # Missing *excluded* nodes are diagnostic, not a reason to reject a
    # safe-to-rank observed subset. Only explicit global gates can block.
    blockers=[reason for reason in unavailable if (
        reason=="TELEMETRY_MISSING_OR_STALE" or
        reason=="FEWER_THAN_TWO_ELIGIBLE_NODES" or
        reason=="GLOBAL_NOMINAL_GREEDY_NOT_OBSERVED")]
    if blockers:
        return PartialChoice("ABSTAIN_UNVERIFIED",tuple(eligible),greedy,None,
                             tuple(unavailable))
    # All cost scenarios use observed historically delivered per-node residuals.
    costs=[]
    for kind in range(4):
        row={}
        for j in eligible:
            cpu=max(builder.cpu[j]) if kind in (1,3) else 0.
            net=max(builder.net[j]) if kind in (2,3) else 0.
            cost=p[j]+cpu+net
            if not math.isfinite(cost) or cost<=0:raise ValueError("bad cost")
            row[j]=cost
        costs.append(row)
    lows=[min(w.values()) for w in costs]
    score={}
    for j in eligible:
        worst_miss=max(int(row[j]>deadline) for row in costs)
        regret=max(row[j]-lo for row,lo in zip(costs,lows))
        score[j]=(worst_miss,regret,p[j],j)
    chosen=min(eligible,key=lambda j:score[j])
    return PartialChoice("READY_PARTIAL_UNCALIBRATED",tuple(eligible),greedy,chosen,())
