#!/bin/bash

# organize results: move, copy (merge), rm.
# source is current ODIR_ROOT.

if [ $# -lt 1 ]
then
	echo "Usage: $0 (mv|cp|rm) [destination results dir]"
	exit 1
fi

OP=$1
DEST=$2

if [ "$OP" != "rm" ] && [ -z "$DEST" ]
then
	echo "Only 'rm' op can have no destination"
	exit 1
fi

BINDIR=`dirname $0`

source $BINDIR/__common.sh

for exp in $EXPERIMENTS
do
	for v in $VARIANTS
	do
		src=$ODIR_ROOT/$exp/$v
		dst=$DEST/$exp/$v
		echo "$OP $src $dst"
		mkdir -p $dst
		if [ "$OP" = "cp" ]
		then
			OP="cp -R"
		fi
		$OP $src/* $dst/
	done
done
