#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', metavar='<url>', help='remote url')
    parser.add_argument('--repo', metavar='<dir>', default='./',
                        help='local repo')
    args = parser.parse_args()

    if args.url is None:
        print('--url is not set')
        exit(1)

    output_lines = subprocess.check_output(
            ['git', '-C', args.repo, 'remote', '-v']
            ).decode().strip().splitlines()
    for line in output_lines:
        fields = line.split()
        if len(fields) != 3:
            continue
        if fields[1] == args.url:
            print(fields[0])
            return

if __name__ == '__main__':
    main()
