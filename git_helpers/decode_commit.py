#!/usr/bin/env python3

import argparse
import sys
import subprocess

import _git

def is_hash(word):
    if len(word) < 10:
        return False
    for c in word:
        if c not in '0123456789abcdef':
            return False
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('text', metavar='<file>',
                        help='file containing the text to decode, or stdin')
    parser.add_argument('--repo', metavar='<repo>',
                        help='path to the repo of the commits')
    parser.add_argument('--contains', action='store_true',
                        help='print containing version of the commits')
    args = parser.parse_args()

    if args.text == 'stdin':
        lines = sys.stdin.read().split('\n')
    else:
        with open(args.text, 'r') as f:
            lines = f.read().split('\n')
    commits_to_decode = {}
    for line in lines:
        print(line.strip())
        for separator in [',', '(', ')', '/']:
            line = line.replace(separator, ' ')
        for word in line.split():
            if is_hash(word):
                if len(word) > 12:
                    word = word[:12]
                commits_to_decode[word] = True

    print('commits on the text')
    for commit in commits_to_decode:
        if args.repo is None:
            args.repo = '.'
        change = _git.Change(commit=commit, repo=args.repo)
        print('- %s: ("%s")' % (change.commit.hashid[:12], change.subject))
        if args.contains:
            print('  - merged in %s' % change.commit.first_contained_version())

if __name__ == '__main__':
    main()
