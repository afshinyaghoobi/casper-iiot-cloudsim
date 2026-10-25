#!/usr/bin/env python3
"""Exploratory count scaling with expected aggregate compute AND bandwidth normalization."""
import sys
from pathlib import Path
nodes=int(sys.argv[1]);assert nodes in (14,28)
p=Path('src/main/java/org/casperiiot/e45/E45Campaign.java')
s=p.read_text()
needle="x[j]=new NodeParams(cap,bw,rtt,sm,Math.max(1000,Math.round(cap*1000)));"
assert s.count(needle)==1
replace="""final double resourceFactor=21.0/NODES;
            final double normalizedCap=cap*resourceFactor;
            final double normalizedBw=bw*resourceFactor;
            x[j]=new NodeParams(normalizedCap,normalizedBw,rtt,sm,Math.max(1000,Math.round(normalizedCap*1000)));"""
s=s.replace(needle,replace)
p.write_text(s)
print('COMPUTE_BANDWIDTH_NORMALIZATION_PASS',nodes,21.0/nodes)
