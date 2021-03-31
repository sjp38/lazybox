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
import sys

class Zone:
    name = None
    free_pages = []

    def __init__(self, name, free_pages):
        self.name = name
        self.free_pages = free_pages

    def nr_free_pages(self):
        ret = 0
        for order, nr_pages in enumerate(self.free_pages):
            ret += 2**order * nr_pages
        return ret

    def nr_usable_pages(self, order):
        ret = 0
        for idx, nr_pages in enumerate(self.free_pages[order:]):
            ret += 2**(order + idx) * nr_pages
        return ret

def hrsf(nr_bytes):
    "human readable size format"
    if nr_bytes > 2**30:
        nr_bytes = "%.2f GiB" % (nr_bytes / 2.0**30)
    elif nr_bytes > 2**20:
        nr_bytes = "%.2f MiB" % (nr_bytes / 2.0**20)
    elif nr_bytes > 2**10:
        nr_bytes = "%.2f KiB" % (nr_bytes / 2.0**10)
    else:
        nr_bytes = "%d B" % nr_bytes
    return nr_bytes

def main():
    parser = argparse.ArgumentParser(description=description, epilog=epilog,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('order', type=int, metavar='<order>',
            help='order of desired pages')
    args = parser.parse_args()
    order = args.order

    with open('/proc/buddyinfo', 'r') as f:
        binfo = f.read()
    """
    binfo is in below format:

    Node 0, zone      DMA      1      1      0      0      2      1      1
    Node 0, zone    DMA32   3986   3751   3348   2811   2044   1233    760
    Node 0, zone   Normal   2380    928   1518   7668  12639  12078  11520
    Node 1, zone   Normal    681   2489   1869  12689  23714  23179  22081
    """

    zones = []
    free_bdpages = []
    for line in binfo.strip('\n').split('\n'):
        fields = line.split()
        zone = Zone(' '.join(fields[:4]), [int(x) for x in fields[4:]])
        zones.append(zone)

    SZ_PAGE = 4096

    for zone in zones:
        usable = zone.nr_usable_pages(order) * SZ_PAGE
        total = zone.nr_free_pages() * SZ_PAGE
        print("%s: %f (total %s, usable %s)" % (zone.name,
            (total - usable) / total, hrsf(total), hrsf(usable)))

    usable = sum([z.nr_usable_pages(order) for z in zones]) * SZ_PAGE
    total = sum([z.nr_free_pages() for z in zones]) * SZ_PAGE
    print("Total: %f (total %s, usable %s)" % (
        (total - usable) / total, hrsf(total), hrsf(usable)))

if __name__ == '__main__':
    main()
