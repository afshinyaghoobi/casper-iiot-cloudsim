package org.casperiiot.e41.core;

import java.util.Arrays;

public final class Conformal {
    private Conformal() {}

    /** One-sided finite-sample split-conformal quantile. */
    public static double qhat(double[] scores, double alpha) {
        if (scores == null || scores.length == 0) return Double.POSITIVE_INFINITY;
        if (!(alpha > 0.0 && alpha < 1.0)) throw new IllegalArgumentException("alpha in (0,1)");
        final double[] s = scores.clone();
        Arrays.sort(s);
        final int n = s.length;
        final int k = (int)Math.ceil((n + 1.0) * (1.0 - alpha));
        return k > n ? Double.POSITIVE_INFINITY : s[k - 1];
    }

    public static double score(double actualLatency, double predictedLatency, double sigma, double delta) {
        return Math.max(0.0, (actualLatency - predictedLatency) / (sigma + delta));
    }

    public static double upper(double predictedLatency, double sigma, double q, double eta) {
        return predictedLatency + eta * q * sigma;
    }
}
