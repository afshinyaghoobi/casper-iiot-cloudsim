#!/usr/bin/env python3
"""E4.3 trace-only instrumentation.

This script patches a workspace copy of the frozen E4.2 campaign only to emit
observability records. It must not change dispatch, calibration, workload,
thresholds, seeds, gates, or simulator behavior.
"""
from pathlib import Path

P = Path("src/main/java/org/casperiiot/e42/E42Campaign.java")
s = P.read_text()


def rep(old: str, new: str, label: str):
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f"instrumentation anchor {label!r}: expected 1 occurrence, found {n}")
    s = s.replace(old, new, 1)

# Static trace sink. Observability only.
rep(
"    private static final long CLOUDSIM_MI_SCALE = 1_000L;\n",
"    private static final long CLOUDSIM_MI_SCALE = 1_000L;\n"
"    private static Path E43_TRACE_OUT = null;\n",
"trace sink")

# Extend metadata only with audit state captured at dispatch.
old_meta = '''    private static final class DispatchMeta {
        final Task task; final int rank; final int node;
        final double predictedLatencyMs, sigmaMs, nominalServiceMs, actualNetworkMs, etaAtDispatch;
        final boolean certified, familyCovered, probe;
        DispatchMeta(Task t,int rank,int node,double pred,double sigma,double nominal,double net,double eta,
                     boolean cert,boolean fwc,boolean probe){
            task=t;this.rank=rank;this.node=node;predictedLatencyMs=pred;sigmaMs=sigma;
            nominalServiceMs=nominal;actualNetworkMs=net;etaAtDispatch=eta;certified=cert;familyCovered=fwc;this.probe=probe;
        }
    }
'''
new_meta = '''    private static final class DispatchMeta {
        final Task task; final int rank; final int node;
        final double predictedLatencyMs, sigmaMs, nominalServiceMs, actualNetworkMs, etaAtDispatch;
        final boolean certified, familyCovered, probe, selectedNodeAffected, selectedNodeAlarmAtDispatch;
        final String candidateFamilyNodes, candidateFamilyAffectedMask, alarmMaskAtDispatch;
        final int probeTarget, healthCounterfactualSelectedNode;
        final boolean healthChangedDispatch, etaChangedCertification, e17AlarmAtDispatch;
        final int e17TransitionAgeAtDispatch;
        DispatchMeta(Task t,int rank,int node,double pred,double sigma,double nominal,double net,double eta,
                     boolean cert,boolean fwc,boolean probe,boolean selectedAffected,boolean selectedAlarm,
                     String familyNodes,String familyAffected,String alarmMask,int probeTarget,
                     int healthCfNode,boolean healthChanged,boolean etaChanged,
                     boolean e17Alarm,int e17Age){
            task=t;this.rank=rank;this.node=node;predictedLatencyMs=pred;sigmaMs=sigma;
            nominalServiceMs=nominal;actualNetworkMs=net;etaAtDispatch=eta;certified=cert;familyCovered=fwc;this.probe=probe;
            selectedNodeAffected=selectedAffected;selectedNodeAlarmAtDispatch=selectedAlarm;
            candidateFamilyNodes=familyNodes;candidateFamilyAffectedMask=familyAffected;alarmMaskAtDispatch=alarmMask;
            this.probeTarget=probeTarget;healthCounterfactualSelectedNode=healthCfNode;
            healthChangedDispatch=healthChanged;etaChangedCertification=etaChanged;
            e17AlarmAtDispatch=e17Alarm;e17TransitionAgeAtDispatch=e17Age;
        }
    }
'''
rep(old_meta, new_meta, "DispatchMeta")

# Trace CLI and header.
old_args = '''        final String scenarioArg = a.getOrDefault("scenarios","ALL");
        final Path out = Path.of(a.getOrDefault("out","e42_seed_"+String.format("%02d",seedIndex)+".csv"));
        final long scientificSeed = 4_202_202_600L + seedIndex;
'''
new_args = '''        final String scenarioArg = a.getOrDefault("scenarios","ALL");
        final Path out = Path.of(a.getOrDefault("out","e42_seed_"+String.format("%02d",seedIndex)+".csv"));
        if(a.containsKey("trace-out")) {
            E43_TRACE_OUT = Path.of(a.get("trace-out"));
            final Path tp=E43_TRACE_OUT.toAbsolutePath().getParent(); if(tp!=null) Files.createDirectories(tp);
            Files.writeString(E43_TRACE_OUT, traceHeader()+"\\n", StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING);
        }
        final long scientificSeed = 4_202_202_600L + seedIndex;
'''
rep(old_args, new_args, "trace args")

