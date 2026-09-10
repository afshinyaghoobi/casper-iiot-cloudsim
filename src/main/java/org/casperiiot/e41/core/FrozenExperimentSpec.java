package org.casperiiot.e41.core;

public final class FrozenExperimentSpec {
    private FrozenExperimentSpec() {}
    public static final int CALIBRATION_EVENTS = 80_000;
    public static final int CALIBRATION_BURNIN = 10_000;
    public static final int DEPLOYMENT_EVENTS = 30_000;
    public static final int CHANGE_TASK = 10_000;
    public static final double BASE_ARRIVAL_TASKS_PER_SEC = 120.0;

    public enum Scenario {
        S0_STATIONARY(1.0,1.0,1.0),
        S1_LAMBDA_X2(2.0,1.0,1.0),
        S2_HIDDEN_COMPUTE_40LOSS(1.0,0.60,1.0),
        S3_HIDDEN_NETWORK_50LOSS(1.0,1.0,0.50);

        public final double arrivalMultiplier;
        public final double computeRetained;
        public final double bandwidthRetained;
        Scenario(double a,double c,double b){arrivalMultiplier=a;computeRetained=c;bandwidthRetained=b;}
    }
}
