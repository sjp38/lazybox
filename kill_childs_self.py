#!/usr/bin/env python3

"""
Kill a process and its entire subprocesses
"""

import os
import signal
import subprocess
import sys
import time

import exp

if len(sys.argv) < 2:
    print("Usage: %s <process id>" % sys.argv[0])
    exit(1)

try:
    pid = int(sys.argv[1])
except:
    print("Wrong pid %s" % sys.argv[1])
    exit(1)

exp.kill_childs_self(pid)
