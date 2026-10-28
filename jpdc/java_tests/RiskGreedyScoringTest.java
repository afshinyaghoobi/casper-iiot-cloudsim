/** Standalone behavioral test of generated-E45 risk-greedy selection semantics.
 * Does NOT run CloudSim and is NOT a simulation result. */
public final class RiskGreedyScoringTest {
  static double sigma(double predicted, double mult) {return (3.0 + .10 * predicted) * mult;}
  static int select(double[] pred, double[] mult, boolean[] eligible) {
    if (pred.length != mult.length || pred.length != eligible.length) throw new IllegalArgumentException("dimensions");
    int choice=-1;double best=Double.POSITIVE_INFINITY;
    for (int node=0;node<pred.length;node++) {
      if (!eligible[node]) continue;
      double score=pred[node]+sigma(pred[node],mult[node]);
      if(score<best){best=score;choice=node;}
    }
    if(choice<0) throw new IllegalArgumentException("no eligible nodes");
    return choice;
  }
  static void require(boolean ok, String why) {if(!ok)throw new AssertionError(why);}
  public static void main(String[] args) {
    require(select(new double[]{10,12},new double[]{1,1},new boolean[]{true,true})==0,"latency ranking");
    require(select(new double[]{10,10},new double[]{2,1},new boolean[]{true,true})==1,"uncertainty ranking");
    require(select(new double[]{10,10},new double[]{1,1},new boolean[]{true,true})==0,"stable tie");
    require(select(new double[]{1,10},new double[]{1,1},new boolean[]{false,true})==1,"eligibility");
    require(select(new double[]{10,10},new double[]{1.1,.9},new boolean[]{true,true})==1,"node sigma tier");
    boolean rejected=false;
    try { select(new double[]{10},new double[]{1},new boolean[]{false}); }
    catch(IllegalArgumentException ex){rejected=true;}
    require(rejected,"no eligible rejection");
    System.out.println("RISK_GREEDY_JAVA_SCORING_PASS 6 checks");
  }
}
