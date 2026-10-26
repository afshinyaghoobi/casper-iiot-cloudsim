from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
old="        PRED_GREEDY(false,false,false,false),"
assert s.count(old)==1
s=s.replace(old,old+"\n        POWER_OF_TWO_PREDICTED(false,false,false,false),")
old="            if(!policy.cp){\n                j=argMin(pred,eligible);\n            }else{"
new="""            if(!policy.cp){
                if(policy==Policy.POWER_OF_TWO_PREDICTED){
                    // Power-of-two candidate sampling adapted for heterogenous online
                    // dispatch: compare predicted network+queue+service latency.
                    // Deterministic per (scientific seed, task index), not runtime timing.
                    final java.util.SplittableRandom draw=new java.util.SplittableRandom(
                        seed ^ (0x9E3779B97F4A7C15L*(t.index()+1L)));
                    final int first=draw.nextInt(NODES);
                    int second=draw.nextInt(NODES-1);
                    if(second>=first) second++;
                    if(eligible.test(first) && eligible.test(second))
                        j=pred[first]<=pred[second]?first:second;
                    else if(eligible.test(first))j=first;
                    else if(eligible.test(second))j=second;
                    else j=argMin(pred,eligible);
                }else j=argMin(pred,eligible);
            }else{"""
assert s.count(old)==1
s=s.replace(old,new)
p.write_text(s)
print("POWER_TWO_PREDICTED_PATCH_PASS")
