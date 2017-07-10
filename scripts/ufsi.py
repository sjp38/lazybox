#!/usr/bin/env python

"""
Unusable Free Space Index

This script calculates `unusable free space index`[0] which represents degree
of fragmentation of system for given order of pages.  The paper describes the
value as below:

    Fu(j) = (TotalFree - sum([2**i * ki for i in range(j, n)])) / TotalFree

    `j` is the desired order of the desired allocation
    `TotalFree` is the number of free pages
    `n` is the largest order of allocation that can be satisfied
    `ki` is the number of free page blocks if order `i`

System has no fragmentation if the value is 0, has more fragmentation as the
value goes to 1.

[0] Gorman, Mel, and Andy Whitcroft. "The what, the why and the where to of
anti-fragmentation." Ottawa Linux Symposium. Vol. 1. 2006.
"""

import subprocess
import sys

if len(sys.argv) < 2:
    print "USAGE: %s <order of desired pages>" % sys.argv[0]
    exit(1)

order = int(sys.argv[1])

binfo = subprocess.check_output("cat /proc/buddyinfo".split())
"""
Node 0, zone      DMA      1      1      0      0      2      1      1
Node 0, zone    DMA32   3986   3751   3348   2811   2044   1233    760
Node 0, zone   Normal   2380    928   1518   7668  12639  12078  11520
Node 1, zone   Normal    681   2489   1869  12689  23714  23179  22081
"""

free_pages = []
for line in binfo.strip('\n').split('\n'):
    fields = line.split()
    free_pages.append([int(x) for x in fields[4:]])

totalfree = 0
for z in free_pages:
    for i, p in enumerate(z):
        totalfree += 2**i * p

nr_usable = 0
for z in free_pages:
    for i, p in enumerate(z[order:]):
        nr_usable += 2**(i+order) * p

print (totalfree - nr_usable) / float(totalfree)
