#!/usr/bin/env python3
"""E4.3 post-hoc diagnosis of frozen E4.2 results. No retuning."""
from pathlib import Path
import argparse, json
import numpy as np
import pandas as pd

SCENARIOS = [
    'S0_STATIONARY','S1_LAMBDA_X2','S2_HIDDEN_COMPUTE_40LOSS',
    'S3_HIDDEN_NETWORK_50LOSS','S4_COMPOUND'
]
COMPARE_POLICIES = [
    'RANKED_CP_STATIC','CASPER_ADAPT_NO_HEALTH','CASPER_HEALTH_STATIC','CASPER_FULL'
]
OUTCOME_METRICS = [
    'post_fwc','shock_fwc','late_fwc','post_air','late_air','post_far','late_far',
    'post_dvr','late_dvr','p99_post_latency_ms','p99_late_latency_ms'
]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',required=True,help='Frozen E4.2 e42_all_runs.csv')
    ap.add_argument('--out',required=True)
    args=ap.parse_args()
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(args.input)

    if len(df)!=1200: raise SystemExit(f'Expected 1200 frozen E4.2 rows, got {len(df)}')
    if df.seed.nunique()!=30: raise SystemExit('Expected 30 E4.2 seeds')

    ranked=df[df.policy=='RANKED_CP_STATIC'].sort_values(['scenario','seed']).reset_index(drop=True)
    equiv=[]
    for policy in COMPARE_POLICIES[1:]:
        g=df[df.policy==policy].sort_values(['scenario','seed']).reset_index(drop=True)
        for metric in OUTCOME_METRICS:
            a=ranked[metric].to_numpy(float); b=g[metric].to_numpy(float)
            finite=np.isfinite(a)&np.isfinite(b)
            max_abs=float(np.max(np.abs(a[finite]-b[finite]))) if finite.any() else np.nan
            equiv.append({
                'reference_policy':'RANKED_CP_STATIC','policy':policy,'metric':metric,
                'allclose':bool(np.allclose(a,b,equal_nan=True)),'max_abs_diff':max_abs
            })
    equiv_df=pd.DataFrame(equiv)
    equiv_df.to_csv(out/'e43_policy_outcome_equivalence.csv',index=False)

    adaptive=df[df.policy.isin(['CASPER_ADAPT_NO_HEALTH','CASPER_FULL'])]
    eta=adaptive.groupby(['scenario','policy']).late_eta.agg(['count','mean','std','min','max']).reset_index()
    eta.to_csv(out/'e43_adaptive_eta.csv',index=False)

    full=df[df.policy=='CASPER_FULL'].copy()
    seed_rows=[]; corr_rows=[]
    for sc in SCENARIOS:
        g=full[full.scenario==sc]
        seed_rows.append({
            'scenario':sc,
            'seeds':len(g),
            'seeds_late_fwc_ge_0_99':int((g.late_fwc>=.99).sum()),
            'mean_late_fwc':float(g.late_fwc.mean()),
            'min_late_fwc':float(g.late_fwc.min()),
            'max_late_fwc':float(g.late_fwc.max()),
            'mean_late_dvr':float(g.late_dvr.mean()),
            'mean_probe_rate':float(g.probe_rate.mean())
        })
        if sc in ['S2_HIDDEN_COMPUTE_40LOSS','S4_COMPOUND']:
            corr_rows.append({
                'scenario':sc,
                'corr_alarm_coverage_vs_late_fwc':float(g.compute_alarm_coverage.corr(g.late_fwc)),
                'corr_alarm_coverage_vs_late_dvr':float(g.compute_alarm_coverage.corr(g.late_dvr)),
                'mean_compute_alarm_coverage':float(g.compute_alarm_coverage.mean())
            })
    seed_df=pd.DataFrame(seed_rows); seed_df.to_csv(out/'e43_seed_gate_frequency.csv',index=False)
    corr_df=pd.DataFrame(corr_rows); corr_df.to_csv(out/'e43_health_association.csv',index=False)

    all_equiv=bool(equiv_df.allclose.all())
    adaptive_eta_inert=bool(np.allclose(adaptive.late_eta.to_numpy(float),1.0))
    diagnosis={
        'stage':'E4.3',
        'source_stage':'E4.2',
        'source_rows':len(df),
        'source_seeds':int(df.seed.nunique()),
        'policy_outcome_equivalence_to_ranked_cp_static':all_equiv,
        'adaptive_late_eta_identically_one':adaptive_eta_inert,
        'mean_full_late_fwc':{r['scenario']:r['mean_late_fwc'] for r in seed_rows},
        'seed_counts_meeting_late_fwc_0_99':{r['scenario']:r['seeds_late_fwc_ge_0_99'] for r in seed_rows},
        'health_association':corr_rows,
        'interpretation':[
            'The health/adaptation variants are outcome-equivalent to RANKED_CP_STATIC at frozen E4.2 run-level metrics.' if all_equiv else 'Outcome equivalence is not exact.',
            'E1.7 adaptation is inert at the reported late-window eta metric because eta remains exactly 1.0.' if adaptive_eta_inert else 'E1.7 eta departs from 1.0 in at least one run.',
            'Aggregate run-level evidence is insufficient to prove the event-level mechanism; trace-only E4.3 instrumentation is required before any architecture change.'
        ],
        'retuning_performed':False
    }
    (out/'E43_DIAGNOSTIC.json').write_text(json.dumps(diagnosis,indent=2))

    report=[
        '# E4.3 Post-hoc Diagnostic Report','',
        'This analysis reads frozen E4.2 publication artifacts only. No E4.2 parameter, threshold, workload, seed, policy, or gate is changed.','',
        f'**Policy outcome equivalence to RANKED_CP_STATIC:** {all_equiv}','',
        f'**Adaptive late eta identically 1.0:** {adaptive_eta_inert}','',
        '## CASPER_FULL seed-level gate frequency','',seed_df.to_markdown(index=False),'',
        '## Health association in compute-degradation scenarios','',corr_df.to_markdown(index=False),'',
        '## Diagnostic conclusion','',
        'The aggregate evidence indicates that the adaptive and health layers did not alter the reported E4.2 outcome metrics relative to RANKED_CP_STATIC. '
        'In addition, the adaptive eta stayed at 1.0. In S2/S4, higher final alarm coverage is not associated with better late FWC in these 30 runs; the observed correlations are negative. '
        'These facts diagnose control-layer ineffectiveness at the aggregate level, but they do not by themselves identify whether the cause is alarm timing, probe targeting, candidate-set composition, sticky exclusion timing, or adaptation-detector non-triggering. '
        'The next permitted step is trace-only instrumentation under E4.3 with scientific decision logic unchanged.'
    ]
    (out/'E43_DIAGNOSTIC_REPORT.md').write_text('\n'.join(report))
    print(json.dumps(diagnosis,indent=2))
    print('E43_DIAGNOSIS COMPLETE; no retuning performed')

if __name__=='__main__': main()