# Calibration metadata constructor: audit fields are neutral because calibration is not traced.
old_cal_meta = '''            meta.put(cl,new DispatchMeta(t,rank,j,predj,sigma,nominal,
                    nominalNetworkMs(t,nodes[j]),1.0,false,true,probe));
'''
new_cal_meta = '''            meta.put(cl,new DispatchMeta(t,rank,j,predj,sigma,nominal,
                    nominalNetworkMs(t,nodes[j]),1.0,false,true,probe,false,false,
                    "","","",probe?j:-1,-1,false,false,false,-1));
'''
rep(old_cal_meta, new_cal_meta, "calibration metadata")

# Add trigger flags around health/adaptation observation and emit after outcome is known.
old_finish = '''                if(policy.health){
                    health[m.node].observe(serviceMs,m.nominalServiceMs);
                    final boolean trueComputeDegraded = scenario.computeRetained < 1.0 && affected[m.node];
                    if(health[m.node].isAlarmed() && !trueComputeDegraded && !acc.countedFalseAlarm[m.node]){
                        acc.countedFalseAlarm[m.node]=true;
                        acc.healthyFalseAlarmNodes++;
                    }
                }
                if(policy.adaptive && m.task.crit()==Crit.MISSION){
                    final double score=Math.max(0.0,(actualLatency-m.predictedLatencyMs)/(m.sigmaMs+1e-12));
                    e17.observe(score);
                }
                if(m.probe && actualLatency>m.task.deadlineMs()) acc.probeDeadlineViolations++;
                if(m.task.crit()==Crit.MISSION){
                    final boolean dvr=actualLatency>m.task.deadlineMs();
                    final boolean far=m.certified && dvr;
                    acc.mission.add(new MissionRec(m.task.index(),m.task.index()>=CHANGE_TASK,
                            m.familyCovered,!m.certified,far,dvr,actualLatency,
                            m.etaAtDispatch));
                }
'''
new_finish = '''                boolean healthAlarmTrigger=false;
                if(policy.health){
                    final boolean alarmBefore=health[m.node].isAlarmed();
                    health[m.node].observe(serviceMs,m.nominalServiceMs);
                    healthAlarmTrigger=!alarmBefore && health[m.node].isAlarmed();
                    final boolean trueComputeDegraded = scenario.computeRetained < 1.0 && affected[m.node];
                    if(health[m.node].isAlarmed() && !trueComputeDegraded && !acc.countedFalseAlarm[m.node]){
                        acc.countedFalseAlarm[m.node]=true;
                        acc.healthyFalseAlarmNodes++;
                    }
                }
                boolean e17AlarmTrigger=false;
                if(policy.adaptive && m.task.crit()==Crit.MISSION){
                    final boolean e17Before=e17.alarmEver();
                    final double score=Math.max(0.0,(actualLatency-m.predictedLatencyMs)/(m.sigmaMs+1e-12));
                    e17.observe(score);
                    e17AlarmTrigger=!e17Before && e17.alarmEver();
                }
                if(m.probe && actualLatency>m.task.deadlineMs()) acc.probeDeadlineViolations++;
                final boolean dvr=actualLatency>m.task.deadlineMs();
                if(m.task.crit()==Crit.MISSION){
                    final boolean far=m.certified && dvr;
                    acc.mission.add(new MissionRec(m.task.index(),m.task.index()>=CHANGE_TASK,
                            m.familyCovered,!m.certified,far,dvr,actualLatency,
                            m.etaAtDispatch));
                }
                if(E43_TRACE_OUT!=null && traceFocus(scenario,policy) &&
                        (m.task.crit()==Crit.MISSION || m.probe || healthAlarmTrigger || e17AlarmTrigger)){
                    appendTrace(seed,scenario,policy,m,actualLatency,dvr,healthAlarmTrigger,e17AlarmTrigger);
                }
'''
rep(old_finish, new_finish, "finish instrumentation")

