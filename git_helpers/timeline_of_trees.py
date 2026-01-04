#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

'''
Receives list of trees and show their evolution history.  E.g.,

2025-01-01 initial commit 1234567890ab for branch-A has made.
2025-02-01 From commit 234567890abc, branch-B has diverged from branch-A.
2025-03-01 branch-B got the final commit 34567890abcd.
2025-04-01 branch-A got the final commit 4567890abcde.
'''

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('trees', nargs='+', metavar='<tree>',
                        help='trees to show their development history')
    args = parser.parse_args()
    print('wip')

if __name__ == '__main__':
    main()
