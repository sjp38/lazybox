#!/bin/bash

BINDIR=`dirname $0`

source $BINDIR/__common.sh

for i in $(seq $REPEATS)
do
	for exp in $EXPERIMENTS
	do
		echo "$exp $i iteration"
		$BINDIR/_gen_exp_cfg.sh $exp $CURRENT_VARIANT | \
		sudo $LBX/run_exps.py -s stdin
	done
done
