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

def is_supported_stat_metric(stat_metric):
    if stat_metric in ['avg', 'min', 'max', 'stdev', 'median']:
        return True
    if len(stat_metric) > 1 and stat_metric[0].lower() == 'p':
        try:
            percentile = float(stat_metric[1:])
            return True
        except:
            return False
    return False

def get_stat(target, nrs):
    if target == 'avg':
        return sum(nrs) / len(nrs)
    elif target == 'min':
        return min(nrs)
    elif target == 'max':
        return max(nrs)
    elif target == 'stdev':
        avg = sum(nrs) / len(nrs)
        variance = sum([pow(v - avg, 2) for v in nrs]) / len(nrs)
        return math.sqrt(variance)
    elif target == 'median':
        return sorted(nrs)[int(len(nrs) / 2)]
    elif len(target) > 0 and target[0].lower() == 'p':
        percentile = int(target[1:])
        idx = int(percentile / 100 * len(nrs))
        return sorted(nrs)[idx]

def single_file_stat(target, path):
    nrs = []
    to_print = []
    if path == 'stdin':
        content = sys.stdin.read()
    else:
        with open(path, 'r') as f:
            content = f.read()
    for l in content.split('\n'):
        fields = l.split()
        if len(nrs) == 0 and len(fields) > 1:
            key = fields[0]
            to_print.append(key)
        if len(fields) > 1:
            nrs.append(float(fields[1]))
        elif len(fields) == 1:
            nrs.append(float(fields[0]))
    to_print.append(get_stat(target, nrs))
    print('\t'.join([str(x) for x in to_print]))

def pr_stderr(msg):
    sys.stderr.write(msg + "\n")

def main():
    parser = argparse.ArgumentParser(description=program_decr,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
            'stat',
            help='type of stat you want.  ' \
                    'avg, min, max, stdev, median, pXX are supported.')
    parser.add_argument('files', metavar='file', type=str, nargs='+',
            help='paths to files')
    args = parser.parse_args()

    if not is_supported_stat_metric(args.stat):
        print('unsupported stat metric')
        exit(1)

    target = args.stat
    paths = args.files

    if len(paths) == 1:
        single_file_stat(target, paths[0])
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
                value = get_stat(target, nrs)
                if target == 'stdev':
                    avg = sum(nrs) / len(nrs)
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

if __name__ == '__main__':
    main()
