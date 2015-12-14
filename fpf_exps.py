#!/usr/bin/env python

import os
import sys
import ssh_args
import time

user, target, port, password = ssh_args.parse_input()
homepath = "/home/%s" % user
remote_exps_cmd = "expect ./remote_exps.exp"
lazybox_path = "%s/lazybox" % homepath
#exps_paths = ["exps/pktgen_todcslab", "exps/pktgen_trafficsample",
#                "exps/pktgen_wireshark"]
exps_paths = ["exps/pktgen_syn64", "exps/pktgen_wireshark"]

fpf_path = "%s/fpf/src/build/fpf" % homepath

fpf_options = []
for cpu in ["3", "1f", "1ff", "3ff", "7ff", "fff", "1fff", "1ffff", "1ffffff", "ffffffff"]:
    for workload in ["-p1 -H1 -m1 -c1 -t1",
                    "-p1 -H1 -m1 -c1 -t40",
                    "-p0 -H0 -m0 -c0 -t0",
                    "-p0 -H0 -m0 -c0 -t1",
                    "-p1 -H1 -m0 -c0 -t0",
                    "-p0 -H0 -m1 -c1 -t0",
                    "-p0 -H0 -m1 -c0 -t0",
                    "-p0 -H0 -m0 -c1 -t0"]:
        option = "-c%s -n4 -- %s" % (cpu, workload)
        option += (" -f /home/sjpark/fpf/data/umd5_10m.fpf " +
                "-D0 -L 2000000 -F /home/sjpark/fpf/pcaps/single_http.pcap")
        fpf_options.append(option)

exp = ""
for option in fpf_options:
    for exps_path in exps_paths:
        start_cmd = "start echo '==========================='\n"
        start_cmd += "start echo '%s'\n" % exps_path
        start_cmd += "start echo '==========================='"
        main_cmd = "main sleep 45"
        back_cmd = "back %s %s %s %s %s %s %s > /dev/null\n" % (
                remote_exps_cmd,
                user, target, port, password, lazybox_path, exps_path)
        back_cmd += "back %s %s" % (fpf_path, option)
        exp = "%s\n%s\n%s\n\n" % (start_cmd, main_cmd, back_cmd)
        with open("tmp.exp", 'w') as f:
            f.write(exp)
        os.system("echo %s >> log" % ("fpf option: " + option + ", exps path: " + exps_path))
        os.system("./run_exps.py tmp.exp")
        time.sleep(5)
#os.system("rm ./tmp.exp")
