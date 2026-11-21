#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

'''
Cherry-pick commits in the given file, supporting comments and skipping.
'''

import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('commits_file', metavar='<file>',
                        help='file containing commits to cherry-pick')
    parser.add_argument('--start_from', metavar='<commit>',
                        help='commit to start cherry picking from')
    args = parser.parse_args()

    with open(args.commits_file, 'r') as f:
        text = f.read()
    for line in text.split('\n'):
        if line.startswith('#') or line == '':
            continue
        fields = line.split()
        if len(fields) < 1:
            continue
        commit = fields[0]
        if args.start_from is not None and commit != args.start_from:
            continue
        result = subprocess.run(['git', 'cherry-pick', commit])
        if result.returncode != 0:
            print('cherry-pick %s fail' % commit)
            exit(1)

if __name__ == '__main__':
    main()
