#!/usr/bin/env python

import os
import subprocess
import sys
import time

"""Input file format
Input file format should specify start commands, main commands, background
commands(maybe profiler), and end comands.
start command prepare experiment, main command do workload, background command
may be profiler, end command should clean up experiment environment.

e.g.,
start insmod abc.ko
main bench1_config1
main bench2_config1
back pcm -ns 1
end rmmod abc.ko

start insmod abc.ko
main bench1_config2
main bench2_config2
back pcm -ns 1
end rmmod abc.ko

"""

START = "start"
MAIN = "main"
BACK = "back"
END = "end"

class Exp:
    start_cmds = []
    end_cmds = []
    main_cmds = []
    back_cmds = []

    main_procs = []
    back_procs = []

    def __init__(self, start, main, back, end):
        self.start_cmds = start
        self.end_cmds = end
        self.main_cmds = main
        self.back_cmds = back

    def __str__(self):
        return "{EXP:\n\tstart: %s\n\tmain: %s\n\tback: %s\n\tend: %s\n}" % (
                self.start_cmds, self.main_cmds, self.back_cmds, self.end_cmds)

    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "USAGE: %s <path to experiments spec file>" % sys.argv[0]
        exit(1)

    exps = []
    starts = []
    mains = []
    backs = []
    ends = []

    with open(sys.argv[1]) as f:
        for line in f:
            if line.startswith('#'):
                continue
            if line[-1] == '\n':
                line = line[:-1]
            if line.startswith(START):
                starts.append(line[len(START):])
            elif line.startswith(MAIN):
                mains.append(line[len(MAIN):])
            elif line.startswith(BACK):
                backs.append(line[len(BACK):])
            elif line.startswith(END):
                ends.append(line[len(END):])
            elif len(line.split()) == 0 and len(mains) > 0:
                exps.append(Exp(starts, mains, backs, ends))
                starts = []
                mains = []
                backs = []
                ends = []
    if len(mains) > 0:
        exps.append(Exp(starts, mains, backs, ends))

    for exp in exps:
        exp.back_procs = []
        print "do exp %s" % exp
        for start in exp.start_cmds:
            subprocess.call(start, shell=True, executable="/bin/bash")
        for back in exp.back_cmds:
            exp.back_procs.append(subprocess.Popen(back, shell=True,
                executable="/bin/bash"))
        for main in exp.main_cmds:
            exp.main_procs.append(subprocess.Popen(main, shell=True,
                executable="/bin/bash"))
        for main_proc in exp.main_procs:
            main_proc.wait()
        print "workload done. kill back procs."
        for back_proc in exp.back_procs:
            back_proc.kill()
        for end in exp.end_cmds:
            subprocess.call(end, shell=True, executable="/bin/bash")
