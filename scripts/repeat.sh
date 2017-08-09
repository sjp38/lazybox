#!/bin/bash

# Execute a command specific times with given delay between execution

USAGE="$0 <delay> <count> <command...>"

if [ $# -lt 3 ]
then
	echo $USAGE
	exit 1
fi

DELAY=$1
COUNT=$2

for i in $(seq 1 $COUNT)
do
	eval ${@:3}
	sleep $DELAY
done
