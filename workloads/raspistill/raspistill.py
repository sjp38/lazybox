#!/usr/bin/env python3

import os
import sys
import time

repeat = 10
warmup = 10

USAGE = "%s <repeat count> <warmup seconds> <output image path>"

if len(sys.argv) < 4:
    print("Usage: ", USAGE)
    exit(1)

repeat = int(sys.argv[1])
warmup = float(sys.argv[2])
img_path = sys.argv[3]

os.system("uname -a")

os.system("dmesg -c > /dev/null")
for i in range(repeat):
    cmd = "/usr/bin/time "
    cmd += "raspistill -t 1 -q 1 -o %s 2>&1" % img_path
    os.system(cmd)
    time.sleep(warmup)
    os.system("dmesg | grep cma")
    os.system("dmesg -c > /dev/null")
    time.sleep(2)
    print("")
