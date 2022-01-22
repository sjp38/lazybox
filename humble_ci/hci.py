#!/usr/bin/env python3

import argparse
import os
import subprocess

'''
Assumption
- This script is periodically called by cron
Input
- path to the repo
- trees to check, and
- test to run against those
Works
- check if the trees have updated
- run the test against the updated ones, and
- provide the reports
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', metavar='<path>',
            help='path to the local repo')
    parser.add_argument('--tree_to_track',
            metavar=('<name>', '<url>', '<branch>'), nargs=3, action='append',
            help='remote tree to track')
    parser.add_argument('--test', metavar='<path>',
            help='test to run')
    args = parser.parse_args()

    if not args.repo or not args.tree_to_track or not args.test:
        print('all options should be given')
        exit(1)

    if not os.path.isdir(args.repo):
        name, url, branch = args.tree_to_track[0]
        # git clone --origin $name $url $args.repo
        cmd = 'git clone --origin'.split()
        cmd += [name, url, args.repo]
        try:
            subprocess.check_output(cmd)
        except subprocess.CalledProcessError as e:
            print('cloning the repo (\'%s\') failed' % ' '.join(cmd))
            exit(1)
        for name, url, branch in args.tree_to_track[1:]:
            cmd = ['git', '-C', args.repo, 'remote', 'add']
            cmd += [name, url]
            try:
                subprocess.check_output(cmd)
            except subprocess.CalledProcessError as e:
                print('adding retmote (\'%s\') failed' % ' '.join(cmd))
                exit(1)
        cmd = ['git', '-C', args.repo, 'remote', 'update']
        try:
            subprocess.check_output(cmd)
        except subprocess.CalledProcessError as e:
            print('updating remotes (\'%s\') failed' % ' '.join(cmd))
            exit(1)

    # check before-update commits
    before_update_commits = {}
    for name, url, branch in args.tree_to_track:
        ref_to_check = '%s/%s' % (name, branch)
        cmd = ['git', '-C', args.repo, 'rev-parse', ref_to_check]
        try:
            commit = subprocess.check_output(cmd).decode().strip()
        except subprocess.CalledProcessError as e:
            print('getting hash of %s (\'%s\') failed' %
                    (ref_to_check, ' '.join(cmd)))
            exit(1)
        before_update_commits[ref_to_check] = commit

    # update
    cmd = ['git', '-C', args.repo, 'remote', 'update']
    try:
        subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        print('updating remotes (\'%s\') failed' % ' '.join(cmd))
        exit(1)

    # check after-update commits
    after_update_commits = {}
    for name, url, branch in args.tree_to_track:
        ref_to_check = '%s/%s' % (name, branch)
        cmd = ['git', '-C', args.repo, 'rev-parse', ref_to_check]
        try:
            commit = subprocess.check_output(cmd).decode().strip()
        except subprocess.CalledProcessError as e:
            print('getting hash of %s (\'%s\') failed' %
                    (ref_to_check, ' '.join(cmd)))
            exit(1)
        after_update_commits[ref_to_check] = commit

    for ref in before_update_commits:
        if before_update_commits[ref] != after_update_commits[ref]:
            cmd = ['git', '-C', args.repo, 'checkout',
                    after_update_commits[ref]]
            try:
                subprocess.check_output(cmd)
            except subprocess.CalledProcessError as e:
                print('checkout %s out (\'%s\') failed' % (ref, ' '.join(cmd)))
                exit(1)

            try:
                subprocess.check_output(args.test)
            except subprocess.CalledProcessError as e:
                print('test failed for %s' % (ref))

if __name__ == '__main__':
    main()
