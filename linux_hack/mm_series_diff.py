#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

import argparse

import mm_series_patches

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('before', metavar='<file>',
                        help='a series file of previous version')
    parser.add_argument('after', metavar='<file>',
                        help='a series file of later version')
    args = parser.parse_args()

    before_nr_patches, out_lines = mm_series_patches.read_series(args.before)
    before_patch_details = [e for e in out_lines
                            if type(e) is mm_series_patches.PatchDetail]

    after_nr_patches, out_lines = mm_series_patches.read_series(args.after)
    after_patch_details = [e for e in out_lines
                            if type(e) is mm_series_patches.PatchDetail]

    branches = set(
            list(before_nr_patches.keys()) + list(after_nr_patches.keys()))

    print('Number of patches per branch')
    print()
    for branch in sorted(branches):
        if branch in before_nr_patches:
            before_nr = before_nr_patches[branch]
        else:
            before_nr = 0
        if branch in after_nr_patches:
            after_nr = after_nr_patches[branch]
        else:
            after_nr = 0
        print('%20s: %4d -> %4d (%4d)' % (branch, before_nr, after_nr, after_nr -
                                     before_nr))
    return

if __name__ == '__main__':
    main()
