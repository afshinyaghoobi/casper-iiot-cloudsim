#!/usr/bin/env python3
import hashlib, json, pathlib, sys
root = pathlib.Path(__file__).resolve().parents[1]
manifest = json.loads((root/'E41_SOURCE_MANIFEST.json').read_text())
exclude_prefixes = ('results/',)
exclude_names = {'E41_STATUS.json','E41_REPORT.md','README.md','E41_SOURCE_MANIFEST.json'}
fail=[]; checked=0
for row in manifest:
    rel=row['path']
    if rel in exclude_names or rel.startswith(exclude_prefixes):
        continue
    p=root/rel
    if not p.exists():
        fail.append((rel,'MISSING',row['sha256']))
        continue
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    checked += 1
    if h != row['sha256']:
        fail.append((rel,h,row['sha256']))
if fail:
    print('FROZEN_SOURCE_VERIFY FAIL')
    for x in fail: print(*x)
    sys.exit(2)
print(f'FROZEN_SOURCE_VERIFY PASS checked={checked}')
