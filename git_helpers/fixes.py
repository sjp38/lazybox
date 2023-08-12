#!/usr/bin/env python3

import argparse
import os
import subprocess

import _git

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

    if args.fixes == None or args.bugs == None:
        print('--fixes and --bugs should be passed')
        parser.print_usage()
        exit(1)

    potential_fixes = _git.read_changes(args.fixes, args.repo)
    for potential_fix in potential_fixes:
        for bug_reference in potential_fix.get_fixing_commit_refs():
            hashid = bug_reference.split()[0]
            subject = bug_reference[len(hashid) + 3:-2]
            try:
                buggy_change = _git.Change(commit=hashid, repo=args.repo)
            except:
                print('# Failed parsing %s' % bug_reference)
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
