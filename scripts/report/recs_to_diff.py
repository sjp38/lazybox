#!/usr/bin/env python2.7

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

import sys

if len(sys.argv) < 2:
    print "Usage: %s <record file>" % sys.argv[0]
    exit(1)

filepath=sys.argv[1]

with open(filepath, 'r') as f:
    first_val = 0
    for idx, line in enumerate(f):
        if idx == 0:
            first_val = int(line.split()[1])
        print idx, int(line.split()[1]) - first_val
