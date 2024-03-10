#!/usr/bin/env python3

import argparse
import sys
import subprocess

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
                commits_to_decode[word] = True

    print('commits on the text')
    for commit in commits_to_decode:
        git_cmd = ['git']
        if args.repo is not None:
            git_cmd += ['-C', args.repo]
        try:
            decoded = subprocess.check_output(
                    git_cmd + ['describe', commit]).decode().strip()
        except:
            decoded = 'unknown'
        print('- %s: %s' % (commit, decoded))

if __name__ == '__main__':
    main()
