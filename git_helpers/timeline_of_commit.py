#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--subject', help='subject of the patch')
    parser.add_argument('--author', help='author of the patch')
    parser.add_argument('--commit', help='commit id of the patch')
    parser.add_argument('trees', nargs='+',
            help='trees to check for the patch')
    args = parser.parse_args()

    if not args.subject and not args.author:
        if not args.commit:
            print('subject and author, or commit are necessary')
            parser.print_help()
            exit(1)
        else:
            subject = subprocess.check_output(['git', 'log', '-n', '1',
                '--pretty=%s', args.commit]).decode().strip()
            author = subprocess.check_output(['git', 'log', '-n', '1',
                '--pretty=%an', args.commit]).decode().strip()
    else:
        subject = args.subject
        author = args.author

    bindir = os.path.dirname(sys.argv[0])
    find_commit_in = os.path.join(bindir, 'find_commit_in.sh')
    timeline = {}
    for tree in args.trees:
        commit_hash = subprocess.check_output([find_commit_in, '--hash_only',
            '--author', author, '--title', subject, tree]).decode().strip()
        if commit_hash == '':
            continue

        author_date = subprocess.check_output(['git', 'log', '-n', '1',
                '--date=iso-strict', '--pretty=%ad',
                commit_hash]).decode().strip()
        author_name_mail = subprocess.check_output(['git', 'log', '-n', '1',
                '--pretty=%an <%ae>', commit_hash]).decode().strip()
        timeline[author_date] = 'authored by %s' % author_name_mail

        committer = subprocess.check_output(['git', 'log', '-n', '1',
                '--pretty=%cn <%ce>', commit_hash]).decode().strip()
        commit_date = subprocess.check_output(['git', 'log', '-n', '1',
                '--date=iso-strict', '--pretty=%cd',
                commit_hash]).decode().strip()
        timeline[commit_date] = 'committed by %s into %s' % (committer, tree)

    for date in sorted(timeline.keys()):
        print('%s: %s' % (date, timeline[date]))

if __name__ == '__main__':
    main()
