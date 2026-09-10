package org.casperiiot.e41.core;

public final class SparseProbeBudget {
    private long normalArrivals;
    private long probes;

    /** Frozen E3.11 policy: only every 100th Normal arrival can be a probe. */
    public boolean onNormalArrival() {
        normalArrivals++;
        if (normalArrivals % FrozenConfig.PROBE_EVERY_NORMAL != 0) return false;
        final long maxAllowed = (long)Math.ceil(FrozenConfig.PROBE_BUDGET * normalArrivals);
        if (probes >= maxAllowed) return false;
        probes++;
        return true;
    }

    public long normalArrivals() { return normalArrivals; }
    public long probes() { return probes; }
    public double rate() { return normalArrivals == 0 ? 0.0 : probes / (double)normalArrivals; }
}
