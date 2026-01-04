#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

'''
Receives list of trees and show their evolution history.  E.g.,

2025-01-01 initial commit 1234567890ab for branch-A has made.
2025-02-01 From commit 234567890abc, branch-B has diverged from branch-A.
2025-03-01 branch-B got the final commit 34567890abcd.
2025-04-01 branch-A got the final commit 4567890abcde.
'''

import argparse
import datetime
import subprocess

def git_commit_date_subject(hashid):
    output = subprocess.check_output(
            ['git', 'log', '-1', hashid, '--date=iso-strict',
             '--pretty=%cd %s']).decode().strip()
    commit_date_str = output[:25]
    commit_date = datetime.datetime.strptime(
            commit_date_str, '%Y-%m-%dT%H:%M:%S%z')
    subject = output[26:]
    return commit_date, subject

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('trees', nargs='+', metavar='<tree>',
                        help='trees to show their development history')
    args = parser.parse_args()

    trees = args.trees

    events = []
    for tree in trees:
        first_commit = subprocess.check_output(
                'git log --pretty=%H | tail -1', shell=True).decode().strip()
        if first_commit in [e[1] for e in events]:
            continue
        commit_date, subject = git_commit_date_subject(first_commit)
        events.append(
                [commit_date, first_commit,
                 '%s ("%s")' % (first_commit[:12], subject), tree,
                 'first commit'])

    for tree_a in trees:
        for tree_b in trees:
            if tree_a == tree_b:
                continue
            diverge_commit = subprocess.check_output(
                    ['git', 'merge-base', tree_a, tree_b]).decode().strip()
            commit_date, subject = git_commit_date_subject(diverge_commit)
            events.append(
                    [commit_date, diverge_commit,
                     '%s ("%s")' % (diverge_commit[:12], subject), tree_a,
                     'last common commit with %s' % tree_b])

    for tree in trees:
        last_commit = subprocess.check_output(
                ['git', 'rev-parse', tree]).decode().strip()
        commit_date, subject = git_commit_date_subject(last_commit)
        events.append(
                [commit_date, last_commit,
                 '%s ("%s")' % (last_commit[:12], subject), tree,
                 'last commit'])

    events.sort(key=lambda x:x[0])
    for event in events:
        date, full_hash, commit_desc, tree, event_desc = event
        print('%s' % date)
        print('\t%s' % commit_desc)
        print('\t%s %s' % (tree, event_desc))

if __name__ == '__main__':
    main()
