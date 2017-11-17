#!/bin/bash

COMM=$1

echo "vsz	rss	comm"
while true;
do
	ps -eo vsz,rss,comm | grep $COMM
	sleep 1
done
