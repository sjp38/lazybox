#!/usr/bin/env python

import sys

if len(sys.argv) != 2:
    print "Usage: %s <interval between lines>"
    sys.exit(1)
interval=int(sys.argv[1])

i = 0
for l in sys.stdin:
    if i % interval == 0:
        print l.strip()
    i += 1
