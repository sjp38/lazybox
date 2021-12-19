#!/usr/bin/env python3

import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('repo', help='git repositories to get the stat from')
    args = parser.parse_args()

    cmd = ('git -C %s log' % args.repo).split()
    cmd.append('--pretty="%an <%ae>"')
    authors_lines = subprocess.check_output(cmd).decode().strip().split('\n')
    authors = {}
    for author in authors_lines:
        if not author in authors:
            authors[author] = 0
        authors[author] += 1

    authors_sorted = sorted(authors, key=authors.get, reverse=True)
    for author in authors_sorted:
        print('%s: %d' % (author, authors[author]))

if __name__ == '__main__':
    main()
