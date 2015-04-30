#!/usr/bin/env python

import os
import sys
import time

repeat = 10
warmup = 10

if len(sys.argv) > 1:
    repeat = int(sys.argv[1])

if len(sys.argv) > 2:
    warmup = float(sys.argv[2])

os.system("uname -a")

for i in range(repeat):
    cmd = "/usr/bin/time sudo nice -20 raspistill -t 1 -q 1 -o img.jpg 2>&1"
    os.system(cmd)
    time.sleep(warmup)
