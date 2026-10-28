#!/usr/bin/env python3
"""Test SHA lock on original candidate reference without changing E4.6."""
import hashlib, tempfile
from pathlib import Path
from validate_s3_strata30 import verify_reference,REFERENCE_SHA256
with tempfile.TemporaryDirectory() as d:
    p=Path(d)/"reference.csv"
    p.write_bytes(b"deliberately wrong reference\n")
    try: verify_reference(p)
    except ValueError: print("HASH_GATE_REJECT_PASS")
    else: raise AssertionError("bad reference accepted")
    assert len(REFERENCE_SHA256)==64
print("SHA_GATE_NEGATIVE_TEST_PASS")