# Add audit-only variables before decision logic.
old_decision_vars = '''            final double eta=policy.adaptive?e17.etaBeforeOutcome():1.0;
            boolean probe=false;
            int j;
            boolean certified=false;
            boolean familyCovered=true;
            int chosenRank=1;
'''
new_decision_vars = '''            final double eta=policy.adaptive?e17.etaBeforeOutcome():1.0;
            final boolean e17AlarmAtDispatch=policy.adaptive && e17.alarmEver();
            final int e17AgeAtDispatch=policy.adaptive?e17.transitionAge():-1;
            boolean probe=false;
            int probeTarget=-1;
            int j;
            boolean certified=false;
            boolean familyCovered=true;
            int chosenRank=1;
            int[] traceFamily=new int[0];
            int healthCfNode=-1;
            boolean healthChanged=false;
            boolean etaChangedCertification=false;
'''
rep(old_decision_vars, new_decision_vars, "decision audit vars")

# Capture family and compute counterfactuals without feeding them back.
old_cp = '''                final int[] family=topK(pred,eligible,3);
                if(family.length==0){
                    j=argMin(pred,baseEligible);
                }else{
                    final double[] upper=new double[family.length];
                    final double[] actualAudit=new double[family.length];
                    for(int p=0;p<family.length;p++){
                        final int k=family[p];
                        final double sigma=fixedSigma(pred[k],nodes[k].sigmaMult());
                        final double q=policy.ranked?cal.qRank[Math.min(p,2)]:cal.qGlobal;
                        upper[p]=pred[k]+eta*q*sigma;
                        actualAudit[p]=counterfactualActualLatencyMs(seed,t,k,nodes,trueNextFree,now,scenario,affected);
                    }
                    for(int p=0;p<family.length;p++) if(actualAudit[p]>upper[p]) familyCovered=false;
                    int safe=-1;
                    for(int p=0;p<family.length;p++) if(upper[p]<=t.deadlineMs()){safe=p;break;}
                    certified=safe>=0;
                    chosenRank=safe>=0?safe+1:1;
                    j=family[safe>=0?safe:0];
                }
'''
new_cp = '''                final int[] family=topK(pred,eligible,3);
                traceFamily=family.clone();
                if(family.length==0){
                    j=argMin(pred,baseEligible);
                }else{
                    final double[] upper=new double[family.length];
                    final double[] actualAudit=new double[family.length];
                    int safeEta1=-1;
                    for(int p=0;p<family.length;p++){
                        final int k=family[p];
                        final double sigma=fixedSigma(pred[k],nodes[k].sigmaMult());
                        final double q=policy.ranked?cal.qRank[Math.min(p,2)]:cal.qGlobal;
                        upper[p]=pred[k]+eta*q*sigma;
                        if(safeEta1<0 && pred[k]+q*sigma<=t.deadlineMs()) safeEta1=p;
                        actualAudit[p]=counterfactualActualLatencyMs(seed,t,k,nodes,trueNextFree,now,scenario,affected);
                    }
                    for(int p=0;p<family.length;p++) if(actualAudit[p]>upper[p]) familyCovered=false;
                    int safe=-1;
                    for(int p=0;p<family.length;p++) if(upper[p]<=t.deadlineMs()){safe=p;break;}
                    certified=safe>=0;
                    etaChangedCertification=((safeEta1>=0)!=certified);
                    chosenRank=safe>=0?safe+1:1;
                    j=family[safe>=0?safe:0];
                }
                if(policy.health && t.crit()==Crit.MISSION){
                    final int[] noHealthFamily=topK(pred,baseEligible,3);
                    if(noHealthFamily.length==0) healthCfNode=argMin(pred,baseEligible);
                    else {
                        int cfSafe=-1;
                        for(int p=0;p<noHealthFamily.length;p++){
                            final int k=noHealthFamily[p];
                            final double sigma=fixedSigma(pred[k],nodes[k].sigmaMult());
                            final double q=policy.ranked?cal.qRank[Math.min(p,2)]:cal.qGlobal;
                            if(pred[k]+eta*q*sigma<=t.deadlineMs()){cfSafe=p;break;}
                        }
                        healthCfNode=noHealthFamily[cfSafe>=0?cfSafe:0];
                    }
                    healthChanged=healthCfNode!=j;
                }
'''
rep(old_cp, new_cp, "CP counterfactual audit")

# Probe target observability.
old_probe = '''                    if(target>=0 && baseEligible.test(target)){
                        j=target; probe=true; acc.probes++;
                    }
'''
new_probe = '''                    if(target>=0 && baseEligible.test(target)){
                        j=target; probe=true; probeTarget=target; acc.probes++;
                    }
'''
rep(old_probe, new_probe, "probe target")

