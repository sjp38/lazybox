#!/usr/bin/env python3

import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('--max', type=int, default=100,
        help='max value in the data')
args = parser.parse_args()

keys = ["system_A", "systemB", "systemC"]
xaxes = range(1,5)

for idx, k in enumerate(keys):
    print(k)
    for x in xaxes:
        print("%d %d" % (x, random.randint(0, args.max)))
    if idx < len(keys) - 1:
        print("\n")
