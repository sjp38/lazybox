#!/usr/bin/env python

import sys

print_alloc_time = len(sys.argv) > 2

with open(sys.argv[1], 'r') as f:
    allocs_started = False
    alloc_times = 0
    for line in f:
        if line.find("Linux raspberrypi") != -1:
            if line.find("-gcma-") != -1:
                print "gcma"
            elif line.find("-cma-") != -1:
                print "cma"

        if not print_alloc_time:
            if line.find("system") != -1 and line.find("elapsed") != -1:
                spltd = line.split()
                user = spltd[0].split("user")[0]
                system = spltd[1].split("system")[0]
                elapsed = spltd[2].split("elapsed")[0]
                elap_min = int(elapsed.split(":")[0])
                elap_sec = float(elapsed.split(":")[1])
                elapsed = elap_min * 60 + elap_sec
                print "%s,%s,%s" % (user, system, elapsed)

        if not print_alloc_time:
            continue

        if line.find("cma_alloc") != -1:
            timestamp = float(line.split(']')[0][1:])
            if not allocs_started:
                allocs_started = True
                allocs_start_time = timestamp
            if line.find("returned") == -1:
                alloc_start_time = timestamp
            else:
                alloc_end_time = timestamp
                alloc_times += alloc_end_time - alloc_start_time
        if line.find("cma_release") != -1:
            if not allocs_started:
                continue
            allocs_started = False
            allocs_end_time = timestamp
            allocs_time = allocs_end_time - allocs_start_time
            print "alloc times: %.6f, allocs time: %.6f" % (alloc_times, allocs_time)
            alloc_times = 0
