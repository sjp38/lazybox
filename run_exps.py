#!/usr/bin/env python

"Help performance evaluation experiments automation"

__author__ = "SeongJae Park"
__email__ = "sj38.park@gmail.com"
__copyright__ = "Copyright (c) 2013-2015, SeongJae Park"
__license__ = "GPLv3"

import sys
from exp import Exp

START = "start"
MAIN = "main"
BACK = "back"
END = "end"

def parse_file(filename):
    exps = []
    starts = []
    mains = []
    backs = []
    ends = []

    prevline = ''
    with open(filename) as f:
        for line in f:
            if line.startswith('#'):
                continue
            line = line.strip('\n').lstrip()
            if line.endswith('\\'):
                prevline += line[:-1]
                continue

            line = prevline + line
            prevline = ''
            if line.startswith(START):
                starts.append(line[len(START):])
            elif line.startswith(MAIN):
                mains.append(line[len(MAIN):])
            elif line.startswith(BACK):
                backs.append(line[len(BACK):])
            elif line.startswith(END):
                ends.append(line[len(END):])
            elif len(line.split()) == 0 and len(mains) > 0:
                exps.append(Exp(starts, mains, backs, ends))
                starts = []
                mains = []
                backs = []
                ends = []
    if len(mains) > 0:
        exps.append(Exp(starts, mains, backs, ends))

    return exps

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "USAGE: %s <path to experiments spec file>" % sys.argv[0]
        exit(1)

    exps = parse_file(sys.argv[1])

    for exp in exps:
        exp.execute()
