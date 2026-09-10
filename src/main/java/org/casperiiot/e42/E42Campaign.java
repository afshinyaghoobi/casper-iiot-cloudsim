package org.casperiiot.e42;

import ch.qos.logback.classic.Level;
import org.cloudsimplus.brokers.DatacenterBrokerSimple;
import org.cloudsimplus.cloudlets.Cloudlet;
import org.cloudsimplus.cloudlets.CloudletSimple;
import org.cloudsimplus.core.CloudSimPlus;
import org.cloudsimplus.datacenters.DatacenterSimple;
import org.cloudsimplus.hosts.Host;
import org.cloudsimplus.hosts.HostSimple;
import org.cloudsimplus.resources.Pe;
import org.cloudsimplus.resources.PeSimple;
import org.cloudsimplus.schedulers.cloudlet.CloudletSchedulerSpaceShared;
import org.cloudsimplus.util.Log;
import org.cloudsimplus.utilizationmodels.UtilizationModelFull;
import org.cloudsimplus.vms.Vm;
import org.cloudsimplus.vms.VmSimple;
import org.casperiiot.e41.core.E17DualMemory;
import org.casperiiot.e41.core.FrozenConfig;
import org.casperiiot.e41.core.NodeHealthDetector;
import org.casperiiot.e41.core.SparseProbeBudget;
import org.casperiiot.e41.core.SparseProbeSelector;
import org.casperiiot.e41.core.VirtualQueueEstimator;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.*;
import java.util.function.IntPredicate;

/**
 * E4.2 publication-scale CloudSim Plus campaign.
 * Scientific architecture is frozen from E3.12/E4.1c.
 */
public final class E42Campaign {
    private static final int NODES = FrozenConfig.TOTAL_NODES;
    private static final int CHANGE_TASK = 10_000;
    private static final double LAMBDA0_PER_MS = 0.12;
    private static final double ARRIVAL_WARMUP_MS = 1_000.0;
    private static final int CAL_BURNIN = 10_000;
    private static final int LATE_MISSION = 250;

    private enum Crit { NORMAL, HIGH, MISSION }
    private enum Scenario {
        S0_STATIONARY(1.0,1.0,1.0),
        S1_LAMBDA_X2(2.0,1.0,1.0),
        S2_HIDDEN_COMPUTE_40LOSS(1.0,0.60,1.0),
        S3_HIDDEN_NETWORK_50LOSS(1.0,1.0,0.50),
        S4_COMPOUND(2.0,0.60,0.50);
        final double arrivalMult, computeRetained, bwRetained;
        Scenario(double a,double c,double b){arrivalMult=a;computeRetained=c;bwRetained=b;}
    }
    private enum Policy {
        CLOUD_ONLY(false,false,false,false),
        EDGE_FIRST(false,false,false,false),
        PRED_GREEDY(false,false,false,false),
        GLOBAL_CP(true,false,false,false),
        RANKED_CP_STATIC(true,true,false,false),
        CASPER_ADAPT_NO_HEALTH(true,true,true,false),
        CASPER_HEALTH_STATIC(true,true,false,true),
        CASPER_FULL(true,true,true,true);
        final boolean cp, ranked, adaptive, health;
        Policy(boolean cp,boolean ranked,boolean adaptive,boolean health){
            this.cp=cp; this.ranked=ranked; this.adaptive=adaptive; this.health=health;
        }
    }

