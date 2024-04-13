#!/usr/bin/env python3

'''
Find how much changes the author made to what files

e.g.,

$ ./profile_author.py "SeongJae Park" --repo ~/linux \
        --since 2023-12-01 --until 2023-12-31 --interval 7
since 2023-12-01 until 2023-12-31
<changed_lines> <file>
322 tools/testing/selftests/damon/_damon_sysfs.py
321 mm/damon/sysfs-schemes.c
171 Documentation/admin-guide/mm/damon/usage.rst
77 mm/damon/core.c
60 mm/damon/core-test.h
55 ..._update_schemes_tried_regions_wss_estimation.py
41 tools/testing/selftests/damon/access_memory.c
37 Documentation/mm/damon/design.rst
33 .../sysfs_update_schemes_tried_regions_hang.py
33 Documentation/ABI/testing/sysfs-kernel-mm-damon
27 tools/testing/selftests/damon/sysfs.sh
27 mm/damon/sysfs.c
24 include/linux/damon.h
3 tools/testing/selftests/damon/Makefile
3 mm/damon/sysfs-common.h
2 mm/damon/dbgfs-test.h
2 mm/damon/dbgfs.c
2 mm/damon/modules-common.c
2 mm/damon/vaddr-test.h
2 mm/damon/vaddr.c
# 1244 total lines
# 20 total files
# 24 commits

since 2023-12-08 until 2023-12-31
[...]
'''

import argparse
import datetime
import subprocess

def changes_made(author, since, until, repo, max_depth):
    cmd = ['git', '-C', repo, 'log', '--pretty=%h', '--stat',
           '--author=%s' % author,
           '--since=%s' % since.strftime('%Y-%m-%d'),
           '--until=%s' % until.strftime('%Y-%m-%d')]
    output = subprocess.check_output(cmd).decode()
    changes = {}
    nr_commits = 0
    for line in output.split('\n'):
        fields = line.split()
        if len(fields) == 1:
            nr_commits += 1
        elif len(fields) == 4:
            filename = fields[0]
            lines = int(fields[2])
            if max_depth is not None:
                filename  = '/'.join(filename.split('/')[:max_depth])
            if not filename in changes:
                changes[filename] = 0
            changes[filename] += lines
    return changes, nr_commits

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
        changes, nr_commits = changes_made(
                args.author, since, until, args.repo, args.max_depth)
        print('since %s until %s' %
              (since.strftime('%Y-%m-%d'), until.strftime('%Y-%m-%d')))
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
        since += interval

if __name__ == '__main__':
    main()
