#!/usr/bin/env python3
"""Locked E4.2 publication aggregation/statistics. No tuning or model selection."""
from pathlib import Path
import argparse, json, math
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon, friedmanchisquare

SCENARIOS = [
    'S0_STATIONARY','S1_LAMBDA_X2','S2_HIDDEN_COMPUTE_40LOSS',
    'S3_HIDDEN_NETWORK_50LOSS','S4_COMPOUND'
]
POLICIES = [
    'CLOUD_ONLY','EDGE_FIRST','PRED_GREEDY','GLOBAL_CP','RANKED_CP_STATIC',
    'CASPER_ADAPT_NO_HEALTH','CASPER_HEALTH_STATIC','CASPER_FULL'
]
ASSURANCE = ['GLOBAL_CP','RANKED_CP_STATIC','CASPER_ADAPT_NO_HEALTH','CASPER_HEALTH_STATIC','CASPER_FULL']
METRICS = [
    'post_fwc','shock_fwc','late_fwc','post_air','late_air','post_far','late_far',
    'post_dvr','late_dvr','p99_post_latency_ms','p99_late_latency_ms','late_eta',
    'probe_rate','probe_dvr','compute_alarm_coverage','healthy_false_alarm_nodes',
    'degraded_nodes_alarmed','mean_mapper_us','max_service_parity_error_ms'
]
BOOT_B = 20_000
BOOT_SEED = 4_202_202_699


def bootstrap_mean_ci(x, rng, b=BOOT_B):
    x=np.asarray(x,float); x=x[np.isfinite(x)]
    if len(x)==0: return (np.nan,np.nan,np.nan)
    idx=rng.integers(0,len(x),size=(b,len(x)))
    means=x[idx].mean(axis=1)
    return float(x.mean()), float(np.quantile(means,.025)), float(np.quantile(means,.975))


def paired_bootstrap_diff(x,y,rng,b=BOOT_B):
    x=np.asarray(x,float); y=np.asarray(y,float)
    m=np.isfinite(x)&np.isfinite(y); x=x[m]; y=y[m]
    if len(x)==0:return (np.nan,np.nan,np.nan)
    d=x-y
    idx=rng.integers(0,len(d),size=(b,len(d)))
    bm=d[idx].mean(axis=1)
    return float(d.mean()),float(np.quantile(bm,.025)),float(np.quantile(bm,.975))


def cliffs_delta_paired_supplement(x,y):
    # Supplementary dominance effect on paired-run marginals, reported as Cliff's delta.
    x=np.asarray(x,float); y=np.asarray(y,float)
    x=x[np.isfinite(x)]; y=y[np.isfinite(y)]
    if len(x)==0 or len(y)==0:return np.nan
    gt=sum(a>b for a in x for b in y); lt=sum(a<b for a in x for b in y)
    return (gt-lt)/(len(x)*len(y))


def safe_wilcoxon(x,y):
    x=np.asarray(x,float); y=np.asarray(y,float)
    m=np.isfinite(x)&np.isfinite(y); x=x[m]; y=y[m]
    if len(x)==0:return np.nan
    d=x-y
    if np.allclose(d,0):return 1.0
    try:return float(wilcoxon(x,y,alternative='two-sided',zero_method='wilcox').pvalue)
    except ValueError:return 1.0


