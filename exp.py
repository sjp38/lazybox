#!/usr/bin/env python

"Describes class and functions for an experiment"

__author__ = "SeongJae Park"
__email__ = "sj38.park@gmail.com"
__copyright__ = "Copyright (c) 2013-2015, SeongJae Park"
__license__ = "GPLv3"

import os
import signal
import subprocess
import time

class Task:
    cmd = None
    popn = None
    completed = False

    def __init__(self, cmd, popn):
        self.cmd = cmd
        self.popn = popn

class Exp:
    start_cmds = []
    end_cmds = []
    main_cmds = []
    back_cmds = []
    check_cmds = []

    main_tasks = []
    back_procs = []

    def __init__(self, start, main, back, end, check):
        self.start_cmds = start
        self.end_cmds = end
        self.main_cmds = main
        self.back_cmds = back
        self.check_cmds = check

    def __str__(self):
        return "{EXP:\n\tstart: %s\n\tmain: %s\n\tback: %s\n\tend: %s\n\tcheck: %s\n}" % (
                self.start_cmds, self.main_cmds, self.back_cmds, self.end_cmds,
                self.check_cmds)

    def __repr__(self):
        return self.__str__()

    def execute(self):
        "Returns True if experiment executed successfully, False if not"
        self.back_procs = []
        self.main_tasks = []
        print "do exp %s" % self
        for start in self.start_cmds:
            subprocess.call(start, shell=True, executable="/bin/bash")
        for back in self.back_cmds:
            self.back_procs.append(subprocess.Popen(back, shell=True,
                executable="/bin/bash", preexec_fn=os.setsid))

        for main in self.main_cmds:
            self.main_tasks.append(Task(main, subprocess.Popen(main,
                shell=True, executable="/bin/bash", preexec_fn=os.setsid)))

        # If more than one main tasks specified, tasks terminated earlier
        # become infinite background job until slowest main task be terminated.
        nr_completed = 0
        while nr_completed < len(self.main_tasks):
            time.sleep(0.5)
            for task in self.main_tasks:
                if task.popn.poll() == None:
                    continue
                print "%s(%s) terminated" % (task.cmd, task.popn.pid)
                task.completed = True
                nr_completed = sum(t.completed for t in self.main_tasks)
                if nr_completed < len(self.main_tasks):
                    task.popn = subprocess.Popen(task.cmd, shell=True,
                            executable="/bin/bash")
        print "whole main workloads done; kill zombie main procs"
        for task in self.main_tasks:
            if task.popn.poll() == None:
                kill_groupof(task.popn.pid, True)

        print "kill background procs"
        for back_proc in self.back_procs:
            if back_proc.poll() == None:
                kill_groupof(back_proc.pid, True)

        for end in self.end_cmds:
            subprocess.call(end, shell=True, executable="/bin/bash")

        for check in self.check_cmds:
            ret = subprocess.call(check, shell=True, executable="/bin/bash")
            print "check %s return %s" % (check, ret)
            if ret != 0:
                print "check %s failed with return code %s" % (check, ret)
                return False
        return True

def kill_groupof(pid, show_hierarchy=False):
    print "now kill process group %s" % os.getpgid(pid)
    if show_hierarchy:
        cmd = 'ps -aeo "%p %r %P %c %a" | grep ' + "%s" % pid
        print cmd
        os.system(cmd)
        cmd = "pstree -p %s" % pid
        print cmd
        p = subprocess.Popen(cmd, shell=True,
                stdout=subprocess.PIPE, bufsize=1)
        while True:
            line = p.stdout.readline()
            if line == '' and p.poll() != None:
                break
            print line

    os.killpg(os.getpgid(pid), 15)
