#!/bin/bash

if [ $# -lt 3 ]
then
	echo "Usage: $0 <chart type> <x label> <y label> [logscale]"
	echo " supported chart types are: scatter, scatter-yerr, clustered_box"
	exit 1
fi

SCRIPT_DIR=`dirname $0`

CHART_TYPE=$1
XLABEL=$2
YLABEL=$3
LOGSCALE=$4

export GNUPLOT_LIB=$SCRIPT_DIR

NR_TRY=0

for ((i = 0; i < 5; i++))
do
	TMPFILE=/tmp/$i.gpdat
	if [ ! -f $TMPFILE ]; then
		break
	fi
	if [ $i -eq 4 ]; then
		echo "/tmp/0-4.gpdat already exists.  Remove them first."
		exit 1
	fi
done

cat /dev/stdin > $TMPFILE

function nr_records {
	awk 'BEGIN{RS="\n\n\n";}{print NR;}' $1 | wc -l
}

# index start from 0
NR_IDXS=$((`nr_records $TMPFILE` - 1))
NR_COLS=`cat $TMPFILE | tail -n 1 | awk '{print NF}'`

if [ $NR_COLS -lt 2 ]
then
	echo "Number of columns is $NR_COLS (< 2).  Maybe something wrong."
	exit 1
fi

gnuplot -e "DATA='$TMPFILE'; NR_IDXS='$NR_IDXS'; NR_COLS='$NR_COLS'; \
		XLABEL='$XLABEL'; YLABEL='$YLABEL'; \
		LOGSCALE='$LOGSCALE'" ./$CHART_TYPE.gp

rm $TMPFILE