    private record NodeParams(double cap, double bwMbps, double rttMs, double sigmaMult, long vmMips) {}
    private record Task(int index, Crit crit, double deadlineMs, double work, double inputMb,
                        double outputMb, double arrivalMs) {}
    private static final class DispatchMeta {
        final Task task; final int rank; final int node;
        final double predictedLatencyMs, sigmaMs, nominalServiceMs, actualNetworkMs, etaAtDispatch;
        final boolean certified, familyCovered, probe;
        DispatchMeta(Task t,int rank,int node,double pred,double sigma,double nominal,double net,double eta,
                     boolean cert,boolean fwc,boolean probe){
            task=t;this.rank=rank;this.node=node;predictedLatencyMs=pred;sigmaMs=sigma;
            nominalServiceMs=nominal;actualNetworkMs=net;etaAtDispatch=eta;certified=cert;familyCovered=fwc;this.probe=probe;
        }
    }
    private record MissionRec(int taskIndex, boolean post, boolean fwc, boolean air, boolean far,
                              boolean dvr, double latencyMs, double eta) {}
    private record Calibration(double[] qRank, double qGlobal, double[] referenceScores,
                               double[] serviceThresholdByNode, int[] rankN, int[] serviceTierN) {}
    private static final class Acc {
        final List<MissionRec> mission = new ArrayList<>();
        long finished, normalArrivals, probes, probeDeadlineViolations, healthyFalseAlarmNodes, degradedAlarmed;
        double mapperNsSum; long mapperCalls; double maxServiceParityErrorMs;
        final boolean[] countedFalseAlarm = new boolean[NODES];
    }

    public static void main(String[] args) throws Exception {
        Log.setLevel(Level.OFF);
        final Map<String,String> a = parseArgs(args);
        final int seedIndex = Integer.parseInt(a.getOrDefault("seed","0"));
        final int deployN = Integer.parseInt(a.getOrDefault("tasks","30000"));
        final int calN = Integer.parseInt(a.getOrDefault("cal","80000"));
        final String scenarioArg = a.getOrDefault("scenarios","ALL");
        final Path out = Path.of(a.getOrDefault("out","e42_seed_"+String.format("%02d",seedIndex)+".csv"));
        final long scientificSeed = 4_202_202_600L + seedIndex;

        if (calN <= CAL_BURNIN) throw new IllegalArgumentException("calibration too short");
        System.out.printf(Locale.US,"E42 seed=%d scientificSeed=%d cal=%d deploy=%d%n",
                seedIndex, scientificSeed, calN, deployN);

        final NodeParams[] nodes = makeNodes(scientificSeed);
        final Calibration cal = runCalibration(scientificSeed, calN, nodes);
        validateCalibration(cal);

        final Path parent = out.toAbsolutePath().getParent();
        if(parent!=null) Files.createDirectories(parent);
        Files.writeString(out, csvHeader()+"\n", StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING);

        final List<Scenario> scenarios = scenarioArg.equals("ALL")
                ? List.of(Scenario.values())
                : Arrays.stream(scenarioArg.split(",")).map(Scenario::valueOf).toList();

        for (Scenario scenario: scenarios) {
            for (Policy policy: Policy.values()) {
                final String row = runDeployment(scientificSeed, deployN, nodes, cal, scenario, policy);
                Files.writeString(out,row+"\n",StandardOpenOption.APPEND);
                System.out.println(row);
                System.gc();
            }
        }
        System.out.println("E42_SEED_COMPLETE seed="+seedIndex+" rows="+(scenarios.size()*Policy.values().length));
    }

