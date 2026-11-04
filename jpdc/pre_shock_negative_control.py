#!/usr/bin/env python3
"""Exact pre-shock placebo consistency of physical S3 mask interventions.
Run: python3 jpdc/pre_shock_negative_control.py DIRECTORY
DIRECTORY holds GitHub Actions physical artifact ZIP files (seed40..43).
Does not re-run CloudSim; all matches are deterministic and per task.
"""
import csv
import io
import pathlib
import sys
import zipfile

ARTIFACTS = {40: 13272215535, 41: 13271273184,
             42: 13270784276, 43: 13272485400}
# Fields correspond to the actual documented trace schema.
COMPARE_COLUMNS = (4, 5, 7, 8, 9, 10)  # task, node, nominal/actual delay, multiplier, latency

def trace(z, arm):
    records = csv.reader(io.StringIO(z.read(f'{arm}/mission_network.csv').decode()))
    before = {}
    for record in records:
        task = int(record[4])
        if task >= 10000:
            continue
        if task in before:
            raise AssertionError(f'duplicate pre-shock task {task}')
        before[task] = record
    return before

def audit(folder):
    n_total = 0
    for seed, artifact in ARTIFACTS.items():
        path = folder / f'github-actions-artifact-{artifact}.zip'
        with zipfile.ZipFile(path) as z:
            base, low, high = (trace(z, arm) for arm in ('baseline', 'low', 'high'))
            ids = set(base)
            assert ids and ids == set(low) == set(high), f'pre task ID mismatch seed {seed}'
            for task in sorted(ids):
                original = tuple(base[task][c] for c in COMPARE_COLUMNS)
                for arm, data in (('low', low), ('high', high)):
                    modified = tuple(data[task][c] for c in COMPARE_COLUMNS)
                    assert original == modified, (seed, task, arm, original, modified)
            n_total += len(ids)
            print(f'PASS seed {seed}: {len(ids)} pre-shock mission tasks exactly matched across 3 masks')
    print(f'PASS {n_total} distinct pre-shock mission task IDs, {n_total * 2} exact arm-to-baseline comparisons')
    print('LIMIT: checks only observed pre-shock CASPER_FULL task traces; no simulator generalization.')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    audit(pathlib.Path(sys.argv[1]))
