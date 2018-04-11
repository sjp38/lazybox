#!/usr/bin/env python

import random

keys = ["systemA", "systemB", "systemC"]
xaxes = range(1,5)

for idx, k in enumerate(keys):
    print k
    for x in xaxes:
        print "%d %d %d" % (x, random.randint(0, 100), random.randint(0,30))
    if idx < len(keys) - 1:
        print "\n"
