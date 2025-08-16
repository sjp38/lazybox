#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

import argparse

def assemble_tree(repo, series_file):
    print('assemble %s on %s' % (series_file, repo))

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