    @SuppressWarnings("unchecked")
    private static Calibration runCalibration(long seed, int n, NodeParams[] nodes) {
        final List<Task> tasks = makeTasks(seed ^ 0xCA11B4A7L,n,Scenario.S0_STATIONARY);
        final int[] missionRank = calibrationRanks(seed,tasks);

        final CloudSimPlus sim = new CloudSimPlus(0.0001);
        final List<Vm> vms = createInfrastructure(sim,nodes);
        final DatacenterBrokerSimple broker = new DatacenterBrokerSimple(sim);
        final IdentityHashMap<Cloudlet,Task> spec = new IdentityHashMap<>();
        final IdentityHashMap<Cloudlet,DispatchMeta> meta = new IdentityHashMap<>();
        final VirtualQueueEstimator vq = new VirtualQueueEstimator(NODES);
        final double[] trueNextFree = new double[NODES];
        final long[] lastObserved = new long[NODES]; Arrays.fill(lastObserved,-1);
        final SparseProbeBudget probeBudget = new SparseProbeBudget();
        final List<Double>[] scoreByRank = new List[]{new ArrayList<>(),new ArrayList<>(),new ArrayList<>()};
        final List<Double> allScores = new ArrayList<>();
        final List<Double>[] serviceByTier = new List[]{new ArrayList<>(),new ArrayList<>(),new ArrayList<>()};
        final long[] finishOrdinal = {0};
        final double[] nextTelemetry = {ARRIVAL_WARMUP_MS};

        final List<Cloudlet> cloudlets = new ArrayList<>(n);
        for (Task t: tasks) {
            final Cloudlet c = new CloudletSimple(Math.max(1,Math.round(t.work()*12)),1,new UtilizationModelFull());
            c.setSubmissionDelay(t.arrivalMs()/1000.0);
            spec.put(c,t);
            c.addOnFinishListener(evt -> {
                final Cloudlet cl=evt.getCloudlet();
                final DispatchMeta m=meta.get(cl);
                if(m==null) return;
                final double serviceMs=(cl.getFinishTime()-cl.getStartTime())*1000.0;
                final double actualLatency=m.actualNetworkMs + cl.getStartWaitTime()*1000.0 + serviceMs;
                lastObserved[m.node]=finishOrdinal[0]++;
                if(m.task.index()>=CAL_BURNIN) {
                    serviceByTier[tier(m.node)].add(serviceMs/Math.max(m.nominalServiceMs,1e-12));
                    if(m.task.crit()==Crit.MISSION) {
                        final double s=Math.max(0.0,(actualLatency-m.predictedLatencyMs)/(m.sigmaMs+1e-12));
                        scoreByRank[m.rank-1].add(s);
                        allScores.add(s);
                    }
                }
            });
            cloudlets.add(c);
        }

        broker.submitVmList(vms);
        broker.setVmMapper(cl -> {
            final Task t=spec.get(cl);
            final double now=t.arrivalMs();
            if(now>=nextTelemetry[0]) {
                vq.resetFromTelemetry(trueNextFree);
                nextTelemetry[0]=now+FrozenConfig.TELEMETRY_PERIOD_MS;
            }
            final double[] pred=predictedLatency(t,nodes,vq,now);
            int rank=1;
            int j;
            boolean probe=false;
            if(t.crit()==Crit.MISSION && t.index()>=CAL_BURNIN) {
                rank=missionRank[t.index()];
                final int[] top=topK(pred,x->true,3);
                j=top[Math.min(rank-1,top.length-1)];
            } else {
                j=argMin(pred,x->true);
                if(t.crit()==Crit.NORMAL && probeBudget.onNormalArrival()) {
                    final int target=SparseProbeSelector.choose(pred,t.deadlineMs(),new boolean[NODES],lastObserved);
                    if(target>=0){j=target;probe=true;}
                }
            }
            final double nominal=nominalServiceMs(t,nodes[j]);
            final double actualService=actualServiceMs(seed,t,j,nominal,1.0);
            cl.setLength(lengthForMs(nodes[j].vmMips(),actualService));
            final double predj=pred[j];
            final double sigma=fixedSigma(predj,nodes[j].sigmaMult());
            trueNextFree[j]=Math.max(trueNextFree[j],now)+actualService;
            vq.onDispatch(j,now,nominal);
            meta.put(cl,new DispatchMeta(t,rank,j,predj,sigma,nominal,
                    nominalNetworkMs(t,nodes[j]),1.0,false,true,probe));
            return vms.get(j);
        });
        broker.submitCloudletList(cloudlets);
        sim.start();
        if(broker.getCloudletFinishedList().size()!=n)
            throw new IllegalStateException("calibration CloudSim completion mismatch");

        final double[] qRank = new double[3];
        final int[] rankN = new int[3];
        for(int r=1;r<=3;r++){
            rankN[r-1]=scoreByRank[r-1].size();
            qRank[r-1]=qhat(scoreByRank[r-1],FrozenConfig.missionRankAlpha(r));
        }
        final double qGlobal=qhat(allScores,FrozenConfig.EPS_MISSION);
        final double[] ref=allScores.stream().mapToDouble(Double::doubleValue).toArray();

        final double[] tierThr=new double[3];
        final int[] tierN=new int[3];
        for(int k=0;k<3;k++){
            tierN[k]=serviceByTier[k].size();
            tierThr[k]=qhat(serviceByTier[k],FrozenConfig.SERVICE_HEALTH_ALPHA);
        }
        final double[] byNode=new double[NODES];
        for(int j=0;j<NODES;j++) byNode[j]=tierThr[tier(j)];

        System.out.printf(Locale.US,
                "CALIBRATION rankN=%s qRank=[%.6f,%.6f,%.6f] qGlobal=%.6f serviceN=%s thr=[%.6f,%.6f,%.6f]%n",
                Arrays.toString(rankN),qRank[0],qRank[1],qRank[2],qGlobal,
                Arrays.toString(tierN),tierThr[0],tierThr[1],tierThr[2]);
        return new Calibration(qRank,qGlobal,ref,byNode,rankN,tierN);
    }

