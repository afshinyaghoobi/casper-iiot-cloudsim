#!/usr/bin/env python3
"""Two real POSIX subprocesses racing on ONE original-source local checkpoint HEAD.

All successors are administrative synthetic checkpoint transitions reusing
ONE previously spent genuine Google2011 part375 SQLite. No new source data.
"""
import argparse
import fcntl
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from google2011_checkpoint_head_cas import advance,bootstrap,read_trusted
from google2011_sqlite_detached_checkpoint import canonical,hashfile,issue

PIN="e8b134abc3f1f4e656d830ee5906548124daddd4ecbecb1cdcfe24c0bf8a83f5"
DB_SHA="ab4851f5fd43f01bbd212a31789b9d88237cfec81db074f921d570ea3d44f5dc"
TRIALS=3
WAIT_SECONDS=12


def child_main(a):
    if a.child_mode=="lock-holder":
        with open(str(a.head)+".lock","a+b") as f:
            fcntl.flock(f.fileno(),fcntl.LOCK_EX)
            Path(a.ready).write_text(str(os.getpid()))
            while True:time.sleep(0.05)
    if a.child_mode!="writer":raise ValueError("bad child")
    # READY marker precedes gate release for each actual separate OS PID.
    Path(a.ready).write_text(json.dumps(dict(pid=os.getpid(),start_monotonic=time.monotonic()))+"\n")
    deadline=time.monotonic()+WAIT_SECONDS
    while not Path(a.gate).exists():
        if time.monotonic()>deadline:raise TimeoutError("real process gate timeout")
        time.sleep(0.005)
    try:
        value=advance(a.head,a.db,a.candidate,trusted_current_head_sha=a.head_pin,
                      trusted_candidate_sha=a.candidate_pin,trusted_latest_ordinal=1)
        output=dict(outcome="SUCCESS",pid=os.getpid(),head_sha=value["candidate_new_head_sha256"])
        rc=0
    except ValueError as exc:
        output=dict(outcome="DENIED",pid=os.getpid(),reason=str(exc))
        rc=17
    Path(a.result).write_text(json.dumps(output,sort_keys=True)+"\n")
    return rc


def wait_ready(paths,children):
    until=time.monotonic()+WAIT_SECONDS
    while time.monotonic()<until:
        if all(p.exists() for p in paths):return
        for c in children:
            if c.poll() is not None:raise AssertionError("child died before contention gate")
        time.sleep(0.01)
    raise TimeoutError("concurrent writer readiness timeout")


