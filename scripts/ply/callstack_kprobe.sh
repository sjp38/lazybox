#!/bin/bash

# Print callstacks and number of fires of a kprobe point

if [ $# -ne 1 ]
then
	echo "Usage: $0 <kernel function name>"
	exit 1
fi

definition=$1

echo "Press Ctrl-C to finish tracing and show result"
echo "Format: <callstack>	<number of calls>"
echo
cmd="sudo ply -c 'kprobe:$definition{ @[stack()].count() }'"
eval "$cmd"
