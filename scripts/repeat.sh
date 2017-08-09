#!/bin/bash

# Execute a command specific times with given delay between execution

if [ $# -lt 3 ]
then
	echo "$0 <delay> <count> <command...>"
	echo "	Use -1 as count for infinite repeat."
	exit 1
fi

DELAY=$1
COUNT=$2

for ((N = 0; N < $COUNT || $COUNT == -1; N++))
do
	eval ${@:3}
	sleep $DELAY
done
