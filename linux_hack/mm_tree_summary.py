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
    patch_series = None
    patch_series_sz = None
    patch_series_idx = None

    def __init__(self, hash, author, subject, tags, subsys_info_map,
                 patch_series, patch_series_sz, patch_series_idx):
        self.hash = hash
        self.author = author
        self.subject = subject
        self.tags = tags
        self.subsys_info_map = subsys_info_map
        self.patch_series = patch_series
        self.patch_series_sz = patch_series_sz
        self.patch_series_idx = patch_series_idx

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
                'patch_series': self.patch_series,
                'patch_series_sz': self.patch_series_sz,
                'patch_series_idx': self.patch_series_idx,
                }

    @classmethod
    def from_kvpairs(cls, kvpairs):
        patch_series = kvpairs.get('patch_series', None)
        patch_series_sz = kvpairs.get('patch_series_sz', None)
        patch_series_idx = kvpairs.get('patch_series_idx', None)
        return Commit(
                kvpairs['hash'], kvpairs['author'], kvpairs['subject'],
                kvpairs['tags'], kvpairs['subsys_info_map'],
                patch_series, patch_series_sz, patch_series_idx)

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
                       '--name-only', '--no-merges', '--reverse',
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
        patch_series = None
        patch_series_sz = None
        patch_series_idx = None
        if pars[1].startswith('Patch series '):
            patch_series = pars[1][len('Patch series '):].replace('\n', ' ')
            for par in pars[2:]:
                if par.startswith('\nThis patch (of '):
                    if par.endswith('):'):
                        patch_series_sz = int(par[len('\nThis patch (of '):-2])
                    elif par.endswith(')'):
                        patch_series_sz = int(par[len('\nThis patch (of '):-1])
                    patch_series_idx = 0
                    break
        else:
            if len(commits) > 1:
                prev_commit = commits[-1]
                if prev_commit.patch_series is not None:
                    prev_patch_series = prev_commit.patch_series
                    prev_patch_series_sz = prev_commit.patch_series_sz
                    prev_patch_series_idx = prev_commit.patch_series_idx
                    if prev_patch_series_sz is not None and \
                            prev_patch_series_idx < prev_patch_series_sz - 1:
                        patch_series = prev_patch_series
                        patch_series_sz = prev_patch_series_sz
                        patch_series_idx = prev_patch_series_idx + 1
        commits.append(Commit(hash, author, subject, tags, subsys_info_map,
                              patch_series, patch_series_sz, patch_series_idx))
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

class Filter:
    allow = None
    matching = None
    category = None
    args = None

    def __init__(self, allow, matching, category, args):
        self.allow = allow
        self.matching = matching
        self.category = category
        self.args = args

    def role_match(self, role, to_check, commit):
        role_people = []
        for subsys_name, info in commit.subsys_info_map.items():
            if role == 'reviewer':
                role_people += info.get('reviewer', [])
            elif role == 'maintainer':
                role_people += info.get('maintainer', [])
        if role == 'norole':
            return not to_check in role_people
        return to_check in role_people

    def match(self, commit):
        if self.category == 'subsystem':
            for subsys in self.args:
                if subsys == 'all':
                    return self.matching
                if subsys in commit.subsys_info_map:
                    return self.matching
        elif self.category == 'author':
            for author in self.args:
                if author == commit.author:
                    return self.matching
                if self.role_match(author, commit.author, commit):
                    return self.matching
        elif self.category == 'reviewer':
            reviewers = commit.tags.get('Reviewed-by:', [])
            reviewers += commit.tags.get('Acked-by:', [])
            for reviewer in self.args:
                if reviewer == 'nobody' and reviewers == []:
                    return self.matching
                if reviewer in reviewers:
                    return self.matching
                for r in reviewers:
                    if self.role_match(reviewer, r, commit):
                        return self.matching
        return not self.matching

def should_filter_out(commit, filters):
    if len(filters) == 0:
        return False
    for filter in filters:
        if filter.match(commit):
            return not filter.allow
    return filters[-1].allow is True

