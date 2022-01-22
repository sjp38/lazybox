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

if __name__ == '__main__':
    main()
