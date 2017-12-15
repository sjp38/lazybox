#!/bin/bash

if [ $# -ne 2 ]
then
	echo "Usage: $0 <ip addr of target machine> <timeout>"
	exit 1
fi

ADDR=$1
TIMEOUT=$2

while true;
do
	if [ $SECONDS -gt $TIMEOUT ]
	then
		echo "Timeout! $SECONDS > $TIMEOUT"
		exit 1
	fi
	if ping $ADDR -c 1 > /dev/null
	then
		break
	fi

	sleep 2
done
