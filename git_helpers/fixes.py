#!/usr/bin/env python3

import argparse
import os
import subprocess

import _git

def read_changes(files_and_or_commits, repo):
    changes = []
    for file_or_commits in files_and_or_commits:
        if os.path.isfile(file_or_commits):
            patch_file = file_or_commits
            changes.append(_git.Change(patch_file=patch_file))
        else:
            commits_range = file_or_commits
            cmd = ['git', '-C', repo, 'log', '--pretty=%H', commits_range]
            commits = subprocess.check_output(cmd).decode().strip().split()
            for commit in commits:
                changes.append(_git.Change(commit=commit, repo=repo))
    return changes

def print_fix_bug(fix, bug):
    if fix.patch:
        fix_str = fix.patch.file_name
    elif fix.commit:
        fix_str = '%s ("%s")' % (fix.commit.hashid[:12], fix.subject)
    print('- %s fixes' % fix_str)
    print('  - %s ("%s")' % (bug.commit.hashid[:12], bug.subject))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', metavar='<dir>', default='./',
            help='local repo')
    parser.add_argument('--fixes', metavar='<file or commits>', nargs='+',
            help='potential fix patch files or commits')
    parser.add_argument('--bugs', metavar='<file or commits>',
            nargs='+',
            help='potential bug patch files or commits')
    args = parser.parse_args()

    potential_fixes = read_changes(args.fixes, args.repo)
    for potential_fix in potential_fixes:
        for bug_reference in potential_fix.get_fixing_commit_refs():
            hashid = bug_reference.split()[0]
            subject = bug_reference[len(hashid) + 3:-2]
            try:
                buggy_change = _git.Change(commit=hashid, repo=args.repo)
            except:
                print('Failed parsing %s' % bug_reference)
                continue
            for patch_or_commits_range in args.bugs:
                if os.path.isfile(patch_or_commits_range):
                    patch_file = patch_or_commits_range
                    if buggy_change.find_matching_patch([patch_file]) != None:
                        print_fix_bug(potential_fix, buggy_change)
                else:
                    commits = patch_or_commits_range
                    if buggy_change.find_matching_commit(
                            args.repo, commits) != None:
                        print_fix_bug(potential_fix, buggy_change)

if __name__ == '__main__':
    main()
