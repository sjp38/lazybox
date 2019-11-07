#!/usr/bin/env python2.7

import random

keys = ["system_A", "systemB", "systemC"]
xaxes = range(1,5)

for idx, k in enumerate(keys):
    print k
    for x in xaxes:
        print "%d %d" % (x, random.randint(0, 100))
    if idx < len(keys) - 1:
        print "\n"
