#!/usr/bin/env python

import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--verbose', '-v', action='store_true', help='verbose output')
args = parser.parse_args()
verbose = args.verbose

res = subprocess.check_output("ps --no-headers -e -o pid".split())
pids = res.split()

nr_vmas_map = {}
for p in pids:
    try:
        with open("/proc/%s/maps" % p, 'r') as f:
            nr_vmas = 0
            for l in f:
                nr_vmas += 1
        nr_vmas_map[p] = nr_vmas
    except:
        pass

print "pid\tnr_vmas"
for p, n in sorted(nr_vmas_map.iteritems(), key=lambda (k,v): (v,k)):
    print "%s\t%d" % (p, nr_vmas_map[p])
print

nr_vmas_sorted = sorted(nr_vmas_map.values())
l = len(nr_vmas_sorted)
print "nr_procs: %d" % l
print "average_nr_vmas: %d" % (sum(nr_vmas_sorted) / l)
print "min\t25th\t50th\t75th\tmax"
print "%d\t%d\t%d\t%d\t%d" % (nr_vmas_sorted[0], nr_vmas_sorted[l / 4],
        nr_vmas_sorted[l / 4], nr_vmas_sorted[l / 4 * 3], nr_vmas_sorted[-1])
