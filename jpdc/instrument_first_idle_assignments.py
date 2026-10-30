#!/usr/bin/env python3
"""Instrumentation of generated E45 only. No policy or scientific CSV changes.
Apply AFTER first_idle_tier_patch.py to the generated E45Campaign.java.
"""
from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
a="        final Acc acc=new Acc();"
b="            return vms.get(j);"
c="        return summarize(seed,n,scenario,policy,acc,affected);"
for anchor in (a,b,c):
    if s.count(anchor)!=1:
        raise SystemExit(f"INSTRUMENTATION_FAIL anchor {anchor!r} occurs {s.count(anchor)} times")
s=s.replace(a,a+"\n        final long[] dispatchByNode=new long[NODES];")
s=s.replace(b,"            dispatchByNode[j]++;\n"+b)
s=s.replace(c,'''        long total=0;
        for(long count:dispatchByNode) total+=count;
        if(total!=n) throw new IllegalStateException("dispatch count mismatch "+total+"/"+n);
        System.out.println("JPDC_NODE_ASSIGNMENTS scenario="+scenario+" policy="+policy+
                " seed="+seed+" counts="+Arrays.toString(dispatchByNode));
'''+c)
p.write_text(s)
print("FIRST_IDLE_NODE_INSTRUMENTATION_PASS")
