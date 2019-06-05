#!/bin/bash

BINDIR=`dirname $0`
cd $BINDIR

if [ ! -f ./ebizzy-0.3/ebizzy ]
then
	echo "ebizzy is not installed at $BINDIR/ebizzy-0.3/ebizzy"
	exit 1
fi

THREADS="1 2 4 9 18 36 72"

for t in $THREADS
do
	./ebizzy-0.3/ebizzy -mTt $t
done
