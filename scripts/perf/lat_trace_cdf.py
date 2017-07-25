#!/usr/bin/env python

import sys

precision = 100
if len(sys.argv) > 1:
    precision = int(sys.argv[1])

data = []
for line in sys.stdin:
    data.append(int(line.split()[1]))

data = sorted(data)

for i in range(precision):
    idx = len(data) / precision * i
    print "%d, %d" % (100 / precision * i, data[idx])

print "%d, %d" % (100, data[-1])