def holm_adjust(pvals):
    p=np.asarray(pvals,float); out=np.full(len(p),np.nan)
    valid=np.flatnonzero(np.isfinite(p))
    if len(valid)==0:return out
    order=valid[np.argsort(p[valid])]
    m=len(order); running=0.0
    for rank,idx in enumerate(order):
        adj=min(1.0,(m-rank)*p[idx]); running=max(running,adj); out[idx]=running
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',required=True)
    ap.add_argument('--out',required=True)
    args=ap.parse_args()
    indir=Path(args.input); out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    files=sorted(indir.rglob('e42_seed_*.csv'))
    if len(files)!=30: raise SystemExit(f'EXPECTED 30 seed CSVs, found {len(files)}')
    df=pd.concat([pd.read_csv(f) for f in files],ignore_index=True)
    df.to_csv(out/'e42_all_runs.csv',index=False)

    if len(df)!=1200: raise SystemExit(f'EXPECTED 1200 rows, got {len(df)}')
    if df.seed.nunique()!=30: raise SystemExit('EXPECTED 30 unique seeds')
    if set(df.scenario)!=set(SCENARIOS): raise SystemExit('scenario set mismatch')
    if set(df.policy)!=set(POLICIES): raise SystemExit('policy set mismatch')
    counts=df.groupby(['scenario','policy']).size()
    if not (counts==30).all(): raise SystemExit('each scenario-policy must have 30 runs')
    if not (df.tasks==30000).all(): raise SystemExit('task-count mismatch')
    if not np.allclose(df.cloudsim_completion,1.0): raise SystemExit('CloudSim completion gate failed')
    if df.max_service_parity_error_ms.max()>2.0: raise SystemExit('CloudSim selected-service parity >2ms')

    rng=np.random.default_rng(BOOT_SEED)
    summary_rows=[]; ci_rows=[]
    for (sc,po),g in df.groupby(['scenario','policy'],sort=False):
        row={'scenario':sc,'policy':po,'n':len(g)}
        for metric in METRICS:
            mean,lo,hi=bootstrap_mean_ci(g[metric],rng)
            row[metric]=mean
            ci_rows.append({'scenario':sc,'policy':po,'metric':metric,'mean':mean,'ci95_low':lo,'ci95_high':hi})
        summary_rows.append(row)
    summary=pd.DataFrame(summary_rows)
    summary.to_csv(out/'e42_summary.csv',index=False)
    pd.DataFrame(ci_rows).to_csv(out/'e42_bootstrap_ci.csv',index=False)

    # FULL-vs-baseline paired tests. Positive differences mean FULL minus baseline.
    test_rows=[]
    compare_metrics=['late_dvr','p99_late_latency_ms','late_fwc','late_air']
    for sc in SCENARIOS:
        z=df[df.scenario==sc]
        full=z[z.policy=='CASPER_FULL'].set_index('seed')
        for metric in compare_metrics:
            group_indices=[]
            for base in POLICIES[:-1]:
                b=z[z.policy==base].set_index('seed')
                common=full.index.intersection(b.index)
                x=full.loc[common,metric].to_numpy(float); y=b.loc[common,metric].to_numpy(float)
                if not (np.isfinite(x)&np.isfinite(y)).any(): continue
                md,lo,hi=paired_bootstrap_diff(x,y,rng)
                p=safe_wilcoxon(x,y)
                delta=cliffs_delta_paired_supplement(x,y)
                test_rows.append({'scenario':sc,'metric':metric,'baseline':base,'n_pairs':len(common),
                                  'mean_diff_full_minus_baseline':md,'ci95_low':lo,'ci95_high':hi,
                                  'wilcoxon_p':p,'cliffs_delta':delta})
                group_indices.append(len(test_rows)-1)
            if group_indices:
                adj=holm_adjust([test_rows[i]['wilcoxon_p'] for i in group_indices])
                for i,a in zip(group_indices,adj):test_rows[i]['holm_p']=a
    tests=pd.DataFrame(test_rows)
    tests.to_csv(out/'e42_paired_tests.csv',index=False)

    # Friedman omnibus on Mission late DVR across all policies.
    fr=[]
    for sc in SCENARIOS:
        p=df[df.scenario==sc].pivot(index='seed',columns='policy',values='late_dvr').reindex(columns=POLICIES)
        if p.isna().any().any():
            stat=pval=np.nan
        else:
            try: stat,pval=friedmanchisquare(*[p[c].to_numpy() for c in POLICIES])
            except ValueError: stat,pval=0.0,1.0
        fr.append({'scenario':sc,'metric':'late_dvr','friedman_chi2':stat,'p':pval,'n':len(p),'k':len(POLICIES)})
    pd.DataFrame(fr).to_csv(out/'e42_friedman.csv',index=False)

    # Prelocked CASPER_FULL gates.
    ss=summary.set_index(['scenario','policy'])
    gate_rows=[]
    for sc in SCENARIOS:
        r=ss.loc[(sc,'CASPER_FULL')]
        gate_rows.append({'scenario':sc,
            'late_fwc_at_least_99':bool(r.late_fwc>=.99),
            'late_air_under_20':bool(r.late_air<.20),
            'probe_rate_at_most_1pct':bool(r.probe_rate<=.01+1e-12),
            'healthy_false_alarm_nodes_across_30_at_most_6':bool(df[(df.scenario==sc)&(df.policy=='CASPER_FULL')].healthy_false_alarm_nodes.sum()<=6),
            'compute_alarm_coverage_at_least_90':bool(r.compute_alarm_coverage>=.90) if sc in ['S2_HIDDEN_COMPUTE_40LOSS','S4_COMPOUND'] else True,
            'max_service_parity_error_at_most_2ms':bool(df[(df.scenario==sc)&(df.policy=='CASPER_FULL')].max_service_parity_error_ms.max()<=2.0),
            'all_cloudsim_completions':bool(np.allclose(df[(df.scenario==sc)&(df.policy=='CASPER_FULL')].cloudsim_completion,1.0))
        })
    gates=pd.DataFrame(gate_rows)
    gates.to_csv(out/'e42_full_gates.csv',index=False)
    gate_cols=[c for c in gates if c!='scenario']
    all_pass=bool(gates[gate_cols].to_numpy(bool).all())

    decision={
        'stage':'E4.2','publication_campaign_gate':'PASS' if all_pass else 'FAIL',
        'all_prelocked_full_casper_gates_pass':all_pass,
        'results_are_publication_scale_cloudsim_plus_evidence':True,
        'cloudsim_plus_dependency':'org.cloudsimplus:cloudsimplus:8.5.7',
        'seeds':30,'scenario_policy_rows':1200,
        'no_result_driven_retuning':True,
        'failed_gates':[{'scenario':row.scenario,'gate':c} for _,row in gates.iterrows() for c in gate_cols if not bool(row[c])]
    }
    (out/'E42_DECISION.json').write_text(json.dumps(decision,indent=2))

    full=summary[summary.policy=='CASPER_FULL'][['scenario','late_fwc','late_air','late_far','late_dvr','p99_late_latency_ms','probe_rate','compute_alarm_coverage','mean_mapper_us']]
    report=['# E4.2 Publication-Scale CloudSim Plus Campaign','',
            f"**Prelocked FULL gate:** {decision['publication_campaign_gate']}",'',
            '30 independent seeds; five scenarios; eight frozen policies/baselines; 1,200 scenario-policy runs.','',
            '## CASPER_FULL summary','',full.to_markdown(index=False),'',
            '## Prelocked gates','',gates.to_markdown(index=False),'',
            '## Statistical analysis','',
            'Paired 95% bootstrap intervals use 20,000 resamples at the seed level. Two-sided paired Wilcoxon tests are Holm-corrected within scenario/metric families. Cliff\'s delta is supplementary. Friedman tests provide the prelocked omnibus comparison for Mission late deadline-violation rate.','',
            'No parameter is retuned from these results. Counterfactual candidate outcomes are audit-only and never feed the scheduler or calibrator.']
    (out/'E42_REPORT.md').write_text('\n'.join(report))
    print(json.dumps(decision,indent=2))
    print('E42_AGGREGATION PASS rows=1200 seeds=30')

if __name__=='__main__': main()
