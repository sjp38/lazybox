#!/usr/bin/env python

"""
Format table in easy-to-read format
"""

import argparse
import sys

def fmt_pr_tbl(rows, field_lengths):
    seperator = ' ' * nr_min_spaces
    for row in rows:
        formatted_fields = []
        for idx, field in enumerate(row):
            field_len = field_lengths[idx]
            spaces = ' ' * (field_len - len(field))
            formatted_fields.append('%s%s' % (field, spaces))

        print(seperator.join(formatted_fields))

def fmt_tbl(lines):
    rows = []
    field_lengths = []

    for line in lines:
        line = line.strip()
        if line == '':
            fmt_pr_tbl(rows, field_lengths)
            print('')
            rows = []
            field_lengths = []
            continue
        if line.startswith('#'):
            continue
        fields = line.split()
        rows.append(fields)
        if field_lengths and len(field_lengths) != len(fields):
            print('Wrong table input: %s' % line)
            exit(1)
        for idx, field in enumerate(fields):
            if len(field_lengths) <= idx:
                field_lengths.append(len(field))
                continue
            if len(field) > field_lengths[idx]:
                field_lengths[idx] = len(field)
    fmt_pr_tbl(rows, field_lengths)

def main():
    global nr_min_spaces

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', metavar='<file>',
            help='input file')
    parser.add_argument('--stdin', action='store_true',
            help='read data from stdin')
    parser.add_argument('--example', action='store_true', help='show example')
    parser.add_argument('--spaces', type=int, default=2,
            help='minimum number of spaces between fields')

    args = parser.parse_args()

    nr_min_spaces = args.spaces

    if not args.file and not args.stdin and not args.example:
        print('no input')
        exit(1)

    if args.example:
        test(args.spaces)
        return

    if args.file:
        with open(args.file, 'r') as f:
            lines = f.read().split('\n')
    elif args.stdin:
        lines = sys.stdin
    fmt_tbl(lines)

def test():
    test_input = """
1 2 3
4  5  6
7	8	  9
abc de 10


12 345 89
# comment
1 2 3"""
    fmt_tbl(test_input.split('\n'))

if __name__ == '__main__':
    main()
