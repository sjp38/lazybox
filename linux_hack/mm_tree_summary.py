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

import argparse
import json
import os
import subprocess

os.sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'version_control')))

import git_remote_name
import review_stat

class Commit:
    hash = None
    author = None
    subject = None
    tags = None
    subsys_info_map = None

    def __init__(self, hash, author, subject, tags, subsys_info_map):
        self.hash = hash
        self.author = author
        self.subject = subject
        self.tags = tags
        self.subsys_info_map = subsys_info_map

    def role_of(self, person):
        for subsys_name, info in self.subsys_info_map.items():
            if 'maintainer' in info:
                maintainers = info['maintainer']
            else:
                maintainers = []
            if person in maintainers:
                return 'maintainer'

            if 'reviewer' in info:
                reviewers = info['reviewer']
            else:
                reviewers = []
            if person in reviewers:
                return 'reviewer'
        return None

    def review_score(self):
        '''
        0 - Not authored by a maintaienr or reviewer, no review
        1 - Not authored by a maintaienr or reviewer, reviewed by someone
        2 - Not authored by a maintaienr or reviewer, reviewed by reviewer
        3 - Not authored by a maintaienr or reviewer, reviewed by maintainer
        10 - Authored by reviewer, no review
        11 - Authored by reviewer, reviewed by someone
        12 - Authored by reviewer, reviewed by reviewer
        13 - Authored by reviewer, reviewed by maintainer
        20 - Authored by maintainer, no review
        21 - Authored by maintainer, reviewed by someone
        22 - Authored by maintainer, reviewed by reviewer
        23 - Authored by maintainer, reviewed by maintainer
        '''
        author_role = self.role_of(self.author)
        reviewer_roles = {}
        if 'Reviewed-by:' in self.tags:
            for reviewer in self.tags['Reviewed-by:']:
                reviewer_roles[self.role_of(reviewer)] = True
        if 'Acked-by:' in self.tags:
            for reviewer in self.tags['Acked-by:']:
                reviewer_roles[self.role_of(reviewer)] = True

        if author_role == 'maintainer':
            if 'maintainer' in reviewer_roles:
                return 23
            if 'reviewer' in reviewer_roles:
                return 22
            if None in reviewer_roles:
                return 21
            if len(reviewer_roles) == 0:
                return 20
        if author_role == 'reviewer':
            if 'maintainer' in reviewer_roles:
                return 13
            if 'reviewer' in reviewer_roles:
                return 12
            if None in reviewer_roles:
                return 11
            if len(reviewer_roles) == 0:
                return 10
        if author_role is None:
            if 'maintainer' in reviewer_roles:
                return 3
            if 'reviewer' in reviewer_roles:
                return 2
            if None in reviewer_roles:
                return 1
            if len(reviewer_roles) == 0:
                return 0

    def reviewed(self):
        return 'Reviewed-by:' in self.tags or 'Acked-by:' in self.tags

    def worrisome(self):
        if self.reviewed():
            return False
        if not 'Signed-off-by:' in self.tags:
            return True

        for subsys_name, info in self.subsys_info_map.items():
            if self.author in info['maintainer']:
                return False
        return True

    def to_kvpairs(self):
        return {
                'hash': self.hash,
                'author': self.author,
                'subject': self.subject,
                'tags': self.tags,
                'subsys_info_map': self.subsys_info_map,
                }

    @classmethod
    def from_kvpairs(cls, kvpairs):
        return Commit(
                kvpairs['hash'], kvpairs['author'], kvpairs['subject'],
                kvpairs['tags'], kvpairs['subsys_info_map'])

def import_json_branch_commits(json_file):
    with open(json_file, 'r') as f:
        kvpairs = json.load(f)
    baseline = kvpairs['baseline']
    branch_commits_kvpairs = kvpairs['branch_commits']
    branch_commits = {}
    for branch in branch_commits_kvpairs:
        branch_commits[branch] = [
                Commit.from_kvpairs(kvp)
                for kvp in branch_commits_kvpairs[branch]]
    return branch_commits, baseline

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
            git_cmd + ['log', '--pretty=%n---%n%H%n%an <%ae>%n%B',
                       '--name-only', '--no-merges',
                       commits_range]).decode().strip()
    commits = []
    for commit_output in output.split('\n---\n'):
        lines = commit_output.split('\n')
        if lines[0] == '---':
            lines = lines[1:]
        hash = lines[0]
        author = lines[1]
        subject = lines[2]

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
        commits.append(Commit(hash, author, subject, tags, subsys_info_map))
    return commits

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

def pr_stat(baseline, branches, branch_commits, subsystems,
            review_score_to_print_commits):
    print('baseline: %s' % baseline)
    for subsys in subsystems:
        print()
        print('# %s' % subsys)
        for branch in branches:
            filtered_commits = []
            review_score_commits = {}
            for commit in branch_commits[branch]:
                if subsys == 'all' or subsys in commit.subsys_info_map:
                    filtered_commits.append(commit)
                    review_score = commit.review_score()
                    if not review_score in review_score_commits:
                        review_score_commits[review_score] = []
                    review_score_commits[review_score].append(commit)
            print('%s: %d commits' % (branch, len(filtered_commits)))
            for score in sorted(review_score_commits.keys()):
                print('  - review score %d: %d commits' %
                      (score, len(review_score_commits[score])))
                if review_score_to_print_commits is not None and \
                        score in review_score_to_print_commits:
                    for c in review_score_commits[score]:
                        print('    - %s ("%s")' % (c.hash[:12], c.subject))

def pr_commits_per_mm_branches(
        linux_dir, export_json_file, import_json_file, subsystems,
        review_score_to_print_commits):
    # it is unclear what branch is base of what branch.  Just give commit to
    # unique branch, with the priorities.  Hotfixes are always important, and
    # mm is more important than nonmm.
    branches = ['mm-hotfixes-stable', 'mm-hotfixes-unstable',
                'mm-stable', 'mm-unstable', 'mm-new',
                'mm-nonmm-stable', 'mm-nonmm-unstable']

    if import_json_file is not None:
        branch_commits, baseline = import_json_branch_commits(import_json_file)
    else:
        branch_commits, baseline = get_mm_branch_commits(linux_dir, branches)

    if export_json_file is not None:
        to_dump = {'baseline': baseline}
        branch_commits_to_dump = {}
        for branch, commits in branch_commits.items():
            branch_commits_to_dump[branch] = [c.to_kvpairs() for c in commits]
        to_dump['branch_commits'] = branch_commits_to_dump
        with open(export_json_file, 'w') as f:
            json.dump(to_dump, f, indent=4)

    pr_stat(baseline, branches, branch_commits, subsystems,
            review_score_to_print_commits)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--linux_dir', metavar='<dir>', default='./',
                        help='path to linux local repo')
    parser.add_argument(
            '--export_info', metavar='<file>',
            help='export commits information in json for quick reuse')
    parser.add_argument('--import_info', metavar='<file>',
                        help='--export_info generated file to reuse')
    parser.add_argument('--subsystem', metavar='<subsystem name>', nargs='+',
                        default=['all'],
                        help='subsystem to show the summary for')
    parser.add_argument('--review_score_to_print_commits', nargs='+', type=int,
                        metavar='<score>',
                        help='list commits of this review score')
    args = parser.parse_args()

    pr_commits_per_mm_branches(
            args.linux_dir, args.export_info, args.import_info, args.subsystem,
            args.review_score_to_print_commits)

if __name__ == '__main__':
    main()
