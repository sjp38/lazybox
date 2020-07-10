#!/bin/bash

# Split data into small segments and plot each segment
#
# This script would be useful for huge dataset.  For example, suppose that the
# data has x range [0-100) and y range [0-100).  If user gives 2 and 2 for
# number of x segments and y segments respectively, this script will split the
# data into four segments ranging at [0-50)/[0-50), [50-100)/[0-50),
# [0-50)/[50-100), [50-100)/[50-100) and plot the four segments.  Also, it will
# sample the data for each plot to have about only 1000 plot points.
# Note that this script assumes single record dataset.

if [ $# -ne 3 ]
then
	echo "Usage: $0 <file> <nr x segments> <nr y segment>"
	exit 1
fi

BINDIR=$(dirname $0)
STATOF="$BINDIR/../scripts/report/statof.py"
SAMPLE="$BINDIR/../scripts/perf/sample.py"
PLOT="$BINDIR/plot_stdin.sh"
YZOOM="$BINDIR/../scripts/report/yzoom.py"

F="$1"
NR_XSEGS="$2"
NR_YSEGS="$3"

FSAMPLED="$F.sampled"

NRDAT=$(cat $F | wc -l)

SEG_WIDTH=1000

cat $F | $SAMPLE $(($NRDAT / $NR_XSEGS / $SEG_WIDTH)) > $FSAMPLED
MIN=$($STATOF min $FSAMPLED)
MAX=$($STATOF max $FSAMPLED)

SEG_HEIGHT=$(( ($MAX - $MIN) / $NR_YSEGS ))

for i in $(seq 1 $NR_XSEGS)
do
	for j in $(seq 1 $NR_YSEGS)
	do
		DAT=$F.$i-$j
		head -n $(( $i * $SEG_WIDTH )) $FSAMPLED | \
			tail -n $SEG_WIDTH | \
			$YZOOM $(( ($NR_YSEGS - $j) * $SEG_HEIGHT )) \
			$(( ($NR_YSEGS - $j + 1) * $SEG_HEIGHT )) > $DAT
		if [ $(cat $DAT | wc -l) -eq 0 ]
		then
			continue
		fi
		cat $DAT | $PLOT scatter-dot "Time" "Virtual Addr"
		mv plot.pdf $F.plot.$i-$j.pdf
	done
done