# Deployment metadata with trace fields.
old_deploy_meta = '''            meta.put(cl,new DispatchMeta(t,chosenRank,j,predj,sigma,nominal,actualNet,eta,
                    certified,familyCovered,probe));
'''
new_deploy_meta = '''            final String familyNodes=joinInts(traceFamily);
            final String familyAffected=maskForNodes(traceFamily,affected);
            final String alarmMaskString=boolMask(alarmMask);
            meta.put(cl,new DispatchMeta(t,chosenRank,j,predj,sigma,nominal,actualNet,eta,
                    certified,familyCovered,probe,affected[j],alarmMask[j],
                    familyNodes,familyAffected,alarmMaskString,probeTarget,
                    healthCfNode,healthChanged,etaChangedCertification,e17AlarmAtDispatch,e17AgeAtDispatch));
'''
rep(old_deploy_meta, new_deploy_meta, "deployment metadata")

# Add trace helpers before parseArgs.
anchor = '''    private static Map<String,String> parseArgs(String[] args){
'''
helpers = r'''    private static boolean traceFocus(Scenario s,Policy p){
        final boolean sc=s==Scenario.S2_HIDDEN_COMPUTE_40LOSS || s==Scenario.S3_HIDDEN_NETWORK_50LOSS || s==Scenario.S4_COMPOUND;
        final boolean po=p==Policy.RANKED_CP_STATIC || p==Policy.CASPER_ADAPT_NO_HEALTH || p==Policy.CASPER_HEALTH_STATIC || p==Policy.CASPER_FULL;
        return sc && po;
    }
    private static String traceHeader(){
        return "seed,scenario,policy,task_index,criticality,arrival_ms,selected_node,selected_node_affected,candidate_family_nodes,candidate_family_affected_mask,alarm_mask_at_dispatch,selected_node_alarm_at_dispatch,probe,probe_target,eta_at_dispatch,e17_alarm_ever,e17_transition_age,certified,family_covered,actual_latency_ms,deadline_ms,deadline_violation,health_counterfactual_selected_node,health_changed_dispatch,eta_changed_certification,health_alarm_trigger,e17_alarm_trigger";
    }
    private static synchronized void appendTrace(long seed,Scenario s,Policy p,DispatchMeta m,double actualLatency,boolean dvr,boolean healthTrigger,boolean e17Trigger){
        try{
            final String row=String.format(Locale.US,
                    "%d,%s,%s,%d,%s,%.9f,%d,%s,%s,%s,%s,%s,%s,%d,%.9f,%s,%d,%s,%s,%.9f,%.9f,%s,%d,%s,%s,%s,%s",
                    seed,s.name(),p.name(),m.task.index(),m.task.crit().name(),m.task.arrivalMs(),m.node,
                    m.selectedNodeAffected,m.candidateFamilyNodes,m.candidateFamilyAffectedMask,m.alarmMaskAtDispatch,
                    m.selectedNodeAlarmAtDispatch,m.probe,m.probeTarget,m.etaAtDispatch,m.e17AlarmAtDispatch,
                    m.e17TransitionAgeAtDispatch,m.certified,m.familyCovered,actualLatency,m.task.deadlineMs(),dvr,
                    m.healthCounterfactualSelectedNode,m.healthChangedDispatch,m.etaChangedCertification,healthTrigger,e17Trigger);
            Files.writeString(E43_TRACE_OUT,row+"\n",StandardOpenOption.APPEND);
        }catch(Exception ex){ throw new RuntimeException(ex); }
    }
    private static String joinInts(int[] x){
        final StringBuilder b=new StringBuilder(); for(int i=0;i<x.length;i++){if(i>0)b.append('|');b.append(x[i]);} return b.toString();
    }
    private static String maskForNodes(int[] nodes,boolean[] mask){
        final StringBuilder b=new StringBuilder(); for(int i=0;i<nodes.length;i++){if(i>0)b.append('|');b.append(mask[nodes[i]]?'1':'0');} return b.toString();
    }
    private static String boolMask(boolean[] x){
        final StringBuilder b=new StringBuilder(x.length); for(boolean v:x)b.append(v?'1':'0'); return b.toString();
    }

'''
rep(anchor, helpers + anchor, "trace helpers")

P.write_text(s)
print("E43_TRACE_INSTRUMENTATION PASS")
