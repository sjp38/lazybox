#!/bin/bash

# Print number of executions of a function

if [ $# -eq 0 ]
then
	echo "Usage: $0 <function name> ..."
	exit 1
fi

echo "# Press Ctrl-C to finish tracing and show results"
echo

plycmd=""
for fn in "${@:1}"
do
	plycmd+="kprobe:$fn {@[caller] = count();} "
done

cmd="sudo ply '$plycmd'"
eval "$cmd"
