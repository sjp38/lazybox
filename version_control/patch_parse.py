#!/usr/bin/env python3

import argparse

import _git

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('patch', metavar='<file>',
            help='patch file to read')
    parser.add_argument('fields', choices=['subject', 'date', 'author',
        'mail_header', 'description', 'diff', 'fixes'],
            nargs='+',
            help='fields to read from the patch')
    args = parser.parse_args()

    change = _git.Change(patch_file=args.patch, set_diff=True)
    for field in args.fields:
        if field == 'subject':
            print(change.subject)
        elif field == 'date':
            print(change.patch.sent_date)
        elif field == 'author':
            print(change.author)
        elif field == 'mail_header':
            print(change.patch.email_header)
        elif field == 'description':
            print(change.description)
        elif field == 'diff':
            print(change.diff)
        elif field == 'fixes':
            print('\n'.join(change.get_fixing_commit_refs()))

if __name__ == '__main__':
    main()
