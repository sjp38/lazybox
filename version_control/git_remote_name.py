#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

import argparse
import subprocess

def get_remote_name_for(repo, url):
    output_lines = subprocess.check_output(
            ['git', '-C', repo, 'remote', '-v']
            ).decode().strip().splitlines()
    urls = [url]
    if url.startswith('git://git.kernel.org'):
        urls.append(url.replace('git://', 'https://'))
    elif url.startswith('https://git.kernel.org'):
        urls.append(url.replace('https://', 'git://'))
    for line in output_lines:
        fields = line.split()
        if len(fields) != 3:
            continue
        if fields[1] in urls:
            return fields[0]
    return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', metavar='<url>', help='remote url')
    parser.add_argument('--repo', metavar='<dir>', default='./',
                        help='local repo')
    args = parser.parse_args()

    if args.url is None:
        print('--url is not set')
        exit(1)

    print(get_remote_name_for(args.repo, args.url))

if __name__ == '__main__':
    main()
