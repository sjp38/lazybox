#!/usr/bin/env python3

import argparse
import os
import subprocess
import time

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

    def __init__(self, repo, tree, installer, test_cmd, state):
        self.repo = repo
        self.tree = tree
        self.installer = installer
        self.test_cmd = test_cmd
        self.state = state

def run_tests(tests):
    for test in tests:
        if test.state == 'finished':
            continue

        if test.state == 'install':
            ref_hash = '%s (%s)' % (test.tree_git_ref(), test.current_commit)
            # TODO: Allow installer do checkout by itself?
            print('# Checkout %s' % ref_hash)
            cmd = ['git', '-C', test.repo, 'checkout', '--quiet',
                    test.current_commit]
            try:
                subprocess.check_output(cmd)
            except subprocess.CalledProcessError as e:
                print('checkout %s out (\'%s\') failed' % (ref, ' '.join(cmd)))
                exit(1)

            if test.install_cmd:
                print('# Install %s' % ref_hash)
                try:
                    subprocess.check_output(test.install_cmd)
                    test.state = 'test'
                except subprocess.CalledProcessError as e:
                    print('installer failed for %s' % ref)
                    test.state = 'install_fail'
            else:
                test.state = 'test'

        if test.state == 'test':
            print('# Test %s' % ref_hash)
            try:
                subprocess.check_output(test.test_cmd)
                print('# PASS %s' % ref_hash)
                test.state = 'finished'
                test.result = 'pass'
            except subprocess.CalledProcessError as e:
                print('# FAIL %s' % ref_hash)
                test.state = 'finished'
                test.result = 'fail'

def git_remote_update(repo):
    cmd = ['git', '-C', repo, 'remote', 'update']
    try:
        subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        print('updating remotes (\'%s\') failed' % ' '.join(cmd))
        exit(1)

def set_repo(repo, trees_to_track):
    name, url, branch = trees_to_track[0]
    cmd = 'git clone --origin'.split()
    cmd += [name, url, repo]
    try:
        subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        print('cloning the repo (\'%s\') failed' % ' '.join(cmd))
        exit(1)
    for name, url, branch in trees_to_track[1:]:
        cmd = ['git', '-C', repo, 'remote', 'add']
        cmd += [name, url]
        try:
            subprocess.check_output(cmd)
        except subprocess.CalledProcessError as e:
            print('adding retmote (\'%s\') failed' % ' '.join(cmd))
            exit(1)
    git_remote_update(repo)

def get_refs_commits(repo, trees_to_track):
    refs_commits = {}

    if not os.path.isdir(repo):
        set_repo(repo, trees_to_track)
        for name, url, branch in trees_to_track:
            refs_commits['%s/%s' % (name, branch)] = None
        return refs_commits

    for name, url, branch in trees_to_track:
        ref_to_check = '%s/%s' % (name, branch)
        cmd = ['git', '-C', repo, 'rev-parse', ref_to_check]
        try:
            commit = subprocess.check_output(cmd).decode().strip()
        except subprocess.CalledProcessError as e:
            print('getting hash of %s (\'%s\') failed' %
                    (ref_to_check, ' '.join(cmd)))
            exit(1)
        refs_commits[ref_to_check] = commit
    return refs_commits

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', metavar='<path>',
            help='path to the local repo')
    parser.add_argument('--tree_to_track',
            metavar=('<name>', '<url>', '<branch>'), nargs=3, action='append',
            help='remote tree to track')
    parser.add_argument('--installer', metavar='<command>',
            help='installer program')
    parser.add_argument('--test', metavar='<command>',
            help='test to run')
    parser.add_argument('--delay', metavar='<seconds>', default=1800, type=int,
            help='delay between continuous tests')
    parser.add_argument('--count', metavar='<count>', default=0, type=int,
            help='how many times to do tests; 0 for infinite')
    args = parser.parse_args()

    if not args.repo or not args.tree_to_track or not args.test:
        print('all options should be given')
        exit(1)

    nr_repeats = 0
    while args.count == 0 or nr_repeats < args.count:
        if nr_repeats >= 1:
            print('# wait %d seconds' % args.delay)
            time.sleep(args.delay)

        tests = []
        for tree in args.tree_to_track:
            tests.append(HciTest(args.repo, tree, args.installer, args.test,
                'init'))

        print('# get references before update')
        for test in tests:
            test.state = 'check_update'
        before_update_commits = get_refs_commits(args.repo, args.tree_to_track)
        for test in tests:
            test.past_commit = before_update_commits[test.tree_git_ref()]

        print('# update remotes')
        git_remote_update(args.repo)

        print('# get references after update')
        after_update_commits = get_refs_commits(args.repo, args.tree_to_track)
        for test in tests:
            test.current_commit = after_update_commits[test.tree_git_ref()]

        print('# schedule tests')
        for test in tests:
            if test.past_commit == test.current_commit:
                test.state = 'finished'
                test.result = 'skip'
                test.skip_reason = 'no update'
            else:
                test.state = 'install'

        print('# run tests')
        run_tests(tests)

        for test in tests:
            print('%s %s' % (test.tree_git_ref(), test.result))

        nr_repeats += 1

if __name__ == '__main__':
    main()
