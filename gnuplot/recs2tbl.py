#!/usr/bin/env python3

"""
Convert records to table
"""

import sys

def main():
    rec_names = []
    keys = []
    recs = []
    rec = {}
    rec_name = ''
    for line in sys.stdin:
        line = line.strip()
        if line == '':
            if rec:
                recs.append(rec)
                rec_names.append(rec_name)
            rec = {}
            rec_name = []
            continue
        if not rec_name:
            rec_name = line
            continue
        key, val = line.split()
        if key[-1] == ':':
            key = key[:-1]
        if not key in keys:
            keys.append(key)
        rec[key] = val
    if rec:
        recs.append(rec)
        rec_names.append(rec_name)

    print('xxx\t%s' % '\t'.join(rec_names))
    for key in keys:
        fields = []
        for idx, rec in enumerate(recs):
            if idx == 0:
                fields.append(key)
            if key in rec:
                fields.append(rec[key])
            else:
                fields.append('-')
        print('\t'.join(fields))

if __name__ == '__main__':
    main()
