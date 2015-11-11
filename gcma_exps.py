#!/usr/bin/env python

import os
import sys
import ssh_args

user, target, port, password = ssh_args.parse_input()

lbpath = "/home/%s/lazybox" % user

bootloader = "grub"
if target == "raspberrypi":
    bootloader = "rasp2"

k_cma = "cma"
k_gcma = "gcma"
k_vanilla = "vanilla"
kernels = [k_cma, k_gcma, k_vanilla]
kparam_cma = "coherent_pool=16M cma=64M smsc95xx.turbo_mode=N"
expspath = "./exps/"
exps = ["gcma", "gcma-blogbench",
        "still", "still-blogbench", "blogbench-still", "blogbench"]

for kernel in kernels:
    for exp in exps:
        kernel_param = ""
        if kernel in [k_cma, k_gcma]:
            kernel_param = kparam_cma
        if kernel == k_vanilla and (exp == "gcma" or exp == "gcma-blogbench"):
            continue
        os.system("expect ./remote_set_kernel.exp %s %s %s %s %s %s %s %s" % (
            user, target, port, password, lbpath, bootloader, kernel, kernel_param))
        if kernel == k_gcma:
            os.system("expect ./remote_zram_swap.exp %s %s %s %s %s 100M" % (
                user, target, port, password, lbpath))
        os.system("expect ./remote_exps.exp %s %s %s %s %s %s" % (
            user, target, port, password, lbpath, expspath + exp))
