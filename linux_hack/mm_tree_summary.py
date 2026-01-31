#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

'''
Show a summary of mm tree status.

TODO:
- Number of commits per branch for given sub-subsystems.
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

def nr_commits(linux_dir, commits_range):
    git_cmd = ['git', '-C', linux_dir]
    return len(subprocess.check_output(
        git_cmd + ['log', '--pretty=%h', commits_range]
        ).decode().strip().splitlines())

def pr_commits_per_mm_branches(linux_dir):
    mm_remote = git_remote_name.get_remote_name_for(
            linux_dir,
            'https://git.kernel.org/pub/scm/linux/kernel/git/akpm/mm.git')
    nr_commits_mm_hotfixes_stable = nr_commits(
            linux_dir, '%s/master..%s/mm-hotfixes-stable' %
            (mm_remote, mm_remote))
    print('mm-hotfixes-stable: %d commits' % nr_commits_mm_hotfixes_stable)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--linux_dir', metavar='<dir>', default='./',
                        help='path to linux local repo')
    args = parser.parse_args()

    pr_commits_per_mm_branches(args.linux_dir)

if __name__ == '__main__':
    main()
