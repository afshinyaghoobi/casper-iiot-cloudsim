#!/usr/bin/env python3
"""Check deadline-policy patch is exactly reversible on the frozen Java anchors.

Runs on repository Java source, without generating/building CloudSim.
"""
from pathlib import Path
import ast
source=Path("src/main/java/org/casperiiot/e42/E42Campaign.java").read_text()
patch=Path("jpdc/deadline_feasible_min_uncertainty_patch.py").read_text()
assert "DEADLINE_FEASIBLE_MIN_UNCERTAINTY" in patch
enum_old="        PRED_GREEDY(false,false,false,false),"
dispatch_old="            if(!policy.cp){\n                j=argMin(pred,eligible);\n            }else{"
assert source.count(enum_old)==1
assert source.count(dispatch_old)==1
tree=ast.parse(patch)
# Read only literal definitions, do not execute the file-modifying patch.
strings=[node.value.value for node in ast.walk(tree) if isinstance(node,ast.Constant) and isinstance(node.value,str)]
new_dispatch=next(v for v in strings if "if(policy==Policy.DEADLINE_FEASIBLE_MIN_UNCERTAINTY)" in v)
new_enum=enum_old+"\n        DEADLINE_FEASIBLE_MIN_UNCERTAINTY(false,false,false,false),"
assert source.count(new_dispatch)==0
modified=source.replace(enum_old,new_enum).replace(dispatch_old,new_dispatch)
assert modified.count("DEADLINE_FEASIBLE_MIN_UNCERTAINTY")==2
assert modified.replace(new_dispatch,dispatch_old).replace(new_enum,enum_old)==source
assert "counterfactualActualLatencyMs" in source
print("DEADLINE_PATCH_REVERSIBILITY_PASS 2 anchors; exact original reconstruction")
