#!/bin/bash

if [ $# -ne 1 ]
then
	echo "Usage: $0 <process name>"
	exit 1
fi

function ticks_used() {
	CMD=$1
	pids=$(pidof "$CMD")
	if [ "$pids" == "" ]
	then
		echo "0"
	fi

	TICKS=0
	for pid in $pids
	do
		TICKS=$(( TICKS + \
			$(awk '{print $14 + $15}' /proc/"$pid"/stat) ))
	done
	echo $TICKS
}

CMD=$1
while true;
do
	BEFORE_TICK=$(ticks_used "$CMD")
	sleep 0.5
	DIFF=$(( $(ticks_used "$CMD") - BEFORE_TICK ))
	if [ $DIFF == "0" ]
	then
		break
	fi
done
