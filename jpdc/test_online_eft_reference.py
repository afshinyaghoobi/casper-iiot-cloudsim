#!/usr/bin/env python3
"""Independent semantic and edge-case checks for EFT reference baseline."""
from online_eft_reference import Task,choose_eft,online_dispatch
from math import isclose
def run():
    assert choose_eft(Task(0,10,(0,0),10),[0,0],[1,2])==(1,5)
    assert choose_eft(Task(0,4,(0,0),10),[0,0],[1,1])==(0,4)
    assert choose_eft(Task(3,3,(0,0),9),[15,0],[1,1])==(1,6)
    assert choose_eft(Task(1,2,(0,8),20),[0,0],[1,4])==(0,3)
    tasks=[Task(0,8,(0,0),10),Task(0,4,(0,0),10)]
    out=online_dispatch(tasks,[1,2])
    assert [r["node"] for r in out]==[1,0]
    assert isclose(out[0]["finish"],4) and isclose(out[1]["finish"],4)
    try: online_dispatch([Task(2,1,(0,),4),Task(1,1,(0,),4)],[1])
    except ValueError: pass
    else: raise AssertionError("future-task input not rejected")
    try: choose_eft(Task(0,1,(0,),1),[0],[0])
    except ValueError: pass
    else: raise AssertionError("zero-speed node accepted")
    print("ONLINE_EFT_REFERENCE_TEST_PASS 7 cases")
if __name__=="__main__":run()
