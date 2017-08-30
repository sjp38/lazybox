#!/bin/bash

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

NR_IDXS=$((`nr_records $TMPFILE` - 1))
gnuplot -e "DATA='$TMPFILE'; NR_IDXS='$NR_IDXS'" ./scatter.gp

rm $TMPFILE
