
import os
import sys

sys.path.append(os.environ['PERF_EXEC_PATH'] + \
	'/scripts/python/Perf-Trace-Util/lib/Perf/Trace')

from perf_trace_context import *
from Core import *


ev_per_time = autodict()

def pr_evcnts_in_time(evnames=[]):
    if not evnames:
        evnames = sorted(ev_per_time.keys())

    title = "  time"
    if len(evnames) == 0:
        return
    for n in evnames:
        title += ", %s" % n
    print title

    secs = sorted(ev_per_time[n])
    for s in secs:
        line = "%6s" % (s - secs[0])
        for n in evnames:
            count = 0
            if s in ev_per_time[n]:
                count = ev_per_time[n][s]
            line += ",%13s" % count
        print line

def nr_total_event(event):
    ret = 0
    for s in ev_per_time[event]:
        ret += ev_per_time[event][s]
    return ret

def event_names():
    return ev_per_time.keys()

def count_event(name, time, count):
    try:
        ev_per_time[name][time] += count
    except TypeError:
        ev_per_time[name][time] = count
