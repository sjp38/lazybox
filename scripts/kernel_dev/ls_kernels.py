#!/usr/bin/env python3

import argparse
import datetime
import sys
import os

GRUBCFG_PATH = "/boot/grub/grub.cfg"

GRUB = "grub"
CUBOX = "cubox"
RASP2 = "rasp2"

def grub_kernels():
    with open(GRUBCFG_PATH) as f:
        lines = f.read()

    kernels = []
    for line in lines.split('\n'):
        tokens = line.split()
        if len(tokens) < 2:
            continue
        if tokens[0] == 'linux':
            kernel_position = tokens[1]
            kernel_name = kernel_position.lstrip('/boot/vmlinuz-')
            if not kernel_name in kernels:
                kernels.append(kernel_name)
    return kernels

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('bootloader', nargs='?', type=str, default='grub',
            choices=[GRUB, CUBOX, RASP2], metavar='bootloader',
            help='bootloader of the system')
    args = parser.parse_args()
    bootloader = args.bootloader

    if bootloader == GRUB:
        kernels = grub_kernels()
        print("\n".join(kernels))
    elif bootloader == CUBOX:
        print(bootloader + " is not supported yet...")
    elif bootloader == RASP2:
        print(bootloader + " is not supported yet...")
    else:
        print("Not supported bootloader %s\n" % bootloader)
