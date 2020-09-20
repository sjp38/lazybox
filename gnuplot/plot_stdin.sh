#!/bin/bash

if [ $# -lt 3 ]
then
	echo "Usage: $0 <chart type> <x label> <y label> [logscale]"
	echo " supported chart types are:"
	echo "         scatter, scatter-yerr, clustered_boxes, heatmap"
	exit 1
fi

BINDIR=$(dirname "$0")

CHART_TYPE=$1
XLABEL=$2
YLABEL=$3
LOGSCALE=$4

export GNUPLOT_LIB=$BINDIR

TMPFILE=$(mktemp /tmp/lbx-gnuplot.XXX)

cat /dev/stdin > "$TMPFILE"

if [ "$LOGSCALE" = "x" ]
then
	LOGSCALE="--xlog"
elif [ "$LOGSCALE" = "y" ]
then
	LOGSCALE="--ylog"
elif [ "$LOGSCALE" = "xy" ]
then
	LOGSCALE="--xlog --ylog"
fi

"$BINDIR/plot.py" --file "$TMPFILE" --type "$CHART_TYPE" \
	--xtitle "$XLABEL" --ytitle "$YLABEL"  "$LOGSCALE"
rm "$TMPFILE"
