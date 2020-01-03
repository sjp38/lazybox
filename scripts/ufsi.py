#!/usr/bin/env python3

description = "Unusable Free Space Index"
epilog = """
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

import argparse
import subprocess
import sys

def human_readable_size_form(nr_bytes):
    if nr_bytes > 2**30:
        nr_bytes = "%.2f GiB" % (nr_bytes / 2.0**30)
    elif nr_bytes > 2**20:
        nr_bytes = "%.2f MiB" % (nr_bytes / 2.0**20)
    elif nr_bytes > 2**10:
        nr_bytes = "%.2f KiB" % (nr_bytes / 2.0**10)
    else:
        nr_bytes = "%d B" % nr_bytes
    return nr_bytes

parser = argparse.ArgumentParser(description=description, epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('order', type=int, metavar='<order>',
        help='order of desired pages')
args = parser.parse_args()
order = args.order

binfo = subprocess.check_output("cat /proc/buddyinfo".split()).decode('utf-8')
"""
Node 0, zone      DMA      1      1      0      0      2      1      1
Node 0, zone    DMA32   3986   3751   3348   2811   2044   1233    760
Node 0, zone   Normal   2380    928   1518   7668  12639  12078  11520
Node 1, zone   Normal    681   2489   1869  12689  23714  23179  22081
"""

zones = []
free_bdpages = []
for line in binfo.strip('\n').split('\n'):
    fields = line.split()
    zones.append(fields[:4])
    free_bdpages.append([int(x) for x in fields[4:]])

free_pages = []
for z in free_bdpages:
    free = 0
    for i, p in enumerate(z):
        free += 2**i * p
    free_pages.append(free)

usable_pages = []
for z in free_bdpages:
    usable = 0
    for i, p in enumerate(z[order:]):
        usable += 2**(i+order) * p
    usable_pages.append(usable)

SZ_PAGE = 4096

for i, z in enumerate(zones):
    print("%s: %f (total %s, usable %s)" % (' '.join(z),
            (free_pages[i] - usable_pages[i]) / float(free_pages[i]),
            human_readable_size_form(free_pages[i] * SZ_PAGE),
            human_readable_size_form(usable_pages[i] * SZ_PAGE)))
print("Total: %f (total %s, usable %s)" % (
        (sum(free_pages) - sum(usable_pages)) / float(sum(free_pages)),
        human_readable_size_form(sum(free_pages) * SZ_PAGE),
        human_readable_size_form(sum(usable_pages) * SZ_PAGE)))
