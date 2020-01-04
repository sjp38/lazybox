#!/usr/bin/env python3

"""
Stub for experiments config file generator

Experiments configuration file describes which experiments should be executed.
For simplicity, it is recommended to be linearly interpretable rather than
procedural. In other words, `loop` or `goto` is not recommended inside
experiments config file.

But, constraining people to write down repeating experiments manually is crime
against humanity. For the reason, it is recommended to write down each user's
own experiments config file generator using their familiar tools. To help
making each user's own generator, this file contains essential code for
automated experiments config file generation.

Users could use this file for their purpose by following steps:
    1. Copy this file
    2. Edit main loop inside the file which commented to be
    3. Run modified copy and redirect stdout to appropriate file

"""

__author__ = "SeongJae Park"
__email__ = "sj38.park@gmail.com"
__copyright__ = "Copyright (c) 2013-2015, SeongJae Park"
__license__ = "GPLv3"

import exp

exps = []

# !!! Edit below loop to fit on your purpose using Python language
for arg1 in [1, 2, 3, 4, 5]:
    for arg2 in ['a', 'b', 'abc']:
        starts = ["echo hi"]
        mains = ["echo main with %s %s > main.out" % (arg1, arg2)]
        # For multiple commands, code could be seems like below
        # mains = ["echo main with %s %s" % (arg1, arg2),
        #           "echo main2 with %s %s" % (arg2, arg1)]
        backs = ["echo back with %s" % (arg1)]
        ends = ["echo buy"]
        checks = ["grep main main.out"]

        # Do not forget to match indentation
        exps.append(exp.Exp(starts, mains, backs, ends, checks))

# !!! Do not edit code below
for exp in exps:
    for start in exp.start_cmds:
        print("start %s" % start)
    for main in exp.main_cmds:
        print("main %s" % main)
    for back in exp.back_cmds:
        print("back %s" % back)
    for end in exp.end_cmds:
        print("end %s" % end)
    for check in exp.check_cmds:
        print("check %s" % check)

    print('')
