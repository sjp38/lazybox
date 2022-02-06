#!/usr/bin/env python3

import argparse
import os
import subprocess
import time
import json

'''
Run the given commands if there were any update to given source code repos.
'''

tests = []
save_file = None

class HciTest:
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

    def tree_git_ref(self):
        return '%s/%s' % (self.tree[0], self.tree[2])

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

    def git_remote_added(self):
        try:
            remotes = subprocess.check_output(
                    ['git', '-C', self.repo, 'remote']).decode().strip().split()
            if not self.tree[0] in remotes:
                return False
        except subprocess.CalledProcessError as e:
            print('git remote failed')
            self.set_state_finished('skip', 'git remote check failed')
            return False
        return True

    def check_update(self):
        if self.state != 'check_update':
            return

        name, url, branch = self.tree
        git_cmd = ['git', '-C', self.repo]

        if not os.path.isdir(os.path.join(self.repo, '.git')):
            os.mkdir(self.repo)
            try:
                subprocess.check_output(git_cmd + ['init'])
            except subprocess.CalledProcessError as e:
                print('git init failed')
                self.set_state_finished('skip', 'git init failed')

        tracking = self.git_remote_added()
        if self.state == 'finished':
            return

        if not tracking:
            try:
                subprocess.check_output(git_cmd + ['remote', 'add', name, url])
                self.past_commit = None
            except subprocess.CalledProcessError as e:
                print('adding remote (\'%s\') failed' % self.tree_git_ref())
                self.set_state_finished('skip', 'adding remote failed')
        else:
            try:
                cmd = git_cmd + ['rev-parse', self.tree_git_ref()]
                commit = subprocess.check_output(cmd).decode().strip()
                self.past_commit = commit
            except subprocess.CalledProcessError as e:
                print('getting hash of %s failed' % self.tree_git_ref())
                self.set_state_finished('skip', 'getting past hash failed')

        if self.state == 'finished':
            return

        try:
            subprocess.check_output(git_cmd + ['fetch', name])
        except subprocess.CalledProcessError as e:
            print('fetching %s failed' % self.tree_git_ref())
            self.set_state_finished('skip', 'fetching failed')

        try:
            cmd = git_cmd + ['rev-parse', self.tree_git_ref()]
            commit = subprocess.check_output(cmd).decode().strip()
            self.current_commit = commit
        except subprocess.CalledProcessError as e:
            print('getting hash of %s failed' % self.tree_git_ref())
            self.set_state_finished('skip', 'getting current hash failed')

    def run(self):
        store_tests(tests, save_file)

        if self.state == 'init':
            store_tests(tests, save_file)
            self.state = 'check_update'

        if self.state == 'check_update':
            store_tests(tests, save_file)
            self.check_update()

            if self.past_commit == self.current_commit:
                self.set_state_finished('skip', 'no update')
            else:
                self.set_state('run')

        if self.state == 'run':
            store_tests(tests, save_file)
            ref_hash = '%s (%s)' % (self.tree_git_ref(), self.current_commit)
            # TODO: Allow installer do checkout by itself?
            print('# Checkout %s' % ref_hash)
            cmd = ['git', '-C', self.repo, 'checkout', '--quiet',
                    self.current_commit]
            try:
                subprocess.check_output(cmd)
            except subprocess.CalledProcessError as e:
                print('checkout %s out (\'%s\') failed' % (ref, ' '.join(cmd)))
                exit(1)

            print('# Run tasks for %s' % ref_hash)
            for cmd in self.cmds[self.nr_complete_cmds:]:
                try:
                    subprocess.check_output(cmd)
                    self.nr_complete_cmds += 1
                    self.set_state_finished('pass')
                except subprocess.CalledProcessError as e:
                    print('Task \'%s\' failed for %s' % (cmd, ref))
                    self.set_state_finished('fail')
                store_tests(tests, save_file)

        print('%s %s (skip reason: %s)' % (self.tree_git_ref(), self.result,
            self.skip_reason))

def store_tests(tests, file_path):
    maps = [x.__dict__ for x in tests]
    print(json.dumps(maps, indent=4))
    with open(file_path, 'w') as f:
        f.write(json.dumps(maps, indent=4))

def load_tests(file_path):
    if not os.path.isfile(file_path):
        return []

    with open(file_path, 'r') as f:
        maps = json.loads(f.read())

        tests = []
        for m in maps:
            test = HciTest(m['repo'], m['tree'], m['cmds'], m['state'])
            test.nr_complete_cmds = m['nr_complete_cmds']
            test.result = m['result']
            test.skip_reason = m['skip_reason']
            test.past_commit = m['past_commit']
            test.current_commit = m['current_commit']

            tests.append(test)
    return tests

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
    parser.add_argument('--save_file', metavar='<file>', default='.hci_tests',
            help='file to save the tests states')
    parser.add_argument('--delay', metavar='<seconds>', default=1800, type=int,
            help='delay between continuous tests')
    parser.add_argument('--count', metavar='<count>', default=0, type=int,
            help='how many times to do tests; 0 for infinite')
    args = parser.parse_args()

    global tests
    global save_file

    save_file = args.save_file

    tests = load_tests(save_file)
    finished = True
    for test in tests:
        if test.state != 'finished':
            finished = False
            break

    if finished:
        tests = []
        for tree in args.tree_to_track:
            tests.append(HciTest(
                args.repo, tree, args.cmds, 'init'))

    nr_repeats = 0
    while args.count == 0 or nr_repeats < args.count:
        if nr_repeats >= 1:
            print('# wait %d seconds' % args.delay)
            time.sleep(args.delay)
            tests = []
            for tree in args.tree_to_track:
                tests.append(HciTest(
                    args.repo, tree, args.cmds, 'init'))

        for test in tests:
            test.run()

        nr_repeats += 1

if __name__ == '__main__':
    main()
