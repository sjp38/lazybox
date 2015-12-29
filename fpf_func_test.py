#!/usr/bin/env python

"Do functional tests of fpf"

__author__ = "SeongJae Park"
__author__ += "\nHara Kang"
__email__ = "sj38.park@gmail.com"
__copyright__ = "Copyright (c) 2015, SeongJae Park"
__copyright__ += "\nCopyright (c) 2015, Hara Kang"
__license__ = "GPLv3"

import os
import sys
import ssh_args
import time

user, target, port, password = ssh_args.parse_input()
homepath = "/home/%s" % user
remote_exps_cmd = "expect ./remote_exps.exp"
lazybox_path = "%s/lazybox" % homepath
exps_paths = ["exps/pktgen_cat_assert", "exps/pktgen_http_single",
        "exps/pktgen_http_single_no_host", "exps/pktgen_http_multi",
        "exps/pktgen_http_multi_no_host", "exps/pktgen_hello",
        "exps/pktgen_dns_small"
        ]

fpf_path = "%s/fpf/src/build/fpf" % homepath

fpf_options = []
for cpu in ["1ffff"]:
    for workload in ["-p1 -H1 -m1 -c1 -t40"]:
        for assertion in [
                '-A "cat:2999999,3000000,3000003/' +
                    'host:baeddel.com,mimasa2525.blog.fc2.com,' +
                    'chocosweete.blogspot.kr" ',
                '-A "method:GET/host:imgnews.naver.net/accept:*\/*/referer:http:\/\/portal.nexentire.co.kr\/mail\/10881002.nsf\/3f733137e3189694492572df001ea342\/4e88d576f77ffd2149257dfd0001a0d5\/Body\/M1.2?OpenElement/' +
                    'user-agent:Mozilla\/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident\/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)" ',
                '-A "method:POST/uri:\/androidagent.jsc/host:-759821884/accept:*\/*/cookie:a854-4d86d21ed2dc491038" ',
                '-A "method:GET/accept:image\/png\, image\/svg+xml\, image\/*;q=0.8\, *\/*;q=0.5/user-agent:Mozilla\/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident\/5.0)/uri:\/m?u=http%3A%2F%2Fimagesearch.naver.com%2Fsearch.naver%3Fsm%3Dext%26viewloc%3D1%26where%3Didetail%26rev%3D31%26query%3D%25EC%259C%25A4%25EC%258A%25B9%25EC%2595%2584%26section%3Dimage%26res_fr%3D0%26res_to%3D0%26ie%3Dutf8%26face%3D0%26color%3D0%26ccl%3D0%26aq%3D0%26spq%3D1%26nx_search_query%3D%25EC%259C%25A4%25EC%258A%25B9%25EC%2595%2584%26nx_and_query%3D%26nx_sub_query%3D%26nx_search_hlquery%3D%26nx_search_fasquery%3D%26datetype%3D0%26startdate%3D0%26enddate%3D0%26start%3D141%26img_id%3Dblog26786680%257C19%257C10166495047_10&e=&i=&pid=SnRudspyi5ossu2pKy4ssssssfl-318834&os=Win32&ln=ko&sr=1920x1080&bw=1904&bh=973&c=24&j=Y&jv=1.8&k=Y&fv=16.0.0.305&sl=&ct=lan&p=Shockwave%20Flash&EOU" ',
                '-A "method:GET/accept:*\/*/referer:http:\/\/with.gsshop.com\/prd\/prd.gs?prdid=14157618&vodFlag=N&utm_source=Remarketing&utm_medium=advertise&utm_campaign=adbey_pop" ',
                '-A "content_type:22/version:769/length:160" ',
                '-A "flags:256/questions:1/answer_rrs:0/authority_rrs:0/additional_rrs:0/host:google.com/query_type:1/query_class:1" '
                    ]:
            option = "-c%s -n4 -- %s" % (cpu, workload)
            option += (" -f /home/sjpark/fpf/data/umd5_10m.fpf " +
                    "-F /home/sjpark/fpf/pcaps/single_http.pcap " +
                    "-D0 -L 2000000 ")
            option += assertion
            fpf_options.append(option)

exp = ""

# exps_path and fpf_options should have same length!!!
for idx, exps_path in enumerate(exps_paths):
        start_cmd = "start echo '==========================='\n"
        start_cmd += "start echo '%s'\n" % exps_path
        start_cmd += "start echo '==========================='"
        main_cmd = "main sleep 45"
        back_cmd = "back %s %s %s %s %s %s %s > /dev/null\n" % (
                remote_exps_cmd,
                user, target, port, password, lazybox_path, exps_path)
        back_cmd += "back %s %s" % (fpf_path, fpf_options[idx])
        exp = "%s\n%s\n%s\n\n" % (start_cmd, main_cmd, back_cmd)
        with open("tmp.exp", 'w') as f:
            f.write(exp)
        os.system("echo %s >> log" % ("fpf option: " + option + ", exps path: " + exps_path))
        os.system("./run_exps.py tmp.exp")
        time.sleep(5)
#os.system("rm ./tmp.exp")
