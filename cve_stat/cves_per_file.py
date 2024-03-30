#!/usr/bin/env python3

'''
Count number of CVEs that affecting specific files and print the output sorted
by the numbers.  Files can be specified using root directory and maximum depth,
like 'du' command.

Examples:

    $ git clone git://git.kernel.org/pub/scm/linux/security/vulns.git \
            ../../vulns
    $ ./cves_per_file.py ../../vulns/cve/published/*/*.mbox --root mm/damon/
    1 mm/damon/vaddr-test.h
    2 mm/damon/dbgfs.c
    $
    $ ./cves_per_file.py ../../vulns/cve/published/*/*.mbox --max_depth 1 \
            | tail -n 5
    22 kernel
    62 arch
    99 fs
    119 net
    351 drivers
    $
    $ ./cves_per_file.py ../../vulns/cve/published/*/*.mbox --max_depth 1 \
            --root drivers | tail -n 5
    11 drivers/i2c
    11 drivers/usb
    20 drivers/infiniband
    56 drivers/gpu
    81 drivers/net
    $
    $ ./cves_per_file.py ../../vulns/cve/published/*/*.mbox --max_depth 1 \
            --root drivers/net | tail -n 5
    2 drivers/net/can
    2 drivers/net/dsa
    6 drivers/net/usb
    26 drivers/net/wireless
    39 drivers/net/ethernet
'''

import argparse
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cve_mbox', metavar='<file>', nargs='+',
                        help='cve description mbox file')
    parser.add_argument('--root', metavar='<dir>',
                        help='root of files to count')
    parser.add_argument('--max_depth', type=int, metavar='<int>',
                        help='similar to that of du')
    args = parser.parse_args()

    if args.max_depth is not None and args.root:
        args.max_depth += len(args.root.split('/'))

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
                    if args.root is not None and not f.startswith(args.root):
                        continue
                    if args.max_depth:
                        f = '/'.join(f.split('/')[:args.max_depth])
                    if not f in counts:
                        counts[f] = 0
                    counts[f] += 1
    for f in sorted(counts.keys(), key=lambda f: counts[f]):
        print(counts[f], f)

    
if __name__ == '__main__':
    main()
