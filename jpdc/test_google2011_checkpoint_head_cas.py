#!/usr/bin/env python3
"""Genuine previously spent Google part375 genesis; synthetic successor CAS tests."""
import json
import shutil
import tempfile
from pathlib import Path
from google2011_checkpoint_head_cas import bootstrap,advance,read_trusted
from google2011_sqlite_detached_checkpoint import canonical,hashfile,issue

PIN="e8b134abc3f1f4e656d830ee5906548124daddd4ecbecb1cdcfe24c0bf8a83f5"
DB_SHA="ab4851f5fd43f01bbd212a31789b9d88237cfec81db074f921d570ea3d44f5dc"

def reject(f,why):
    try:f()
    except ValueError as e:
        assert why in str(e),(why,str(e))
        return
    raise AssertionError("unsafe stale or forged source HEAD admitted")

def run(db_original,checkpoint_original):
    assert hashfile(db_original)==DB_SHA
    assert hashfile(checkpoint_original)==PIN
    with tempfile.TemporaryDirectory() as temp:
        root=Path(temp);db=root/"source.sqlite";cp=root/"genesis.json";head=root/"trusted_head.json"
        shutil.copyfile(db_original,db);shutil.copyfile(checkpoint_original,cp)
        reject(lambda:bootstrap(head,db,cp,trusted_genesis_sha="0"*64),"genesis")
        assert not head.exists()
        gen=bootstrap(head,db,cp,trusted_genesis_sha=PIN)
        h1=gen["head_sha256"]
        assert read_trusted(head,h1)["ordinal"]==1
        reject(lambda:bootstrap(head,db,cp,trusted_genesis_sha=PIN),"already initialized")
        reject(lambda:read_trusted(head,None),"independently trusted")
        # The exact same original archived SQLite is re-checkpointed as an
        # ADMINISTRATIVE-only chain. No original new source file is ingested.
        second=root/"synthetic_admin2.json"
        second.write_bytes(canonical(issue(db,ordinal=2,previous_sha=PIN)))
        sha2=hashfile(second)
        reject(lambda:advance(head,db,second,trusted_current_head_sha=None,
              trusted_candidate_sha=sha2,trusted_latest_ordinal=1),"independently trusted")
        reject(lambda:advance(head,db,second,trusted_current_head_sha=h1,
              trusted_candidate_sha="0"*64,trusted_latest_ordinal=1),"candidate")
        reject(lambda:advance(head,db,second,trusted_current_head_sha=h1,
              trusted_candidate_sha=sha2,trusted_latest_ordinal=0),"missing trusted")
        reject(lambda:advance(head,db,second,trusted_current_head_sha=h1,
              trusted_candidate_sha=sha2,trusted_latest_ordinal=1,inject_failure=True),"injected")
        assert hashfile(head)==h1  # fault before atomic replace changed NOTHING
        current=advance(head,db,second,trusted_current_head_sha=h1,
                        trusted_candidate_sha=sha2,trusted_latest_ordinal=1)
        h2=current["candidate_new_head_sha256"]
        assert read_trusted(head,h2)["ordinal"]==2
        assert not current["protected_external_head_publication"]
        reject(lambda:read_trusted(head,h1),"external trusted head")
        reject(lambda:advance(head,db,second,trusted_current_head_sha=h1,
              trusted_candidate_sha=sha2,trusted_latest_ordinal=1),"external trusted head")
        wrong=root/"wrong_predecessor.json"
        wrong.write_bytes(canonical(issue(db,ordinal=3,previous_sha=PIN)))
        reject(lambda:advance(head,db,wrong,trusted_current_head_sha=h2,
              trusted_candidate_sha=hashfile(wrong),trusted_latest_ordinal=2),"predecessor")
        third=root/"synthetic_admin3.json"
        third.write_bytes(canonical(issue(db,ordinal=3,previous_sha=sha2)))
        sha3=hashfile(third)
        reject(lambda:advance(head,db,third,trusted_current_head_sha=h2,
              trusted_candidate_sha=sha3,trusted_latest_ordinal=1),"stale expected head ordinal")
        current3=advance(head,db,third,trusted_current_head_sha=h2,
                         trusted_candidate_sha=sha3,trusted_latest_ordinal=2)
        h3=current3["candidate_new_head_sha256"]
        assert read_trusted(head,h3)["ordinal"]==3
        # A coordinated replacement of HEAD and head contents cannot hide
        # from an *unchanged*, independently supplied h3 trusted anchor.
        head.write_bytes(canonical(dict(read_trusted(head,h3),ordinal=1)))
        reject(lambda:read_trusted(head,h3),"external trusted head")
    print("JPDC_GOOGLE2011_REAL_GENESIS_SYNTHETIC_CAS_STALE_RACE_CRASH_NEGATIVES_PASS")

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--db",required=True)
    p.add_argument("--checkpoint",required=True)
    a=p.parse_args()
    run(Path(a.db),Path(a.checkpoint))
