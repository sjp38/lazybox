#!/usr/bin/env python

import os
import sys
import ssh_args
import time

user, target, port, password = ssh_args.parse_input()
homepath = "/home/%s" % user
remote_exps_cmd = "expect ./remote_exps.exp"
lazybox_path = "%s/lazybox" % homepath
exps_paths = ["exps/pktgen_todcslab", "exps/pktgen_trafficsample",
                "exps/pktgen_wireshark"]
fpf_path = "%s/fpf/src/build/fpf" % homepath

exp = ""
for exps_path in exps_paths:
    start_cmd = "start echo '==========================='\n"
    start_cmd += "start echo '%s'\n" % exps_path
    start_cmd += "start echo '==========================='"
    main_cmd = "main sleep 30"
    back_cmd = "back %s %s %s %s %s %s %s > /dev/null\n" % (
            remote_exps_cmd,
            user, target, port, password, lazybox_path, exps_path)
    back_cmd += "back %s -c 1ff -n 4 -- -f %s/fpf/data/umd5_10m.fpf" % (
            fpf_path, homepath)
    exp = "%s\n%s\n%s\n\n" % (start_cmd, main_cmd, back_cmd)
    with open("tmp.exp", 'w') as f:
        f.write(exp)
    os.system("./run_exps.py tmp.exp")
    time.sleep(5)
#os.system("rm ./tmp.exp")
