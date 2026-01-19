#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

'''
Similar to list_mm_patches, but use quilt series file.
'''

import argparse
import os

def pr_patch_detail(patch_name, series_path):
    series_dir = os.path.dirname(series_path)
    txt_dir = os.path.join(series_dir, '..', 'txt')
    txt_file = os.path.join(
            txt_dir, '%s.txt' % patch_name[:-1 * len('.patch')])
    if not os.path.isfile(txt_file):
        return False
    with open(txt_file, 'r') as f:
        txt = f.read()
    series_desc = None
    pars = txt.split('\n\n')
    for par in pars:
        par = par.strip()
        if par.startswith('Patch series '):
            series_desc = ' '.join(par.splitlines())
        if series_desc is not None and \
                par.startswith('This patch (of ') and par.endswith('):'):
            sz_series = int(par.split()[3][:-2])
            print('%s (%d patches)' % (series_desc, sz_series))
    for line in pars[0].splitlines():
        fields = line.split()
        if len(fields) == 0:
            continue
        if fields[0] == 'Subject:':
            print(' '.join(fields[1:]))
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('series', metavar='<file>', help='the series file')
    args = parser.parse_args()

    nr_patches = {'total': 0}
    branches = {}
    with open(args.series, 'r') as f:
        for line in f:
            fields = line.split()
            if fields[0] == '#BRANCH':
                branch_name = fields[1]
                branches[branch_name] = True
                if not branch_name in nr_patches:
                    nr_patches[branch_name] = 0
                print(line.strip())
                continue
            if fields[0] == '#ENDBRANCH':
                branches[fields[1]] = False
                print(line.strip())
                continue
            if line.startswith('#'):
                if len(fields) > 2:
                    print(' - %s' % line.strip())
                continue
            is_patch = pr_patch_detail(fields[0], args.series)
            if is_patch is False:
                continue
            for branch, now_in_it in branches.items():
                if now_in_it is False:
                    continue
                nr_patches[branch] += 1
            nr_patches['total'] += 1

    print()
    for branch, nr in nr_patches.items():
        print('%s: %d patches' % (branch, nr))

if __name__ == '__main__':
    main()
