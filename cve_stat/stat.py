#!/usr/bin/env python3

import argparse

import _linux_kernel_cve

def pr_break_to_report_stat(cves, tree, thresholds):
    nrs_for_thres = {thres: 0 for thres in thresholds}
    nr_total = 0
    for cve in cves:
        if not tree in cve.break_commits:
            continue
        nr_total += 1
        committed_date = cve.break_commits[tree].committed_date

        for thres in thresholds:
            if committed_date >= cve.added_date + thres:
                nrs_for_thres[thres] += 1
    print('%s tree' % tree)
    for thres in thresholds:
        print('%d/%d (%.3f %%) CVEs are reported %d weeks after committed' %
                (nrs_for_thres[thres], nr_total,
                    nrs_for_thres[thres] / nr_total * 100,
                    thres / 7 / 24 / 3600)),

def pr_fix_to_report_stat(cves, tree, thresholds, before):
    nrs_for_thres = {thres: 0 for thres in thresholds}
    nr_total = 0
    nr_not_yet_fixed = 0
    for cve in cves:
        if not tree in cve.break_commits:
            continue
        nr_total += 1
        if not tree in cve.fix_commits:
            nr_not_yet_fixed += 1
            continue
        committed_date = cve.fix_commits[tree].committed_date

        for thres in thresholds:
            if before and committed_date <= cve.added_date - thres:
                nrs_for_thres[thres] += 1
            if not before and committed_date >= cve.added_date + thres:
                nrs_for_thres[thres] += 1
    print('%s tree' % tree)
    for thres in thresholds:
        print('%d/%d (%.3f %%) CVEs are fixed %d weeks %s being added' %
                (nrs_for_thres[thres], nr_total,
                    nrs_for_thres[thres] / nr_total * 100,
                    thres / 7 / 24 / 3600,
                    'before' if before else 'after'))
    if not before:
        print('%d/%d (%.3f %%) CVEs are not fixed yet' %
                (nr_not_yet_fixed, nr_total,
                    nr_not_yet_fixed / nr_total * 100))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dumpfile',
            help='dumped LinuxKernelCve json file')
    args = parser.parse_args()

    cves = _linux_kernel_cve.load_kernel_cves_from_json(args.dumpfile).values()
    for before in [True, False]:
        for tree in ['mainline', '6.4', '6.1', '5.15', '5.10', '5.4', '4.19',
                '4.14']:
            pr_fix_to_report_stat(cves, tree,
                    [
                        1,
                        7 * 24 * 3600,
                        2 * 7 * 24 * 3600,
                        4 * 7 * 24 * 3600,
                        8 * 7 * 24 * 3600,
                        16 * 7 * 24 * 3600,
                        32 * 7 * 24 * 3600,
                        64 * 7 * 24 * 3600,
                        128 * 7 * 24 * 3600,
                        ], before)
            print()
    for tree in ['mainline', '6.4', '6.1', '5.15', '5.10', '5.4', '4.19',
            '4.14']:
        pr_break_to_report_stat(cves, tree,
                [
                    -1 * 7 * 24 * 3600,
                    1,
                    7 * 24 * 3600,
                    2 * 7 * 24 * 3600,
                    4 * 7 * 24 * 3600,
                    8 * 7 * 24 * 3600,
                    16 * 7 * 24 * 3600,
                    32 * 7 * 24 * 3600,
                    64 * 7 * 24 * 3600,
                    128 * 7 * 24 * 3600,
                    ])
        print()

if __name__ == '__main__':
    main()
