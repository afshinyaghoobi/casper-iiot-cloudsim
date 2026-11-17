#!/usr/bin/env python3
"""Local source checkpoint-head compare-and-swap demo with external trust pins.

This does NOT publish a protected new head to GitHub. A caller must obtain
trusted head SHA from an independent protected authority each invocation.
"""
import argparse
import fcntl
import hashlib
import json
import os
import tempfile
from pathlib import Path
from google2011_sqlite_detached_checkpoint import canonical,verify,hashfile
from google2011_guarded_resume import trusted_arguments

GENESIS_CHECKPOINT="e8b134abc3f1f4e656d830ee5906548124daddd4ecbecb1cdcfe24c0bf8a83f5"
VERSION="jpdc-local-head-cas-v1"

def record_sha(d):
    return hashlib.sha256(canonical(d)).hexdigest()

def read_trusted(head,expected_head_sha):
    if not expected_head_sha or len(expected_head_sha)!=64:
        raise ValueError("HEAD_CAS_DENIED independently trusted latest head SHA required")
    raw=Path(head).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=expected_head_sha:
        raise ValueError("HEAD_CAS_DENIED local HEAD mismatch external trusted head")
    data=json.loads(raw)
    if raw!=canonical(data) or data.get("version")!=VERSION:
        raise ValueError("HEAD_CAS_DENIED malformed head")
    trusted_arguments(data.get("checkpoint_sha256"),data.get("ordinal"))
    return data

def _locked(head):
    lock=Path(str(head)+".lock")
    lock.parent.mkdir(parents=True,exist_ok=True)
    f=lock.open("a+b")
    fcntl.flock(f.fileno(),fcntl.LOCK_EX)
    return f

def _publish_atomic(head,data,inject_failure=False):
    head=Path(head)
    encoded=canonical(data)
    fd,tmp=tempfile.mkstemp(prefix=".checkpoint-head-",dir=str(head.parent))
    try:
        with os.fdopen(fd,"wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        if inject_failure:
            raise ValueError("HEAD_CAS_DENIED injected failure before replace")
        os.replace(tmp,head)
        directory=os.open(str(head.parent),os.O_RDONLY)
        try:os.fsync(directory)
        finally:os.close(directory)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
    return hashlib.sha256(encoded).hexdigest()

def bootstrap(head,db,checkpoint,*,trusted_genesis_sha,ordinal=1):
    """Create local HEAD only from caller-pinned authentic genesis checkpoint."""
    if trusted_genesis_sha!=GENESIS_CHECKPOINT or ordinal!=1:
        raise ValueError("HEAD_CAS_DENIED original genesis trust pin mismatch")
    verify(db,checkpoint,trusted_sha=trusted_genesis_sha,
           minimum_ordinal=1,expected_latest_ordinal=1)
    head=Path(head);head.parent.mkdir(parents=True,exist_ok=True)
    lock=_locked(head)
    try:
        if head.exists():raise ValueError("HEAD_CAS_DENIED HEAD already initialized")
        data=dict(version=VERSION,ordinal=1,checkpoint_sha256=trusted_genesis_sha,
                  prior_head_record_sha256=None,original_source_data_batches=1,
                  external_trust_publication_confirmed=False)
        digest=_publish_atomic(head,data)
        return dict(status="PASS",action="BOOTSTRAP_LOCAL_CANDIDATE",
                    head_sha256=digest,ordinal=1,
                    protected_external_head_publication=False)
    finally:lock.close()

def advance(head,db,candidate,*,trusted_current_head_sha,
            trusted_candidate_sha,trusted_latest_ordinal,
            inject_failure=False):
    """Serial local CAS. Never silently accept HEAD record as its own trusted pin."""
    trusted_arguments(trusted_current_head_sha,trusted_latest_ordinal)
    trusted_arguments(trusted_candidate_sha,trusted_latest_ordinal)
    lock=_locked(head)
    try:
        prior=read_trusted(head,trusted_current_head_sha)
        if prior["ordinal"]!=trusted_latest_ordinal:
            raise ValueError("HEAD_CAS_DENIED stale expected head ordinal")
        candidate_path=Path(candidate)
        raw=candidate_path.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=trusted_candidate_sha:
            raise ValueError("HEAD_CAS_DENIED candidate detached checkpoint pin mismatch")
        obj=json.loads(raw)
        if raw!=canonical(obj):
            raise ValueError("HEAD_CAS_DENIED candidate checkpoint noncanonical")
        if (obj.get("ordinal")!=prior["ordinal"]+1 or
            obj.get("previous_checkpoint_sha256")!=prior["checkpoint_sha256"]):
            raise ValueError("HEAD_CAS_DENIED successor ordinal/predecessor mismatch")
        verify(db,candidate,trusted_sha=trusted_candidate_sha,
               expected_latest_ordinal=prior["ordinal"]+1,
               expected_predecessor=prior["checkpoint_sha256"])
        next_head=dict(version=VERSION,ordinal=prior["ordinal"]+1,
                       checkpoint_sha256=trusted_candidate_sha,
                       prior_head_record_sha256=trusted_current_head_sha,
                       original_source_data_batches=1,
                       external_trust_publication_confirmed=False)
        next_digest=_publish_atomic(head,next_head,inject_failure)
        return dict(status="PASS",action="LOCAL_CANDIDATE_ADVANCED",
                    previous_head_sha256=trusted_current_head_sha,
                    candidate_new_head_sha256=next_digest,
                    ordinal=next_head["ordinal"],
                    protected_external_head_publication=False,
                    original_source_data_batches=1,
                    stage65="FAIL",java_python_parity="FAIL")
    finally:lock.close()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--head",required=True)
    p.add_argument("--db",required=True)
    p.add_argument("--checkpoint",required=True)
    p.add_argument("--bootstrap",action="store_true")
    p.add_argument("--trusted-genesis-sha")
    p.add_argument("--trusted-current-head-sha")
    p.add_argument("--trusted-candidate-sha")
    p.add_argument("--trusted-latest-ordinal",type=int)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    if a.bootstrap:
        result=bootstrap(a.head,a.db,a.checkpoint,trusted_genesis_sha=a.trusted_genesis_sha)
    else:
        result=advance(a.head,a.db,a.checkpoint,
                       trusted_current_head_sha=a.trusted_current_head_sha,
                       trusted_candidate_sha=a.trusted_candidate_sha,
                       trusted_latest_ordinal=a.trusted_latest_ordinal)
    Path(a.out).write_bytes(canonical(result))
    print("JPDC_LOCAL_EXTERNAL_HEAD_CAS",json.dumps(result,sort_keys=True))
if __name__=="__main__":main()
