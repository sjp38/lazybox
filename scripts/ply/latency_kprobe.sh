#!/bin/bash

# Print latency of a function having kprobe and kretprobe

if [ $# -ne 1 ]
then
	echo "Usage: $0 <function name>"
	exit 1
fi

FUNCTION=$1

cmd="sudo ply -A -c \
'kprobe:$FUNCTION
{
	@start[pid()] = nsecs()
}

kretprobe:$FUNCTION / @start[pid()] /
{
	@latency.quantize(nsecs() - @start[pid()]);
	@start[pid()] = nil;
}'"

eval $cmd
