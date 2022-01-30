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

def run_tests(repo, before_update_commits, after_update_commits,
        installer, test):
    for ref in before_update_commits:
        if before_update_commits[ref] == after_update_commits[ref]:
            print('# Skip %s (%s): No update' %
                    (ref, after_update_commits[ref]))
            continue

        ref_hash = '%s (%s)' % (ref, after_update_commits[ref])
        print('# Checkout %s' % ref_hash)
        cmd = ['git', '-C', repo, 'checkout', '--quiet',
                after_update_commits[ref]]
        try:
            subprocess.check_output(cmd)
        except subprocess.CalledProcessError as e:
            print('checkout %s out (\'%s\') failed' % (ref, ' '.join(cmd)))
            exit(1)

        if installer:
            print('# Install %s' % ref_hash)
            try:
                subprocess.check_output(installer)
            except subprocess.CalledProcessError as e:
                print('installer failed for %s' % ref)

        print('# Test %s' % ref_hash)
        test_passed = True
        try:
            subprocess.check_output(test)
        except subprocess.CalledProcessError as e:
            print('# FAIL %s' % ref_hash)
            test_passed = False
        if test_passed:
            print('# PASS %s' % ref_hash)

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
    parser.add_argument('--test', metavar='<path>',
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

        print('# get references before update')
        before_update_commits = get_refs_commits(args.repo, args.tree_to_track)
        print('# update remotes')
        git_remote_update(args.repo)
        print('# get references after update')
        after_update_commits = get_refs_commits(args.repo, args.tree_to_track)
        print('# run tests')
        run_tests(args.repo, before_update_commits, after_update_commits,
                args.installer, args.test)

        nr_repeats += 1

if __name__ == '__main__':
    main()
