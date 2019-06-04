#!/usr/bin/env python2.7

import sys

nr_sample = 60

legend = []
data = []
thenext = False
for line in sys.stdin:
    splt = line.split()
    if len(splt) == 15 and splt[0] == 'timeDiff,':
        if len(legend) == 0:
            legend = splt
        thenext = True
        continue
    elif not thenext:
        continue
    thenext = False
    data.append([float(x) for x in line.split(',')])

if len(data) < 1:
    exit(1)

if len(data[0]) < 1:
    exit(1)

if len(data) > 60:
    data = data[-60:]

out = []
for i in range(len(data[0])):
    sum_ = 0
    for j in range(len(data)):
        sum_ += data[j][i]
    out.append(str(sum_ / len(data)))
print " ".join(legend)
print ", ".join(out)
