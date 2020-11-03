#!/bin/bash

function usage() {
	echo "Usage: $0 <target>"
	echo
	echo "TARGET"
	echo "    1: Free pagecache"
	echo "    2: Free dentries and inodes"
	echo "    3: Free pagecache, dentries, and inodes"
	exit 1
}

if [ $# -ne 1 ]
then
	usage
fi

ARG=$1

if [ "$ARG" -lt 1 ] || [ "$ARG" -gt 3 ]
then
	usage
fi

echo "$ARG" > /proc/sys/vm/drop_caches
