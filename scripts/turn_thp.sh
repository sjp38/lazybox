#!/bin/bash

SYSFS_THP_ENABLED=/sys/kernel/mm/transparent_hugepage/enabled

if [ $# -ne 1 ];
then
	echo "Usage: $0 <always|madvise|never>"
	echo ""
	echo "Current status: " $(cat $SYSFS_THP_ENABLED)
	echo ""
	exit 1
fi

echo $1 > $SYSFS_THP_ENABLED
