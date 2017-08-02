#!/usr/bin/env python

import os
import sys

def parse_cpuinfo():
    cpus = []

    with open('/proc/cpuinfo', 'r') as f:
        cpu = {}
        cpus.append(cpu)
        for line in f:
            line = line.strip()
            if line == "":
                cpu = {}
                cpus.append(cpu)
                continue

            tokens = line.split(':')
            key = tokens[0].strip()
            val = ''
            if len(tokens) > 1:
                val = tokens[1].strip()
            cpu[key] = val
    return cpus[:-1]

def parse_topology():
    sysfs_cpu_path = "/sys/devices/system/cpu/"
    cpuids = []
    for item in os.listdir(sysfs_cpu_path):
        if not os.path.isdir(os.path.join(sysfs_cpu_path, item)):
            continue
        if not item.startswith("cpu"):
            continue
        try:
            cpuids.append(int(item[3:]))
        except ValueError:
            print "no int"
            continue

    cpus = {}
    for cpuid in cpuids:
        cpuinfo = {}
        cpus[cpuid] = cpuinfo
        cpuinfo["cpuid"] = cpuid
        for field in ["physical_package_id", "core_id"]:
            value = -1
            try:
                with open(sysfs_cpu_path + "cpu%s/topology/%s" %
                        (cpuid, field), 'r') as f:
                    value = int(f.read().strip())
            except IOError:
                pass
            cpuinfo[field] = value
    for cpuid in sorted(cpus.keys()):
        c = cpus[cpuid]
        print "cpuid: %s, socket: %s, core: %s" % (
                c["cpuid"], c["physical_package_id"], c["core_id"])

def pr_topology(cpus):
    sockets = {}
    for c in cpus:
        try:
            sockets[int(c["physical id"])].append(c)
        except KeyError as e:
            sockets[int(c["physical id"])] = [c]
    for sk in sorted(sockets.keys()):
        print "[socket %s]" % sk
        pcores = {}
        for c in sockets[sk]:
            try:
                pcores[int(c["core id"])].append(c)
            except KeyError as e:
                pcores[int(c["core id"])] = [c]
        output = "\t"
        for idx, pk in enumerate(sorted(pcores.keys())):
            output += '(' + ','.join(["%3s" % c["processor"] for c in pcores[pk]]) + '), '
            if idx % 8 == 7:
                output += "\n\t"
        output += "\n"
        print output

def pr_fields():
    for f in sorted(cpus[0].keys() + ["topology"]):
        print "'" + f + "'"

USAGE = "USAGE: %s <field>" % sys.argv[0]

if __name__ == "__main__":
    cpus = parse_cpuinfo()

    if len(sys.argv) < 2:
        print USAGE
        print "\nAvaliable fields are:"
        pr_fields()
        exit(0)
    key = sys.argv[1]

    if key == "topology":
        pr_topology(cpus)
        exit(0)

    if not key in cpus[0].keys():
        print USAGE
        print "\nKey '%s' is wrong.  Valid keys are:" % key
        pr_fields()
        exit(1)

    output = ''
    for i, cpu in enumerate(cpus):
        if i % 8 == 0:
            output += 'cpu %3d-%3d: ' % (i, i + 7)
        output += '%s, ' % cpu[key]
        if i % 8 == 7:
            output += '\n'
    print output
