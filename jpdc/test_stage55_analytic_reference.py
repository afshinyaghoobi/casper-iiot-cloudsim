#!/usr/bin/env python3
"""Stage55 analytically independent fixed-route FIFO test fixtures."""
from analytic_fcfs_reference_stage55 import audit

def original(i,a,cpu=1,deadline=10):
    return ("S0_STATIONARY",i,"MISSION",deadline,1,.01,.01,a)

def row(i,j,a,cpu,net,start,finish):
    return dict(task=i,node=j,arrival_ms=a,cpu_ms=cpu,network_ms=net,
                start_ms=start,finish_ms=finish,wait_ms=start-a,
                latency_ms=finish-a+net)

def main():
    # FIFO queue, idle gap, and true parallel servers.
    src=[original(0,10),original(1,11),original(2,12),original(3,15)]
    good=[row(0,0,10,4,2,10,14),row(1,0,11,3,2,14,17),
          row(2,1,12,3,2,12,15),row(3,1,15,1,2,15,16)]
    out=audit(good,src,2)
    assert out["status"]=="PASS"
    assert out["max_absolute_error_ms"]==dict.fromkeys(
        ("start_ms","finish_ms","wait_ms","latency_ms"),0.0)
    assert out["deadline_misses"]["MISSION"]==0
    # Duplicate task, fabricated wait and non-FCFS bypass must be detected.
    bad=[good+[good[0]],
         [dict(x,wait_ms=0) if x["task"]==1 else x for x in good],
         [dict(x,start_ms=11,finish_ms=14,wait_ms=0,latency_ms=5)
          if x["task"]==1 else x for x in good]]
    for rows in bad:
        try:
            audit(rows,src,2)
        except (AssertionError,ValueError):
            continue
        raise AssertionError("Stage55 accepted invalid analytical FIFO fixture")
    print("JPDC_STAGE55_LINDLEY_REFERENCE_CONTRACT_PASS")
if __name__=="__main__":main()
