#!/usr/bin/env python

"Help performance evaluation experiments automation"

__author__ = "SeongJae Park"
__email__ = "sj38.park@gmail.com"
__copyright__ = "Copyright (c) 2013-2015, SeongJae Park"
__license__ = "GPLv3"

import os
import signal
import sys
import time
from exp import Exp

RETRY_LIMIT = 10

START = "start "
MAIN = "main "
BACK = "back "
END = "end "
CHECK = "check "

def parse_lines(f, exps, starts, mains, backs, ends, checks):
    prevline = ''
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
        elif line.startswith(CHECK):
            checks.append(line[len(CHECK):])
        elif len(line.split()) == 0 and len(mains) > 0:
            exps.append(Exp(starts, mains, backs, ends, checks))
            starts = []
            mains = []
            backs = []
            ends = []
            checks = []
    if len(mains) != 0:
        exps.append(Exp(starts, mains, backs, ends, checks))

def parse_file(filename):
    exps = []
    starts = []
    mains = []
    backs = []
    ends = []
    checks = []

    f = sys.stdin
    if filename != "stdin":
        f = open(filename)
    else:
        print "receive experiments specification from stdin"

    parse_lines(f, exps, starts, mains, backs, ends, checks)

    if filename != "stdin":
        f.close()

    return exps

got_sigterm = False
current_exps = []

def sig_handler(signal, frame):
    global current_exps
    global got_sigterm

    print "[run_exps] received signal %s" % signal
    got_sigterm = True
    for exp in current_exps:
        exp.terminate_tasks()
    exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "USAGE: %s <path to experiments spec file> ..." % sys.argv[0]
        exit(1)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    global current_exps
    for exp_file in sys.argv[1:]:
        current_exps = parse_file(exp_file)

        for exp in current_exps:
            success = False
            nr_retry = 0
            while not success and nr_retry < RETRY_LIMIT:
                # wait until sighandler do cleaning and exit().
                if got_sigterm:
                    time.sleep(1)
                    continue
                success = exp.execute()
                nr_retry += 1
