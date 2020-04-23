#!/bin/bash

# Consume entire memory + <sz spike> periodically

if [ $# -ne 2 ]
then
	echo "Usage: $0 <spike size (MiB)> <interval (seconds)>"
	exit 1
fi

if [ ! -f "$HOME/memwalk/memwalk" ]
then
	echo "Install memwalk at $HOME/memwalk/memwalk first."
	echo "You can clone it from https://github.com/sjp38/memwalk"
	exit 1
fi

BINDIR=$(dirname "$0")
cd $BINDIR

MWALK=$HOME/memwalk/memwalk

SZ_SPIKE=$(($1 * 1024 * 1024))
INTERVAL=$2

MEMCG=$(grep memory /proc/$$/cgroup | awk -F: '{print $3}')
MEMCG=/sys/fs/cgroup/memory/$MEMCG
MEMLIM=$(cat "$MEMCG"/memory.limit_in_bytes)

while :;
do
	sleep "$INTERVAL"
	MEM_IN_USE=$(cat "$MEMCG"/memory.usage_in_bytes)
	TO_CONSUME=$((MEMLIM - MEM_IN_USE + SZ_SPIKE))
	echo "consume $TO_CONSUME bytes"
	$MWALK $TO_CONSUME 64 0 -q
done
