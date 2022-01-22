#!/usr/bin/env python3

import argparse

'''
Assumption
- This script is periodically called by cron
Input
- path to the repo
- trees to check, and
- test to run against those
Works
- check if the trees have updated
- run the test against the updated ones, and
- provide the reports
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', metavar='<path>',
            help='path to the local repo')
    parser.add_argument('--tree_to_track',
            metavar=('<name>', '<url>', '<branch>'), nargs=3, action='append',
            help='remote tree to track')
    parser.add_argument('--test', metavar='<path>',
            help='test to run')
    args = parser.parse_args()
    print(args)

if __name__ == '__main__':
    main()
