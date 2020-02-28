#!/bin/bash

LBX=$HOME/lazybox
PSWPIN=$1/pswpin

$LBX/scripts/report/recs_to_diff.py $PSWPIN > $2/pswpin.diff
NR_SWPIN=0
TOTAL_SWPIN=0
for swpin in `awk '{print $2}' $2/pswpin.diff`
do
	TOTAL_SWPIN=$(($TOTAL_SWPIN + $swpin))
	NR_SWPIN=$(($NR_SWPIN + 1))
done
echo "swpin.avg: " $(($TOTAL_SWPIN / $NR_SWPIN)) > $2/pswpin.avg
