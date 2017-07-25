#!/usr/bin/env python

"""
Report buddy allocator stat
"""

import subprocess
import sys

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
    print "%s %d (%d GiB)" % (" ".join(fields[0:4]), free_mem, free_mem / 2**30)
