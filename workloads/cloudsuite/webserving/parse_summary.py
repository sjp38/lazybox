#!/usr/bin/env python

"""
Receive summary.xml from stdin and print out essential fields
"""

import xml.etree.ElementTree as ET
import sys

def walk_elem(elem, level=0):
    outindent = "    " * level
    indent = "    " * (level + 1)
    print outindent, "{"
    print indent, "tag: ", elem.tag
    print indent, "attr: ", elem.attrib
    print indent, "text: ", elem.text
    for child in elem:
        walk_elem(child, level + 1)
    print outindent, "}"

xmldat = "".join(sys.stdin)
root = ET.fromstring(xmldat)
#walk_elem(root, 0)

print "users:\t", root.find("./driverSummary/users").text
print "nr_ops:\t", root.find("./driverSummary/totalOps").text
print "ops:\t", root.find("./benchSummary/metric").text

response_times = root.findall("./driverSummary/responseTimes/operation")
for op in response_times:
    for lat in op:
        if lat.tag == "passed":
            continue
        if lat.tag == "percentile":
            lat.tag = "%s%s %s" % (lat.attrib["nth"], lat.attrib["suffix"], lat.tag)
        print "%s %s: %s" % (op.attrib["name"], lat.tag, lat.text)
