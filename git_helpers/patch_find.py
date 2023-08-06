#!/usr/bin/env python3

import argparse

import _git

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('patch', metavar='<file>',
            help='path to the patch file')
    parser.add_argument('--commits', metavar='<commits range reference>',
            help='commits range to find patch in')
    parser.add_argument('--patches', metavar='<patch file>', nargs='+',
            help='patch files to find patch in')
    parser.add_argument('--repo', metavar='<dir>', default='./',
            help='local repo for --commits')
    args = parser.parse_args()

    if args.commits == None and args.patches == None:
        print('--commits or --patches should be given')
        parser.print_help()
        exit(1)

    patch = _git.Patch(args.patch)
    if args.commits:
        commit = patch.change.commit_in(args.repo, args.commits)
        if commit == None:
            exit(1)
        print('%s ("%s")' % (commit.hashid[:12], patch.change.subject))
    else:
        for patch_file in args.patches:
            if patch.change.maybe_same(_git.Patch(patch_file).change):
                print(patch_file)
                exit(0)
        print('no matching patch file found')
        exit(1)

if __name__ == '__main__':
    main()
