#!/usr/bin/env python3

import argparse

import _linux_kernel_cve

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dumpfile',
            help='dumped LinuxKernelCve json file')
    args = parser.parse_args()

    cves = _linux_kernel_cve.load_kernel_cves_from_json(args.dumpfile).values()
    print('total: %d' % len(cves))
    nr_fixed_before_added = {
            1: 0,
            7 * 24 * 3600: 0,
            2 * 7 * 24 * 3600: 0,
            4 * 7 * 24 * 3600: 0,
            8 * 7 * 24 * 3600: 0,
            16 * 7 * 24 * 3600: 0,
            32 * 7 * 24 * 3600: 0,
            64 * 7 * 24 * 3600: 0,
            128 * 7 * 24 * 3600: 0,
            }
    for cve in cves:
        if not 'mainline' in cve.fix_commits:
            continue
        committed_date = cve.fix_commits['mainline'].committed_date

        for thres in nr_fixed_before_added:
            if committed_date <= cve.added_date - thres:
                nr_fixed_before_added[thres] += 1
    for thres in sorted(nr_fixed_before_added.keys()):
        print('fixed %d weeks before added: %d (%f)' %
                (thres / 7 / 24 / 3600, nr_fixed_before_added[thres],
                    nr_fixed_before_added[thres] / len(cves)))

if __name__ == '__main__':
    main()
