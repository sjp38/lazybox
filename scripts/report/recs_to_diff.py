#!/usr/bin/env python3

"""
Convert record to diff from first value.  For example, files with content
```
pswpin 123
pswpin 124
pswpin 126
```

Will be converted to
```
0 0
1 1
2 2
```
"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('record_file', metavar='<file>', help='record file')
args = parser.parse_args()

filepath = args.record_file

with open(filepath, 'r') as f:
    first_val = 0
    for idx, line in enumerate(f):
        if idx == 0:
            first_val = int(line.split()[1])
        print(idx, int(line.split()[1]) - first_val)
