import java.lang.reflect.*;
import java.util.*;

/** Read-only reflection into ORIGINAL frozen E42 calibration rank and quantile methods. */
public final class OriginalCalibrationReferenceHarness {
    @SuppressWarnings({"unchecked","rawtypes"})
    public static void main(String[] ignored) throws Exception {
        final long seed=4202202640L;
        final Class<?> owner=Class.forName("org.casperiiot.e42.E42Campaign");
        final Class<?> scenario=Class.forName("org.casperiiot.e42.E42Campaign$Scenario");
        final Method makeTasks=owner.getDeclaredMethod("makeTasks",long.class,int.class,scenario);
        final Method ranks=owner.getDeclaredMethod("calibrationRanks",long.class,List.class);
        final Method qhat=owner.getDeclaredMethod("qhat",List.class,double.class);
        makeTasks.setAccessible(true);ranks.setAccessible(true);qhat.setAccessible(true);
        final Object stationary=Enum.valueOf((Class<? extends Enum>)scenario,"S0_STATIONARY");
        final List<?> tasks=(List<?>)makeTasks.invoke(null,seed ^ 0xCA11B4A7L,80000,stationary);
        final int[] rank=(int[])ranks.invoke(null,seed,tasks);
        int count=0;
        for(int i=10000;i<tasks.size();i++){
            Object t=tasks.get(i);
            Method crit=t.getClass().getDeclaredMethod("crit");crit.setAccessible(true);
            if(crit.invoke(t).toString().equals("MISSION")){
                System.out.printf(Locale.US,"JPDC_CAL_RANK,%d,%d%n",i,rank[i]);
                count++;
            }
        }
        System.out.printf(Locale.US,"JPDC_CAL_RANK_COUNT,%d%n",count);
        int[] sizes={0,1,2,10,99,199,200,997};
        double[] alphas={.006,.003,.001,.01,.10};
        for(int n:sizes){
            final List<Double> values=new ArrayList<>(n);
            for(int i=0;i<n;i++){
                values.add(.5+((i*37+11)%113)/100.0+(i%7)*1e-6);
            }
            for(int k=0;k<alphas.length;k++){
                double result=(double)qhat.invoke(null,values,alphas[k]);
                System.out.printf(Locale.US,"JPDC_CAL_QHAT,%d,%d,%.17g%n",n,k,result);
            }
        }
        System.out.println("JPDC_CALIBRATION_REFERENCE_COMPLETE");
    }
}
