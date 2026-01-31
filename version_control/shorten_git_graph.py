#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

'''
Show git log graph in deduplicated way for easily reading branch divergence
history.
'''

import argparse
import subprocess

def is_commit_hash(field):
    try:
        int(field, 16)
    except:
        return False
    return True

def graph_of(line):
    for field in line.split():
        if is_commit_hash(field):
            return line[:line.find(field)]
    return ''

def do_it(content):
    lines = content.splitlines()
    nr_collapsed = 0
    for idx, line in enumerate(lines):
        if idx == 0:
            print(line)
            continue
        if idx == len(lines) - 1:
            print(line)
            break

        if graph_of(line) == graph_of(lines[idx - 1]) and \
                graph_of(line) == graph_of(lines[idx + 1]) and \
                line.find('(') == -1 and line.find('*') != -1:
            nr_collapsed += 1
        else:
            if nr_collapsed > 0:
                print('[...] (%s commits)' % nr_collapsed)
            print(line)
            nr_collapsed = 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', metavar='<dir>',
                        help='path to the local repo')
    parser.add_argument('--commits', metavar='<commits>',
                        help='commits range to show the graph')
    args = parser.parse_args()

    git_output = subprocess.check_output(
            ['git', '-C', args.repo, 'log', args.commits, '--decorate',
             '--graph', '--pretty=%d']).decode().strip()
    do_it(git_output)

if __name__ == '__main__':
    main()
