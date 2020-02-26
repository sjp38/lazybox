#!/bin/bash

BINDIR=`dirname $0`

source $BINDIR/__common.sh

for exp in $EXPERIMENTS
do
	for v in $VARIANTS
	do
		for d in $ODIR_ROOT/$exp/$v/0*
		do
			$BINDIR/_parse.sh $exp $d
		done
	done
done

for exp in $EXPERIMENTS
do
	for v in $VARIANTS
	do
		ODIR=$ODIR_ROOT/$exp/$v
		$BINDIR/_stat.sh $exp $ODIR
	done
done
