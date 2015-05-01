#!/usr/bin/env python

import sys

data_file = sys.argv[1]
target_cols = sys.argv[2:-1]
csv_gran = float(sys.argv[-1])

datas = []
counts = {}
cdf = {}

with open(data_file, 'r') as f:
    for line in f:
        data = []
        for target in target_cols:
            target_col = int(target)
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
    print "%s,%s" % (key, out_data)
