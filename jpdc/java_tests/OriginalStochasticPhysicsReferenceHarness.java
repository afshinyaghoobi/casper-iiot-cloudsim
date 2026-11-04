import java.lang.reflect.*;
import java.util.*;

/** Read-only native reference into original frozen E42 stochastic physics. */
public final class OriginalStochasticPhysicsReferenceHarness {
    @SuppressWarnings({"unchecked","rawtypes"})
    public static void main(String[] ignored) throws Exception {
        Class<?> owner=Class.forName("org.casperiiot.e42.E42Campaign");
        Class<?> scenario=Class.forName("org.casperiiot.e42.E42Campaign$Scenario");
        Class<?> taskClass=Class.forName("org.casperiiot.e42.E42Campaign$Task");
        Class<?> nodeClass=Class.forName("org.casperiiot.e42.E42Campaign$NodeParams");
        Method mkNodes=owner.getDeclaredMethod("makeNodes",long.class);
        Method mkTasks=owner.getDeclaredMethod("makeTasks",long.class,int.class,scenario);
        Method affected=owner.getDeclaredMethod("affectedMask",long.class,scenario);
        Method nominal=owner.getDeclaredMethod("nominalServiceMs",taskClass,nodeClass);
        Method actual=owner.getDeclaredMethod("actualServiceMs",long.class,taskClass,int.class,double.class,double.class);
        Method network=owner.getDeclaredMethod("nominalNetworkMs",taskClass,nodeClass);
        for(Method m:new Method[]{mkNodes,mkTasks,affected,nominal,actual,network})m.setAccessible(true);
        int[] indices={0,1,2,9980,9999,10000,10001,10002,10004,11000,11999,13000,
                       15000,17000,19999,20000,21000,22000,23000,24000,25000,27000,29000,29999};
        String[] scenarios={"S0_STATIONARY","S1_LAMBDA_X2","S2_HIDDEN_COMPUTE_40LOSS",
            "S3_HIDDEN_NETWORK_50LOSS","S4_COMPOUND"};
        for(int seedIndex:new int[]{50,51}){
            long seed=4202202600L+seedIndex;
            Object[] nodes=(Object[])mkNodes.invoke(null,seed);
            for(String name:scenarios){
                Object sc=Enum.valueOf((Class<? extends Enum>)scenario,name);
                boolean[] mask=(boolean[])affected.invoke(null,seed,sc);
                StringBuilder bits=new StringBuilder();
                for(boolean value:mask)bits.append(value?'1':'0');
                System.out.printf(Locale.US,"STOCH_MASK,%d,%s,%s%n",seedIndex,name,bits);
                List<?> tasks=(List<?>)mkTasks.invoke(null,seed^0xD3F10A77L,30000,sc);
                double computeRetained=((Number)scenario.getDeclaredField("computeRetained").get(sc)).doubleValue();
                double bwRetained=((Number)scenario.getDeclaredField("bwRetained").get(sc)).doubleValue();
                for(int i:indices){
                    Object t=tasks.get(i);
                    for(int node=0;node<21;node++){
                        double n=((Number)nominal.invoke(null,t,nodes[node])).doubleValue();
                        double mult=i>=10000 && mask[node] && computeRetained<1 ? 1/computeRetained:1;
                        double cpu=((Number)actual.invoke(null,seed,t,node,n,mult)).doubleValue();
                        double baseNet=((Number)network.invoke(null,t,nodes[node])).doubleValue();
                        double net=baseNet*(i>=10000&&mask[node]&&bwRetained<1?1/bwRetained:1);
                        System.out.printf(Locale.US,"STOCH_PAIR,%d,%s,%d,%d,%.17g,%.17g%n",
                            seedIndex,name,i,node,cpu,net);
                    }
                }
            }
        }
        System.out.println("STOCH_REFERENCE_COMPLETE");
    }
}
