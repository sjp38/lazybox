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
    parser.add_argument('--author', action='store_true',
                        help='print author information')
    parser.add_argument('--matching', nargs='+', metavar='<git reference>',
                        help='find matching changes from given references')
    parser.add_argument('--show_original_text', action='store_true',
                        help='show original text')
    args = parser.parse_args()

    if args.text == 'stdin':
        lines = sys.stdin.read().split('\n')
    else:
        with open(args.text, 'r') as f:
            lines = f.read().split('\n')
    commits_to_decode = {}
    for line in lines:
        if args.show_original_text:
            print(line.strip())
        for separator in [',', '(', ')', '/', '[', ']']:
            line = line.replace(separator, ' ')
        for word in line.split():
            if is_hash(word):
                if len(word) > 12:
                    word = word[:12]
                commits_to_decode[word] = True

    print('commits on the text')
    for commit in sorted(commits_to_decode.keys()):
        if args.repo is None:
            args.repo = '.'
        try:
            change = _git.Change(commit=commit, repo=args.repo)
        except:
            # probably wrong commit.  Ignore.
            continue
        print('- %s: ("%s")' % (change.commit.hashid[:12], change.subject))
        if args.author:
            print('  - authored by %s at %s' %
                  (change.author, change.commit.author_date))
        if args.contains:
            print('  - merged in %s' % change.commit.first_contained_version())
        if args.matching:
            for to_find_from in args.matching:
                matching_change = change.find_matching_change(
                        [to_find_from], args.repo)
                if matching_change == None:
                    continue
                print('  - matching change (%s) found from %s' %
                      (matching_change.commit.hashid[:12], to_find_from))
                if args.contains:
                    print('    - merged in %s' %
                          matching_change.commit.first_contained_version())

if __name__ == '__main__':
    main()
