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
import review_stat

class Commit:
    hash = None
    tags = None
    subsys_info_map = None

    def __init__(self, hash, tags, subsys_info_map):
        self.hash = hash
        self.tags = tags
        self.subsys_info_map = subsys_info_map

commit_subsys_info_map = {}

def get_subsys_info_map(commit, touching_files, linux_dir):
    if commit in commit_subsys_info_map:
        return commit_subsys_info_map[commit]
    subsys_info_map = review_stat.get_subsys_of_files(
            touching_files, linux_dir)
    commit_subsys_info_map[commit] = subsys_info_map
    return subsys_info_map

def commits_in(linux_dir, commits_range):
    git_cmd = ['git', '-C', linux_dir]
    output = subprocess.check_output(
            git_cmd + ['log', '--pretty=%n---%n%H%n%B', '--name-only',
                       '--no-merges', commits_range]).decode().strip()
    commits = []
    for commit_output in output.split('\n---\n'):
        lines = commit_output.split('\n')
        hash = lines[0]

        pars = commit_output.split('\n\n')
        tag_lines = pars[-2].strip().splitlines()
        tags = {}
        for line in tag_lines:
            fields = line.split()
            tag = fields[0]
            if not tag in tags:
                tags[tag] = []
            tags[tag].append(line[len(tag) + 1:])

        touching_files = pars[-1].strip().splitlines()
        subsys_info_map = get_subsys_info_map(hash, touching_files, linux_dir)
        commits.append(Commit(hash, tags, subsys_info_map))
    return commits

def pr_commits_per_mm_branches(linux_dir, subsystems):
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

    for branch in branches:
        print('%s: %d commits' % (branch, len(branch_commits[branch])))
        nr_reviewed = len([c for c in branch_commits[branch] if
                           'Reviewed-by:' in c.tags or 'Acked-by:' in c.tags])
        print('  - %d reviewed' % nr_reviewed)
    print('Total: %d commits' % len(categorized_commits))

    if subsystems is None:
        return

    for subsys in subsystems:
        print()
        print('# %s' % subsys)
        for branch in branches:
            filtered_commits = []
            for commit in branch_commits[branch]:
                if subsys in commit.subsys_info_map:
                    filtered_commits.append(commit)
            print('%s: %d commits' % (branch, len(filtered_commits)))
            nr_reviewed = len(
                    [c for c in filtered_commits
                     if 'Reviewed-by:' in c.tags or 'Acked-by:' in c.tags])
            print('  - %d reviewed' % nr_reviewed)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--linux_dir', metavar='<dir>', default='./',
                        help='path to linux local repo')
    parser.add_argument('--subsystem', metavar='<subsystem name>', nargs='+',
                        help='subsystem to show the summary for')
    args = parser.parse_args()

    pr_commits_per_mm_branches(args.linux_dir, args.subsystem)

if __name__ == '__main__':
    main()
