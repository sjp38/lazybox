#!/bin/bash

# Print latencies of a process context function having kprobe and kretprobe

if [ $# -eq 0 ]
then
	echo "Usage: $0 <function name> ..."
	exit 1
fi

plycmd=""
for fn in "${@:1}"
do
	plycmd+="kprobe:$fn {start[kpid] = time; callers[kpid] = caller;}"
	plycmd+="
	kretprobe:$fn / start[kpid] / {
		@latencies[callers[kpid]] = quantize(time - start[kpid]);
		delete start[kpid];
		delete callers[kpid];
	} "
done

cmd="sudo ply '$plycmd'"
eval "$cmd"
