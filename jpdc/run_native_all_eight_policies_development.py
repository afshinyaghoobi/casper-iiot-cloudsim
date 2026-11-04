#!/usr/bin/env python3
"""Frozen eight-policy development matrix. Not a confirmatory holdout."""
import argparse,json,math
from pathlib import Path
from independent_physical_calibration_stage3 import calibrate
from independent_casper_deployment_stage4 import simulate,POLICIES,POLICY_FLAGS

SEED=50
SCENARIOS=("S2_HIDDEN_COMPUTE_40LOSS","S3_HIDDEN_NETWORK_50LOSS")
N=12000
# Previously published Stage4 native development results, frozen before eight-mode addition.
PREVIOUS={
 ("S2_HIDDEN_COMPUTE_40LOSS","PRED_GREEDY"):19,
 ("S2_HIDDEN_COMPUTE_40LOSS","CASPER_HEALTH_STATIC"):18,
 ("S2_HIDDEN_COMPUTE_40LOSS","CASPER_FULL"):18,
 ("S3_HIDDEN_NETWORK_50LOSS","PRED_GREEDY"):25,
 ("S3_HIDDEN_NETWORK_50LOSS","CASPER_HEALTH_STATIC"):25,
 ("S3_HIDDEN_NETWORK_50LOSS","CASPER_FULL"):25,
}
def execute():
    cal=calibrate(SEED,80000,include_reference=True)
    assert len(cal['reference_scores'])==cal['mission_score_count']
    rows=[]
    for scenario in SCENARIOS:
        for policy in POLICIES:
            r=simulate(SEED,scenario,policy,cal,N)
            flags=POLICY_FLAGS[policy]
            assert r['policy_flags']==flags and r['status']=='PASS'
            assert r['deployment_tasks']==N and sum(r['node_dispatch_counts'])==N
            assert sum(r['rank_counts'].values())==r['mission_tasks']
            assert r['mission_tasks']>=250 and r['post_mission_tasks']>0
            assert 0<=r['mission_deadline_misses']<=r['mission_tasks']
            if flags['adaptive']:
                assert r['adaptive_feedback_events']==r['mission_tasks']
            else:
                assert r['adaptive_feedback_events']==r['eta_gt_one_dispatches']==0
            if not flags['health']:
                assert r['health_alarm_transitions']==r['health_alarmed_nodes']==r['probes']==0
            if not flags['cp']:
                assert r['post_cert_rate']==0 and r['post_false_cert_rate'] is None
                assert r['post_abstention_rate'] is None and r['post_family_covered_rate'] is None
            else:
                assert r['post_cert_rate'] is not None
                assert r['post_false_cert_rate']<=r['post_cert_rate']+1e-12
            key=(scenario,policy)
            if key in PREVIOUS:
                assert r['mission_deadline_misses']==PREVIOUS[key],(
                    "previous three-policy development regression",key,r['mission_deadline_misses'],PREVIOUS[key])
            rows.append(r)
            print('EIGHT_MODE_RESULT',scenario,policy,'MISSION_misses',r['mission_deadline_misses'],
                  'ranks',r['rank_counts'],'alarm_transitions',r['health_alarm_transitions'],
                  'eta_gt1',r['eta_gt_one_dispatches'])
    assert len(rows)==16 and sum(x['deployment_tasks'] for x in rows)==192000
    return {
      'status':'PASS','scope':'known development seed50, NONconfirmatory, no p-values',
      'independent_physical_queue':'strict_FCFS_not_CloudSimPlus_SpaceShared_equivalent',
      'calibration':{k:v for k,v in cal.items() if k!='reference_scores'},
      'total_task_policy_observations':192000,
      'policies':list(POLICIES),'scenarios':list(SCENARIOS),'rows':rows,
    }
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args()
    result=execute();out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+'\n')
    print('JPDC_NATIVE_ALL_EIGHT_DEVELOPMENT_MATRIX_PASS')
