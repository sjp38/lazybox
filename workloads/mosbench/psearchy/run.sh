#!/bin/bash

BINDIR=`dirname $0`
cd $BINDIR

if [ ! -f ../mosbench/psearchy/mkdb/pedsort ]
then
	echo "The execution file is not found."
	exit 1
fi

if [ $# -ne 1 ]
then
	echo "Usage: $0 <number of cores>"
	exit 1
fi

NR_CORES=$1

TARGET_DIR=linux-4.19.10
if [ ! -d $TARGET_DIR ]
then
	if [ ! -f linux-4.19.10.tar.xz ]
	then
		wget https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-4.19.10.tar.xz
	fi
	tar xvf linux-4.19.10.tar.xz
fi

rm -fr /tmp/db
mkdir /tmp/db
for i in $(seq 0 $(($NR_CORES - 1)))
do
	mkdir /tmp/db/db$i
done

find $TARGET_DIR -type f | \
	../mosbench/psearchy/mkdb/pedsort -t /tmp/db/db -c $NR_CORES -m 1024
