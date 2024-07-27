#!/usr/bin/env python3

import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', metavar='<dir>', help='linux repo')
    args = parser.parse_args()

    maintainers_file = os.path.join(args.repo, 'MAINTAINERS')
    if not os.path.isfile(maintainers_file):
        print('wrong --repo')
        exit(1)

    with open(maintainers_file, 'r') as f:
        content = f.read()

    subsystems = {}

    lists_started = False
    for paragraph in content.split('\n\n'):
        if (lists_started is False and
            paragraph.startswith('3C59X NETWORK DRIVER')):
            lists_started = True
        if not lists_started:
            continue
        lines = paragraph.split('\n')
        subsystem = {'name': lines[0]}
        for line in lines[1:]:
            if line.startswith('M:'):
                subsystem['maintainer'] = line
        subsystems[lines[0]] = subsystem
    print(subsystems)

if __name__ == '__main__':
    main()
