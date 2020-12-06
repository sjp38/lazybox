#!/bin/bash

# Print number of executions of a function

if [ $# -ne 1 ]
then
	echo "Usage: $0 <function name>"
	exit 1
fi

TARGET=$1

echo "Press Ctrl-C to finish tracing and show results"
echo "Format: <function>	<number of calls>"
echo

cmd="sudo ply \
'kprobe:$TARGET
{
	@[caller] = count();
}'"

eval "$cmd"
