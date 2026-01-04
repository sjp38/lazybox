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

class Commit:
    date = None
    hash = None
    subject = None

    def __init__(self, date, hash, subject):
        self.date = date
        self.hash = hash
        self.subject = subject

    def __eq__(self, other):
        return self.hash == other.hash

class Event:
    commit = None
    event_type = None   # first_commit, last_common_commit, last_commit
    trees_of_event = None

    def __init__(self, commit, event_type, trees_of_event):
        self.commit = commit
        self.event_type = event_type
        self.trees_of_event = trees_of_event

def git_commit_of(hashid):
    output = subprocess.check_output(
            ['git', 'log', '-1', hashid, '--date=iso-strict',
             '--pretty=%cd %s']).decode().strip()
    commit_date_str = output[:25]
    commit_date = datetime.datetime.strptime(
            commit_date_str, '%Y-%m-%dT%H:%M:%S%z')
    subject = output[26:]
    return Commit(commit_date, hashid, subject)

def add_event(events, commit_hash, event_type, tree):
    for event in events:
        if event.commit.hash != commit_hash:
            continue
        if event.event_type != event_type:
            continue
        if not tree in event.trees_of_event:
            event.trees_of_event.append(tree)
        return
    commit = git_commit_of(commit_hash)
    events.append(Event(commit, event_type, [tree]))

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
        add_event(events, first_commit, 'first_commit', tree)

    for tree_a in trees:
        for tree_b in trees:
            if tree_a == tree_b:
                continue
            diverge_commit = subprocess.check_output(
                    ['git', 'merge-base', tree_a, tree_b]).decode().strip()
            add_event(events, diverge_commit, 'last_common_commit', tree_a)
            add_event(events, diverge_commit, 'last_common_commit', tree_b)

    for tree in trees:
        last_commit = subprocess.check_output(
                ['git', 'rev-parse', tree]).decode().strip()
        add_event(events, last_commit, 'last_commit', tree)

    events.sort(key=lambda x:x.commit.date)
    for event in events:
        commit = event.commit
        print('%s' % commit.date)
        print('%s ("%s")' % (commit.hash[:12], commit.subject))
        print('%s of %s' % (event.event_type, ', '.join(event.trees_of_event)))
        print()

if __name__ == '__main__':
    main()
