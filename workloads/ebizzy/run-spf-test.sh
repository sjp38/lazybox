#!/bin/bash

BINDIR=$(dirname "$0")
cd "$BINDIR" || exit 1

if [ ! -f ./ebizzy-0.3/ebizzy ]
then
	echo "ebizzy is not installed at $BINDIR/ebizzy-0.3/ebizzy"
	exit 1
fi

if [ -z "$THREADS" ]
then
	THREADS="1 2 4 9 18 36 72"
fi

for t in $THREADS
do
	PERF=$(./ebizzy-0.3/ebizzy -mTt "$t" | grep records/s)
	echo "$t $PERF"
done
