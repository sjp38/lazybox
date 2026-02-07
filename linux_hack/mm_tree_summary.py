#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

'''
Show a summary of mm tree status.
- Number of commits per branch for given sub-subsystems.
- List of commits per branch for given sub-subsystems.

TODO:
- Number of commits per branch for given sub-subsystems per review status
  - review stat
    - No review and not authored by a maintainer or a reviewer
    - Reviewed by someone
    - No review but authored by a reviewer
    - Reviewed by a reviewer
    - No reviewe but authored by a maintainer
    - Reviewed by a maintainer
'''

import os

import summary_trees

os.sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'version_control')))

import git_remote_name

def get_mm_branch_commits(linux_dir, branches):
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
            if commit.hash in categorized_commits:
                continue
            filtered_commits.append(commit)
            categorized_commits[commit.hash] = True
        branch_commits[branch] = filtered_commits
    baseline = subprocess.check_output(
            ['git', '-C', linux_dir, 'describe', '%s/master' %
             mm_remote, '--match', 'v*']).decode().strip()
    return branch_commits, baseline

def main():
    args = summary_trees.set_get_args(skip_branches_args=True)
    args.git_remote_name = git_remote_name.get_remote_name_for(
            args.linux_dir,
            'https://git.kernel.org/pub/scm/linux/kernel/git/akpm/mm.git')
    args.baseline = '%s/master' % args.git_remote_name
    args.branch = ['mm-hotfixes-stable', 'mm-hotfixes-unstable',
                     'mm-stable', 'mm-unstable', 'mm-new',
                     'mm-nonmm-stable', 'mm-nonmm-unstable']
    summary_trees.summary_trees(args)

if __name__ == '__main__':
    main()
