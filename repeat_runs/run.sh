#!/bin/bash

BINDIR=`dirname $0`

source $BINDIR/__common.sh

for i in $(seq $REPEATS)
do
	for exp in $EXPERIMENTS
	do
		for var in $VARIANTS
		do
			echo "$i time $exp/$var"
			$BINDIR/_gen_exp_cfg.sh $exp $var | \
			sudo $LBX/run_exps.py stdin
		done
	done
done
