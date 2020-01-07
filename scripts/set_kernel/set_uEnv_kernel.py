#!/usr/bin/env python3

import datetime
import sys
import os

UENV_PATH = "/boot/uEnv.txt"

bak_ts = datetime.datetime.now().strftime("%y%m%d%H%M%S")

def set_kernel_version(target_kernel):
    cmd = "./change_cubox_kernel.sh %s" % target_kernel
    print("change kernel to %s using cmd: %s\n" % (target_kernel, cmd))
    os.system(cmd)

def set_kernel_param(kernel_param):
    uEnv_content = "mmcargs=setenv bootargs " + kernel_param
    cmd = 'echo "%s" > %s' % (uEnv_content, UENV_PATH)
    print("set kernel param using cmd: ", cmd)
    os.system(cmd)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USAGE: %s <kernel name> [kernel parameter]\n" % sys.argv[0])
        print("\t kernel name: (cma|gcma|vanilla)")
        quit()
    kernel_name = sys.argv[1]
    kernel_param = ""
    if len(sys.argv) > 3:
        kernel_param = ' '.join(sys.argv[2:])
    print("set kernel %s with parameter %s\n" % (kernel_name, kernel_param))

    set_kernel_version(kernel_name)
    if kernel_param != "":
        set_kernel_param(kernel_param)
