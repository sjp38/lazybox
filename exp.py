#!/usr/bin/env python

"Describes class and functions for an experiment"

__author__ = "SeongJae Park"
__email__ = "sj38.park@gmail.com"
__copyright__ = "Copyright (c) 2013-2015, SeongJae Park"
__license__ = "GPLv3"

import datetime
import os
import signal
import subprocess
import time

def ltime():
    return datetime.datetime.now().strftime("[%H:%M:%S] ")

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

    def terminate_tasks(self):
        print ltime(), "terminate tasks of exp %s" % self
        for task in self.main_tasks:
            if task.popn.poll() == None:
                kill_childs_self(task.popn.pid)

        print ltime(), "kill background procs"
        for back_proc in self.back_procs:
            if back_proc.poll() == None:
                kill_childs_self(back_proc.pid)

    def execute(self):
        "Returns True if experiment executed successfully, False if not"
        self.back_procs = []
        self.main_tasks = []
        print ltime(), "do exp %s" % self
        for start in self.start_cmds:
            subprocess.call(start, shell=True, executable="/bin/bash")
        for back in self.back_cmds:
            self.back_procs.append(subprocess.Popen(back, shell=True,
                executable="/bin/bash"))

        for main in self.main_cmds:
            self.main_tasks.append(Task(main, subprocess.Popen(main,
                shell=True, executable="/bin/bash")))

        # If more than one main tasks specified, tasks terminated earlier
        # become infinite background job until slowest main task be terminated.
        nr_completed = 0
        while nr_completed < len(self.main_tasks):
            time.sleep(0.5)
            for task in self.main_tasks:
                if task.popn.poll() == None:
                    continue
                print ltime(), "%s(%s) terminated" % (task.cmd, task.popn.pid)
                task.completed = True
                nr_completed = sum(t.completed for t in self.main_tasks)
                if nr_completed < len(self.main_tasks):
                    task.popn = subprocess.Popen(task.cmd, shell=True,
                            executable="/bin/bash")
        self.terminate_tasks()

        for end in self.end_cmds:
            subprocess.call(end, shell=True, executable="/bin/bash")

        for check in self.check_cmds:
            ret = subprocess.call(check, shell=True, executable="/bin/bash")
            print ltime(), "check %s return %s" % (check, ret)
            if ret != 0:
                print ltime(), "check %s failed with return code %s" % (check, ret)
                return False
        return True

def kill_childs_self(pid):
    childs = all_childs(pid)
    for child in reversed(childs):
        if child == pid:
            continue
        try:
            # send INT, TERM and than KILL to give a chance to be terminated
            # well and than to ensure it terminated because TERM could be
            # handled by process while KILL couldn't.
            # Because the processes are stopeed by SIGSTOP that sent from
            # childs_of(), we should send SIGCONT, too.  It may spawn one more
            # child while it.  But, let's just hope for now...
            print ltime(), "kill child: ", child
            os.kill(child, signal.SIGINT)
            os.kill(child, signal.SIGCONT)
            time.sleep(2)   # kill_run_exps needs long time...
            os.kill(child, signal.SIGTERM)
            time.sleep(0.5)
            os.kill(child, signal.SIGKILL)
        except OSError as e:
            print ltime(), "error %s occurred while killing child %s" % (e, child)
    try:
        print ltime(), "kill self: %s" % pid
        os.kill(pid, signal.SIGTERM)
        os.kill(pid, signal.SIGKILL)
    except OSError as e:
        print ltime(), "error %s occurred while killing self %s" % (e, pid)

def all_childs(pid):
    while True:
        childs = childs_of(pid, True)
        childs_again = childs_of(pid, True)
        print ltime(), "got childs ", childs, "for first time"
        print ltime(), "got childs ", childs_again, "for second time"
        if cmp(childs, childs_again) != 0:
            print ltime(), "childs are not identical. get childs again"
            continue
        break
    return childs

def childs_of(pid, stop_childs):
    childs = []
    p = subprocess.Popen('pstree -p %s' % pid, shell=True,
            stdout=subprocess.PIPE, bufsize=1)
    for line in p.stdout:
        print ltime(), line
        spltd = line.split('(')
        for idx, entry in enumerate(spltd):
            # skip thread
            if idx > 0 and spltd[idx-1][-1] == '}':
                continue
            if entry.find(')') == -1:
                continue
            child_id = entry.split(')')[0]
            if not child_id.isdigit():
                continue
            if stop_childs:
                os.kill(int(child_id), signal.SIGSTOP)
            childs.append(int(child_id))
    return childs
