#!/usr/bin/env python

import getpass
import os
import sys

USAGE="%s <user name> <target> <ssh port> [password]" % sys.argv[0]

def parse_input():
    if len(sys.argv) < 4:
        print "usage: ", USAGE
        print ""
        exit(1)

    user = sys.argv[1]
    target = sys.argv[2]
    port = sys.argv[3]
    if len(sys.argv) > 4:
        password = sys.argv[4]
    else:
        password = getpass.getpass("password for %s at %s: " % (user, target))
    return user, target, port, password