    private static String runDeployment(long seed,int n,NodeParams[] nodes,Calibration cal,
                                        Scenario scenario,Policy policy) {
        final List<Task> tasks=makeTasks(seed ^ 0xD3F10A77L,n,scenario);
        final boolean[] affected=affectedMask(seed,scenario);

        final CloudSimPlus sim=new CloudSimPlus(0.0001);
        final List<Vm> vms=createInfrastructure(sim,nodes);
        final DatacenterBrokerSimple broker=new DatacenterBrokerSimple(sim);
        final IdentityHashMap<Cloudlet,Task> spec=new IdentityHashMap<>();
        final IdentityHashMap<Cloudlet,DispatchMeta> meta=new IdentityHashMap<>();
        final VirtualQueueEstimator vq=new VirtualQueueEstimator(NODES);
        final double[] trueNextFree=new double[NODES];
        final NodeHealthDetector[] health=new NodeHealthDetector[NODES];
        for(int j=0;j<NODES;j++) health[j]=new NodeHealthDetector(cal.serviceThresholdByNode[j]);
        final E17DualMemory e17=policy.adaptive?new E17DualMemory(cal.referenceScores):null;
        final SparseProbeBudget probeBudget=new SparseProbeBudget();
        final long[] lastObserved=new long[NODES]; Arrays.fill(lastObserved,-1);
        final long[] finishOrdinal={0};
        final double[] nextTelemetry={ARRIVAL_WARMUP_MS};
        final Acc acc=new Acc();

        final List<Cloudlet> cloudlets=new ArrayList<>(n);
        for(Task t:tasks){
            final Cloudlet c=new CloudletSimple(Math.max(1,Math.round(t.work()*12)),1,new UtilizationModelFull());
            c.setSubmissionDelay(t.arrivalMs()/1000.0);
            spec.put(c,t);
            c.addOnFinishListener(evt -> {
                final Cloudlet cl=evt.getCloudlet();
                final DispatchMeta m=meta.get(cl);
                if(m==null)return;
                acc.finished++;
                final double serviceMs=(cl.getFinishTime()-cl.getStartTime())*1000.0;
                final double planned=lengthToMs(cl.getLength(),nodes[m.node].vmMips());
                acc.maxServiceParityErrorMs=Math.max(acc.maxServiceParityErrorMs,Math.abs(serviceMs-planned));
                final double actualLatency=m.actualNetworkMs+cl.getStartWaitTime()*1000.0+serviceMs;
                lastObserved[m.node]=finishOrdinal[0]++;

                if(policy.health){
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
            });
            cloudlets.add(c);
        }

        broker.submitVmList(vms);
        broker.setVmMapper(cl -> {
            final long wall0=System.nanoTime();
            final Task t=spec.get(cl);
            final double now=t.arrivalMs();
            if(now>=nextTelemetry[0]){
                vq.resetFromTelemetry(trueNextFree);
                nextTelemetry[0]=now+FrozenConfig.TELEMETRY_PERIOD_MS;
            }

            final double[] pred=predictedLatency(t,nodes,vq,now);
            final boolean[] alarmMask=new boolean[NODES];
            if(policy.health) for(int j=0;j<NODES;j++) alarmMask[j]=health[j].isAlarmed();

            final IntPredicate baseEligible = switch(policy){
                case CLOUD_ONLY -> j -> j>=18;
                case EDGE_FIRST -> j -> j<12;
                default -> j -> true;
            };
            final IntPredicate eligible = j -> baseEligible.test(j) && (!policy.health || !alarmMask[j]);

            final double eta=policy.adaptive?e17.etaBeforeOutcome():1.0;
            boolean probe=false;
            int j;
            boolean certified=false;
            boolean familyCovered=true;
            int chosenRank=1;

            if(!policy.cp){
                j=argMin(pred,eligible);
            }else{
                final int[] family=topK(pred,eligible,3);
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
            }

            if(policy.health && t.crit()==Crit.NORMAL){
                acc.normalArrivals++;
                if(probeBudget.onNormalArrival()){
                    final int target=SparseProbeSelector.choose(pred,t.deadlineMs(),alarmMask,lastObserved);
                    if(target>=0 && baseEligible.test(target)){
                        j=target; probe=true; acc.probes++;
                    }
                }
            }else if(t.crit()==Crit.NORMAL){
                acc.normalArrivals++;
            }

            if(j<0) j=argMin(pred,x->true);

            final double nominal=nominalServiceMs(t,nodes[j]);
            final double computeMult=(t.index()>=CHANGE_TASK && affected[j] && scenario.computeRetained<1.0)
                    ? 1.0/scenario.computeRetained : 1.0;
            final double actualService=actualServiceMs(seed,t,j,nominal,computeMult);
            final double netMult=(t.index()>=CHANGE_TASK && affected[j] && scenario.bwRetained<1.0)
                    ? 1.0/scenario.bwRetained : 1.0;
            final double actualNet=nominalNetworkMs(t,nodes[j])*netMult;
            cl.setLength(lengthForMs(nodes[j].vmMips(),actualService));

            final double predj=pred[j];
            final double sigma=fixedSigma(predj,nodes[j].sigmaMult());
            trueNextFree[j]=Math.max(trueNextFree[j],now)+actualService;
            vq.onDispatch(j,now,nominal);

            final long ns=System.nanoTime()-wall0;
            acc.mapperNsSum+=ns; acc.mapperCalls++;
            meta.put(cl,new DispatchMeta(t,chosenRank,j,predj,sigma,nominal,actualNet,eta,
                    certified,familyCovered,probe));
            return vms.get(j);
        });
        broker.submitCloudletList(cloudlets);
        sim.start();

        if(acc.finished!=n || broker.getCloudletFinishedList().size()!=n)
            throw new IllegalStateException("deployment completion mismatch "+policy+" "+scenario+" "+acc.finished+"/"+n);

        if(policy.health && scenario.computeRetained<1.0){
            long x=0; for(int j=0;j<NODES;j++) if(affected[j]&&health[j].isAlarmed())x++;
            acc.degradedAlarmed=x;
        }
        if(acc.maxServiceParityErrorMs>2.0)
            throw new IllegalStateException("CloudSim service parity error >2ms: "+acc.maxServiceParityErrorMs);

        return summarize(seed,n,scenario,policy,acc,affected);
    }

    private static String summarize(long seed,int n,Scenario s,Policy p,Acc a,boolean[] affected){
        final List<MissionRec> ordered=a.mission.stream().sorted(Comparator.comparingInt(MissionRec::taskIndex)).toList();
        final List<MissionRec> post=ordered.stream().filter(MissionRec::post).toList();
        final List<MissionRec> late=post.size()<=LATE_MISSION?post:post.subList(post.size()-LATE_MISSION,post.size());
        final List<MissionRec> shock=post.size()<=LATE_MISSION?post:post.subList(0,LATE_MISSION);
        final double postFwc=p.cp?meanBool(post,MissionRec::fwc):Double.NaN;
        final double lateFwc=p.cp?meanBool(late,MissionRec::fwc):Double.NaN;
        final double shockFwc=p.cp?meanBool(shock,MissionRec::fwc):Double.NaN;
        final double postAir=p.cp?meanBool(post,MissionRec::air):Double.NaN;
        final double lateAir=p.cp?meanBool(late,MissionRec::air):Double.NaN;
        final double postFar=p.cp?meanBool(post,MissionRec::far):Double.NaN;
        final double lateFar=p.cp?meanBool(late,MissionRec::far):Double.NaN;
        final double postDvr=meanBool(post,MissionRec::dvr);
        final double lateDvr=meanBool(late,MissionRec::dvr);
        final double p99Post=quantile(post.stream().mapToDouble(MissionRec::latencyMs).toArray(),.99);
        final double p99Late=quantile(late.stream().mapToDouble(MissionRec::latencyMs).toArray(),.99);
        final double etaLate=p.adaptive?late.stream().mapToDouble(MissionRec::eta).average().orElse(1):1;
        final double probeRate=a.normalArrivals==0?0:a.probes/(double)a.normalArrivals;
        final double probeDvr=a.probes==0?0:a.probeDeadlineViolations/(double)a.probes;
        final long affectedN=countTrue(affected);
        final double alarmCov=(p.health && s.computeRetained<1.0 && affectedN>0)?a.degradedAlarmed/(double)affectedN:Double.NaN;
        final double meanMapperUs=a.mapperCalls==0?0:a.mapperNsSum/a.mapperCalls/1000.0;
        return String.format(Locale.US,
                "%d,%s,%s,%d,%d,%d,%.9f,%.9f,%.9f,%.9f,%.9f,%.9f,%.9f,%.9f,%.9f,%.6f,%.6f,%.6f,%.9f,%.9f,%.9f,%d,%d,%.6f,%.6f,%.1f",
                seed,s.name(),p.name(),n,a.mission.size(),post.size(),
                postFwc,shockFwc,lateFwc,postAir,lateAir,postFar,lateFar,
                postDvr,lateDvr,p99Post,p99Late,etaLate,probeRate,probeDvr,
                alarmCov,a.healthyFalseAlarmNodes,a.degradedAlarmed,
                meanMapperUs,a.maxServiceParityErrorMs,1.0);
    }

    private static String csvHeader(){
        return "seed,scenario,policy,tasks,mission_n,post_mission_n,post_fwc,shock_fwc,late_fwc,post_air,late_air,post_far,late_far,post_dvr,late_dvr,p99_post_latency_ms,p99_late_latency_ms,late_eta,probe_rate,probe_dvr,compute_alarm_coverage,healthy_false_alarm_nodes,degraded_nodes_alarmed,mean_mapper_us,max_service_parity_error_ms,cloudsim_completion";
    }

    private static List<Vm> createInfrastructure(CloudSimPlus sim,NodeParams[] nodes){
        final List<Host> hosts=new ArrayList<>(NODES);
        final List<Vm> vms=new ArrayList<>(NODES);
        for(int j=0;j<NODES;j++){
            final long hostMips=Math.max(nodes[j].vmMips()+1000,Math.round(nodes[j].vmMips()*1.25));
            final List<Pe> pes=List.of(new PeSimple(hostMips));
            hosts.add(new HostSimple(16_384,100_000,10_000_000,pes));
            vms.add(new VmSimple(nodes[j].vmMips(),1)
                    .setRam(4096).setBw(10_000).setSize(100_000)
                    .setCloudletScheduler(new CloudletSchedulerSpaceShared()));
        }
        new DatacenterSimple(sim,hosts);
        return vms;
    }

    private static NodeParams[] makeNodes(long seed){
        final Random r=new Random(seed ^ 0x51A7E123L);
        final NodeParams[] x=new NodeParams[NODES];
        for(int j=0;j<NODES;j++){
            final double cap,bw,rtt,sm;
            if(j<12){cap=u(r,2.5,6);bw=u(r,80,250);rtt=u(r,2,10);sm=1.10;}
            else if(j<18){cap=u(r,8,20);bw=u(r,150,600);rtt=u(r,8,28);sm=1.0;}
            else{cap=u(r,30,70);bw=u(r,300,1200);rtt=u(r,30,80);sm=.90;}
            x[j]=new NodeParams(cap,bw,rtt,sm,Math.max(1000,Math.round(cap*1000)));
        }
        return x;
    }

    private static List<Task> makeTasks(long seed,int n,Scenario scenario){
        final Random r=new Random(seed);
        final List<Task> out=new ArrayList<>(n);
        double time=ARRIVAL_WARMUP_MS;
        for(int i=0;i<n;i++){
            final double pm=i>=CHANGE_TASK?scenario.arrivalMult:1.0;
            time += (-Math.log(Math.max(1e-15,1-r.nextDouble()))/LAMBDA0_PER_MS)/pm;
            final double z=r.nextDouble();
            final Crit c=z<.80?Crit.NORMAL:(z<.95?Crit.HIGH:Crit.MISSION);
            final double D=switch(c){
                case NORMAL -> u(r,500,2000);
                case HIGH -> u(r,100,500);
                case MISSION -> u(r,40,120);
            };
            final double work=switch(c){
                case NORMAL -> lognormal(r,25,.45);
                case HIGH -> lognormal(r,45,.50);
                case MISSION -> lognormal(r,18,.35);
            };
            final double in=switch(c){
                case NORMAL -> lognormal(r,.40,.55);
                case HIGH -> lognormal(r,1.0,.60);
                case MISSION -> lognormal(r,.05,.40);
            };
            final double o=switch(c){
                case NORMAL -> lognormal(r,.08,.40);
                case HIGH -> lognormal(r,.20,.50);
                case MISSION -> lognormal(r,.01,.35);
            };
            out.add(new Task(i,c,D,work,in,o,time));
        }
        return out;
    }

    private static int[] calibrationRanks(long seed,List<Task> tasks){
        final int[] rank=new int[tasks.size()];
        final List<Integer> idx=new ArrayList<>();
        for(Task t:tasks) if(t.index()>=CAL_BURNIN && t.crit()==Crit.MISSION) idx.add(t.index());
        final List<Integer> vals=new ArrayList<>(idx.size());
        for(int k=0;k<idx.size();k++) vals.add((k%3)+1);
        Collections.shuffle(vals,new Random(seed ^ 0xA11CE77L));
        for(int k=0;k<idx.size();k++) rank[idx.get(k)]=vals.get(k);
        return rank;
    }

    private static double[] predictedLatency(Task t,NodeParams[] nodes,VirtualQueueEstimator vq,double now){
        final double[] p=new double[NODES];
        for(int j=0;j<NODES;j++)
            p[j]=nominalNetworkMs(t,nodes[j])+vq.predictedBacklogMs(j,now)+nominalServiceMs(t,nodes[j]);
        return p;
    }
    private static double nominalServiceMs(Task t,NodeParams n){return t.work()/n.cap()*12.0;}
    private static double nominalNetworkMs(Task t,NodeParams n){return n.rttMs()+(t.inputMb()+t.outputMb())*8000.0/n.bwMbps();}
    private static double fixedSigma(double pred,double mult){return (3.0+.10*pred)*mult;}

    private static double actualServiceMs(long seed,Task t,int node,double nominal,double computeMult){
        final double z=serviceNoise(seed,t.index(),node);
        return Math.max(.2,nominal*computeMult*(1+.18*z));
    }
    private static double counterfactualActualLatencyMs(long seed,Task t,int node,NodeParams[] nodes,
                                                         double[] trueNextFree,double now,
                                                         Scenario scenario,boolean[] affected){
        final double cm=(t.index()>=CHANGE_TASK && affected[node] && scenario.computeRetained<1)
                ?1/scenario.computeRetained:1;
        final double bm=(t.index()>=CHANGE_TASK && affected[node] && scenario.bwRetained<1)
                ?1/scenario.bwRetained:1;
        final double svc=actualServiceMs(seed,t,node,nominalServiceMs(t,nodes[node]),cm);
        final double q=Math.max(0,trueNextFree[node]-now);
        return nominalNetworkMs(t,nodes[node])*bm+q+svc;
    }

    private static double serviceNoise(long seed,int task,int node){
        long h=mix64(seed ^ (((long)task)<<21) ^ (node*0x9E3779B97F4A7C15L));
        final double u1=((h>>>11)*0x1.0p-53);
        h=mix64(h+0xD1B54A32D192ED03L);
        final double u2=((h>>>11)*0x1.0p-53);
        double g=Math.sqrt(-2*Math.log(Math.max(u1,1e-15)))*Math.cos(2*Math.PI*u2)*.28;
        h=mix64(h+0x94D049BB133111EBL);
        final double ut=((h>>>11)*0x1.0p-53);
        if(ut<.08){
            h=mix64(h+0xBF58476D1CE4E5B9L);
            final double ue=((h>>>11)*0x1.0p-53);
            g += -Math.log(Math.max(1e-15,1-ue))*.7;
        }
        return Math.max(g,-.8);
    }

    private static boolean[] affectedMask(long seed,Scenario s){
        final boolean[] m=new boolean[NODES];
        if(s.computeRetained>=1 && s.bwRetained>=1) return m;
        final List<Integer> a=new ArrayList<>(); for(int j=0;j<NODES;j++)a.add(j);
        Collections.shuffle(a,new Random(seed ^ (0xBADC0FFEL + 31L*s.ordinal())));
        for(int k=0;k<6;k++)m[a.get(k)]=true;
        return m;
    }

    private static int tier(int node){return node<12?0:(node<18?1:2);}
    private static long lengthForMs(long mips,double ms){return Math.max(1,Math.round(mips*ms/1000.0));}
    private static double lengthToMs(long len,long mips){return len*1000.0/mips;}

    private static int argMin(double[] x,IntPredicate ok){
        int b=-1; double v=Double.POSITIVE_INFINITY;
        for(int j=0;j<x.length;j++)if(ok.test(j)&&x[j]<v){v=x[j];b=j;}
        return b;
    }
    private static int[] topK(double[] x,IntPredicate ok,int k){
        return java.util.stream.IntStream.range(0,x.length).filter(ok)
                .boxed().sorted(Comparator.comparingDouble(j->x[j])).limit(k).mapToInt(Integer::intValue).toArray();
    }

    private static double qhat(List<Double> values,double alpha){
        if(values.isEmpty())return Double.POSITIVE_INFINITY;
        final double[] a=values.stream().mapToDouble(Double::doubleValue).sorted().toArray();
        final int k=(int)Math.ceil((a.length+1)*(1-alpha));
        return k>a.length?Double.POSITIVE_INFINITY:a[k-1];
    }
    private static void validateCalibration(Calibration c){
        if(c.referenceScores.length<200)throw new IllegalStateException("insufficient E1.7 reference");
        for(double q:c.qRank)if(!Double.isFinite(q))throw new IllegalStateException("non-finite ranked conformal q");
        if(!Double.isFinite(c.qGlobal))throw new IllegalStateException("non-finite global conformal q");
        long infiniteHealth=Arrays.stream(c.serviceThresholdByNode).filter(q -> !Double.isFinite(q)).count();
        if(infiniteHealth>0) System.out.println("CALIBRATION_SUPPORT_WARNING conservative_infinite_health_threshold_nodes="+infiniteHealth);
        System.out.println("CALIBRATION_VALIDATION PASS");
    }

    private interface BoolGetter { boolean get(MissionRec r); }
    private static double meanBool(List<MissionRec>x,BoolGetter g){
        if(x.isEmpty())return Double.NaN; long n=0;for(MissionRec r:x)if(g.get(r))n++;return n/(double)x.size();
    }
    private static double quantile(double[] x,double q){
        if(x.length==0)return Double.NaN; Arrays.sort(x);
        return x[(int)Math.ceil((x.length-1)*q)];
    }
    private static long countTrue(boolean[]x){long n=0;for(boolean b:x)if(b)n++;return n;}

    private static double u(Random r,double a,double b){return a+(b-a)*r.nextDouble();}
    private static double lognormal(Random r,double median,double sigma){return Math.exp(Math.log(median)+sigma*r.nextGaussian());}
    private static long mix64(long z){
        z=(z^(z>>>30))*0xbf58476d1ce4e5b9L;
        z=(z^(z>>>27))*0x94d049bb133111ebL;
        return z^(z>>>31);
    }
    private static Map<String,String> parseArgs(String[] args){
        final Map<String,String> m=new HashMap<>();
        for(int i=0;i<args.length;i++){
            if(args[i].startsWith("--")){
                final String key=args[i].substring(2);
                final String val=(i+1<args.length && !args[i+1].startsWith("--"))?args[++i]:"true";
                m.put(key,val);
            }
        }
        return m;
    }
}
