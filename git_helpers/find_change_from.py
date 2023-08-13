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

    matching_change = change.find_matching_change(args.patch_or_commits,
            args.repo)
    if matching_change != None:
        if matching_change.commit:
            print('%s ("%s")' %
                    (matching_change.commit.hashid[:12], change.subject))
            if args.describe_contains:
                print('first appeared in %s' %
                        matching_change.commit.first_contained_version())
        else:
            print(matching_change.patch.file_name)
        exit(0)
    exit(1)

if __name__ == '__main__':
    main()
