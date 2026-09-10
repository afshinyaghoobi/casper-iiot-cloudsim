package org.casperiiot.e41.core;

import java.util.Arrays;

public final class CoreParitySmoke {
    private static int passed = 0;
    private static int failed = 0;

    private static void check(String name, boolean condition) {
        if (condition) { passed++; System.out.println("PASS " + name); }
        else { failed++; System.out.println("FAIL " + name); }
    }

    private static boolean close(double a, double b) { return Math.abs(a-b) < 1e-9; }

    public static void main(String[] args) {
        check("topology_12_6_3", FrozenConfig.EDGE_NODES==12 && FrozenConfig.FOG_NODES==6 && FrozenConfig.CLOUD_NODES==3 && FrozenConfig.TOTAL_NODES==21);
        check("mission_epsilon", close(FrozenConfig.EPS_MISSION, .01));
        check("rank_alphas", close(FrozenConfig.missionRankAlpha(1),.006) && close(FrozenConfig.missionRankAlpha(2),.003) && close(FrozenConfig.missionRankAlpha(3),.001));

        double[] s999 = new double[999]; for (int i=0;i<s999.length;i++) s999[i]=i;
        double[] s998 = new double[998]; for (int i=0;i<s998.length;i++) s998[i]=i;
        check("qhat_rank3_n999_finite", Double.isFinite(Conformal.qhat(s999,.001)));
        check("qhat_rank3_n998_infinite", Double.isInfinite(Conformal.qhat(s998,.001)));
        check("one_sided_score", close(Conformal.score(120,100,10,0),2.0) && close(Conformal.score(90,100,10,0),0.0));

        VirtualQueueEstimator vq = new VirtualQueueEstimator(2);
        vq.resetFromTelemetry(new double[]{0,0});
        vq.onDispatch(0,10,5);
        check("virtual_next_free", close(vq.predictedNextFreeMs(0),15));
        check("virtual_backlog", close(vq.predictedBacklogMs(0,12),3));
        vq.resetFromTelemetry(new double[]{20,0});
        check("virtual_telemetry_reset", close(vq.predictedBacklogMs(0,18),2));

        NodeHealthDetector h1 = new NodeHealthDetector(1.25);
        double[] ratios1={1.30,1.31,1.00,1.40,1.00,1.50,1.60,1.00};
        for(double r:ratios1) h1.observe(r,1.0);
        check("health_alarm_5_of_8", h1.isAlarmed());
        NodeHealthDetector h2 = new NodeHealthDetector(1.25);
        double[] ratios2={1.30,1.31,1.00,1.40,1.00,1.50,1.00,1.00};
        for(double r:ratios2) h2.observe(r,1.0);
        check("health_no_alarm_4_of_8", !h2.isAlarmed());

        SparseProbeBudget pb = new SparseProbeBudget();
        int probes=0; for(int i=0;i<10000;i++) if(pb.onNormalArrival()) probes++;
        check("probe_every_100", probes==100);
        check("probe_budget_le_1pct", pb.rate() <= .01 + 1e-12);

        double[] lat={5,1,3,2}; boolean[] alarmed={false,true,false,false};
        int[] fam=CandidateGate.topKHealthy(lat,alarmed,3);
        check("health_gate_excludes_alarmed", Arrays.equals(fam,new int[]{3,2,0}));
        double[] u={50,1,35,20};
        check("first_safe", CandidateGate.firstSafe(fam,u,30)==3);

        check("e17_windows_frozen", FrozenConfig.E17_SLOW_WINDOW==200 && FrozenConfig.E17_FAST_WINDOW==50 && FrozenConfig.E17_DETECTOR_WINDOW==50 && FrozenConfig.E17_DETECTOR_EXCEEDANCES==12 && FrozenConfig.E17_TRANSITION_HOLD==200);
        check("eta_clip", close(FrozenConfig.clipEta(.5),1.0) && close(FrozenConfig.clipEta(4),3.0) && close(FrozenConfig.clipEta(1.7),1.7));

        double[] ref = new double[1000]; for(int i=0;i<ref.length;i++) ref[i]=1.0;
        E17DualMemory e17 = new E17DualMemory(ref);
        for(int i=0;i<38;i++) e17.observe(1.0);
        for(int i=0;i<12;i++) e17.observe(2.0);
        check("e17_detector_12_of_50", e17.alarmEver());
        check("e17_eta_bounded", e17.etaBeforeOutcome() >= 1.0 && e17.etaBeforeOutcome() <= 3.0);

        long[] last={10,-1,5}; boolean[] halarm={false,false,false}; double[] plat={20,25,15};
        check("probe_least_recently_observed", SparseProbeSelector.choose(plat,30,halarm,last)==1);
        check("probe_point_deadline_plausible", SparseProbeSelector.choose(new double[]{40,35,31},30,halarm,last)==-1);

        check("e312_event_counts", FrozenExperimentSpec.CALIBRATION_EVENTS==80000 && FrozenExperimentSpec.DEPLOYMENT_EVENTS==30000 && FrozenExperimentSpec.CHANGE_TASK==10000);
        check("e312_scenarios", FrozenExperimentSpec.Scenario.S1_LAMBDA_X2.arrivalMultiplier==2.0 && FrozenExperimentSpec.Scenario.S2_HIDDEN_COMPUTE_40LOSS.computeRetained==.60 && FrozenExperimentSpec.Scenario.S3_HIDDEN_NETWORK_50LOSS.bandwidthRetained==.50);

        System.out.printf("CORE_PARITY passed=%d failed=%d%n", passed, failed);
        if (failed != 0) System.exit(2);
    }
}
