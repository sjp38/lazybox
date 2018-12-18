#!/usr/bin/env python

import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--target', nargs='+', help='specify target pids')
parser.add_argument('--verbose', '-v', action='store_true', help='verbose output')
args = parser.parse_args()
target_pids = args.target
verbose = args.verbose

res = subprocess.check_output("ps --no-headers -e -o pid,cmd".split())
procs = []
for l in res.split('\n'):
    fields = l.split()
    if len(fields) > 0:
        pid = fields[0]
    cmd = ""
    if len(fields) > 1:
        cmd = fields[1]
    procs.append("%s(%s)" % (pid, cmd))

nr_anon_vmas = 0
nr_file_vmas = 0

nr_vmas_map = {}
for p in procs:
    pid = p.split('(')[0]
    if target_pids and not pid in target_pids:
        continue
    try:
        with open("/proc/%s/maps" % pid, 'r') as f:
            nr_vmas = 0
            for l in f:
                nr_vmas += 1
                fields = l.split()
                if len(fields) < 6:
                    nr_anon_vmas += 1
                    continue
                if not fields[5] in ['[stack]', '[vvar]', '[vdso]',
                        '[vsyscall]']:
                    nr_file_vmas += 1
        nr_vmas_map[p] = nr_vmas
    except:
        pass

print "proc\tnr_vmas"
for p, n in sorted(nr_vmas_map.iteritems(), key=lambda (k,v): (v,k)):
    print "%s\t%d" % (p, nr_vmas_map[p])
print

nr_vmas_sorted = sorted(nr_vmas_map.values())
l = len(nr_vmas_sorted)
print "nr_procs: %d" % l
print "nr_total_vmas: %d" % sum(nr_vmas_sorted)
print "nr_anon_vmas: %d" % nr_anon_vmas
print "nr_file_vmas: %d" % nr_file_vmas
print "average_nr_vmas: %d" % (sum(nr_vmas_sorted) / l)
print "min\t25th\t50th\t75th\tmax"
print "%d\t%d\t%d\t%d\t%d" % (nr_vmas_sorted[0], nr_vmas_sorted[l / 4],
        nr_vmas_sorted[l / 4], nr_vmas_sorted[l / 4 * 3], nr_vmas_sorted[-1])
