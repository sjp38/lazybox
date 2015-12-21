#!/usr/bin/env python

import sys

def load_idx(cells, index):
    for idx, cell in enumerate(cells):
        index[idx] = cell.strip()

def load_logs(path):
    logs = {}
    log = None
    index = {}
    with open(path, 'r') as f:
        for line in f:
            if line.find("fpf option: ") == 0:
                log = []
                logs[line.rstrip('\n')] = log
                continue
            spltd = line.replace(" ", "").strip("\n").split(',')
            if spltd[0].find("thrs_stat") != 0:
                continue;
            if spltd[0] == "thrs_stat_cols":
                load_idx(spltd, index)
                continue
            result = {}
            log.append(result)
            for idx, val in enumerate(spltd):
                if val.strip() == "":
                    continue
                result[index[idx]] = val
    return logs, index

def pr_logs(logs, index):
    for option in logs.keys():
        print "option: ", option, "\n"
        for result in logs[option]:
            for key in index.keys().sort():
                print key, ": ", result[index[key]]

def isnumeric(val):
    return str(val).replace(".", "").replace("-", "").isdigit()

def cmp_cores(a, b):
    if len(a.split(",")) < 2 or len(b.split(",")) < 2:
        return 0
    corea = int(float(a.split(",")[1]))
    coreb = int(float(b.split(",")[1]))
    return corea - coreb

def pr_avg_logs(exps, index, sitems):
    str_ = ""

    for idx in sorted(index.keys()):
        str_ += index[idx] + ","
    print str_
    str_ = ""

    out = []
    for option in exps.keys():
        match = True
        for item in sitems:
            if option.find(item) == -1:
                match = False
                break
        if not match:
            continue

        exp = exps[option]
        avgs = {}

        for idx in index.keys():
             avgs[index[idx]] = 0

        unmatured = 0
        for idx, result in enumerate(exp):
            if result["totalpps"] == "0":
                unmatured += 1
                continue
            if idx == 0 or (unmatured != 0 and idx == unmatured + 1):
                unmatured += 1
                continue

            for key in result.keys():
                if isnumeric(result[key]):
                    avgs[key] += float(result[key])
                else:
                    avgs[key] = result[key]

        for idx in sorted(index.keys()):
            key = index[idx]
            if len(exp) == 0:
                avgs[key] = "NO RESULT!!!,"
                continue
            if isnumeric(avgs[key]):
                avgs[key] /= (len(exp) - unmatured)
            str_ += "%s" % avgs[key] + ","
        out.append(str_)
        str_ = ""
    out.sort(cmp_cores)
    for line in out:
        print line

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s <log file path> [option search items]" % sys.argv[0]
        exit(1)
    print "%s with option %s" % (sys.argv[0], " ".join(sys.argv[1:]))
    logs, index = load_logs(sys.argv[1])
    pr_avg_logs(logs, index, sys.argv[2:])
