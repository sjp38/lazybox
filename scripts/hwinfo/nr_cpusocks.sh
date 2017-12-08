#!/bin/bash

echo $((`grep "^physical id" /proc/cpuinfo | sort | tail -n 1 | \
	awk '{print $4}'` + 1))
