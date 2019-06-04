#!/usr/bin/env python2.7

import subprocess
import sys
import time

remaining_spawns = int(sys.argv[1]) - 1

if remaining_spawns > 0:
    print 'will spawn %d more child' % remaining_spawns
    cmd = '%s %d' % (__file__, remaining_spawns)
    subprocess.call(cmd, shell=True)

while True:
    time.sleep(3)
