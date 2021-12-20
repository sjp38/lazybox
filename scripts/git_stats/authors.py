#!/usr/bin/env python3

import argparse
import subprocess

def parse_git_output_by_commits(git_output):
    authors_lines = git_output.split('\n')
    authors = {}
    for author in authors_lines:
        if not author in authors:
            authors[author] = 0
        authors[author] += 1
    return authors

def parse_git_output_by_lines(git_output):
    # example input is:
    #     sj38.park@gmail.com
    #
    #      1 file changed, 1 insertion(+), 1 deletion(-)
    #     sj38.park@gmail.com
    #
    #      1 file changed, 2 insertions(+)

    authors = {}
    lines = git_output.split('\n')
    for idx in range(0, len(lines), 3):
        author = lines[idx].strip()
        if not author in authors:
            authors[author] = 0
        changes_fields = lines[idx + 2].strip().split()
        for idx, field in enumerate(changes_fields):
            if field in ['insertions(+),', 'insertions(+)', 'deletions(-)',
                    'insertion(+),', 'insertion(+)', 'deletion(-)']:
                authors[author] += int(changes_fields[idx - 1])
    return authors

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
    parser.add_argument('--sortby', choices=['commits', 'lines'],
            default='commits', help='metric to sort authors by')
    args = parser.parse_args()

    cmd = ('git -C %s log' % args.repo).split()
    cmd.append('--pretty=%an <%ae>')
    if args.since:
        cmd.append('--since=%s' % args.since)
    if args.until:
        cmd.append('--until=%s' % args.until)
    if args.sortby == 'lines':
        cmd.append('--shortstat')
        cmd.append('--no-merges')

    git_output = subprocess.check_output(cmd).decode().strip()
    if args.sortby == 'commits':
        authors = parse_git_output_by_commits(git_output)
    else:
        authors = parse_git_output_by_lines(git_output)

    authors_sorted = sorted(authors, key=authors.get, reverse=True)
    if args.max_nr_authors:
        authors_sorted = authors_sorted[:args.max_nr_authors]
    for author in authors_sorted:
        print('%s: %d %s' % (author, authors[author], 'commits' if args.sortby
            == 'commits' else 'lines'))

    print('# %d authors in total' % len(authors))

if __name__ == '__main__':
    main()
