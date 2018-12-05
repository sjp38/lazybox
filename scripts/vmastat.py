#!/usr/bin/env python

import subprocess

res = subprocess.check_output("ps --no-headers -e -o pid".split())
pids = res.split()

nr_proc_vmas = []
for p in pids:
    try:
        with open("/proc/%s/maps" % p, 'r') as f:
            nr_vmas = 0
            for l in f:
                nr_vmas += 1
        nr_proc_vmas.append(nr_vmas)
    except:
        nr_proc_vmas.append(-1)

nr_vmas_sorted = sorted([n for n in nr_proc_vmas if n != -1])
l = len(nr_vmas_sorted)
print "nr_procs: %d" % l
print "average_nr_vmas: %d" % (sum(nr_vmas_sorted) / l)
print "min\t25th\t50th\t75th\tmax"
print "%d\t%d\t%d\t%d\t%d" % (nr_vmas_sorted[0], nr_vmas_sorted[l / 4],
        nr_vmas_sorted[l / 2], nr_vmas_sorted[l / 4 * 3], nr_vmas_sorted[-1])
