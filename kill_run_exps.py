#!/usr/bin/env python3

import argparse
import os
import signal
import subprocess
import sys
import time

import exp

parser = argparse.ArgumentParser()
parser.add_argument('exp_path', metavar='<exp file>', type=str)
args = parser.parse_args()

exp_path = args.exp_path

print("\n\n%s[kill_run_exps] It's time to say good-bye, run_exps %s!\n\n"
        % (exp.ltime(), exp_path))

p = subprocess.Popen("ps -ef | grep run_exps.py",
        stdout=subprocess.PIPE, shell=True)
out, err = p.communicate()

print(out)

pid = 0
out = out.decode('utf-8').split('\n')
for line in out:
    spltd = line.split()
    if len(spltd) < 8:
        continue
    if spltd[7] != "python":
        continue
    if os.path.split(spltd[8])[1] != "run_exps.py":
        continue
    if spltd[9] != exp_path:
        continue
    pid = int(spltd[1])
    break

if pid == 0:
    print("the process not found...")
    exit(1)

while True:
    childs = exp.childs_of(pid, False)
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError as e:
        print("error %s while sending SIGTERM" % e)
    childs = exp.childs_of(pid, False)
    if len(childs) == 0:
        break
    print("childs of process %s still exists. send signal again after 1 sec" %
            pid)
    time.sleep(1)

print("\n\n%s[kill_run_exps] Now run_exps %s cleaned up!\n\n" % (
        exp.ltime(), exp_path))
