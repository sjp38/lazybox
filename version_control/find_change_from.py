#!/usr/bin/env python3

'''
Load a change from a patch or commit, and find matching change from patches
queue or commits range
'''

import argparse

import _git

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--patch', metavar='<file>',
            help='patch containing the change')
    parser.add_argument('--commit', metavar='<commit>',
            help='commit containing the change')
    parser.add_argument('--subject', metavar='<subject>',
            help='subject of the change')
    parser.add_argument('--author', metavar='<author name <author email>>',
            help='author of the change')

    parser.add_argument('--repo', metavar='<dir>', default='./',
            help='local repo to find the change from')
    parser.add_argument('patch_or_commits', metavar='<file or commits>',
            nargs='+',
            help='commits range or patch files to find the change from')

    parser.add_argument('--describe_contains', action='store_true',
            help='show \'git describe --contains\' for found commit together')
    parser.add_argument('--remote_repo', metavar='<url>',
            help='show https url for the found commit using this')
    args = parser.parse_args()

    if args.patch == None and args.commit == None and args.subject == None:
        print('--patch, --commit, or --subject should be set')
        exit(1)

    if args.patch:
        change = _git.Change(patch_file=args.patch)
    elif args.commit:
        change = _git.Change(commit=args.commit, repo=args.repo)
    elif args.subject:
        change = _git.Change(subject=args.subject, author=args.author)

    found = False
    for to_find_from in args.patch_or_commits:
        matching_change = change.find_matching_change([to_find_from],
                args.repo)
        if matching_change == None:
            continue
        found = True
        if len(args.patch_or_commits) > 1:
            print('found it from %s' % to_find_from)
        if matching_change.commit:
            print('%s ("%s")' %
                    (matching_change.commit.hashid[:12], change.subject))
            if args.describe_contains:
                print('- merged in %s' %
                        matching_change.commit.first_contained_version())
            if args.remote_repo:
                print('- url: %s' %
                        matching_change.url(args.remote_repo, None))
        else:
            print(matching_change.patch.file_name)
    exit(0 if found else 1)

if __name__ == '__main__':
    main()
