#!/usr/bin/env python3

import argparse
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cve_mbox', metavar='<file>', nargs='+',
                        help='cve description mbox file')
    args = parser.parse_args()

    counts = {}

    for mbox in args.cve_mbox:
        if mbox == 'stdin':
            cve_description = sys.stdin.read()
        else:
            with open(mbox, 'r') as f:
                cve_description = f.read()

        paragraphs = cve_description.split('\n\n')
        for par in paragraphs:
            lines = par.split('\n')
            if lines[0] == 'The file(s) affected by this issue are:':
                for f in lines[1:]:
                    f = f.strip()
                    if not f in counts:
                        counts[f] = 0
                    counts[f] += 1
    for f in sorted(counts.keys(), key=lambda f: counts[f]):
        print(counts[f], f)

    
if __name__ == '__main__':
    main()
