#!/bin/bash

function usage() {
	echo "Usage: $0 <1-3>"
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
