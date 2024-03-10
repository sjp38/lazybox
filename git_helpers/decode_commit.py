#!/usr/bin/env python3

import argparse
import sys
import subprocess

def is_hash(word):
    if len(word) < 10:
        return False
    for c in word:
        if c not in '0123456789abcdef':
            return False
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('text', metavar='<file>',
                        help='file containing the text to decode, or stdin')
    args = parser.parse_args()

    if args.text == 'stdin':
        lines = sys.stdin.read().split('\n')
    else:
        with open(args.text, 'r') as f:
            lines = f.read().split('\n')
    for line in lines:
        print(line.strip())
        for separator in [',', '(', ')', '/']:
            line = line.replace(separator, ' ')
        for word in line.split():
            if is_hash(word):
                try:
                    decoded = subprocess.check_output(
                            ['git', 'describe', word]).decode().strip()
                except:
                    decoded = 'unknown'
                print('# decoding commit %s: %s' % (word, decoded))

if __name__ == '__main__':
    main()
