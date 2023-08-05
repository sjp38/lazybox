#!/usr/bin/env python3

import argparse

import _patch

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('patch', metavar='<file>',
            help='path to the patch file')
    parser.add_argument('commits', metavar='<commits range reference>',
            help='commits range to find patch in')
    args = parser.parse_args()

    patch = _patch.Patch(args.patch)
    try:
        print(patch.commit_in(args.commits))
    except:
        # not found
        exit(1)

if __name__ == '__main__':
    main()
