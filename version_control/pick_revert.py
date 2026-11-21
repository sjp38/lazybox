#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

'''
Cherry-pick or revert commits in the given file, supporting comments and
skipping.
'''

import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('commits_file', metavar='<file>',
                        help='file containing commits to cherry-pick')
    parser.add_argument('--start_from', metavar='<commit>',
                        help='commit to start cherry picking from')
    parser.add_argument('--skip_pick_xs', action='store_true',
                        help='do not use -xs option for cherry-pick')
    args = parser.parse_args()

    with open(args.commits_file, 'r') as f:
        text = f.read()
    for line in text.split('\n'):
        if line.startswith('#') or line == '':
            continue
        fields = line.split()
        if len(fields) < 1:
            continue
        do_revert = False
        if fields[0] == 'revert':
            if len(fields) < 2:
                print('no commit for revert')
                exit(1)
            commit = fields[1]
        elif fields[0] == 'pick':
            if len(fields) < 2:
                print('no commit for pick')
                exit(1)
            commit = fields[1]
        else:
            commit = fields[0]
        if args.start_from is not None and commit != args.start_from:
            continue
        if do_revert is False:
            cmd = ['git', 'cherry-pick', commit]
            if not args.skip_pick_xs:
                cmd.append('-xs')
        else:
            cmd = ['git', 'revert', '-s', '--no-edit', commit]
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print('cherry-pick %s fail' % commit)
            exit(1)

if __name__ == '__main__':
    main()
