#!/usr/bin/env python3

import argparse

import _linux_kernel_cve

def secs_to_days(secs):
    return secs / 3600 / 24

def pr_percentiles(values):
    values = sorted(values)
    print('0 %d' % (secs_to_days(values[0] - 1)))
    for i in range(1, 100):
        print('%d %d' % (i, secs_to_days(values[int(i / 100 * len(values))])))
    print('100 %d' % (secs_to_days(values[-1] + 1)))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dumpfile',
            help='dumped LinuxKernelCve json file')
    parser.add_argument('--metric',
            choices=[
                'report_to_fix_authored',
                'report_to_fix_committed',
                'broken_to_reported',
                ],
            help='metric to show')
    parser.add_argument('--skip_negatives', action='store_true',
            help='ignore negative metrics (useful for logscale plotting)')
    args = parser.parse_args()

    cves = _linux_kernel_cve.load_kernel_cves_from_json(args.dumpfile).values()

    report_to_fix_committed_secs = {}   # tree: [sec]
    report_to_fix_authored_secs = {}    # tree: [sec]
    broken_to_reported_secs = {}
    for tree in ['mainline', '6.4', '6.1', '5.15', '5.10', '5.4', '4.19',
                '4.14']:
        for cve in cves:
            if not tree in cve.fix_commits:
                continue
            if not tree in report_to_fix_committed_secs:
                report_to_fix_committed_secs[tree] = []
            if not tree in report_to_fix_authored_secs:
                report_to_fix_authored_secs[tree] = []
            if not tree in broken_to_reported_secs:
                broken_to_reported_secs[tree] = []

            secs = cve.fix_commits[tree].committed_date - cve.added_date
            if not args.skip_negatives or secs >= 0:
                report_to_fix_committed_secs[tree].append(secs)

            secs = cve.fix_commits[tree].authored_date - cve.added_date
            if not args.skip_negatives or secs >= 0:
                report_to_fix_authored_secs[tree].append(secs)

            if not tree in cve.break_commits:
                continue
            secs = cve.added_date - cve.break_commits[tree].committed_date
            if not args.skip_negatives or secs >= 0:
                broken_to_reported_secs[tree].append(secs)

    for tree in ['mainline', '6.4', '6.1', '5.15', '5.10', '5.4', '4.19',
                '4.14']:
        print(tree)
        if args.metric == 'report_to_fix_authored':
            pr_percentiles(report_to_fix_authored_secs[tree])
        elif args.metric == 'report_to_fix_committed':
            pr_percentiles(report_to_fix_committed_secs[tree])
        elif args.metric == 'broken_to_reported':
            pr_percentiles(broken_to_reported_secs[tree])

        print()
        print()

if __name__ == '__main__':
    main()
