#!/usr/bin/env python3
"""SYNTHETIC-only checks; not original Google task rows."""
import base64
import gzip
import hashlib
import json
from google2011_full_spent_partition_stream_pilot import (
    crc32c_bytes,scan_full_gzip,EXPECTED_COMPRESSED_BYTES)

def reject(f):
    try:f()
    except (ValueError,AssertionError,EOFError,OverflowError):return
    raise AssertionError("malformed synthetic source incorrectly accepted")

def main():
    assert crc32c_bytes(b"123456789")=="4waSgw=="  # CRC32C standard 0xe3069283
    assert crc32c_bytes(b"")=="AAAAAA=="
    # All 1024 simulated prefix events are clearly NOT real original records:
    # the previous historical prefix guard must reject any made-up source.
    dummy=b"0,,1,0,,0,u,0,0,0.1,0.1,,\n"*1024
    synthetic_gzip=gzip.compress(dummy,mtime=0)
    padded=synthetic_gzip+b"\x00"*(EXPECTED_COMPRESSED_BYTES-len(synthetic_gzip))
    meta=dict(md5Hash=base64.b64encode(hashlib.md5(padded).digest()).decode(),
              crc32c=crc32c_bytes(padded))
    reject(lambda:scan_full_gzip(padded,meta))
    reject(lambda:scan_full_gzip(padded[:-1],meta))
    reject(lambda:scan_full_gzip(b"hello",meta))
    assert len(synthetic_gzip)<EXPECTED_COMPRESSED_BYTES
    print("JPDC_GOOGLE2011_FULL_STREAM_SYNTHETIC_NEGATIVE_TESTS_PASS")
if __name__=="__main__":main()
