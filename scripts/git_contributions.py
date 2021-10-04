#!/usr/bin/env python3

import subprocess
import datetime

def main():
    today = datetime.date.today()
    start_date = datetime.date(today.year - 1, today.month, today.day)
    since = start_date.strftime('%Y-%m-%d')
    cmd = 'git log --pretty=%cd --date=format:%Y-%m-%d'.split()
    cmd.append('--since=%s' % since)
    commit_dates = subprocess.check_output(cmd).decode().strip().split('\n')
    if len(commit_dates) == 0:
        return

    nr_commits = [0] * 365

    for commit_date in commit_dates:
        year, month, day = [int(x) for x in commit_date.split('-')]
        date = datetime.date(year, month, day)
        index = (date - start_date).days - 1
        nr_commits[index] += 1

    for day in range(0, 7):
        for week in range(0, 52):
            commits = 0
            idx = week * 7 + day

            if idx < 365:
                commits = nr_commits[idx]
            print('%d %d %d' % (day, week, commits))

if __name__ == '__main__':
    main()
