#!/usr/bin/env python

"Stub for experiments config file generator"

import exp

exps = []

# Edit below loop to fit on your purpose using Python language
for arg1 in [1, 2, 3, 4, 5]:
    for arg2 in ['a', 'b', 'abc']:
        starts = ["echo hi"]
        mains = ["echo main with %s %s" % (arg1, arg2)]
        backs = ["echo back with %s" % (arg1)]
        ends = ["echo buy"]

        # Do not edit code below
        exps.append(exp.Exp(starts, mains, backs, ends))

for exp in exps:
    for start in exp.start_cmds:
        print "start %s" % start
    for main in exp.main_cmds:
        print "main %s" % main
    for back in exp.back_cmds:
        print "back %s" % back
    for end in exp.end_cmds:
        print "end %s" % end
    print ""
