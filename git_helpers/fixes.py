#!/usr/bin/env python3

import argparse
import os
import subprocess

import _git

def print_fix_bug(fix, bug, remote_git_url, remote_queue_url):
    print('- fix: %s' % fix.subject)
    if remote_git_url:
        print('  - url: %s' % fix.url(remote_git_url, remote_queue_url))
    else:
        if fix.commit:
            print('  - commit %s' % fix.commit.hashid)
        if fix.patch:
            print('  - patch %s' % fix.patch.file_name)
    print('- bug: %s' % bug.subject)
    if remote_queue_url:
        print('    - url: %s' % bug.url(remote_git_url, remote_queue_url))
    else:
        if bug.commit:
            print('  - commit %s' % bug.commit.hashid)
        if bug.patch:
            print('  - patch %s' % bug.patch.file_name)
    print()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', metavar='<dir>', default='./',
            help='local repo')
    parser.add_argument('--fixes', metavar='<file or commits>', nargs='+',
            help='potential fix patch files or commits')
    parser.add_argument('--bugs', metavar='<file or commits>',
            nargs='+',
            help='potential bug patch files or commits')
    parser.add_argument('--remote_git_url', metavar='<url>',
            help='show https url for the found bug/fix commits using this')
    parser.add_argument('--patches_queue_url', metavar='<url>',
            help='show https url for the found bug/fix patches using this')
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
                print('# Failed parsing %s from %s' %
                        (bug_reference, potential_fix))
                continue
            for patch_or_commits_range in args.bugs:
                if os.path.isfile(patch_or_commits_range):
                    patch_file = patch_or_commits_range
                    if buggy_change.find_matching_patch([patch_file]) != None:
                        print_fix_bug(potential_fix, buggy_change,
                                args.remote_git_url, args.patches_queue_url)
                else:
                    commits = patch_or_commits_range
                    if buggy_change.find_matching_commit(
                            args.repo, commits) != None:
                        print_fix_bug(potential_fix, buggy_change,
                                args.remote_git_url, args.patches_queue_url)

if __name__ == '__main__':
    main()
