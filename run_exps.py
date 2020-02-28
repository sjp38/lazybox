#!/usr/bin/env python3

"Help performance evaluation experiments automation"

__author__ = "SeongJae Park"
__email__ = "sj38.park@gmail.com"
__copyright__ = "Copyright (c) 2013-2020, SeongJae Park"
__license__ = "GPLv3"

import argparse
import os
import signal
import sys
import time

import exp

def parse_lines(f):
    START = "start "
    MAIN = "main "
    BACK = "back "
    END = "end "
    CHECK = "check "

    exps = []
    starts = []
    mains = []
    backs = []
    ends = []
    checks = []

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
            exps.append(exp.Exp(starts, mains, backs, ends, checks))
            starts = []
            mains = []
            backs = []
            ends = []
            checks = []
    if len(mains) != 0:
        exps.append(exp.Exp(starts, mains, backs, ends, checks))
    return exps

def parse_file(filename):
    f = sys.stdin
    if filename != 'stdin':
        f = open(filename)

    exps = parse_lines(f)

    if filename != 'stdin':
        f.close()

    return exps

got_sigterm = False
current_exps = []

def sig_handler(signal, frame):
    global current_exps
    global got_sigterm

    print('[run_exps] received signal %s' % signal)
    got_sigterm = True
    for exp in current_exps:
        exp.terminate_tasks()
    exit(1)

if __name__ == '__main__':
    RETRY_LIMIT = 10
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='store_true',
            help='Make some noisy log')
    parser.add_argument('--silence', '-s', action='store_true',
            help='Do not print log message at all')
    parser.add_argument('--dryrun', action='store_true',
            help='print what command will be executed only')
    parser.add_argument('exp_files', metavar='<file>', nargs='+',
            help='experiment spec file')
    args = parser.parse_args()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    dryrun = args.dryrun
    if args.verbose:
        exp.verbose = True
    if args.silence:
        exp.silence = True

    for exp_file in args.exp_files:
        current_exps = parse_file(exp_file)
        if dryrun:
            print(current_exps)
            continue

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
