#!/usr/bin/env python

import sys

data = []
for line in sys.stdin:
    data.append(int(line.split()[1]))

data = sorted(data)

for i in range(100):
    print "%d, %d" % (i, data[len(data) / 100 * i])
