#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('interval', metavar='<interval>', type=int,
        help='interval between lines')
args = parser.parse_args()
interval = args.interval

i = 0
for l in sys.stdin:
    if i % interval == 0:
        print(l.strip())
    i += 1
