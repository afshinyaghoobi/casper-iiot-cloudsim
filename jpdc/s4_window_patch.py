from pathlib import Path
p=Path("src/main/java/org/casperiiot/e45/E45Campaign.java")
s=p.read_text()
needle='final List<MissionRec> late=post.size()<=LATE_MISSION?post:post.subList(post.size()-LATE_MISSION,post.size());'
assert s.count(needle)==1
s=s.replace(needle,needle+'''
        if(p==Policy.CASPER_FULL && s==Scenario.S4_COMPOUND) {
            for(int window : new int[]{250,500,1000,2000}) {
                final List<MissionRec> tail=post.size()<=window?post:post.subList(post.size()-window,post.size());
                System.out.printf(java.util.Locale.US,
                  "JPDC_WINDOW scenario=%s seed=%d size=%d lateDvr=%.9f lateFwc=%.9f%n",
                   s.name(),seed,window,meanBool(tail,MissionRec::dvr),meanBool(tail,MissionRec::fwc));
            }
            System.out.printf(java.util.Locale.US,"JPDC_WINDOW scenario=%s seed=%d size=POST lateDvr=%.9f lateFwc=%.9f%n",
              s.name(),seed,meanBool(post,MissionRec::dvr),meanBool(post,MissionRec::fwc));
        }
''')
p.write_text(s)
print("WINDOW_AUDIT_PATCH_PASS")
