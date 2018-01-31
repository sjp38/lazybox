#!/usr/bin/env python

program_decr = """
Construct and show a human readable, gnuplot convertible data in table or
records format from multiple files that containing results of experiment(s).

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

fpath = os.path.realpath(os.path.dirname(__file__))
sys.path.append(fpath + '/../gen_report')
import ltldat

def commonpath(paths):
    if len(paths) < 2:
        print "[ERROR] commonpath() should receive 2 or more paths!"
        exit(1)
    splitted = [p.split('/') for p in paths]
    common = []
    for idx, field in enumerate(splitted[0]):
        matched = 0
        for other in splitted[1:]:
            if other[idx] == field:
                matched += 1
        if matched == len(paths) - 1:
            common.append(field)
    cpath = '/'.join(common)
    if os.path.isdir(cpath):
        return cpath
    while len(cpath) > 0:
        cpath = cpath[:-1]
        if os.path.isdir(cpath):
            return cpath
    return cpath

def common_suffixpath(paths):
    if len(paths) < 2:
        print "[ERROR] cut_commonsuffix() should receive 2 or more paths!"
        exit(1)
    splitted = [p.split('/') for p in paths]
    common = []
    for idx, field in reversed(list(enumerate(splitted[0]))):
        matched = 0
        for other in splitted[1:]:
            if other[idx] == field:
                matched += 1
        if matched == len(paths) - 1:
            common.append(field)
    cpath = '/'.join(reversed(common))
    if cpath != '':
        cpath = '/' + cpath
    return cpath


parser = argparse.ArgumentParser(description=program_decr,
        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('form', choices=['table', 'records'],
        help='format to be used')
parser.add_argument('files', metavar='file', type=str, nargs='+',
        help='paths to files')
parser.add_argument('-n', '--normalize', action='store_true',
        help='normalize the table to first file value')
args = parser.parse_args()

form = vars(args)['form']
paths = vars(args)['files']
if len(paths) == 0:
    parser.print_help()
    exit(1)

normalize = vars(args)['normalize']

title = os.path.basename(paths[0])
for p in paths:
    if os.path.basename(p) != title:
        print "All filename should be %s but %s" % (title, p)
        exit(1)

commpath = commonpath(paths)
dirs = [os.path.dirname(p) for p in paths]
variants = [os.path.relpath(d, commpath) for d in dirs]
uniqueid_useless = True
for v in variants:
    if os.path.dirname(v) == '':
        uniqueid_useless = False
        break
if uniqueid_useless:
    variants = [os.path.dirname(v) for v in variants]
comm_suffix = common_suffixpath(variants)
variants = [v[0:len(v) - len(comm_suffix)] for v in variants]

if form == 'table':
    text = title + "\n\n\n"
    for idx, path in enumerate(paths):
        text += variants[idx] + "\n"
        with open(path, 'r') as f:
            for line in f:
                if line.startswith("#"):
                    continue
                line = line.replace(':', '')
                text += line
        text += "\n\n"

    table = ltldat.from_human_readable_records(text)
    if normalize:
        table = table.normalize()
    print table.human_readable_txt()
if form == 'records':
    text = ""
    for idx, path in enumerate(paths):
        text += variants[idx] + "\n"
        with open(path, 'r') as f:
            for line in f:
                if line.startswith("#"):
                    continue
                line = line.replace(':', '')
                text += line
        text += "\n\n"

    print text.strip()
