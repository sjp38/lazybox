#!/bin/bash

if [ $# -ne 1 ]
then
	echo "Usage: $0 <chart type>"
	echo " supported chart types are: scatter, clustered_box"
	exit 1
fi

SCRIPT_DIR=`dirname $0`

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
	echo "Number of columns are $NR_COLS (< 2).  Maybe something wrong."
	exit 1
fi

gnuplot -e "DATA='$TMPFILE'; NR_IDXS='$NR_IDXS'; NR_COLS='$NR_COLS'" ./$1.gp

rm $TMPFILE
