#!/usr/bin/env python3

import sys

cma_times_output = []

with open(sys.argv[1], 'r') as f:
    allocs_started = False
    cma_alloc_secs = 0.0
    cma_chunk_alloc_secs = 0.0
    for line in f:
        if line.find("Linux raspberrypi") != -1:
            if line.find("-gcma-") != -1:
                print("gcma")
                cma_times_output.append("gcma")
            elif line.find("-cma-") != -1:
                print("cma")
                cma_times_output.append("cma")
            elif line.find("-vanilla-") != -1:
                print("vanilla")
                cma_times_output.append("vanilla")

        if line.find("system") != -1 and line.find("elapsed") != -1:
            spltd = line.split()
            user = spltd[0].split("user")[0]
            system = spltd[1].split("system")[0]

            elapsed = spltd[2].split("elapsed")[0]
            elap_min = int(elapsed.split(":")[0])
            elap_sec = float(elapsed.split(":")[1])
            elapsed = elap_min * 60 + elap_sec

            cpu = spltd[3].split("%")[0]
            print(",%s,%s,%s,%s" % (user, system, elapsed,cpu))

        if line.find("cma_alloc()") != -1 and line.find("consumed") != -1:
            cma_alloc_secs += float(line.split()[-2]) / 1000 / 1000 / 1000
            if not allocs_started:
                allocs_started = True
        if line.find("vc_cma_alloc_chunks") != -1:
            cma_chunk_alloc_secs += float(line.split()[-2]) / 1000 / 1000 / 1000
        if line.find("cma_release") != -1:
            if not allocs_started:
                continue
            allocs_started = False
            cma_times_output.append(",%.6f, %.6f" % (
                                     cma_alloc_secs, cma_chunk_alloc_secs))
            cma_alloc_secs = 0.0
            cma_chunk_alloc_secs = 0.0

for line in cma_times_output:
    print(line)
