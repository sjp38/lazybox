#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

import argparse

import mm_series_patches

def patch_detail_of(subject, patch_details):
    for detail in patch_details:
        if detail.subject == subject:
            return detail
    return None

def pr_new_patch(detail, before_branches, last_detail):
    pr_patch_series = False
    if detail.patch_series is not None:
        if last_detail is None:
            pr_patch_series = True
        elif last_detail.patch_series != detail.patch_series:
            pr_patch_series = True
    if pr_patch_series:
        print('- Patch series "%s" # %s patches' %
              (detail.patch_series, detail.sz_series))

    comments = []
    if before_branches != []:
        comments.append('was in %s' % ', '.join(before_branches))

    indent = ''
    if detail.patch_series is not None:
        comments.append('%s/%s series' % (detail.idx_series, detail.sz_series))
        indent = '  '

    fields = ['%s- %s' % (indent,detail.subject)]
    if comments != []:
        fields.append('# %s' % ', '.join(comments))
    print(' '.join(fields))

def pr_new_patches_in(branch, before_details, after_details):
    last_pr = None
    for after in after_details:
        if not branch in after.branches:
            continue
        if after.branches[branch] is False:
            continue
        before = patch_detail_of(after.subject, before_details)
        if before is None:
            before_branches = []
        else:
            before_branches = [
                    b for b in before.branches if before.branches[b] is True]
        if branch in before_branches:
            continue

        pr_new_patch(after, before_branches, last_pr)
        last_pr = after

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

    for branch in branches:
        print()
        print('Patches added to %s' % branch)
        pr_new_patches_in(branch, before_patch_details, after_patch_details)

if __name__ == '__main__':
    main()