def run(db_source,cp_source,out_dir):
    if hashfile(db_source)!=DB_SHA or hashfile(cp_source)!=PIN:
        raise ValueError("archived original source is not the fixed prereg genuine data")
    out=Path(out_dir);out.mkdir(parents=True,exist_ok=True)
    observations=[]
    for trial in range(TRIALS):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)
            db=folder/"original.sqlite";cp=folder/"genuine.json";head=folder/"head.json"
            shutil.copyfile(db_source,db);shutil.copyfile(cp_source,cp)
            h1=bootstrap(head,db,cp,trusted_genesis_sha=PIN)["head_sha256"]
            candidate=folder/"synthetic_successor2.json"
            candidate.write_bytes(canonical(issue(db,ordinal=2,previous_sha=PIN)))
            csha=hashfile(candidate)
            gate=folder/"release"
            procs=[];readies=[];result_paths=[]
            for i in range(2):
                ready=folder/f"ready{i}.json";result=folder/f"result{i}.json"
                cmd=[sys.executable,__file__,"--child-mode","writer",
                     "--head",str(head),"--db",str(db),"--candidate",str(candidate),
                     "--head-pin",h1,"--candidate-pin",csha,
                     "--ready",str(ready),"--result",str(result),"--gate",str(gate)]
                procs.append(subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True))
                readies.append(ready);result_paths.append(result)
            try:
                wait_ready(readies,procs)
                launch=[json.loads(p.read_text()) for p in readies]
                if launch[0]["pid"]==launch[1]["pid"]:
                    raise AssertionError("not two genuine separate OS processes")
                # Both processes are running simultaneously waiting for SAME gate.
                if not all(c.poll() is None for c in procs):raise AssertionError("not concurrent")
                gate.write_text("release\n")
                statuses=[]
                for p in procs:
                    try:_,stderr=p.communicate(timeout=WAIT_SECONDS)
                    except subprocess.TimeoutExpired:
                        p.kill();p.communicate()
                        raise AssertionError("concurrent CAS writer stalled")
                    statuses.append(dict(exit_code=p.returncode,stderr=stderr[-1500:]))
                results=[json.loads(p.read_text()) for p in result_paths]
                counts={k:sum(x["outcome"]==k for x in results) for k in ("SUCCESS","DENIED")}
                if counts!={"SUCCESS":1,"DENIED":1}:
                    raise AssertionError("CAS failed unique-winner property")
                if sorted(c.returncode for c in procs)!=[0,17]:
                    raise AssertionError("unexpected OS subprocess exit status")
                if not any("local HEAD mismatch external trusted head" in x.get("reason","") for x in results):
                    raise AssertionError("losing writer did not detect stale head")
                winning=next(x for x in results if x["outcome"]=="SUCCESS")
                if hashfile(head)!=winning["head_sha"] or read_trusted(head,winning["head_sha"])["ordinal"]!=2:
                    raise AssertionError("final HEAD not exactly one promoted successor")
                observations.append(dict(trial=trial+1,unique_writer_pids=True,
                    simultaneous_running_at_release=True,winners=1,stale_denials=1,
                    final_ordinal=2,worker_exit_codes=sorted(c.returncode for c in procs),
                    candidate_external_head_published=False))
            finally:
                for proc in procs:
                    if proc.poll() is None:proc.kill();proc.communicate()
    # A real OS lock-owner SIGKILL test: kernel must release flock after death.
    with tempfile.TemporaryDirectory() as temp:
        folder=Path(temp)
        db=folder/"original.sqlite";cp=folder/"genuine.json";head=folder/"head.json"
        shutil.copyfile(db_source,db);shutil.copyfile(cp_source,cp)
        h1=bootstrap(head,db,cp,trusted_genesis_sha=PIN)["head_sha256"]
        lock_ready=folder/"lock_ready"
        lock_owner=subprocess.Popen(
            [sys.executable,__file__,"--child-mode","lock-holder",
             "--head",str(head),"--ready",str(lock_ready)],
            stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
        try:
            wait_ready([lock_ready],[lock_owner])
            original_head_sha=hashfile(head)
            os.kill(lock_owner.pid,signal.SIGKILL)
            lock_owner.communicate(timeout=WAIT_SECONDS)
            if lock_owner.returncode!=-signal.SIGKILL:raise AssertionError("lock owner was not SIGKILLed")
            if hashfile(head)!=original_head_sha:raise AssertionError("killed lock-holder mutated HEAD")
            candidate=folder/"synthetic_admin2.json"
            candidate.write_bytes(canonical(issue(db,ordinal=2,previous_sha=PIN)))
            promoted=advance(head,db,candidate,trusted_current_head_sha=h1,
                trusted_candidate_sha=hashfile(candidate),trusted_latest_ordinal=1)
            if read_trusted(head,promoted["candidate_new_head_sha256"])["ordinal"]!=2:
                raise AssertionError("OS lock not released on SIGKILL")
        finally:
            if lock_owner.poll() is None:lock_owner.kill();lock_owner.communicate()
    audit=dict(status="PASS",classification="POSIX_ACTUAL_2_PROCESS_LOCAL_HEAD_CAS",
        original_source_genuine_one_previously_spent_part375=True,
        source_original_event_rows_from_previous_artifact=130812,
        independent_google_source_files_new=0,
        actual_race_trials=TRIALS,workers_per_trial=2,
        total_unique_winners=TRIALS,total_stale_writer_denials=TRIALS,
        actual_sigkill_held_lock_and_reacquired=True,
        local_file_system_only=True,distributed_multi_runner_CAS_verified=False,
        protected_git_head_publication_verified=False,
        simultaneous_source_acquisition=False,
        authentic_external_ledger=False,
        all_500_source_files_scanned=False,
        stage65_safety="FAIL",java_python_queue_parity="FAIL",
        trials=observations)
    (out/"audit.json").write_bytes(canonical(audit))
    (out/"audit_repeat_contract.json").write_bytes(canonical(audit))
    print("JPDC_REAL_TWO_PROCESS_GOOGLE_OLD_SOURCE_LOCAL_CAS_PASS",json.dumps({
        k:v for k,v in audit.items() if k!="trials"},sort_keys=True))


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--db")
    p.add_argument("--checkpoint")
    p.add_argument("--out")
    p.add_argument("--child-mode")
    p.add_argument("--head")
    p.add_argument("--candidate")
    p.add_argument("--head-pin")
    p.add_argument("--candidate-pin")
    p.add_argument("--ready")
    p.add_argument("--result")
    p.add_argument("--gate")
    a=p.parse_args()
    if a.child_mode:sys.exit(child_main(a))
    if not all((a.db,a.checkpoint,a.out)):p.error("parent requires --db --checkpoint --out")
    run(Path(a.db),Path(a.checkpoint),Path(a.out))


if __name__=="__main__":main()
