#!/usr/bin/env python3

'''
Find how much changes the author made to what files

e.g.,

$ ./profile_author.py "SeongJae Park" --repo ~/linux \
        --since 2023-01-01 --until 2023-12-31 --interval 60 \
        --max_depth 2 --max_files 3
since 2023-01-01 until 2023-03-02
# <changed_lines> <file>
724 mm/damon
138 Documentation/admin-guide
94 Documentation/mm
# 1233 total lines
# 30 total files
# 45 commits

since 2023-03-02 until 2023-05-01
# <changed_lines> <file>
14 tools/Makefile
5 mm/damon
# 19 total lines
# 2 total files
# 3 commits

[...]
'''

import argparse
import datetime
import subprocess

def changes_made(author, since, until, repo, branch, max_depth):
    cmd = ['git', '-C', repo, 'log', '--pretty=commit %h %an <%ae>',
           '--stat', '--author=%s' % author,
           '--since=%s' % since.strftime('%Y-%m-%d'),
           '--until=%s' % until.strftime('%Y-%m-%d')]
    if branch is not None:
        cmd.append(branch)
    output = subprocess.check_output(cmd).decode()
    changes = {}
    nr_commits = 0
    authors = {}
    for line in output.split('\n'):
        fields = line.split()
        if line.startswith('commit'):
            nr_commits += 1
            author = ' '.join(fields[2:])
            if not author in authors:
                authors[author] = True
        elif len(fields) == 4:
            filename = fields[0]
            lines = int(fields[2])
            if max_depth is not None:
                filename  = '/'.join(filename.split('/')[:max_depth])
            if not filename in changes:
                changes[filename] = 0
            changes[filename] += lines
    return changes, nr_commits, list(authors.keys())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('author', metavar='<author>',
                        help='the author to make the profile for')
    parser.add_argument('--since', metavar='<date (YYYY-MM-DD)>',
                        help='start date to generate profile for')
    parser.add_argument('--until', metavar='<date (YYYY-MM-DD)>',
                        help='end date to generate profile for')
    parser.add_argument('--interval', metavar='<days>', type=int,
                        help='days to generate sub-profile for')
    parser.add_argument('--repo', metavar='<repo>', default='./',
                        help='path to the git repository')
    parser.add_argument('--branch', metavar='<branch>',
                        help='branch of the repo to generate profile for')
    parser.add_argument('--max_depth', metavar='<int>', type=int,
                        help='maximum depth of files to count')
    parser.add_argument('--max_files', metavar='<int>', type=int,
                        help='maximum number of files to show on profile')
    args = parser.parse_args()

    if args.until is None:
        until = datetime.datetime.now()
    else:
        until = datetime.datetime.strptime(args.until, '%Y-%m-%d')
    if args.since is None:
        since = until - datetime.timedelta(days = 365)
    else:
        since = datetime.datetime.strptime(args.since, '%Y-%m-%d')

    if args.interval is None:
        interval = until - since
    else:
        interval = datetime.timedelta(days=args.interval)

    while since < until:
        next_since = min(since + interval, until)
        changes, nr_commits, authors = changes_made(
                args.author, since, next_since, args.repo, args.branch,
                args.max_depth)
        print('# below changes made by')
        for author in authors:
            print('# - %s' % author)
        print('# since %s until %s' %
              (since.strftime('%Y-%m-%d'), next_since.strftime('%Y-%m-%d')))
        print('# <changed_lines>', '<file>')
        files = sorted(changes.keys(), key=lambda k: changes[k], reverse=True)
        if args.max_files is not None:
            files = files[:args.max_files]
        for filename in files:
            lines = changes[filename]
            print(lines, filename)
        print('#', sum(changes.values()), 'total lines')
        print('#', len(changes), 'total files')
        print('#', nr_commits, 'commits')
        print()
        since = next_since

if __name__ == '__main__':
    main()
