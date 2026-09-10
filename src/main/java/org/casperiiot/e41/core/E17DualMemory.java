package org.casperiiot.e41.core;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

/** Frozen E1.7 slow/fast dual-memory envelope. Eta is computed before the current outcome is observed. */
public final class E17DualMemory {
    private final double referenceQ95;
    private final Deque<Double> slow = new ArrayDeque<>(FrozenConfig.E17_SLOW_WINDOW);
    private final Deque<Double> recent = new ArrayDeque<>(FrozenConfig.E17_SLOW_WINDOW);
    private final Deque<Boolean> detector = new ArrayDeque<>(FrozenConfig.E17_DETECTOR_WINDOW);
    private boolean alarmEver;
    private int transitionAge = -1;

    public E17DualMemory(double[] calibrationReference) {
        if (calibrationReference.length < FrozenConfig.E17_SLOW_WINDOW) throw new IllegalArgumentException("need >=200 reference scores");
        double[] sorted = calibrationReference.clone();
        java.util.Arrays.sort(sorted);
        for (int i=0;i<FrozenConfig.E17_SLOW_WINDOW;i++) {
            int idx = (int)Math.floor(i * (sorted.length - 1.0) / (FrozenConfig.E17_SLOW_WINDOW - 1.0));
            slow.addLast(sorted[idx]);
        }
        referenceQ95 = empiricalQ(slow, .95);
    }

    public double etaBeforeOutcome() {
        final double slowEta = FrozenConfig.clipEta(referenceQ95 > 0 ? empiricalQ(slow,.95)/referenceQ95 : 1.0);
        if (transitionAge >= 0 && transitionAge < FrozenConfig.E17_TRANSITION_HOLD && recent.size() >= FrozenConfig.E17_FAST_WINDOW) {
            final List<Double> x = new ArrayList<>(recent);
            final List<Double> tail = x.subList(x.size()-FrozenConfig.E17_FAST_WINDOW, x.size());
            final double fastEta = FrozenConfig.clipEta(referenceQ95 > 0 ? empiricalQ(tail,.95)/referenceQ95 : 1.0);
            return Math.max(slowEta, fastEta);
        }
        return slowEta;
    }

    public void observe(double score) {
        push(slow, score, FrozenConfig.E17_SLOW_WINDOW);
        push(recent, score, FrozenConfig.E17_SLOW_WINDOW);
        push(detector, score > referenceQ95, FrozenConfig.E17_DETECTOR_WINDOW);
        if (!alarmEver && detector.size()==FrozenConfig.E17_DETECTOR_WINDOW) {
            int n=0; for(boolean b:detector) if(b) n++;
            if (n >= FrozenConfig.E17_DETECTOR_EXCEEDANCES) {
                alarmEver=true; transitionAge=0;
            }
        }
        if (transitionAge >= 0) transitionAge++;
    }

    public boolean alarmEver() { return alarmEver; }
    public int transitionAge() { return transitionAge; }
    public double referenceQ95() { return referenceQ95; }

    private static <T> void push(Deque<T> q, T x, int max) {
        if(q.size()==max) q.removeFirst();
        q.addLast(x);
    }

    private static double empiricalQ(Iterable<Double> values, double tau) {
        List<Double> l=new ArrayList<>(); for(double v:values) l.add(v);
        l.sort(Double::compareTo);
        int idx=(int)Math.ceil((l.size()-1)*tau);
        return l.get(idx);
    }
}
