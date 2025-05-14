#!/usr/bin/env python3

import sys

def main():
    lines = sys.stdin.read()
    collected_lines = []
    for line in lines.split('\n'):
        if line == '':
            print(' '.join(collected_lines))
            print()
            collected_lines = []
            continue
        collected_lines.append(line)
    print(' '.join(collected_lines))

if __name__ == '__main__':
    main()
