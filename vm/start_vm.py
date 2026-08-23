#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

import argparse
import os
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--disk', default='overlay.disk', metavar='<file>',
                        help='disk to boot')
    parser.add_argument('--nr_cores', type=int, metavar='<int>',
                        help='number of cores for the VM')
    parser.add_argument('--memory_mb', metavar='<mega_bytes>',
                        help='memory size for the VM')
    parser.add_argument('--ssh_port', default=2242,
                        help='SSH port for the VM')
    parser.add_argument('--numa', action='append', nargs=3,
                        help='numa id, CPUs, mem size; e.g., 0 0-2 4G')
    parser.add_argument('--serial_file', metavar='<file>',
                        help='pipe serial output to a given file')
    parser.add_argument('--show_qemu_cmd', action='store_true',
                        help='show qemu cmd only')
    args = parser.parse_args()

    if args.nr_cores is None:
        res = subprocess.run(
                ['nproc'], capture_output=True, text=True, check=True)
        args.nr_cores = int(res.stdout) / 2

    if args.memory_mb is None:
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if not line.startswith('MemTotal:'):
                    continue
                fields = line.split()
                total_mem_kb = int(fields[1])
                args.memory_mb = int(total_mem_kb / 4 / 1024)
                break
    if args.memory_mb is None:
        print('no Memtotal?')
        exit(1)

    cmd = [
            'sudo', 'qemu-system-x86_64', '-enable-kvm', '-cpu', 'host',
            '-smp', '%d' % args.nr_cores, '-m', '%s' % args.memory_mb,
            '-drive', 'file=%s,if=virtio,cache=none' % args.disk,
            '-net', 'user,hostfwd=tcp::%s-:22' % args.ssh_port, '-net', 'nic',
            '-nographic']
    if args.numa is not None:
        for id, cpus, mem_size in args.numa:
            mem_id='mem%s' % id
            cmd += ['-object',
                    'memory-backend-ram,id=mem%s,size=%s' % (id, mem_size)]
            if cpus is not 'none':
                cmd += ['-numa',
                        'node,nodeid=%s,cpus=%s,memdev=mem%s' % (id, cpus, id)]
            else:
                cmd += ['-numa', 'node,nodeid=%s,memdev=mem%s' % (id, id)]
    if args.serial_file is not None:
        cmd += ['-serial', 'file:%s'% args.serial_file]

    if args.show_qemu_cmd is True:
        print(' '.join(cmd))
        exit(0)

    os.execlp('sudo', *cmd)

if __name__ == '__main__':
    main()
