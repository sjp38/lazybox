#!/usr/bin/env python3

'''
Find commits for stable in specific commits range is in given trees

E.g.,

$ ../lazybox/linux_hack/stable_commits_check.py \
        --src v5.15..linus/master --files mm/damon include/linux/damon \
        --dest v5.15..stable/linux-6.6.y
- 13d0599ab3b2 ("mm/damon/lru_sort: fix quota status loss due to online tunings")
  - Cc: <stable@vger.kernel.org>        [6.0+]
  - merged in v5.15..stable/linux-6.6.y (3c4441b23bf7)
- 1b0ca4e4ff10 ("mm/damon/reclaim: fix quota stauts loss due to online tunings")
  - Cc: <stable@vger.kernel.org>        [5.19+]
  - merged in v5.15..stable/linux-6.6.y (9cad9a2e896c)
- e9e3db69966d ("mm/damon/core: check apply interval in damon_do_apply_schemes()")
  - Cc: <stable@vger.kernel.org>        [6.7.x]
  - not merged in v5.15..stable/linux-6.6.y
'''

import argparse
import os
import subprocess

os.sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'git_helpers')))

import _git

def get_stable_cc_line(change):
    for line in change.description.split('\n'):
        fields = line.split()
        if len(fields) < 2 or fields[0] != 'Cc:':
            continue
        if fields[1].startswith('stable') or fields[1].startswith('<stable'):
            return line

def pr_stable_change(change):
    print('- %s ("%s")' % (change.commit.hashid[:12], change.subject))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', metavar='<changes>',
                        help='changes to find for-stable changes')
    parser.add_argument('--files', metavar='<path>', nargs='+',
                        help='the files')
    parser.add_argument('--repo', metavar='<repo>', default='./',
                        help='the repo')
    parser.add_argument('--dest', metavar='<changes>', nargs='+',
                        help='changes to find if the stable changes in')
    parser.add_argument('--unmerged', action='store_true',
                        help='show unmerged cases only')
    args = parser.parse_args()

    if args.src is None or args.dest is None:
        print('--src and --dest should be given')
        exit(1)

    git_cmd = ['git', '-C', args.repo]
    cmd = git_cmd + ['log', args.src, '--grep', '^Cc: stable', '--grep',
                     '^Cc: <stable', '--pretty=%H']
    if args.files is not None:
        cmd += ['--'] + args.files
    stable_commits = subprocess.check_output(cmd).decode().strip().split('\n')
    for commit in stable_commits:
        change = _git.Change(commit=commit, repo=args.repo)
        for dest in args.dest:
            matching_change = change.find_matching_change([dest], args.repo)
            if matching_change is None:
                pr_stable_change(change)
                print('  - not merged in %s' % dest)
                for line in change.description.strip().split('\n'):
                    fields = line.split()
                    if len(fields) < 3:
                        continue
                    if fields[0] == 'Fixes:':
                        try:
                            bug = _git.Change(commit=fields[1], repo=args.repo)
                        except:
                            print('failed getting bug (%s) for fix (%s)' %
                                  (fields[1], change.commit.hashid[:12]))
                            continue
                        matching_bug = bug.find_matching_change([dest],
                                                                args.repo)
                        if matching_bug is not None:
                            print('  - !!! the bug (%s) is merged in' %
                                  matching_bug.subject)
                continue
            if args.unmerged is True:
                continue
            pr_stable_change(change)
            print('  - merged in %s (%s)' %
                  (dest, matching_change.commit.hashid[:12]))

if __name__ == '__main__':
    main()
