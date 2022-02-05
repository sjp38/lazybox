#!/usr/bin/env python3

import argparse
import os
import subprocess
import time
import json

'''
Checks update to the given program and run the given test if there was any
change.

Assumption
- This script is periodically called by cron, after boot
Input
- path to the repo
- trees to check, and
- test to run against those
Works
- check if the trees have updated
- run the test against the updated ones, and
- provide the reports

TODO
- cleanup code
- support installation
- support reboot
'''

class HciTest:
    repo = None
    tree = None # [remote name, remote url, branch]
    install_cmd = None
    test_cmd = None
    past_commit = None
    current_commit = None
    state = None # init, check_update, install, test, finished
    result = None # skip, pass, fail
    skip_reason = None

    def tree_git_ref(self):
        return '%s/%s' % (self.tree[0], self.tree[2])

    def __init__(self, repo, tree, install_cmd, test_cmd, state):
        self.repo = repo
        self.tree = tree
        self.install_cmd = install_cmd
        self.test_cmd = test_cmd
        self.state = state

    def set_state_finished(self, result, skip_reason=None):
        if not result in ['pass', 'fail', 'skip']:
            raise ValueError('wrong result \'%s\'' % result)
        if result == 'skip' and skip_reason == None:
            raise ValueError('skip reason is not given')
        self.state = 'finished'
        self.result = result
        self.skip_reason = skip_reason

    def set_state(self, state):
        valid_states = ['init', 'check_update', 'install', 'test']
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
        if self.state == 'init':
            self.state = 'check_update'

        if self.state == 'check_update':
            self.check_update()
            if self.past_commit == self.current_commit:
                self.set_state_finished('skip', 'no update')
            else:
                self.set_state('install')

        if self.state == 'install':
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

            if self.install_cmd:
                print('# Install %s' % ref_hash)
                try:
                    subprocess.check_output(self.install_cmd)
                    self.set_state('test')
                except subprocess.CalledProcessError as e:
                    print('install command failed for %s' % ref)
                    self.set_state_finished('skip', 'install failed')
            else:
                self.set_state('test')

        if self.state == 'test':
            print('# Test %s' % ref_hash)
            try:
                subprocess.check_output(self.test_cmd)
                print('# PASS %s' % ref_hash)
                self.set_state_finished('pass')
            except subprocess.CalledProcessError as e:
                print('# FAIL %s' % ref_hash)
                self.set_state_finished('fail')

        print('%s %s (skip reason: %s)' % (self.tree_git_ref(), self.result,
            self.skip_reason))

def store_tests(tests, file_path):
    maps = [x.__dict__ for x in tests]
    with open(file_path, 'w') as f:
        f.write(json.dumps(maps, indent=4))

def load_tests(file_path):
    with open(file_path, 'r') as f:
        maps = json.loads(f.read())

        tests = []
        for m in maps:
            test = HciTest(m['repo'], m['tree'], m['install_cmd'],
                    m['test_cmd'], m['state'])
            if 'result' in m:
                test.result = m['result']
            if 'skip_reason' in m:
                test.skip_reason = m['skip_reason']
            tests.append(test)
    return tests

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', metavar='<path>', required=True,
            help='path to the local repo')
    parser.add_argument('--tree_to_track', required=True,
            metavar=('<name>', '<url>', '<branch>'), nargs=3, action='append',
            help='remote tree to track')
    parser.add_argument('--install_cmd', metavar='<command>',
            help='install command')
    parser.add_argument('--test', metavar='<command>', required=True,
            help='test to run')
    parser.add_argument('--delay', metavar='<seconds>', default=1800, type=int,
            help='delay between continuous tests')
    parser.add_argument('--count', metavar='<count>', default=0, type=int,
            help='how many times to do tests; 0 for infinite')
    args = parser.parse_args()

    nr_repeats = 0
    while args.count == 0 or nr_repeats < args.count:
        if nr_repeats >= 1:
            print('# wait %d seconds' % args.delay)
            time.sleep(args.delay)

        tests = []
        for tree in args.tree_to_track:
            HciTest(args.repo, tree, args.install_cmd, args.test, 'init').run()

        nr_repeats += 1

if __name__ == '__main__':
    main()
