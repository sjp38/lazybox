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

LNXSRC=linux-4.19.10
TMPD=./tmp
TARGET_DIR=$TMPD/$LNXSRC
if [ ! -d $TARGET_DIR ]
then
	mkdir -p $TMPD
	sudo mount -t tmpfs -o rw,size=10G tmpfs $TMPD
	sudo chown $USER $TMPD

	if [ ! -f linux-4.19.10.tar.xz ]
	then
		wget https://cdn.kernel.org/pub/linux/kernel/v4.x/$LNXSRC.tar.xz
	fi
	tar -C $TMPD -xvf linux-4.19.10.tar.xz
fi

rm -fr $TMPD/db
for i in $(seq 0 $(($NR_CORES - 1)))
do
	mkdir -p $TMPD/db/db$i
done

find $TARGET_DIR -type f | \
	../mosbench/psearchy/mkdb/pedsort -t $TMPD/db/db -c $NR_CORES -m 1024
