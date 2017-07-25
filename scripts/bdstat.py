#!/usr/bin/env python

"""
Report buddy allocator stat
"""

import subprocess
import sys
import time

def pr_buddystat():
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
        free_mem = 0
        for i, freep in enumerate(fields[4:]):
            free_mem += int(freep) * 2**i * 4096

        if free_mem > 2**30:
            free_mem = "%.2f GiB" % (free_mem / 2.0**30)
        elif free_mem > 2**20:
            free_mem = "%.2f MiB" % (free_mem / 2.0**20)
        elif free_mem > 2**10:
            free_mem = "%.2f KiB" % (free_mem / 2.0**10)
        else:
            free_mem = "%d B" % free_mem

        print "%s %s" % (" ".join(fields[0:4]), free_mem)

if __name__ == "__main__":
    delay = -1
    if len(sys.argv) > 1:
        delay = float(sys.argv[1])

    while True:
        pr_buddystat()
        if delay == -1:
            break
        time.sleep(delay)
