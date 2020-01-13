#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('min', metavar='<min>', type=int, help='minimal y value')
parser.add_argument('max', metavar='<max>', type=int, help='maximum y value')
args = parser.parse_args()

ymin = args.min
ymax = args.max

for l in sys.stdin:
    # We support hexadecimal with prefix '0x'
    yval = int(l.split()[1], 0)
    if yval > ymin and yval < ymax:
        print(l.strip())
