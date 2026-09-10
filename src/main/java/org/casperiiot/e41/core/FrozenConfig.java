package org.casperiiot.e41.core;

public final class FrozenConfig {
    private FrozenConfig() {}

    public static final int EDGE_NODES = 12;
    public static final int FOG_NODES = 6;
    public static final int CLOUD_NODES = 3;
    public static final int TOTAL_NODES = 21;

    public static final double EPS_NORMAL = 0.10;
    public static final double EPS_HIGH = 0.05;
    public static final double EPS_MISSION = 0.01;
    public static final double[] RANK_WEIGHTS = {0.60, 0.30, 0.10};

    public static final int E17_SLOW_WINDOW = 200;
    public static final int E17_FAST_WINDOW = 50;
    public static final int E17_DETECTOR_WINDOW = 50;
    public static final int E17_DETECTOR_EXCEEDANCES = 12;
    public static final int E17_TRANSITION_HOLD = 200;
    public static final double E17_ETA_MIN = 1.0;
    public static final double E17_ETA_MAX = 3.0;

    public static final double TELEMETRY_PERIOD_MS = 50.0;
    public static final double SERVICE_HEALTH_ALPHA = 0.01;
    public static final int HEALTH_WINDOW = 8;
    public static final int HEALTH_EXCEEDANCES = 5;

    public static final double PROBE_BUDGET = 0.01;
    public static final int PROBE_EVERY_NORMAL = 100;

    public static double missionRankAlpha(int rankOneBased) {
        if (rankOneBased < 1 || rankOneBased > 3) throw new IllegalArgumentException("rank 1..3");
        return EPS_MISSION * RANK_WEIGHTS[rankOneBased - 1];
    }

    public static double clipEta(double eta) {
        return Math.max(E17_ETA_MIN, Math.min(E17_ETA_MAX, eta));
    }
}
