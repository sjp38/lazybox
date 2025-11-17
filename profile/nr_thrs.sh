#!/bin/bash

if [ $# -ne 1 ]
then
	echo "Usage: $0 <pid>"
	exit 1
fi

pid=$1

grep "^Threads" /proc/"$pid"/status | awk '{print $2}'
