#!/usr/bin/env python3

'''
This script gets number of commits per day for last one year and prints the
data in a heatmap-visualization-ready format (day, week, number of commits).

Example usage:

    $ cd linux
    $ $lazybox/scripts/git_contributions.py | \
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
- specific branches
- more colors other than gray scale
- specific range of days
'''

import argparse
import datetime
import os
import subprocess

def get_commit_dates(repo, since):
    cmd = ['git', '-C', '%s' % repo]
    cmd += 'log --pretty=%cd --date=format:%Y-%m-%d'.split()
    cmd.append('--since=%s' % since)
    return subprocess.check_output(cmd).decode().strip().split('\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('repos', nargs='+',
            help='git repositories to count commits')
    parser.add_argument('--since',
            help='since when in YYYY-MM-DD format')
    args = parser.parse_args()

    today = datetime.date.today()
    today_weekday = today.weekday()
    if not args.since:
        start_date = datetime.date(today.year - 1, today.month,
                today.day - today_weekday)
    else:
        year, month, day = [int(x) for x in args.since.split('-')]
        start_date = datetime.date(year, month, day)
    since = start_date.strftime('%Y-%m-%d')

    commit_dates = []
    for repo in args.repos:
        commit_dates += get_commit_dates(repo, since)
    if len(commit_dates) == 0:
        return

    duration = (today - start_date).days + today_weekday
    nr_commits = [0] * duration
    for commit_date in commit_dates:
        year, month, day = [int(x) for x in commit_date.split('-')]
        date = datetime.date(year, month, day)
        index = (date - start_date).days - 1
        nr_commits[index] += 1

    for day in range(0, 7):
        for week in range(0, int(duration / 7)):
            commits = 0
            idx = week * 7 + day

            if idx < duration:
                commits = nr_commits[idx]
            print('%d %d %d' % (day, week, commits))

if __name__ == '__main__':
    main()
