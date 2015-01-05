#!/usr/bin/env python

"Help performance evaluation experiments automation"

__author__ = "SeongJae Park"
__email__ = "sj38.park@gmail.com"
__copyright__ = "Copyright (c) 2013, SeongJae Park"
__license__ = "GPLv3"

import os
import subprocess
import sys
import time

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

    def execute(self):
        self.back_procs = []
        print "do exp %s" % self
        for start in self.start_cmds:
            subprocess.call(start, shell=True, executable="/bin/bash")
        for back in self.back_cmds:
            self.back_procs.append(subprocess.Popen('exec ' + back, shell=True,
                executable="/bin/bash"))
        for main in self.main_cmds:
            self.main_procs.append(subprocess.Popen(main, shell=True,
                executable="/bin/bash"))
        for main_proc in self.main_procs:
            main_proc.wait()
        print "workload done. kill back procs."
        for back_proc in self.back_procs:
            back_proc.kill()
            back_proc.wait()
        for end in self.end_cmds:
            subprocess.call(end, shell=True, executable="/bin/bash")

def parse_file(filename):
    exps = []
    starts = []
    mains = []
    backs = []
    ends = []

    with open(filename) as f:
        for line in f:
            if line.startswith('#'):
                continue
            line = line.strip('\n')
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

    return exps

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "USAGE: %s <path to experiments spec file>" % sys.argv[0]
        exit(1)

    exps = parse_file(sys.argv[1])

    for exp in exps:
        exp.execute()
