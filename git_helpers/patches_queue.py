#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

import argparse
import os
import subprocess

def assemble_tree(repo, series_file):
    patches_dir = os.path.dirname(series_file)
    git_cmd = ['git', '-C', repo]

    with open(series_file, 'r') as f:
        baseline_checkout_done = False
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                continue
            # first non-comment line is the baseline
            if baseline_checkout_done is False:
                rc = subprocess.call(git_cmd + ['checkout', line])
                if rc != 0:
                    print('baseline checkout failed')
                    exit(1)
                baseline_checkout_done = True
                continue
            patch = os.path.join(patches_dir, line)
            rc = subprocess.call(git_cmd + ['am', patch])
            if rc != 0:
                print('git am %s failed' % patch)
                exit(1)

def make_patches_series(series_file, commits):
    print('convert commits to patches series')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dst')
    parser.add_argument('src')
    parser.description = 'Convert commits to/from patches series.'
    args = parser.parse_args()

    if os.path.isfile(args.src):
        assemble_tree(args.dst, args.src)
    else:
        make_patches_series(args.dst, args.src)

if __name__ == '__main__':
    main()
