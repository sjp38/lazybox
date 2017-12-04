#!/bin/bash

BINDIR=`dirname $0`

parse_perfout() {
	echo "Swpin"
	perf script | grep swpin | sed -e 's/://' | sed -e 's/page=//' |
		awk '{print $4 " " $7}'
	echo
	echo
	echo "swpout"
	perf script | grep swpout | sed -e 's/://' | sed -e 's/page=//' |
		awk '{print $4 " " $7}'
}

parse_perfout |
	$BINDIR/../../gnuplot/plot_stdin.sh scatter \
		"Time (seconds)" "Page Frame"
