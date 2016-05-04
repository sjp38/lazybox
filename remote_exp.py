#!/usr/bin/env python

import os
import sys
import ssh_args

USAGE="%s <user name> <target> <ssh port> [password] [exp]" % sys.argv[0]

user, target, port, password = ssh_args.parse_input(USAGE)
if len(sys.argv) < 6:
    exp = raw_input("exp to run in remote: ")
else:
    exp = sys.argv[5]

lbpath = "/home/%s/lazybox" % user

if password == "__lb_registered":
    cmd = "expect ./remote_exps_registered.exp %s %s %s %s %s" % (
            user, target, port, lbpath, exp)
else:
    cmd = "expect ./remote_exps.exp %s %s %s %s %s %s" % (
            user, target, port, password, lbpath, exp)
print "[remote_exp.py] do cmd $ ", cmd
os.system(cmd)
