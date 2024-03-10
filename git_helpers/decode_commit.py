#!/usr/bin/env python3

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
    for line in sys.stdin:
        print(line.strip())
        for word in line.split():
            if is_hash(word):
                try:
                    decoded = subprocess.check_output(['git', 'describe', word])
                except:
                    decoded = 'unknown'
                print('# decoding commit %s: %s' % (word, decoded))

if __name__ == '__main__':
    main()
