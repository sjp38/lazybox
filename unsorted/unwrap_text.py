#!/usr/bin/env python3

import argparse
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ignore_prefix_len', type=int,
                        help='length of prefixes in input lines to ignore')
    args = parser.parse_args()

    lines = sys.stdin.read().split('\n')
    if args.ignore_prefix_len > 0:
        for idx, line in enumerate(lines):
            lines[idx] = line[args.ignore_prefix_len:]

    collected_lines = []
    for line in lines:
        if line == '':
            print(' '.join(collected_lines))
            print()
            collected_lines = []
            continue
        collected_lines.append(line)
    print(' '.join(collected_lines))

if __name__ == '__main__':
    main()
