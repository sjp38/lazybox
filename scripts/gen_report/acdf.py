#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('data_file', metavar='<file>', type=str, help='data file')
parser.add_argument('target_column', metavar='<target column>', nargs='+',
        type=int, help='data file')
parser.add_argument('granularity', metavar='<granularity>', type=float,
        help='cdf granularity')
args = parser.parse_args()

data_file = args.data_file
target_cols = args.target_column
csv_gran = args.granularity

datas = []
counts = {}
cdf = {}

with open(data_file, 'r') as f:
    for line in f:
        data = []
        for target_col in target_cols:
            if len(line.split(',')) < target_col + 1:
                continue

            data.append(float(line.split(',')[target_col]))
        datas.append(data)

for data in datas:
    for idx, val in enumerate(data):
        key = int(val / csv_gran)
        if not counts.has_key(key):
            counts[key] = [0] * len(data)
        counts[key][idx] += 1

part_sums = [0] * len(sys.argv)
for key in sorted(counts):
    for idx, val in enumerate(counts[key]):
        if not cdf.has_key(key):
            cdf[key] = [0] * (len(sys.argv) - 3)
        cdf[key][idx] = counts[key][idx] + part_sums[idx]
        part_sums[idx] += counts[key][idx]

for key in sorted(cdf):
    out_data = ""
    for val in cdf[key]:
        out_data += str(val) + ','
    print("%s,%s" % (key, out_data))
