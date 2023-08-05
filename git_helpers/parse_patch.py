#!/usr/bin/env python3

import argparse

import _patch

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('patch', metavar='<file>',
            help='patch file to read')
    parser.add_argument('fields', choices=['subject', 'date', 'author',
        'mail_header', 'description', 'diff', 'fixes'],
            nargs='+',
            help='fields to read from the patch')
    args = parser.parse_args()

    patch = _patch.Patch(args.patch)
    for field in args.fields:
        if field == 'subject':
            print(patch.subject)
        elif field == 'date':
            print(patch.date)
        elif field == 'author':
            print(patch.author)
        elif field == 'mail_header':
            print(patch.email_header)
        elif field == 'description':
            print(patch.description_body)
        elif field == 'diff':
            print(patch.diff)
        elif field == 'fixes':
            print('\n'.join(patch.fixes))

if __name__ == '__main__':
    main()
