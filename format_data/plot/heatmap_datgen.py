#!/usr/bin/env python3

import random

for x in range(5):
    for y in range(5):
        print("%d %d %d" % (x, y, random.randint(0,10)))
