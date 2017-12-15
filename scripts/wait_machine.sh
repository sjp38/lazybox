#!/bin/bash

if [ $# -ne 3 ]
then
	echo "Usage: $0 <on|off> <target machine ip> <timeout>"
	exit 1
fi

ONOFF=$1
ADDR=$2
TIMEOUT=$3

while true;
do
	if [ $SECONDS -gt $TIMEOUT ]
	then
		echo "Timeout! $SECONDS > $TIMEOUT"
		exit 1
	fi
	if ping $ADDR -c 1 > /dev/null
	then
		if [ $ONOFF = "on" ]
		then
			break
		fi
	else
		if [ $ONOFF = "off" ]
		then
			break
		fi
	fi

	sleep 2
done
