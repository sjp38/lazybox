#!/usr/bin/env python3

import argparse
import os
import subprocess
import time
import json

'''
Run the given commands if there were any update to given source code repos.
'''

tasks = []
save_file = None

class HciTasks:
    repo = None
    tree = None # [remote name, remote url, branch]
    cmds = None # list of commands to run for each update to each repo/tree
                # If any of command fails, we fail.
    nr_complete_cmds = None
    past_commit = None
    current_commit = None
    state = None # init, check_update, run, finished
    result = None # skip, pass, fail
    skip_reason = None

    def __init__(self, repo, tree, cmds, state):
        self.repo = repo
        self.tree = tree
        self.cmds = cmds
        self.nr_complete_cmds = 0
        self.state = state
        self.result = None
        self.skip_reason = None
        self.past_commit = None
        self.current_commit = None

    def set_state_finished(self, result, skip_reason=None):
        if not result in ['pass', 'fail', 'skip']:
            raise ValueError('wrong result \'%s\'' % result)
        if result == 'skip' and skip_reason == None:
            raise ValueError('skip reason is not given')
        self.state = 'finished'
        self.result = result
        self.skip_reason = skip_reason

    def set_state(self, state):
        valid_states = ['init', 'check_update', 'run']
        if not state in valid_states:
            raise ValueError('wrong state \'%s\'' % state)
        self.state = state

    def tree_git_ref(self):
        return '%s/%s' % (self.tree[0], self.tree[2])

    def git_cmd(self):
        return ['git', '-C', self.repo]

    def git_run(self, commands_list, description):
        cmd = self.git_cmd() + commands_list
        try:
            return subprocess.check_output(cmd).decode().strip()
        except subprocess.CalledProcessError as e:
            msg = 'Failed %s (%s)' % (description, ' '.join(cmd))
            print(msg)
            self.set_state_finished('skip', msg)
            return None

    def git_remote_added(self):
        remotes = self.git_run(['remote'], 'git remote check')
        if remotes == None:
            return None
        return self.tree[0] in remotes.split()

    def git_remote_fetched(self):
        remote_branches = self.git_run(['branch', '-r'], 'fetched check')
        if remote_branches == None:
            return None
        remote_branches = [line.split()[0] for line in
                remote_branches.split('\n')]
        return self.tree_git_ref() in remote_branches

    def git_commit_id(self, description):
        return self.git_run(['rev-parse', self.tree_git_ref()], description)

    def check_update(self):
        if self.state != 'check_update':
            return

        name, url, branch = self.tree
        git_ref = self.tree_git_ref()

        if not os.path.isdir(os.path.join(self.repo, '.git')):
            os.mkdir(self.repo)
            if self.git_run(['init'], 'repo init') == None:
                return

        remote_added = self.git_remote_added()
        if remote_added == None:
            return

        if not remote_added:
            self.past_commit = None
            if self.git_run(['remote', 'add', name, url],
                    'adding remote') == None:
                return
        else:
            remote_fetched = self.git_remote_fetched()
            if self.state == None:
                return
            if remote_fetched:
                commit = self.git_commit_id('getting old hash of %s' % git_ref)
                if commit == None:
                    return
                self.past_commit = commit

        if self.git_run(['fetch', name, branch],
                'fetching %s' % git_ref) == None:
            return

        commit = self.git_commit_id('getting new hash of %s' % git_ref)
        if commit == None:
            return
        self.current_commit = commit

    def run(self):
        store_tasks(tasks, save_file)

        if self.state == 'init':
            store_tasks(tasks, save_file)
            if uncond_single_run:
                self.set_state('run')
            else:
                self.state = 'check_update'

        if self.state == 'check_update':
            store_tasks(tasks, save_file)
            self.check_update()

            if self.past_commit == self.current_commit:
                self.set_state_finished('skip', 'no update')
            else:
                self.set_state('run')

        git_ref = self.tree_git_ref()
        if self.state == 'run':
            store_tasks(tasks, save_file)
            task_env = os.environ.copy()
            task_env["HUMBLE_CI_REPO"] = os.path.abspath(self.repo)
            task_env["HUMBLE_CI_REMOTE"] = self.tree[0]
            task_env["HUMBLE_CI_URL"] = self.tree[1]
            task_env["HUMBLE_CI_BRANCH"] = self.tree[2]

            for cmd in self.cmds[self.nr_complete_cmds:]:
                try:
                    output = subprocess.check_output(cmd, env=task_env,
                            shell=True)
                    if pr_cmd_output:
                        print('cmd %s output:\n%s' % (cmd, output.decode()))
                    self.nr_complete_cmds += 1
                    self.set_state_finished('pass')
                except subprocess.CalledProcessError as e:
                    print('Task \'%s\' failed for %s' % (cmd, git_ref))
                    self.set_state_finished('fail')
                store_tasks(tasks, save_file)

        print('%s %s (skip reason: %s)' % (git_ref, self.result,
            self.skip_reason))

