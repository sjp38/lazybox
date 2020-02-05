#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', metavar='<memfree file>',
        help='file containing memfree data')
args = parser.parse_args()
filepath = args.file

free_values = []
with open(filepath, 'r') as f:
    for line in f:
        free_values.append(int(line.split()[1]))

initfree = free_values[0]
for idx, v in enumerate(free_values):
    print(idx, initfree - v)
