#!/bin/bash

# organize results: move, copy (merge), rm.
# source is current ODIR_ROOT.

if [ $# -lt 1 ] || ( [ "$1" != "mv" ] && [ "$1" != "cp" ] && [ "$1" != "rm" ] )
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
		if [ "$OP" = "rm" ]
		then
			echo "rm -fr $src"
			rm -fr $src
			continue
		fi

		dst=$DEST/$exp/$v
		mkdir -p $dst
		if [ "$OP" = "cp" ]
		then
			OP="cp -R"
		fi
		echo "$OP $src/* $dst/"
		$OP $src/* $dst
	done
done
