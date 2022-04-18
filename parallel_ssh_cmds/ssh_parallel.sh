#!/bin/bash

if [ $# -lt 2 ]
then
	echo "Usage: $0 <cmd> <host>..."
	exit 1
fi

cmd=$1

arguments=( "$@" )
unset arguments[0]

for host in ${arguments[@]}
do
	ssh "$host" "$cmd" &
done

wait
