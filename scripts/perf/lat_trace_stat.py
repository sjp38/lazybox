#!/usr/bin/env python2.7

import sys

data = []
for line in sys.stdin:
    data.append(int(line.split()[1]))

average = -1
min_ = -1
max_ = -1
if len(data) > 0:
    average = sum(data) / float(len(data))
    min_ = min(data)
    max_ = max(data)
print "avg, min, max, count: %.3f, %d, %d, %d" % (
        average, min_, max_, len(data))
