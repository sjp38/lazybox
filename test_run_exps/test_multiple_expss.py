#!/usr/bin/env python2.7

"test multiple experiments spec files support of run_exps.py"

import os

testdir = os.path.abspath(os.path.dirname(__file__))
lzdir = os.path.join(os.path.dirname(__file__), os.pardir)
lzdir = os.path.abspath(lzdir)
cmd = "%s %s %s" % (os.path.join(lzdir, "run_exps.py"),
        os.path.join(testdir, "hello"), os.path.join(testdir, "bye"))
print "execute: ", cmd
os.system(cmd)
