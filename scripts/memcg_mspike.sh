#!/bin/bash

# Create artificial memory shortage on a memcgroup

if [ $# -ne 2 ]
then
	echo "Usage: $0 <spike size (MiB)> <interval (seconds)>"
	exit 1
fi

if [ ! -f $HOME/memwalk/memwalk ]
then
	echo "Install memwalk at $HOME/memwalk/memwalk first."
	echo "You can clone it from https://github.com/sjp38/memwalk"
	exit 1
fi

BINDIR=`dirname $0`
cd $BINDIR

MWALK=$HOME/memwalk/memwalk

SZ_SPIKE=$(($1 * 1024 * 1024))
INTERVAL=$2

MEMCG=`cat /proc/$$/cgroup | grep memory | awk -F: '{print $3}'`
MEMCG=/sys/fs/cgroup/memory/$MEMCG
MEMLIMFILE=$MEMCG/memory.limit_in_bytes
MEMLIM=`cat $MEMLIMFILE`

while :;
do
	sleep $INTERVAL
	MEM_IN_USE=`cat $MEMCG/memory.usage_in_bytes`
	TARGET_LIM=$(($MEM_IN_USE - $SZ_SPIKE))
	echo "Shrink mem lim to $TARGET_LIM"
	sudo bash -c "echo $TARGET_LIM > $MEMLIMFILE"
	sleep 2
	sudo bash -c "echo $MEMLIM > $MEMLIMFILE"
done
