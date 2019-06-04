#!/usr/bin/env python2.7

import sys

if len(sys.argv) != 2:
    print "Usage: %s <interval between lines>" % sys.argv[0]
    sys.exit(1)
interval=int(sys.argv[1])

i = 0
for l in sys.stdin:
    if i % interval == 0:
        print l.strip()
    i += 1
