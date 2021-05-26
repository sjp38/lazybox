#!/bin/bash

while :
do
	grep MemFree /proc/meminfo >> "$1/memfree"
	sleep 1
done
