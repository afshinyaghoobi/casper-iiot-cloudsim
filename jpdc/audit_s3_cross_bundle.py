#!/usr/bin/env python3
"""Reproduce cross-bundle aggregate and paired checks using the two archived ZIPs.
Usage: python jpdc/audit_s3_cross_bundle.py controlled_mask.zip mask_eta_factorial.zip
No third-party packages. Does not independently rerun CloudSim.
"""
import csv,io,math,sys,zipfile

def rows(z,name):
    return list(csv.DictReader(io.StringIO(z.read(name).decode())))
def eq(a,b):
    return math.isclose(float(a),float(b),abs_tol=1e-7,rel_tol=0)
def check(condition,msg):
    if not condition: raise AssertionError(msg)
    print("PASS",msg)
def sign(values):
    pos=sum(v>1e-10 for v in values);neg=sum(v< -1e-10 for v in values)
    n=pos+neg
    p=min(1,2*sum(math.comb(n,k) for k in range(min(pos,neg)+1))/2**n) if n else 1.
    return p,pos,neg,len(values)-n

def main(mpath,fpath):
    with zipfile.ZipFile(mpath) as m,zipfile.ZipFile(fpath) as f:
        masks=rows(m,"per_seed_conditions.csv")
        arms=rows(f,"all_conditions.csv")
        summary=rows(m,"four_seed_summary.csv")
        aggregate=rows(f,"four_seed_aggregate.csv")
        interactions=rows(f,"seed_interactions.csv")
        tests=rows(f,"interaction_tests.csv")
        deltas=rows(m,"paired_high_minus_low.csv")
        seeds=(40,41,42,43)
        check(len(masks)==12 and {int(r["seed_index"]) for r in masks}==set(seeds),"physical mask cohort")
        check(len(arms)==16 and {int(r["seed"]) for r in arms}==set(seeds),"factorial cohort")
        mm={(int(r["seed_index"]),r["condition"]):r for r in masks}
        ff={(int(r["seed"]),r["mask"],r["mode"]):r for r in arms}
        metrics=("late_far","late_air","late_dvr","late_fwc","late_eta",
                 "post_far","post_air","post_dvr","post_fwc")
        for s in seeds:
            for mask in ("low","high"):
                for metric in metrics:
                    check(eq(mm[s,mask][metric],ff[s,mask,"adaptive"][metric]),
                          f"cross-archive {s}/{mask}/{metric}")
            stored=next(r for r in interactions if int(r["seed"])==s)
            for metric in ("late_far","late_air","late_dvr","late_fwc"):
                low=float(ff[s,"low","adaptive"][metric])-float(ff[s,"low","clamped"][metric])
                high=float(ff[s,"high","adaptive"][metric])-float(ff[s,"high","clamped"][metric])
                check(eq(high-low,stored["interaction_"+metric]),f"factorial interaction {s}/{metric}")
        for r in aggregate:
            group=[ff[s,r["mask"],r["mode"]] for s in seeds]
            for key in ("far","air","dvr","fwc"):
                count=sum(round(float(x["late_"+key])*250) for x in group)
                check(count==int(r["late_"+key+"_count"]) and
                      eq(count/1000,r["late_"+key+"_rate"]),
                      f"factorial pooled count {r['mask']}/{r['mode']}/{key}")
        for r in tests:
            vals=[float(x["interaction_"+r["metric"]]) for x in interactions]
            p,positive,negative,ties=sign(vals)
            check(eq(sum(vals)/4,r["interaction_mean"]) and
                  eq(p,r["exact_two_sided_sign_p_exploratory"]) and
                  (positive,negative,ties)==(int(r["positive"]),int(r["negative"]),int(r["ties"])),
                  "seed-level exact sign "+r["metric"])
            loo=[sum(vals[:i]+vals[i+1:])/3 for i in range(4)]
            print("SENSITIVITY",r["metric"],"leave-one-out mean range",min(loo),max(loo))
        for r in deltas:
            s=int(r["seed_index"])
            for metric in ("late_far","late_air","late_dvr","late_fwc",
                           "post_far","post_air","post_dvr","post_fwc"):
                difference=float(mm[s,"high"][metric])-float(mm[s,"low"][metric])
                check(eq(difference,r["delta_"+metric]),f"physical contrast {s}/{metric}")
        for r in summary:
            metric=r["metric"]
            low=sum(float(mm[s,"low"][metric]) for s in seeds)/4
            high=sum(float(mm[s,"high"][metric]) for s in seeds)/4
            check(eq(low,r["low_mean"]) and eq(high,r["high_mean"])
                  and eq(high-low,r["mean_high_minus_low"]),"physical summary "+metric)
        print("PASS all derived-archive consistency checks; n=4 independent seeds")
if __name__=="__main__":
    if len(sys.argv)!=3: sys.exit(__doc__)
    main(sys.argv[1],sys.argv[2])
