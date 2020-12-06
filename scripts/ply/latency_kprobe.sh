#!/bin/bash

# Print latencies of a process context function having kprobe and kretprobe

if [ $# -ne 1 ]
then
	echo "Usage: $0 <function name>"
	exit 1
fi

FUNCTION=$1

echo "Press Ctrl-C to finish tracing and show results"
echo "Format: <latency range)> <distribution>"
echo

cmd="sudo ply \
'kprobe:$FUNCTION
{
	start[kpid] = time;
	callers[kpid] = caller;
}

kretprobe:$FUNCTION / start[kpid] /
{
	@latencies[callers[kpid]] = quantize(time - start[kpid]);
	delete start[kpid];
	delete callers[kpid];
}'"

eval "$cmd"
