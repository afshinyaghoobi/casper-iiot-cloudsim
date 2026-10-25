#!/usr/bin/env python3
"""Experimental topology scaling; frozen source never edited."""
from pathlib import Path
import sys
total=int(sys.argv[1]); assert total in (14,21,28)
edge=total*4//7; fog=total*2//7; cloud=total-edge-fog
assert (edge,fog,cloud) in ((8,4,2),(12,6,3),(16,8,4))
p=Path('src/main/java/org/casperiiot/e45/E45Campaign.java')
s=p.read_text()
pairs=[
 ('private static final int NODES = FrozenConfig.TOTAL_NODES;',f'private static final int NODES = {total};'),
 ('case CLOUD_ONLY -> j -> j>=18;',f'case CLOUD_ONLY -> j -> j>={edge+fog};'),
 ('case EDGE_FIRST -> j -> j<12;',f'case EDGE_FIRST -> j -> j<{edge};'),
 ('if(j<12){cap=',f'if(j<{edge}){{cap='),
 ('else if(j<18){cap=',f'else if(j<{edge+fog}){{cap='),
 ('return node<12?0:(node<18?1:2);',f'return node<{edge}?0:(node<{edge+fog}?1:2);'),
 ('for(int k=0;k<6;k++)m[a.get(k)]=true;',f'for(int k=0;k<{2*total//7};k++)m[a.get(k)]=true;')
]
for old,new in pairs:
 assert s.count(old)==1,(old,s.count(old))
 s=s.replace(old,new)
p.write_text(s)
print(f'TOPOLOGY_PATCH_PASS total={total} edge={edge} fog={fog} cloud={cloud} affected={2*total//7}')
