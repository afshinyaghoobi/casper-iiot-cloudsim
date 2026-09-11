#!/usr/bin/env python3
from pathlib import Path
import argparse, json
import pandas as pd

FOCUS_SCENARIOS=['S2_HIDDEN_COMPUTE_40LOSS','S3_HIDDEN_NETWORK_50LOSS','S4_COMPOUND']
FOCUS_POLICIES=['RANKED_CP_STATIC','CASPER_ADAPT_NO_HEALTH','CASPER_HEALTH_STATIC','CASPER_FULL']

def b(x):
    if x.dtype==bool: return x
    return x.astype(str).str.lower().eq('true')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
    files=sorted(Path(a.input).rglob('e43_trace_seed_*.csv'))
    if len(files)!=30: raise SystemExit(f'EXPECTED 30 trace CSVs, found {len(files)}')
    df=pd.concat([pd.read_csv(f) for f in files],ignore_index=True)
    if df.seed.nunique()!=30: raise SystemExit('EXPECTED 30 unique seeds')
    if not set(df.scenario).issubset(set(FOCUS_SCENARIOS)): raise SystemExit('scenario mismatch')
    if not set(df.policy).issubset(set(FOCUS_POLICIES)): raise SystemExit('policy mismatch')
    out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    df.to_csv(out/'E43_TRACE_ALL.csv',index=False)

    rows=[]
    for (sc,po),g in df.groupby(['scenario','policy']):
        mission=g[g.criticality.eq('MISSION')]
        probe=g[b(g.probe)]
        fam_aff=mission.candidate_family_affected_mask.fillna('').astype(str).map(lambda s:'1' in s.split('|'))
        health_changed=b(mission.health_changed_dispatch) if len(mission) else pd.Series(dtype=bool)
        eta_changed=b(mission.eta_changed_certification) if len(mission) else pd.Series(dtype=bool)
        prealarm_probe=(b(probe.selected_node_affected)&~b(probe.selected_node_alarm_at_dispatch)) if len(probe) else pd.Series(dtype=bool)
        trig=g[b(g.health_alarm_trigger)]
        e17=g[b(g.e17_alarm_trigger)]
        rows.append({
            'scenario':sc,'policy':po,'trace_rows':len(g),'mission_rows':len(mission),'probe_rows':len(probe),
            'mission_family_contains_affected_fraction':float(fam_aff.mean()) if len(fam_aff) else None,
            'mission_dispatch_changed_by_health_fraction':float(health_changed.mean()) if len(health_changed) else None,
            'certification_changed_by_eta_fraction':float(eta_changed.mean()) if len(eta_changed) else None,
            'probes_to_affected_before_alarm_fraction':float(prealarm_probe.mean()) if len(prealarm_probe) else None,
            'health_alarm_trigger_count':int(len(trig)),'e17_trigger_count':int(len(e17)),
            'e17_trigger_seed_count':int(e17.seed.nunique()) if len(e17) else 0,
        })
    summary=pd.DataFrame(rows)
    summary.to_csv(out/'E43_TRACE_SUMMARY.csv',index=False)

    alarm=df[b(df.health_alarm_trigger)].copy()
    if len(alarm):
        alarm['ms_from_change']=alarm.arrival_ms-alarm.change_arrival_ms
        first=alarm.sort_values('task_index').groupby(['seed','scenario','policy','selected_node'],as_index=False).first()
    else: first=alarm
    first.to_csv(out/'E43_FIRST_ALARMS.csv',index=False)

    e17=df[b(df.e17_alarm_trigger)].sort_values('task_index')
    if len(e17): e17=e17.groupby(['seed','scenario','policy'],as_index=False).first()
    e17.to_csv(out/'E43_E17_TRIGGERS.csv',index=False)

    findings=[]
    for _,r in summary.iterrows():
        findings.append({k:(None if pd.isna(v) else (v.item() if hasattr(v,'item') else v)) for k,v in r.items()})
    decision={
        'stage':'E4.3_TRACE_ONLY','scientific_logic_changed':False,'seeds':30,
        'focus_scenarios':FOCUS_SCENARIOS,'focus_policies':FOCUS_POLICIES,
        'trace_rows':int(len(df)),'summary':findings,
        'interpretation_guardrail':'diagnostic only; no retuning or architecture change authorized by this analysis'
    }
    (out/'E43_TRACE_DIAGNOSTIC.json').write_text(json.dumps(decision,indent=2))
    md=['# E4.3 Trace-Only Diagnostic','',f"Trace rows: {len(df):,}",'',summary.to_markdown(index=False),'',
        'This phase is observational only. E4.2 scientific decisions, thresholds, seeds, workload, gates, and policies were not changed.']
    (out/'E43_TRACE_REPORT.md').write_text('\n'.join(md))
    print(json.dumps(decision,indent=2)); print('E43_TRACE_ANALYSIS PASS')
if __name__=='__main__': main()
