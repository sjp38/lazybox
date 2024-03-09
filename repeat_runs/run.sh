#!/bin/bash

BINDIR=$(dirname "$0")

source "$BINDIR/__common.sh"

for i in $(seq "$REPEATS")
do
	for exp in $EXPERIMENTS
	do
		for var in $VARIANTS
		do
			echo "$i iter of $exp/$var"
			"$BINDIR"/_gen_exp_cfg.sh "$exp" "$var" | \
			sudo "$LBX"/parallel_runs/run_exps.py stdin
		done
	done
done
