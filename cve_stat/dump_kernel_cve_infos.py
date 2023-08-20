#!/usr/bin/env python3

import argparse
import json
import os
import sys

bindir = os.path.dirname(sys.argv[0])

import _linux_kernel_cve

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--linux_kernel_cves', metavar='<dir>',
            default=os.path.join(bindir, '..', '..', 'linux_kernel_cves'),
            help='path to local linux_kernel_cves repo')
    parser.add_argument('--linux', metavar='<dir>',
            default=os.path.join(bindir, '..', '..', 'linux'),
            help='path to local linux repo')
    parser.add_argument('--output', metavar='<file>',
            default='dumped_cve_info.json',
            help='path to json file to dump the information')
    args = parser.parse_args()

    data_dir = os.path.join(args.linux_kernel_cves, 'data')
    with open(os.path.join(data_dir, 'kernel_cves.json'), 'r') as f:
        main_infos = json.load(f)
    with open(os.path.join(data_dir, 'stream_data.json'), 'r') as f:
        stream_breaks = json.load(f)
    with open(os.path.join(data_dir, 'stream_fixes.json'), 'r') as f:
        stream_fixes = json.load(f)

    to_dump = {}
    for cve_name in main_infos:
        to_dump[cve_name] = _linux_kernel_cve.LinuxKernelCve(cve_name,
                args.linux_kernel_cves, main_infos, stream_breaks,
                stream_fixes, args.linux).to_kvpairs()
        print(json.dumps(to_dump[cve_name], indent=4))
    with open(args.output, 'w') as f:
        json.dump(to_dump, f, indent=4)

if __name__ == '__main__':
    main()
