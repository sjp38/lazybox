#!/usr/bin/python3

import os
import sys

fpath = os.path.realpath(os.path.dirname(__file__))
sys.path.append(fpath + '/../')
import exp

if len(sys.argv) < 2:
    print("Usage: %s <pid>" % (sys.argv[0]))
    exit(1)

pid = int(sys.argv[1])

for pid in exp.childs_of(pid, False, print_tree=False):
    print(pid)
