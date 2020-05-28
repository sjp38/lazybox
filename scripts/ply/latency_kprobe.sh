#!/bin/bash

# Print latency of a function having kprobe and kretprobe

if [ $# -ne 1 ]
then
	echo "Usage: $0 <function name>"
	exit 1
fi

FUNCTION=$1

echo "Press Ctrl-C to finish tracing and show results"
echo "Format: <latency range (nanoseconds)> <distribution>"
echo

cmd="sudo ply -A -c \
'kprobe:$FUNCTION
{
	@start[tid()] = nsecs()
}

kretprobe:$FUNCTION / @start[tid()] /
{
	@latency.quantize(nsecs() - @start[tid()]);
	@start[tid()] = nil;
}'"

eval "$cmd"
