#!/bin/bash

if [ $# -ne 3 ]
then
	echo "Usage: $0 <delay> <count> <command>"
	exit 1
fi

delay=$1
count=$2
cmd=$3

iter=0

while [ $iter -lt $count ] || [ $count -eq -1 ]
do
	$cmd
	sleep $delay
	iter=$(($iter + 1))
done
