#!/usr/bin/env python3

import random

keys = ["metric", "sysA", "sysB", "sysC", "sysD", "sysE", "sysF", "sysG"]
xaxes = ["metricA", "metricBB", "metricC", "metricD", "metricE", "metricF"]

print("\t".join(keys))
line = ""
for i in range(len(xaxes)):
    values = [str(random.randint(0, 100000)) for _ in keys[1:]]
    print("%s\t%s" % (xaxes[i], "\t".join(values)))

