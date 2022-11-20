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
    __find_commit_in = os.path.join(bindir, '__find_commit_in.sh')
    for tree in args.trees:
        commit_hash = subprocess.check_output([__find_commit_in, author,
            subject, tree]).decode().strip()
        if commit_hash == '':
            continue
        author_date = subprocess.check_output(['git', 'log', '-n', '1',
                '--date=iso-strict', '--pretty=%ad',
                commit_hash]).decode().strip()
        committer = subprocess.check_output(['git', 'log', '-n', '1',
                '--pretty=%cn', commit_hash]).decode().strip()
        commit_date = subprocess.check_output(['git', 'log', '-n', '1',
                '--date=iso-strict', '--pretty=%cd',
                commit_hash]).decode().strip()

        print('authored in %s, committed by %s in %s to %s' % (author_date,
            committer, commit_date, tree))

if __name__ == '__main__':
    main()
