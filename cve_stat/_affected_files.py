#!/usr/bin/env python3

import argparse
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cve_mbox', metavar='<file>',
                        help='cve description mbox file')
    args = parser.parse_args()

    if args.cve_mbox == 'stdin':
        cve_description = sys.stdin.read()
    else:
        with open(args.cve_mbox, 'r') as f:
            cve_description = f.read()

    paragraphs = cve_description.split('\n\n')
    for par in paragraphs:
        lines = par.split('\n')
        if lines[0] == 'The file(s) affected by this issue are:':
            print('\n'.join(l.strip() for l in lines[1:]))
    
if __name__ == '__main__':
    main()
