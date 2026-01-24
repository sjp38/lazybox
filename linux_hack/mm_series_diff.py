#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

import argparse

import mm_series_patches

def patch_detail_of(subject, patch_details):
    for detail in patch_details:
        if detail.subject == subject:
            return detail
    return None

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

    branches = []
    with open(args.after, 'r') as f:
        for line in f:
            fields = line.split()
            if len(fields) == 2 and fields[0] == '#ENDBRANCH':
                branches.append(fields[1])

    print('Number of patches per branch')
    print()
    for branch in branches:
        if branch in before_nr_patches:
            before_nr = before_nr_patches[branch]
        else:
            before_nr = 0
        if branch in after_nr_patches:
            after_nr = after_nr_patches[branch]
        else:
            after_nr = 0
        print('%20s: %4d -> %4d (%4d)' % (
            branch, before_nr, after_nr, after_nr - before_nr))

    print()
    print('Patches newly added')
    for after in after_patch_details:
        if patch_detail_of(after.subject, before_patch_details) is not None:
            continue
        print('- %s' % after.subject)

    print()
    print('Patches dropped')
    for before in before_patch_details:
        if patch_detail_of(before.subject, after_patch_details) is not None:
            continue
        print('- %s' % before.subject)

if __name__ == '__main__':
    main()
