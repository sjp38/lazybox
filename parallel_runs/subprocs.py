#!/usr/bin/python3

import argparse
import os
import sys

import exp

parser = argparse.ArgumentParser()
parser.add_argument('pid', metavar='<pid>', type=int, help='process id')
args = parser.parse_args()


pid = args.pid

for pid in exp.childs_of(pid, False, print_tree=False):
    print(pid)
