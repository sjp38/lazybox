#!/usr/bin/env python

"""
Format table in easy-to-read format
"""

import sys

def main():
    rows = []
    field_lengths = []
    for line in sys.stdin:
        line = line.strip()
        if line == '' or line.startswith('#'):
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

    for row in rows:
        formatted_fields = []
        for idx, field in enumerate(row):
            field_len = field_lengths[idx]
            spaces = ' ' * (field_len - len(field))
            formatted_fields.append('%s%s' % (field, spaces))
        print(' '.join(formatted_fields))

if __name__ == '__main__':
    main()
