#!/usr/bin/env python

import os

LOGPATH = "log"

for traffic in ["syn64", "wireshark"]:
    for workload in ["-p1 -H1 -m1 ' -c1 ' -t1",
                    "-p1 -H1 -m1 ' -c1 ' -t40",
                    "-p0 -H0 -m0 ' -c0 ' -t0",
                    "-p0 -H0 -m0 ' -c0 ' -t1",
                    "-p1 -H1 -m0 ' -c0 ' -t1",
                    "-p0 -H0 -m1 ' -c1 ' -t0",
                    "-p0 -H0 -m1 ' -c0 ' -t0",
                    "-p0 -H0 -m0 ' -c1 ' -t0",
                    "' -c3 '",
                    "' -c1f '",
                    "' -c1ff '",
                    "' -c1ffff '",
                    "' -c1ffffff '",
                    "' -c1ffffffff '"]:,
        keyword = traffic + " " + workload
        cmd = "./fpf_log_reduce.py %s %s" % (LOGPATH, keyword)
        os.system(cmd)
