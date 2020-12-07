#!/bin/bash

# Print callstacks and number of fires of a kprobe point

if [ $# -eq 0 ]
then
	echo "Usage: $0 <kernel function name>..."
	exit 1
fi

echo "Press Ctrl-C to finish tracing and show result"
echo "Format: <callstack>	<number of calls>"
echo

plycmd=""

for fn in "${@:1}"
do
	plycmd+="kprobe:$fn {@[stack] = count();} "
done

cmd="sudo ply '$plycmd'"
eval "$cmd"
