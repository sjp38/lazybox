#!/usr/bin/env python

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
print "avg, min, max: %.3f, %d, %d" % (average, min_, max_)
