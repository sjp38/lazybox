#!/usr/bin/env python3

'''
This script gets number of commits per day for last one year and prints the
data in a heatmap-visualization-ready format (day, week, number of commits).

Example usage:

    $ ./nr_commits.py <the git repo>... | \
            ~/lazybox/gnuplot/plot.py stdout --type heatmap \
            --stdout_first_row_display "        Number of commits per day" \
            --stdout_first_col_display \
            "Mon " "Tue " "Wed " "Thu " "Fri " "Sat " "Sun "
        Number of commits per day
    Mon 000000000300200200002000100000000000010001121100101121
    Tue 000000000000000100100000000000000000100000000000000000
    Wed 000001000000001200000000000000000000020000000000000000
    Thu 000001000000000100003001000000000100000000101000000000
    Fri 000000000000003000000000000000000100000000000000002000
    Sat 002222133212302300000021110211111200101201221911102120
    Sun 000223332210220200010011201000001200102111020001111230
    # color samples: 0123456789
    # values range: [0-47]
    # unit of the number: 5.222

TODO
- more colors other than gray scale
'''

import argparse
import datetime
import os
import subprocess

def get_commit_dates(repo, git_ref, since, until, author):
    if not os.path.isdir(os.path.join(repo, '.git')):
            return []
    cmd = ['git', '-C', '%s' % repo]
    cmd += 'log --pretty=%cd --date=format:%Y-%m-%d'.split()
    cmd.append('--since=%s' % since.strftime('%Y-%m-%d'))
    cmd.append('--until=%s' % until.strftime('%Y-%m-%d'))
    cmd.append(git_ref)
    if author:
        cmd.append('--author=%s' % author)
    try:
        dates = subprocess.check_output(cmd).decode().strip().split('\n')
    except subprocess.CalledProcessError as e:
        dates = []
    if dates == ['']:
        dates = []
    return dates

def get_date_from_yyyymmdd(txt):
    return datetime.date(*[int(x) for x in txt.split('-')])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('repos', nargs='+', metavar='<dir>',
            help='git repositories to count commits')
    parser.add_argument('--heads', nargs='+', metavar='<git heads>',
            help='git heads of the repositories to count commits')
    parser.add_argument('--since', metavar='<date>',
            help='since when in YYYY-MM-DD format')
    parser.add_argument('--until', metavar='<date>',
            help='until when in YYYY-MM-DD format')
    parser.add_argument('--author', metavar='<author>',
            help='author of the commits')
    args = parser.parse_args()

    if not args.heads:
        args.heads = ['HEAD'] * len(args.repos)
    elif len(args.heads) == 1:
        args.heads *= len(args.repos)
    elif len(args.heads) != len(args.repos):
        print('Wrong number of heads')

    if args.until:
        until = get_date_from_yyyymmdd(args.until)
    else:
        until = datetime.date.today()

    if args.since:
        since = get_date_from_yyyymmdd(args.since)
    else:
        since = until - datetime.timedelta(365)
    since -= datetime.timedelta(since.weekday())

    commit_dates = []
    for idx, repo in enumerate(args.repos):
        commit_dates += get_commit_dates(repo, args.heads[idx], since, until,
                args.author)
    if len(commit_dates) == 0:
        return

    duration = (until - since).days + 1
    nr_commits = [0] * duration
    for commit_date in commit_dates:
        date = get_date_from_yyyymmdd(commit_date)
        index = (date - since).days
        nr_commits[index] += 1

    nr_weeks = duration // 7
    if duration % 7:
        nr_weeks += 1
    for day in range(0, 7):
        for week in range(0, nr_weeks):
            commits = 0
            idx = week * 7 + day

            if idx < duration:
                commits = nr_commits[idx]
            print('%d %d %d' % (day, week, commits))

if __name__ == '__main__':
    main()
