#!/usr/bin/env python

"""
Format table in easy-to-read format
"""

import sys

def fmt_pr_tbl(rows, field_lengths):
    for row in rows:
        formatted_fields = []
        for idx, field in enumerate(row):
            field_len = field_lengths[idx]
            spaces = ' ' * (field_len - len(field))
            formatted_fields.append('%s%s' % (field, spaces))
        print(' '.join(formatted_fields))

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
    fmt_tbl(sys.stdin)

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
