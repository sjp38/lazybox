#!/usr/bin/env python

import sys

ymin = int(sys.argv[1])
ymax = int(sys.argv[2])

for l in sys.stdin:
	yval = int(l.split()[1], 0)
	if yval > ymin and yval < ymax:
		print l.strip()

