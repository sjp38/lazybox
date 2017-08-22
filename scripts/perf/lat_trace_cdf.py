#!/usr/bin/env python

import sys

precision = 100
if len(sys.argv) > 1:
    precision = int(sys.argv[1])

data = []
for line in sys.stdin:
    data.append(int(line.split()[1]))

if len(data) == 0:
    exit(0)

data = sorted(data)

for i in range(precision):
    idx = len(data) / precision * i
    if idx == len(data):
        break
    print "%d %.3f" % (data[idx], 100.0 / precision * i)

print "%d %d" % (data[-1], 100)
