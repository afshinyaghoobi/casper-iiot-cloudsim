#!/usr/bin/env python3
"""Unfrozen network-shock severity generalization; deployment only, calibration frozen.
Changes realized network delay AND counterfactual actual latency consistently.
"""
import sys
from pathlib import Path
percent=int(sys.argv[1])
assert percent in (25,50,75)
p=Path('src/main/java/org/casperiiot/e45/E45Campaign.java')
s=p.read_text()
assert s.count('scenario.bwRetained')==4,s.count('scenario.bwRetained')
# Only change references in actual-delay and counterfactual-delay computation,
# leaving immutable scenario metadata, seed logic and task generation unchanged.
s=s.replace('scenario.bwRetained<1.0','effectiveBwRetained(scenario)<1.0')
s=s.replace('1.0/scenario.bwRetained','1.0/effectiveBwRetained(scenario)')
s=s.replace('scenario.bwRetained<1)','effectiveBwRetained(scenario)<1)')
s=s.replace('1/scenario.bwRetained','1/effectiveBwRetained(scenario)')
assert s.count('effectiveBwRetained(scenario)')==4
needle='    public static void main(String[] args) throws Exception {'
helper='''    // Exploratory only: applied to actual and counterfactual network physics.
    private static double effectiveBwRetained(Scenario scenario) {
        return scenario==Scenario.S3_HIDDEN_NETWORK_50LOSS || scenario==Scenario.S4_COMPOUND
                ? PERCENT_RETAINED : scenario.bwRetained;
    }
    private static final double PERCENT_RETAINED = PERCENT_PLACEHOLDER;

'''
assert s.count(needle)==1
s=s.replace(needle,helper.replace('PERCENT_PLACEHOLDER',f'{percent/100:.2f}')+needle)
p.write_text(s)
print('NETWORK_GENERALIZATION_PATCH_PASS retained',percent,'percent')
