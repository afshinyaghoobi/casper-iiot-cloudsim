package org.casperiiot.e41.core;

import java.util.ArrayDeque;
import java.util.Deque;

public final class NodeHealthDetector {
    private final double threshold;
    private final int window;
    private final int requiredExceedances;
    private final Deque<Boolean> recent;
    private boolean alarmed;

    public NodeHealthDetector(double threshold) {
        this(threshold, FrozenConfig.HEALTH_WINDOW, FrozenConfig.HEALTH_EXCEEDANCES);
    }

    public NodeHealthDetector(double threshold, int window, int requiredExceedances) {
        this.threshold = threshold;
        this.window = window;
        this.requiredExceedances = requiredExceedances;
        this.recent = new ArrayDeque<>(window);
    }

    public boolean observe(double actualServiceMs, double nominalPredictedServiceMs) {
        if (alarmed) return true;
        final double ratio = actualServiceMs / Math.max(nominalPredictedServiceMs, 1e-12);
        if (recent.size() == window) recent.removeFirst();
        recent.addLast(ratio > threshold);
        if (recent.size() == window) {
            int n = 0;
            for (boolean b : recent) if (b) n++;
            if (n >= requiredExceedances) alarmed = true;
        }
        return alarmed;
    }

    public boolean isAlarmed() { return alarmed; }
}
