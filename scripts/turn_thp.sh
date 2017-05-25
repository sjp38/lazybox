#!/bin/bash

if [ $# -ne 1 ];
then
	echo "Usage: $0 <always|madvise|never>"
	echo ""
	echo "Current status: "
	cat /sys/kernel/mm/transparent_hugepage/enabled
	exit 1
fi

echo $1 > /sys/kernel/mm/transparent_hugepage/enabled
