#!/usr/bin/env python

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
        if line.find('initrd') != -1:
            kernel_position = line.split()[1]
            kernel_name = kernel_position.lstrip('/boot/initrd.img-')
            if not kernel_name in kernels:
                kernels.append(kernel_name)
    return kernels

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("USAGE: %s <bootloader>\n" %
                sys.argv[0])
        print "\tbootloader: (%s|%s|%s)" % (GRUB, CUBOX, RASP2)
        quit()
    bootloader = sys.argv[1]

    if bootloader == GRUB:
        kernels = grub_kernels()
        print "\n".join(kernels)
    elif bootloader == CUBOX:
        print bootloader + " is not supported yet..."
    elif bootloader == RASP2:
        print bootloader + " is not supported yet..."
    else:
        print "Not supported bootloader %s\n" % bootloader
