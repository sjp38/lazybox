#!/usr/bin/env python

import os
import sys

fpath = os.path.realpath(os.path.dirname(__file__))
sys.path.append(fpath + '/../gen_report')
import ltldat

# Assumes table format of files_to.py only.

data = sys.stdin.read().strip().split('\n')[1:]
legends = data[0].split()[1:]
for idx, leg in enumerate(legends):
    print leg
    for line in data[1:]:
        fields = line.split()
        print "%s\t%s" % (fields[0], fields[idx + 1])
    if idx < len(legends) - 1:
        print "\n"
