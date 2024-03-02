#!/usr/bin/env python3

import argparse
import datetime
import sys
import os

GRUBCFG_PATH = "/boot/grub/grub.cfg"
GRUB_PATH = "/etc/default/grub"

UENV_PATH = "/boot/uEnv.txt"

GRUB = "grub"
CUBOX = "cubox"
RASP2 = "rasp2"

bak_ts = datetime.datetime.now().strftime("%y%m%d%H%M%S")

def set_grub_kernel(target_kernel):
    with open(GRUBCFG_PATH) as f:
        lines = f.read()

    prev_section = False
    found = False
    position = 0
    for line in lines.split('\n'):
        if line.find('Previous') != -1 or line.find('Advanced') != -1:
            prev_section = True
            position = 0
            print('previous or advanced line found: %s' % line)
            continue;

        tokens = line.split()
        if len(tokens) < 2:
            continue
        if tokens[0] == "linux":
            kernel_position = tokens[1]
            kernel_name = kernel_position.lstrip('/boot/vmlinuz-')
            if kernel_name == target_kernel:
                found = True
                break
            else:
                position += 1
    if not found:
        print("failed. kernel %s not found" % target_kernel)
        return

    set_default = '%s' % position
    if prev_section:
        set_default = '"1>%s"' % set_default

    if backup_grub:
        cmd = "cp -f %s %s.bak.%s" % (GRUBCFG_PATH, "grub.cfg", bak_ts)
        print("backup with cmd %s" % cmd)
        os.system(cmd)

    cmd = "sed -i 's/.*set default.*/set default=%s/' %s" % (
            set_default, GRUBCFG_PATH)
    print("set kernel with cmd: ", cmd)
    ret = os.system(cmd)
    if ret != 0:
        print("FAILED to set kernel!!!")

def set_uenv_kernel(target_kernel):
    # TODO: relative path based on assumption should be removed in future
    cmd = "./bin/change_cubox_kernel.sh %s" % target_kernel
    print("change kernel to %s using cmd: %s\n" % (target_kernel, cmd))
    os.system(cmd)

def set_rasp2_kernel(target_kernel):
    cmd = "cp -R /boots/%s/* /" % target_kernel
    print("change kernel to %s using cmd %s\n" % (target_kernel, cmd))
    os.system(cmd)
    cmd = "cp /boots/config.%s.txt /boot/config.txt" % target_kernel
    print("change config using cmd: %s\n" % cmd)
    os.system(cmd)

def set_grub_kernel_param(kernel_param):
    if backup_grub:
        cmd = "cp -f %s %s.bak.%s" % (GRUB_PATH, "grub", bak_ts)
        print("backup with cmd %s" % cmd)
        os.system(cmd)

    kernel_param = kernel_param.replace('/', '\/')
    cmd = "sed -i 's/%s*/%s\"%s\"/' %s" % ("GRUB_CMDLINE_LINUX_DEFAULT=.",
            "GRUB_CMDLINE_LINUX_DEFAULT=", kernel_param, GRUB_PATH)
    print("set kernel param with cmd: ", cmd)
    os.system(cmd)

    cmd = "update-grub"
    print(cmd)
    os.system(cmd)

def set_uenv_kernel_param(kernel_param):
    uEnv_content = "mmcargs=setenv bootargs " + kernel_param
    cmd = 'echo "%s" > %s' % (uEnv_content, UENV_PATH)
    print("set kernel param using cmd: ", cmd)
    os.system(cmd)

def set_rasp2_kernel_param(kernel_param):
    orig_cmdline = "dwc_otg.lpm_enable=0 console=ttyAMA0,115200 console=tty1"
    orig_cmdline += " root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline"
    orig_cmdline += " rootwait"
    cmdline = orig_cmdline + " " + kernel_param
    with open('/boot/cmdline.txt', 'w') as f:
        f.write(cmdline)
    print("kernel param changed to: ")
    os.system("cat /boot/cmdline.txt")
    print("")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--bootloader', type=str, default=GRUB,
            choices=[GRUB, CUBOX, RASP2], metavar='<bootloader>',
            help='bootloader of the system')
    parser.add_argument('kernel_name', type=str, metavar='<kernel>',
            help='name of kernel to be used')
    parser.add_argument('kernel_param', nargs='*', type=str,
            metavar='<kernel parameter>',
            help='parameter of the kernel to be used')
    parser.add_argument('--backup', action='store_true',
            help='backup the grub config file')
    args = parser.parse_args()

    bootloader=args.bootloader
    kernel_name = args.kernel_name
    kernel_param = ' '.join(args.kernel_param)
    backup_grub = args.backup

    print("set kernel %s with parameter '%s' on %s" %
            (kernel_name, kernel_param, bootloader))

    if bootloader == GRUB:
        if kernel_param != "":
            set_grub_kernel_param(kernel_param)
        set_grub_kernel(kernel_name)
    elif bootloader == CUBOX:
        set_uenv_kernel(kernel_name)
        if kernel_param != "":
            set_uenv_kernel_param(kernel_param)
    elif bootloader == RASP2:
        set_rasp2_kernel(kernel_name)
        set_rasp2_kernel_param(kernel_param + " ")
    else:
        print("Not supported bootloader %s\n" % bootloader)
