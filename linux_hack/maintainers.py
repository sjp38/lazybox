#!/usr/bin/env python3

import argparse
import os

def parse_maintainers(maintainers_file):
    with open(maintainers_file, 'r') as f:
        content = f.read()

    subsystems = {}
    keys = {
            'M:': 'maintainer',
            'R:': 'reviewer',
            'L:': 'list',
            'S:': 'status',
            'W:': 'webpage',
            'F:': 'files',
            }

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
            for key in keys:
                if line.startswith(key):
                    converted_key = keys[key]
                    if not converted_key in subsystem:
                        subsystem[converted_key] = []
                    subsystem[converted_key].append(' '.join(line.split()[1:]))
        subsystems[lines[0]] = subsystem
    return subsystems

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', metavar='<dir>', help='linux repo')
    args = parser.parse_args()

    maintainers_file = os.path.join(args.repo, 'MAINTAINERS')
    if not os.path.isfile(maintainers_file):
        print('wrong --repo')
        exit(1)

    subsystems = parse_maintainers(maintainers_file)

    print(subsystems)

if __name__ == '__main__':
    main()