def store_tasks(tasks, file_path):
    maps = [x.__dict__ for x in tasks]
    if pr_status:
        print(json.dumps(maps, indent=4))
    with open(file_path, 'w') as f:
        f.write(json.dumps(maps, indent=4))

def load_tasks(file_path):
    if not os.path.isfile(file_path):
        return []

    with open(file_path, 'r') as f:
        maps = json.loads(f.read())

        tasks = []
        for m in maps:
            task = HciTasks(m['repo'], m['tree'], m['cmds'], m['state'])
            task.nr_complete_cmds = m['nr_complete_cmds']
            task.result = m['result']
            task.skip_reason = m['skip_reason']
            task.past_commit = m['past_commit']
            task.current_commit = m['current_commit']

            tasks.append(task)
    return tasks

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', metavar='<path>', required=True,
            help='path to the local repo')
    parser.add_argument('--tree_to_track', required=True,
            metavar=('<name>', '<url>', '<branch>'), nargs=3, action='append',
            help='remote tree to track')
    parser.add_argument('--cmds', metavar='<command>', nargs='+',
            required=True,
            help='commands to run for each repo update')
    parser.add_argument('--uncond_single_run', action='store_true',
            help='unconditionally run the commands for the trees once')
    parser.add_argument('--save_file', metavar='<file>', default='.hci_tasks',
            help='file to save the tasks states')
    parser.add_argument('--delay', metavar='<seconds>', default=1800, type=int,
            help='delay between updates checks')
    parser.add_argument('--count', metavar='<count>', default=0, type=int,
            help='how many times to do update checks; 0 for infinite')
    parser.add_argument('--pr_status', action='store_true',
            help='print status whenever changed')
    parser.add_argument('--pr_cmd_output', action='store_true',
            help='print the cmds output')
    args = parser.parse_args()

    global tasks
    global save_file
    global pr_status
    global pr_cmd_output
    global uncond_single_run

    save_file = args.save_file
    pr_status = args.pr_status
    pr_cmd_output = args.pr_cmd_output
    uncond_single_run = args.uncond_single_run

    tasks = load_tasks(save_file)
    finished = True
    for task in tasks:
        if task.state != 'finished':
            finished = False
            break

    if finished:
        tasks = []
        for tree in args.tree_to_track:
            tasks.append(HciTasks(
                args.repo, tree, args.cmds, 'init'))

    nr_repeats = 0
    while args.count == 0 or nr_repeats < args.count:
        if nr_repeats >= 1:
            if uncond_single_run:
                break
            print('# wait %d seconds' % args.delay)
            time.sleep(args.delay)
            tasks = []
            for tree in args.tree_to_track:
                tasks.append(HciTasks(
                    args.repo, tree, args.cmds, 'init'))

        for task in tasks:
            task.run()

        nr_repeats += 1

if __name__ == '__main__':
    main()
