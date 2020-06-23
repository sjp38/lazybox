#!/bin/bash

# organize results: move, copy (merge), rm.
# source is current ODIR_ROOT.

if [ $# -lt 1 ] || ( [ "$1" != "cp" ] && [ "$1" != "rm" ] )
then
	echo "Usage: $0 (cp|rm) [destination results dir]"
	exit 1
fi

OP=$1
DEST=$2

if [ "$OP" != "rm" ] && [ -z "$DEST" ]
then
	echo "Only 'rm' op can have no destination"
	exit 1
fi

BINDIR=$(dirname "$0")

source $BINDIR/__common.sh

for exp in $EXPERIMENTS
do
	exp_basename=$(basename "$exp")
	for v in $VARIANTS
	do
		src="$ODIR_ROOT/$exp_basename/$v"
		if [ "$OP" = "rm" ]
		then
			echo "rm -fr $src"
			rm -fr "$src"
			continue
		fi

		dst=$DEST/$exp_basename/$v
		mkdir -p "$dst"
		if [ "$OP" = "cp" ]
		then
			OP="cp -R"
		fi

		merged=0
		for s in $(find $src -name "[0-9][0-9]")
		do
			uid=$(basename $s)
			candidate="$dst/$uid"
			while [ -d "$candidate" ]
			do
				merged=1
				uid=$((10#$uid + 1))
				uid=$(printf "%02d" $uid)
				candidate="$dst/$uid"
				if [ $uid -gt 99 ]
				then
					echo "uid > 99!"
					exit 1
				fi
			done
			echo "cp -R $s $candidate"
			cp -R "$s" "$candidate"
		done

		if [ $merged -ne 0 ]
		then
			continue
		fi

		echo "cp -R $src/* $dst/"
		cp -R "$src/"* "$dst"
	done
done