def pr_stat(baseline, branches, branch_commits, subsystems, filters,
            full_commits_list, review_scores, review_score_to_print_commits):
    print('baseline: %s' % baseline)
    for subsys in subsystems:
        print()
        print('# %s' % subsys)
        for branch in branches:
            filtered_commits = []
            review_score_commits = {}
            nr_patch_series = 0
            nr_series_patches = 0
            nr_non_series_patches = 0
            for commit in branch_commits[branch]:
                if subsys == 'all' or subsys in commit.subsys_info_map:
                    if should_filter_out(commit, filters):
                        continue
                    filtered_commits.append(commit)
                    review_score = commit.review_score()
                    if not review_score in review_score_commits:
                        review_score_commits[review_score] = []
                    review_score_commits[review_score].append(commit)
                    if commit.patch_series is not None:
                        nr_series_patches += 1
                        if commit.patch_series_idx in [None, 0]:
                            nr_patch_series += 1
                    else:
                        nr_non_series_patches += 1
            print('%s: %d total, %d (%d) series, %d non-series commits' %
                  (branch, len(filtered_commits), nr_patch_series,
                   nr_series_patches, nr_non_series_patches))
            for score in sorted(review_score_commits.keys()):
                if not score in review_scores:
                    continue
                print('  - review score %d: %d commits' %
                      (score, len(review_score_commits[score])))
                if review_score_to_print_commits is not None and \
                        score in review_score_to_print_commits:
                    for c in review_score_commits[score]:
                        print('    - %s ("%s")' % (c.hash[:12], c.subject))
            if full_commits_list:
                for c in filtered_commits:
                    if c.patch_series is not None:
                        if c.patch_series_idx == 0:
                            print('  - sereis %s (%d commits)' %
                                  (c.patch_series, c.patch_series_sz))
                        print('    - %s %s (%s/%s)' %
                              (c.hash[:12], c.subject, c.patch_series_idx,
                               c.patch_series_sz))
                        print('      - review score: %d' % c.review_score())
                    else:
                        print('  - %s %s' % (c.hash[:12], c.subject))
                        print('    - review score: %d' % c.review_score())

def pr_commits_per_mm_branches(
        linux_dir, export_json_file, import_json_file, subsystems, filters,
        full_commits_list, review_scores, review_score_to_print_commits):
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

    pr_stat(baseline, branches, branch_commits, subsystems, filters,
            full_commits_list, review_scores, review_score_to_print_commits)

def args_to_filters(args):
    filters = []
    if args is not None:
        for filter_fields in args:
            if len(filter_fields) < 2:
                print('<2 fields: %s' % filter_fields)
                exit(1)
            allow_reject = filter_fields[0]
            if not allow_reject in ['allow', 'reject']:
                print('wrong allow_reject: %s' % filter_fields)
                exit(1)
            if filter_fields[1] == 'not':
                matching = False
                fields = filter_fields[2:]
            else:
                matching = True
                fields = filter_fields[1:]
            category = fields[0]
            filter_args = fields[1:]
            filters.append(Filter(
                allow_reject == 'allow', matching, category, filter_args))
    return filters

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
    parser.add_argument('--review_score', nargs='+', type=int,
                        metavar='<score>', default=[0, 1, 2, 3, 10, 11, 12, 13,
                                                    20, 21, 22, 23],
                        help='review scores to show stat for')
    parser.add_argument('--review_score_to_print_commits', nargs='+', type=int,
                        metavar='<score>',
                        help='list commits of this review score')
    parser.add_argument('--full_commits_list', action='store_true',
                        help='Show full list of commits')
    parser.add_argument('--filter', nargs='+', action='append',
                        help='<allow|reject> [not] <category> [option]...')

    # keywords: nobody, norole, reviewer, maintainer
    parser.add_argument('--reviewed_by', nargs='+', metavar='<person or role>',
                        help='filter commits by reviewers')
    parser.add_argument(
            '--not_reviewed_by', nargs='+', metavar='<person or role>',
            help='filter commits by reviewers')
    args = parser.parse_args()

    filters = args_to_filters(args.filter)

    pr_commits_per_mm_branches(
            args.linux_dir, args.export_info, args.import_info, args.subsystem,
            filters, args.full_commits_list, args.review_score,
            args.review_score_to_print_commits)

if __name__ == '__main__':
    main()
