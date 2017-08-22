#!/usr/bin/env python

import sys

if len(sys.argv) < 2:
    print "Usage: %s <field name>" % sys.argv[0]
    exit(1)

# example input line is output of `$ perf script`.  It may looks as below.
# command, pid, tid, timestamp, tracepoint name, and trace
#
# memwalk  3837 [012]   383.632199: kmem:mm_page_alloc: \
#           page=0x2f95b76 pfn=49896310 order=0 migratetype=0 \
#           gfp_flags=GFP_NOWAIT|__GFP_NOWARN

wanted = sys.argv[1]

data = []
for line in sys.stdin:
    tokens = line.split()
    try:
        time = float(tokens[3][:-1]) * 1000 * 1000 * 1000   # nano second level
    except ValueError:
        # ignore
        continue
    for fields in tokens[5:]:
        key, value = fields.split('=')
        if key == wanted:
            data.append(int(value))

average = -1
min_ = -1
max_ = -1
if len(data) > 0:
    average = sum(data) / float(len(data))
    min_ = min(data)
    max_ = max(data)
print "avg, min, max, count: %.3f, %d, %d, %d" % (
        average, min_, max_, len(data))
