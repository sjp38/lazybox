#!/usr/bin/env python3

program_decr = """
Make user specified status (average, min, max, stdev) from single or multiple
files with same format.  In case of single file, it assumes the file to be in a
single record format and get statistic of second field only.  In case of
multiple files, it assumes the files to be in table format.  The input file
should be generated using `files_to.py`.
"""

import argparse
import math
import os
import sys

fpath = os.path.realpath(os.path.dirname(__file__))
sys.path.append(fpath + '/../gen_report')
import ltldat

parser = argparse.ArgumentParser(description=program_decr,
        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('stat', choices=['avg', 'min', 'max', 'stdev'],
        help='type of stat you want')
parser.add_argument('files', metavar='file', type=str, nargs='+',
        help='paths to files')
args = parser.parse_args()

target = vars(args)['stat']
paths = vars(args)['files']

def single_file_stat(path):
    nrs = []
    key = ''
    to_print = []
    with open(path, 'r') as f:
        for l in f:
            fields = l.split()
            if not key:
                key = fields[0]
                to_print.append(key)
            nrs.append(float(fields[1]))
    if target == 'avg':
        to_print.append(sum(nrs) / len(nrs))
    elif target == 'min':
        to_print.append(min(nrs))
    elif target == 'max':
        to_print.append(max(nrs))
    elif target == 'stdev':
        avg = sum(nrs) / len(nrs)
        variance = sum([pow(v - avg, 2) for v in nrs]) / len(nrs)
        to_print.append(math.sqrt(variance))
    print('\t'.join([str(x) for x in to_print]))

def pr_stderr(msg):
    sys.stderr.write(msg + "\n")

if len(paths) == 0:
    parser.print_help()
    exit(1)

if len(paths) == 1:
    single_file_stat(paths[0])
    exit(0)

datas = []
for p in paths:
    with open(p, 'r') as f:
        datas.append(f.read().strip().split('\n'))
        if len(datas[0]) != len(datas[-1]):
            print("[Error] Number of lines are different for %s!" % p)
            exit(1)

for lidx in range(len(datas[0])):
    lines = [data[lidx] for data in datas]
    values = []
    for fidx in range(len(lines[0].split())):
        fields = [l.split()[fidx] for l in lines]
        value = ""
        try:
            nrs = [float(f) for f in fields]
            if target == 'avg':
                value = sum(nrs) / len(nrs)
            elif target == 'min':
                value = min(nrs)
            elif target == 'max':
                value = max(nrs)
            elif target == 'stdev':
                avg = sum(nrs) / len(nrs)
                variance = sum([pow(v - avg, 2) for v in nrs]) / len(nrs)
                value = math.sqrt(variance)
                if value > avg / 10:
                    pr_stderr("[WARNING] stdev %s, avg %s, %.2f stdev/avg!" % (
                        value, avg, float(value) / avg))
        except ValueError:
            if not all(f == fields[0] for f in fields):
                print("[Error] different text field! %s" % fields)
                exit(1)
            value = fields[0]
        values.append(value)
    print("\t".join([str(v) for v in values]))
