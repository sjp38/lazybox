#!/bin/bash

# Print per-process execution time of a process context function having kprobe
# and kretprobe

if [ $# -eq 0 ]
then
	echo "Usage: $0 <function name> ..."
	exit 1
fi

plycmd=""
for fn in "${@:1}"
do
	plycmd+="kprobe:$fn {start[kpid] = time;}"
	plycmd+="
	kretprobe:$fn / start[kpid] / {
		latency[kpid] = time - start[kpid];
		if ($fn[kpid])
			$fn[kpid] = $fn[kpid] + latency[kpid];
		else
			$fn[kpid] = latency[kpid];
		delete latency[kpid];
		delete start[kpid];
	} "
done

cmd="sudo ply '$plycmd'"
eval "$cmd"
