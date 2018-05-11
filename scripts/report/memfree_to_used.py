#!/usr/bin/env python

import sys

if len(sys.argv) < 2:
    print "Usage: %s <memfree file>" % sys.argv[0]
    exit(1)

filepath = sys.argv[1]

free_values = []
with open(filepath, 'r') as f:
    for line in f:
        free_values.append(int(line.split()[1]))

initfree = free_values[0]
for idx, v in enumerate(free_values):
    print idx, initfree - v
