#!/usr/bin/env python3

for i in range(0, 16):
    line = ''
    for j in range(0, 16):
        val = i * 16 + j
        line += u'\u001b[48;5;%dm %d \u001b[0m' % (val, val)
    print(line)
