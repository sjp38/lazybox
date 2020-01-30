#!/usr/bin/env python3

"""
Kill a process and its entire subprocesses
"""

import argparse
import os
import signal
import subprocess
import sys
import time

import exp

parser = argparse.ArgumentParser()
parser.add_argument('pid', metavar='<pid>', type=int,
        help = 'process id of target')
args = parser.parse_args()

pid = args.pid

exp.kill_childs_self(pid)
