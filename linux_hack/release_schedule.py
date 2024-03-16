#!/usr/bin/env python3

# TODO
# - expect rc8 based on the history
# - support merge window schedule

import argparse
import datetime
import os
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.description = 'Expect future linux release schedule'
    parser.add_argument('--linux', metavar='<repo>', default='./',
                        help='path to the linux tree')
    parser.add_argument('--until', metavar='<days>', type=int, default=365,
                        help='future days to expect the schedule until')
    args = parser.parse_args()

    major_ver = None
    minor_ver = None
    with open(os.path.join(args.linux, 'Makefile'), 'r') as f:
        for line in f:
            fields = line.strip().split()
            if fields[:2] == ['VERSION', '=']:
                major_ver = int(fields[2])
            if fields[:2] == ['PATCHLEVEL', '=']:
                minor_ver = int(fields[2])
            if fields[:2] == ['EXTRAVERSION', '=']:
                if len(fields) > 2:
                    minor_ver -= 1
                break
    curr_ver = 'v%s.%s' % (major_ver, minor_ver)
    git_cmd = ['git', '-C', args.linux]
    curr_ver_date = subprocess.check_output(
            ['git', '-C', args.linux, 'log', '-1', '--pretty=%cd',
             '--date=iso', curr_ver]).decode().strip().split()[0]
    ver_date = datetime.datetime.strptime(curr_ver_date, '%Y-%m-%d')
    ver = [major_ver, minor_ver]

    now = datetime.datetime.now()

    while ver_date - now < datetime.timedelta(days=args.until):
        # 9 weeks per release
        ver_date += datetime.timedelta(days=63)
        ver[1] += 1
        print('%s: v%d.%d' % (ver_date.strftime('%Y-%m-%d'), ver[0], ver[1]))

if __name__ == '__main__':
    main()
