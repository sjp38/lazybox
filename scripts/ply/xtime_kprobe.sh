#!/bin/bash

# Print per-process execution time of a process context function having kprobe
# and kretprobe

if [ $# -ne 1 ]
then
	echo "Usage: $0 <target>"
	exit 1
fi

TARGET=$1

echo "Press Ctrl-C to finish tracing and show results"
echo "Format:  <tid> <execution time>"
echo

cmd="sudo ply \
'kprobe:$TARGET
{
	start[kpid] = time;
}

kretprobe:$TARGET / start[kpid] /
{
	latency[kpid] = time - start[kpid];
	if (xtimes[kpid])
		xtimes[kpid] = xtimes[kpid] + latency[kpid];
	else
		xtimes[kpid] = latency[kpid];
	delete latency[kpid];
	delete start[kpid];
}'"

eval "$cmd"
