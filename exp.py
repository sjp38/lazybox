#!/usr/bin/env python

"Describes class and functions for an experiment"

__author__ = "SeongJae Park"
__email__ = "sj38.park@gmail.com"
__copyright__ = "Copyright (c) 2013, SeongJae Park"
__license__ = "GPLv3"

import os
import signal
import subprocess

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
            self.back_procs.append(subprocess.Popen(back, shell=True,
                executable="/bin/bash"))
        for main in self.main_cmds:
            self.main_procs.append(subprocess.Popen(main, shell=True,
                executable="/bin/bash"))
        for main_proc in self.main_procs:
            main_proc.wait()
        print "workload done. kill back procs."
        for back_proc in self.back_procs:
            childs = all_childs(back_proc.pid)
            for child in reversed(childs):
                if child == back_proc.pid:
                    continue
                try:
                    print "kill ", child
                    os.kill(child, signal.SIGTERM)
                except OSError as e:
                    print "error %s occurred while killing child %s" % (
                            e, child)
            print "kill processes with ppid: ", back_proc.pid
            subprocess.call('pkill -P %d' % back_proc.pid, shell=True)
            os.kill(back_proc.pid, signal.SIGTERM)
        for end in self.end_cmds:
            subprocess.call(end, shell=True, executable="/bin/bash")

def all_childs(pid):
    childs = []
    p = subprocess.Popen('pstree -p %s' % pid, shell=True,
            stdout=subprocess.PIPE, bufsize=1)
    while True:
        line = p.stdout.readline()
        if line == '' and p.poll() != None:
            break
        print line
        spltd = line.split('(')
        for entry in spltd:
            if entry.find(')') != -1:
                child_id = entry.split(')')[0]
                if child_id.isdigit():
                    childs.append(int(child_id))
    return childs
