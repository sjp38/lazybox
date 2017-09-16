#!/usr/bin/env python

program_decr = """
Construct and show a human readable, gnuplot convertible data from multiple
files that containing results of experiment(s).

Each file should be located in '<common directory>/
<variance level1>/.../<variance levelN>/<unique id>/ directory.  Unique id
would be id of repeated run or 'avg' or 'stdev', etc.  Variance should be more
common for lower level and more specific for higher level.  For example,
following case would be possible:
```
results/workloadA/systemA/configA/1/perf
results/workloadA/systemA/configA/2/perf
results/workloadA/systemA/configA/avg/perf
results/workloadA/systemA/configB/1/perf
results/workloadA/systemB/configA/1/perf
```

Each file should be constructed with `<key>: <value>` lines.
"""

import argparse
import os
import sys

sys.path.append(os.environ['HOME'] + '/lazybox/scripts/gen_report')
import ltldat

parser = argparse.ArgumentParser(description=program_decr,
        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('files', metavar='file', type=str, nargs='+',
        help='paths to files')
args = parser.parse_args()

paths = vars(args)['files']
if len(paths) == 0:
    parser.print_help()
    exit(1)

title = os.path.basename(paths[0])
for p in paths:
    if os.path.basename(p) != title:
        print "All filename should be %s but %s" % (title, p)
        exit(1)

commpath = os.path.commonprefix(paths)
dirs = [os.path.dirname(p) for p in paths]
variants = [os.path.relpath(d, commpath) for d in dirs]
uniqueid_useless = True
for v in variants:
    if os.path.dirname(v) == '':
        uniqueid_useless = False
        break
if uniqueid_useless:
    variants = [os.path.dirname(v) for v in variants]

text = title + "\n\n\n"
for idx, path in enumerate(paths):
    text += variants[idx] + "\n"
    with open(path, 'r') as f:
        for line in f:
            line = line.replace(':', '')
            text += line
    text += "\n\n"

print ltldat.from_human_readable_txt(text).human_readable_txt()
