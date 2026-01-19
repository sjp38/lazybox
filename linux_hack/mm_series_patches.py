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
        return
    with open(txt_file, 'r') as f:
        txt = f.read()
    series_desc = None
    for par in txt.split('\n\n'):
        par = par.strip()
        if par.startswith('Patch series '):
            series_desc = ' '.join(par.splitlines())
        if series_desc is not None and \
                par.startswith('This patch (of ') and par.endswith('):'):
            sz_series = int(par.split()[3][:-2])
            print('%s (%d patches)' % (series_desc, sz_series))
            return

    for line in txt.splitlines():
        fields = line.split()
        if len(fields) == 0:
            continue
        if fields[0] == 'Subject:':
            print(' '.join(fields[1:]))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('series', metavar='<file>', help='the series file')
    args = parser.parse_args()

    with open(args.series, 'r') as f:
        for line in f:
            fields = line.split()
            if fields[0] == '#ENDBRANCH':
                print(fields[1])
                print()
            if line.startswith('#'):
                continue
            pr_patch_detail(fields[0], args.series)

if __name__ == '__main__':
    main()
