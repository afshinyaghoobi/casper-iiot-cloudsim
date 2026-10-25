#!/usr/bin/env python3
"""Exploratory expected-compute-normalized scale variant; requires topology_patch.py first."""
from pathlib import Path
import sys
nodes=int(sys.argv[1])
assert nodes in (14,28)
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
needle="x[j]=new NodeParams(cap,bw,rtt,sm,Math.max(1000,Math.round(cap*1000)));"
assert s.count(needle)==1
s=s.replace(needle,"final double normalizedCap=cap*(21.0/NODES);\n            x[j]=new NodeParams(normalizedCap,bw,rtt,sm,Math.max(1000,Math.round(normalizedCap*1000)));")
p.write_text(s)
print("COMPUTE_NORMALIZATION_PASS nodes",nodes,"factor",21.0/nodes)
