#!/usr/bin/env python3

import sys

if len(sys.argv) < 3:
    print("Usage: %s <min> <max>" % sys.argv[0])
    sys.exit(1)

ymin = int(sys.argv[1])
ymax = int(sys.argv[2])

for l in sys.stdin:
    # We support hexadecimal with prefix '0x'
    yval = int(l.split()[1], 0)
    if yval > ymin and yval < ymax:
        print(l.strip())
