#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

'''
Show a summary of mm tree status.
- Number of commits per branch for given sub-subsystems.

TODO:
- Number of commits per branch for given sub-subsystems per review status
  - review stat
    - No review
    - No review but authored by maintainer
    - No review but authored by reviewer
- List of commits per branch for given sub-subsystems.
'''

import argparse
import os
import subprocess

os.sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'version_control')))

import git_remote_name

def commits_in(linux_dir, commits_range):
    git_cmd = ['git', '-C', linux_dir]
    return subprocess.check_output(
            git_cmd + ['log', '--pretty=%H', '--no-merges', commits_range]
            ).decode().split()

def pr_commits_per_mm_branches(linux_dir):
    mm_remote = git_remote_name.get_remote_name_for(
            linux_dir,
            'https://git.kernel.org/pub/scm/linux/kernel/git/akpm/mm.git')

    # it is unclear what branch is base of what branch.  Just give commit to
    # unique branch, with the priorities.  Hotfixes are always important, and
    # mm is more important than nonmm.
    branches = ['mm-hotfixes-stable', 'mm-hotfixes-unstable',
                'mm-stable', 'mm-unstable', 'mm-new',
                'mm-nonmm-stable', 'mm-nonmm-unstable']
    branch_commits = {}
    categorized_commits = {}
    for idx, branch in enumerate(branches):
        commits = commits_in(
                linux_dir, '%s/master..%s/%s' % (mm_remote, mm_remote, branch))
        filtered_commits = []
        for commit in commits:
            if commit in categorized_commits:
                continue
            filtered_commits.append(commit)
            categorized_commits[commit] = True
        branch_commits[branch] = filtered_commits

    for branch in branches:
        print('%s: %d commits' % (branch, len(branch_commits[branch])))
    print('Total: %d commits' % len(categorized_commits))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--linux_dir', metavar='<dir>', default='./',
                        help='path to linux local repo')
    args = parser.parse_args()

    pr_commits_per_mm_branches(args.linux_dir)

if __name__ == '__main__':
    main()
