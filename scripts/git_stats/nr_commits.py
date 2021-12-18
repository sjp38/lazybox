#!/usr/bin/env python3

'''
This script gets number of commits per day for last one year and prints the
data in a heatmap-visualization-ready format (day, week, number of commits).

Example usage:

    $ cd linux
    $ $lazybox/scripts/git_stats/nr_commits.py | \
            $lazybox/gnuplot/plot.py stdout --type heatmap
    2204227254202322335120345423321831233520131323410000
    2312243345610232335110136343311223344431125243310000
    4113322246110242423130924264212242433430132232211000
    2201123333200353245102554243211324435432221422410000
    1214333353100124322020323362221232435200232223130000
    0000110000000000020002000001000000011100000010000000
    0000000000000001100000001020100010000000010000100000
    # color samples: 0123456789
    # values range: [1-884]
    # unit of the number: 98.111

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
    parser.add_argument('repos', nargs='+',
            help='git repositories to count commits')
    parser.add_argument('--heads', nargs='+',
            help='git heads of the repositories to count commits')
    parser.add_argument('--since', help='since when in YYYY-MM-DD format')
    parser.add_argument('--until', help='until when in YYYY-MM-DD format')
    parser.add_argument('--author', help='author of the commits')
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
