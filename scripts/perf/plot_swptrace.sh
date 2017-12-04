#!/bin/bash

BINDIR=`dirname $0`

MIDFILE=perf-scr.out
MAX_SAMPLES=1000

perf script > $MIDFILE
NR_SAMPLES=`cat $MIDFILE | wc -l`
if [ $NR_SAMPLES -gt $MAX_SAMPLES ]
then
	echo "Too big ($NR_SAMPLES) data.  Shrink to $MAX_SAMPLES data"
	$BINDIR/sample.py $(($NR_SAMPLES / $MAX_SAMPLES)) < $MIDFILE > $MIDFILE.tmp
	mv $MIDFILE.tmp $MIDFILE
fi

parse_perfout() {
	echo "Swpin"
	cat $MIDFILE | grep swpin | sed -e 's/://' | sed -e 's/page=//' |
		awk '{print $4 " " $7}'
	echo
	echo
	echo "swpout"
	cat $MIDFILE | grep swpout | sed -e 's/://' | sed -e 's/page=//' |
		awk '{print $4 " " $7}'
}

parse_perfout |
	$BINDIR/../../gnuplot/plot_stdin.sh scatter \
		"Time (seconds)" "Page Frame"
