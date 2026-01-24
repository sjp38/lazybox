#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

'''
Similar to list_mm_patches, but use quilt series file.
'''

import argparse
import copy
import json
import os

class PatchDetail:
    patch_series = None
    sz_series = None
    idx_series = None
    subject = None
    author = None
    tags = None
    branches = None
    comments = None
    patch_file = None

    def __init__(self, patch_series, idx_series, sz_series, subject, author,
                 tags, branches, comments, patch_file):
        self.patch_series = patch_series
        self.idx_series = idx_series
        self.sz_series = sz_series
        self.subject = subject
        self.author = author
        self.tags = tags
        self.branches = branches
        self.comments = comments
        self.patch_file = patch_file

    def __str__(self):
        lines = []
        if self.patch_series is not None:
            lines.append(
                    '%s # %s patches' % (self.patch_series, self.sz_series))
        lines.append(self.subject)
        lines.append('# From: %s' % self.author)
        for tag, tagged_ones in self.tags.items():
            for tagged_one in tagged_ones:
                lines.append('# %s %s' % (tag, tagged_one))
        return '\n'.join(lines)

    def to_kvpairs(self):
        return self.__dict__

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

def get_patch_detail(patch_name, series_path, prev_patch, branches, comments):
    series_dir = os.path.dirname(series_path)
    txt_dir = os.path.join(series_dir, '..', 'txt')
    txt_file = os.path.join(
            txt_dir, '%s.txt' % patch_name[:-1 * len('.patch')])
    if not os.path.isfile(txt_file):
        return None

    patches_dir = os.path.join(series_dir, '..', 'patches')
    patch_file = os.path.join(patches_dir, patch_name)
    if not os.path.isfile(patch_file):
        patch_file = None
    else:
        patch_file = os.path.realpath(patch_file)

    series_desc = None
    idx_series = None
    sz_series = None
    subject = None
    author = None
    tags = {}

    with open(txt_file, 'r') as f:
        txt = f.read()
    pars = txt.split('\n\n')
    for par in pars:
        par = par.strip()
        if par.startswith('Patch series '):
            series_desc = ' '.join(par.splitlines())
            idx_series = 0
        if series_desc is not None and \
                par.startswith('This patch (of ') and par.endswith('):'):
            sz_series = int(par.split()[3][:-2])
    if series_desc is not None and sz_series is None:
        sz_series = 1
    for line in pars[0].splitlines():
        fields = line.split()
        if len(fields) == 0:
            continue
        if fields[0] == 'Subject:':
            subject = ' '.join(fields[1:])
        if fields[0] == 'From:':
            author = ' '.join(line.split()[1:])
    for line in pars[-1].splitlines():
        fields = line.split()
        if len(fields) < 2:
            continue
        if fields[0].endswith(':'):
            tag = fields[0]
            tagged = line[len(tag) + 1:]
            if not tag in tags:
                tags[tag] = []
            tags[tag].append(tagged)
    if series_desc is None and prev_patch is not None:
        if prev_patch.patch_series is not None and \
                prev_patch.sz_series is not None:
            if prev_patch.idx_series < prev_patch.sz_series - 1:
                series_desc = prev_patch.patch_series
                idx_series = prev_patch.idx_series + 1
                sz_series = prev_patch.sz_series
    return PatchDetail(series_desc, idx_series, sz_series, subject, author,
                       tags, branches, comments, patch_file)

def read_series(series_file):
    nr_patches = {'total': 0}
    branches = {}
    out_lines = []
    patch_comments = []
    with open(series_file, 'r') as f:
        prev_patch = None
        for line in f:
            fields = line.split()
            if len(fields) == 0:
                continue
            if fields[0] == '#BRANCH':
                branch_name = fields[1]
                branches[branch_name] = True
                if not branch_name in nr_patches:
                    nr_patches[branch_name] = 0
                out_lines.append(line.strip())
                continue
            if fields[0] == '#ENDBRANCH':
                branch_name = fields[1]
                branches[branch_name] = False
                out_lines.append('%s # %d patches' % (
                    line.strip(), nr_patches[branch_name]))
                continue
            if line.startswith('#'):
                if len(fields) > 2:
                    out_lines.append(line.strip())
                    patch_comments.append(line.strip())
                continue
            patch_detail = get_patch_detail(
                    fields[0], series_file, prev_patch,
                    copy.deepcopy(branches), patch_comments)
            if patch_detail is None:
                continue
            patch_comments = []
            prev_patch = patch_detail
            out_lines.append(patch_detail)
            for branch, now_in_it in branches.items():
                if now_in_it is False:
                    continue
                nr_patches[branch] += 1
            nr_patches['total'] += 1
    return nr_patches, out_lines

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('series', metavar='<file>', help='the series file')
    parser.add_argument('--output_format', choices=['text', 'json'],
                        default='text', help='output format')
    parser.add_argument('--comments', action='store_true',
                        help='print comments only')
    args = parser.parse_args()

    nr_patches, out_lines = read_series(args.series)

    if args.comments is True:
        for line in out_lines:
            if type(line) is str:
                print('- %s' % line)
        return

    if args.output_format == 'text':
        for branch in sorted(nr_patches.keys()):
            nr = nr_patches[branch]
            print('%s: %d patches' % (branch, nr))
        for line in out_lines:
            if type(line) is not PatchDetail and line.startswith('#BRANCH'):
                branch_name = line.split()[1]
                print('%s # %d patches' % (line, nr_patches[branch_name]))
                continue
            print('%s' % line)
    elif args.output_format == 'json':
        patch_details = [e for e in out_lines if type(e) is PatchDetail]
        print(json.dumps(
            [p.to_kvpairs() for p in patch_details], sort_keys=True, indent=4))

if __name__ == '__main__':
    main()
