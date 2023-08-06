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

    parser.add_argument('--repo', metavar='<dir>', default='./',
            help='local repo to find the change from')
    parser.add_argument('--commits', metavar='<commits range reference>',
            help='commits range to find the change from')
    parser.add_argument('--patches', metavar='<patch file>', nargs='+',
            help='patch files to find the change from')
    args = parser.parse_args()

    if (args.patch == None and args.commit == None) or (args.patch != None and
            args.commit != None):
        print('--patch or --commit should be set (not both)')
        exit(1)

    if args.commits == None and args.patches == None:
        print('--commits or --patches should be given')
        exit(1)

    if args.patch:
        change = _git.Patch(args.patch).change
    else:
        change = _git.Commit(args.commit, args.repo, None).change

    if args.commits:
        commit = change.commit_in(args.repo, args.commits)
        if commit == None:
            exit(1)
        print('%s ("%s")' % (commit.hashid[:12], commit.change.subject))
    else:
        patch = change.patch_in(args.patches)
        if patch != None:
            print(patch.file_name)
            exit(0)
        print('no matching patch file found')
        exit(1)

if __name__ == '__main__':
    main()
