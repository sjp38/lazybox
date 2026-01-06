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
    after_diverge_commit_to_trees = None

    def __init__(self, commit, event_type, trees_of_event):
        self.commit = commit
        self.event_type = event_type
        self.trees_of_event = trees_of_event
        self.after_diverge_commit_to_trees = {}

def git_commit_of(hashid):
    output = subprocess.check_output(
            ['git', 'log', '-1', hashid, '--date=iso-strict',
             '--pretty=%cd %s']).decode().strip()
    commit_date_str = output.split()[0]
    commit_date = datetime.datetime.strptime(
            commit_date_str, '%Y-%m-%dT%H:%M:%S%z')
    subject = output[len(commit_date_str) + 1:]
    return Commit(commit_date, hashid, subject)

def add_after_diverge_commit(event, tree):
    common_commit = event.commit.hash
    after_diverge_commit = subprocess.check_output(
            'git log --pretty=%%H %s..%s | tail -1' % (
                common_commit, tree), shell=True).decode().strip()
    # it was the last commit?
    if after_diverge_commit == '':
        after_diverge_commit = common_commit
    if not after_diverge_commit in event.after_diverge_commit_to_trees:
        event.after_diverge_commit_to_trees[after_diverge_commit] = [tree]
    else:
        event.after_diverge_commit_to_trees[after_diverge_commit].append(tree)

def add_event(events, commit_hash, event_type, tree):
    for event in events:
        if event.commit.hash != commit_hash:
            continue
        if event.event_type != event_type:
            continue
        if not tree in event.trees_of_event:
            event.trees_of_event.append(tree)
            add_after_diverge_commit(event, tree)
        return
    commit = git_commit_of(commit_hash)
    events.append(Event(commit, event_type, [tree]))
    add_after_diverge_commit(events[-1], tree)

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
            try:
                diverge_commit = subprocess.check_output(
                        ['git', 'merge-base', tree_a, tree_b]).decode().strip()
            except:
                # no common commit
                continue
            add_event(events, diverge_commit, 'last_common_commit', tree_a)
            add_event(events, diverge_commit, 'last_common_commit', tree_b)

    for tree in trees:
        last_commit = subprocess.check_output(
                ['git', 'rev-parse', tree]).decode().strip()
        add_event(events, last_commit, 'last_commit', tree)

    events.sort(key=lambda x:x.commit.date)
    for event in events:
        commit = event.commit
        print ('On %s, %s for %s is made as commit %s ("%s").' % (
            commit.date, event.event_type.replace('_', ' '),
            ', '.join(event.trees_of_event), commit.hash[:12], commit.subject))
        if event.event_type == 'last_common_commit':
            for commit_hash, trees in event.after_diverge_commit_to_trees.items():
                commit = git_commit_of(commit_hash)
                print('%s diverged to %s ("%s") (%s).' % (
                    ', '.join(trees), commit.hash[:12], commit.subject,
                    commit.date))
        print()

if __name__ == '__main__':
    main()
