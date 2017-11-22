#!/bin/bash

# Print out memory footprint of a command in 1 second interval.

if [ $# -ne 1 ]
then
	echo "Usage: $0 <command name>"
	exit 1
fi

COMM=$1

echo "vsz	rss	comm"
while true;
do
	ps -eo vsz,rss,comm | grep $COMM
	sleep 1
done
