#!/usr/bin/env python

import sys

data = []
for line in sys.stdin:
    data.append(int(line.split()[1]))

print "avg, min, max"
print "%.3f, %d, %d" % (sum(data) / float(len(data)), min(data), max(data))
