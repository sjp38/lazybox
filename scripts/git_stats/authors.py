#!/usr/bin/env python3

import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('repo', metavar='<dir>',
            help='git repositories to get the stat from')
    parser.add_argument('--since', metavar='<date>',
            help='since when in YYYY-MM-DD format')
    parser.add_argument('--until', metavar='<date>',
            help='until when in YYYY-MM-DD format')
    parser.add_argument('--max_nr_authors', type=int, metavar='<number>',
            help='max number of authors to list')
    args = parser.parse_args()

    cmd = ('git -C %s log' % args.repo).split()
    cmd.append('--pretty=%an <%ae>')
    if args.since:
        cmd.append('--since=%s' % args.since)
    if args.until:
        cmd.append('--until=%s' % args.until)
    authors_lines = subprocess.check_output(cmd).decode().strip().split('\n')
    authors = {}
    for author in authors_lines:
        if not author in authors:
            authors[author] = 0
        authors[author] += 1

    authors_sorted = sorted(authors, key=authors.get, reverse=True)
    if args.max_nr_authors:
        authors_sorted = authors_sorted[:args.max_nr_authors]
    for author in authors_sorted:
        print('%s: %d commits' % (author, authors[author]))

    print('# %d authors in total' % len(authors))

if __name__ == '__main__':
    main()
