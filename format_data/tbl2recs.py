#!/usr/bin/env python3

"""
Transfer table to records

For example, converts

    <...> name1 name2
    key1  val11 val12
    key2  val21 val22
    ...

to

    name1
    key1    val11
    key2    val21


    name2
    key1    val12
    key2    val22
"""

import sys

def main():
    names = None
    recs = []
    keys = []
    for line in sys.stdin:
        line = line.strip()
        if line.startswith('#'):
            continue
        if not names:
            names = line.split()[1:]
            continue
        for idx, field in enumerate(line.split()):
            if idx == 0:
                key = field
                keys.append(key)
                continue
            if len(recs) < idx:
                rec = {}
                recs.append(rec)
            else:
                rec = recs[idx - 1]
            rec[key] = field

    for idx, rec in enumerate(recs):
        print(names[idx])
        for key in keys:
            print('%s\t%s' % (key, rec[key]))
        if idx != len(recs) - 1:
            print('\n')

if __name__ == '__main__':
    main()
