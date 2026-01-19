#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

'''
Similar to list_mm_patches, but use quilt series file.
'''

import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('series', metavar='<file>', help='the series file')
    args = parser.parse_args()

    with open(args.series, 'r') as f:
        for line in f:
            fields = line.split()
            if fields[0] == '#ENDBRANCH':
                print(fields[1])
                print()
            if line.startswith('#'):
                continue
            print(fields[0])

if __name__ == '__main__':
    main()
