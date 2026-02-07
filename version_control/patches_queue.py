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

def final_patch_path(patch_name, patches_dir):
    name_wo_prefix_number = '-'.join(patch_name.split('-')[1:])
    name_wo_extension = name_wo_prefix_number[:-1 * len('.patch')]
    suffix = 0
    for existing_file in os.listdir(patches_dir):
        existing_name = existing_file[:-1 * len('.patch')]
        existing_name_fields = existing_name.split('-')
        if existing_name_fields[-1].isdigit():
            existing_name = '-'.join(existing_name_fields[:-1])
        if existing_name == name_wo_extension:
            suffix += 1

    final_path = os.path.join(patches_dir, name_wo_extension)
    if suffix > 0:
        final_path += '-%d' % suffix
    final_path += '.patch'
    return final_path

def make_patches_series(series_file, repo, commits_range, commits_list=[]):
    git_cmd = ['git', '-C', repo]
    patches_dir = os.path.dirname(series_file)

    patches_list = []
    commits = []
    if commits_range is not None:
        commits = subprocess.check_output(
                git_cmd + ['log', '--reverse', '--pretty=%H', commits_range])
        commits = commits.decode().strip().split()
    commits += commits_list
    for commit in commits:
        patch = subprocess.check_output(
                git_cmd + ['format-patch', '%s^..%s' % (commit, commit)])
        patch = patch.decode().strip()
        patch_path = os.path.join(repo, patch)
        # cut out first line magic timestamp line to avoid unnecessary diff
        with open(patch_path, 'r') as f:
            patch_lines = f.read().split('\n')
        with open(patch_path, 'w') as f:
            f.write('\n'.join(patch_lines[1:]))
        final_patch = final_patch_path(patch, patches_dir)
        os.rename(patch_path, final_patch)
        patches_list.append(os.path.basename(final_patch))
        print(final_patch)

    baseline = subprocess.check_output(
            git_cmd + ['describe', '%s^' % commits[0]]).decode().strip()
    with open(series_file, 'w') as f:
        f.write('\n'.join([baseline] + patches_list))
        f.write('\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--series')
    parser.add_argument('--commits')
    parser.add_argument('--repo', default='./',)
    parser.add_argument('--remote_update', action='store_true')
    parser.description = 'Convert commits to/from patches series.'
    args = parser.parse_args()

    if args.series is None:
        print('--series is not provided')
        exit(1)

    if args.commits is None:
        if args.remote_update:
            if subprocess.call(['git', '-C', args.repo, 'remote', 'update']):
                print('git remote update fail')
                exit(1)
        assemble_tree(args.repo, args.series)
    else:
        make_patches_series(
                args.series, args.repo, commits_range=args.commits,
                commits_list=[])

if __name__ == '__main__':
    main()
