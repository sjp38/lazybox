#!/bin/bash

if [ $# -ne 1 ]
then
	echo "Usage: $0 <pid>"
	exit 1
fi

pid=$1

cat /proc/$pid/status | grep "^Threads" | awk '{print $2}'
