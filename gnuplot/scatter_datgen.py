#!/usr/bin/env python

import random

keys = ["systemA", "systemB", "systemC"]
xaxes = range(1,5)

for k in keys:
    print k
    for x in xaxes:
        print "%d %d" % (x, random.randint(0, 100))
    print "\n"
