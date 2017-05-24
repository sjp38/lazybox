#!/bin/bash

if [ $# -ne 1 ];
then
	echo "Usage: $0 <always|madvise|never>"
	exit 1
fi

echo $1 > /sys/kernel/mm/transparent_hugepage/enabled
