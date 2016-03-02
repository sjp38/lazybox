#!/usr/bin/env python

"Help argument parsing for remote experiments"

__author__ = "SeongJae Park"
__email__ = "sj38.park@gmail.com"
__copyright__ = "Copyright (c) 2015-2016, SeongJae Park"
__license__ = "GPLv3"

import getpass
import os
import sys

USAGE="%s <user name> <target> <ssh port> [password]" % sys.argv[0]

def parse_input(custom_usage=USAGE):
    if len(sys.argv) < 4:
        print "usage: ", custom_usage
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
