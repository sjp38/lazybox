#!/bin/bash

if [ $# -ne 1 ]
then
	echo "Usage: $0 <process name>"
	exit 1
fi

function nr_running() {
	CMD=$1
	pids=`pidof $CMD`
	if [ pids == "" ]
	then
		echo "0"
	fi

	NR_RUNNING=0
	for pid in $pids
	do
		if [ `grep "running" /proc/$pid/status | wc -l` -eq 1 ]
		then
			NR_RUNNING=$(( $NR_RUNNING + 1 ))
		fi
		if [ `grep "disk sleep" /proc/$pid/status | wc -l` -eq 1 ]
		then
			NR_RUNNING=$(( $NR_RUNNING + 1 ))
		fi
	done
	echo $NR_RUNNING
}

CMD=$1
while true;
do
	sleep 1
	if [ `nr_running $CMD` == "0" ]
	then
		break
	fi
done
