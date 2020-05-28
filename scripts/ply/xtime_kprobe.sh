#!/bin/bash

# Print total execution time of functions having kprobe and kretprobe

if [ $# -ne 1 ]
then
	echo "Usage: $0 <target>"
	exit 1
fi

TARGET=$1

echo "Press Ctrl-C to finish tracing and show results"
echo "Format: <tid>	<execution time (nanoseconds)>"
echo

cmd="sudo ply -c \
'kprobe:$TARGET
{
	@start[tid()] = nsecs();
}

kretprobe:$TARGET / @start[tid()] /
{
	latency = nsecs() - @start[tid()];
	@xtimes[tid()] = @xtimes[tid()] + latency;
	@start[tid()] = nil;
}'"

eval "$cmd"
